[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Setup', 'Cleanup')]
    [string]$Action
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$transcriptPath = Join-Path $PSScriptRoot "ticket13-sql-$($Action.ToLowerInvariant()).transcript.log"
[IO.File]::WriteAllText($transcriptPath, '')
Start-Transcript -LiteralPath $transcriptPath -Append | Out-Null

$database = 'MesIngest_Ticket13_Golden'
$login = 'MesIngestTicket13Golden'
$firewallRule = 'MesIngest Ticket13 Golden SQL'
$credentialPath = Join-Path $env:LOCALAPPDATA 'MesIngestWatch\ticket13-golden-sql.credential.xml'
$vmCredentialPath = Join-Path $env:LOCALAPPDATA 'MesIngestWatch\gpt_win11.credential.xml'
$sqlRegistry = 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQLServer'
$tcpRegistry = Join-Path $sqlRegistry 'SuperSocketNetLib\Tcp'

function Open-MasterConnection {
    $connection = New-Object System.Data.SqlClient.SqlConnection `
        'Server=localhost;Database=master;Integrated Security=True;Encrypt=True;TrustServerCertificate=True'
    $connection.Open()
    return $connection
}

function Remove-DedicatedSqlObjects {
    $connection = Open-MasterConnection
    try {
        $command = $connection.CreateCommand()
        $command.CommandText = @"
            IF DB_ID(N'$database') IS NOT NULL
            BEGIN
                ALTER DATABASE [$database] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                DROP DATABASE [$database];
            END;
            IF SUSER_ID(N'$login') IS NOT NULL
            BEGIN
                IF EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'$login')
                    DROP LOGIN [$login];
            END;
"@
        [void]$command.ExecuteNonQuery()
    }
    finally {
        $connection.Dispose()
    }
}

if ($Action -eq 'Cleanup') {
    $vmCredential = Import-Clixml -LiteralPath $vmCredentialPath
    $session = New-PSSession -VMName gpt_win11 -Credential $vmCredential
    try {
        Invoke-Command -Session $session -ScriptBlock {
            $adapter = Get-NetAdapter |
                Where-Object MacAddress -eq '00-15-5D-64-9B-06' |
                Select-Object -First 1
            if ($null -ne $adapter) {
                Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 `
                    -ErrorAction SilentlyContinue |
                    Where-Object IPAddress -eq '192.168.200.2' |
                    Remove-NetIPAddress -Confirm:$false -ErrorAction SilentlyContinue
                Set-NetIPInterface -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 `
                    -Dhcp Enabled -ErrorAction SilentlyContinue
            }
        }
    }
    finally {
        Remove-PSSession $session
    }
    Disconnect-VMNetworkAdapter -VMName gpt_win11 -ErrorAction SilentlyContinue
    Get-NetFirewallRule -DisplayName $firewallRule -ErrorAction SilentlyContinue |
        Remove-NetFirewallRule
    Remove-DedicatedSqlObjects
    Remove-Item -LiteralPath $credentialPath -Force -ErrorAction SilentlyContinue
    Set-ItemProperty -LiteralPath $sqlRegistry -Name LoginMode -Value 1
    Set-ItemProperty -LiteralPath $tcpRegistry -Name Enabled -Value 0
    Restart-Service -Name MSSQLSERVER -Force
    (Get-Service MSSQLSERVER).WaitForStatus('Running', [TimeSpan]::FromSeconds(60))
    [pscustomobject]@{
        Status = 'CLEANED'
        LoginMode = (Get-ItemProperty $sqlRegistry).LoginMode
        TcpEnabled = (Get-ItemProperty $tcpRegistry).Enabled
        VmSwitch = (Get-VMNetworkAdapter -VMName gpt_win11).SwitchName
        CredentialFilePresent = Test-Path -LiteralPath $credentialPath
    }
    Stop-Transcript | Out-Null
    exit 0
}

$connection = Open-MasterConnection
try {
    $command = $connection.CreateCommand()
    $command.CommandText = "SELECT DB_ID(N'$database'), SUSER_ID(N'$login');"
    $reader = $command.ExecuteReader()
    [void]$reader.Read()
    $databaseExists = -not $reader.IsDBNull(0)
    $loginExists = -not $reader.IsDBNull(1)
    $reader.Close()
}
finally {
    $connection.Dispose()
}
$firewallExists = $null -ne (Get-NetFirewallRule -DisplayName $firewallRule -ErrorAction SilentlyContinue)
$credentialExists = Test-Path -LiteralPath $credentialPath
$loginMode = (Get-ItemProperty $sqlRegistry).LoginMode
$tcpEnabled = (Get-ItemProperty $tcpRegistry).Enabled
$vmSwitch = (Get-VMNetworkAdapter -VMName gpt_win11).SwitchName
if ($databaseExists -or $loginExists -or $firewallExists -or $credentialExists `
    -or $loginMode -ne 1 -or $tcpEnabled -ne 0 -or -not [string]::IsNullOrWhiteSpace($vmSwitch)) {
    throw 'Refusing setup because the dedicated targets or original SQL/VM network state are not clean.'
}

$createdDatabase = $false
$createdLogin = $false
$changedSql = $false
$connectedVm = $false
try {
    $passwordBytes = New-Object byte[] 36
    [Security.Cryptography.RandomNumberGenerator]::Fill($passwordBytes)
    $password = [Convert]::ToBase64String($passwordBytes) + 'aA1!'

    $connection = Open-MasterConnection
    try {
        $command = $connection.CreateCommand()
        $command.CommandText = "CREATE DATABASE [$database];"
        [void]$command.ExecuteNonQuery()
        $createdDatabase = $true
        $escapedPassword = $password.Replace("'", "''")
        $command.CommandText = "CREATE LOGIN [$login] WITH PASSWORD=N'$escapedPassword', CHECK_POLICY=OFF, DEFAULT_DATABASE=[$database];"
        [void]$command.ExecuteNonQuery()
        $createdLogin = $true
    }
    finally {
        $connection.Dispose()
    }

    $databaseConnection = New-Object System.Data.SqlClient.SqlConnection `
        "Server=localhost;Database=$database;Integrated Security=True;Encrypt=True;TrustServerCertificate=True"
    $databaseConnection.Open()
    try {
        $command = $databaseConnection.CreateCommand()
        $command.CommandText = "CREATE USER [$login] FOR LOGIN [$login]; ALTER ROLE [db_owner] ADD MEMBER [$login];"
        [void]$command.ExecuteNonQuery()
    }
    finally {
        $databaseConnection.Dispose()
    }

    $securePassword = ConvertTo-SecureString $password -AsPlainText -Force
    $credential = New-Object Management.Automation.PSCredential($login, $securePassword)
    New-Item -ItemType Directory -Path (Split-Path -Parent $credentialPath) -Force | Out-Null
    $credential | Export-Clixml -LiteralPath $credentialPath

    Set-ItemProperty -LiteralPath $sqlRegistry -Name LoginMode -Value 2
    Set-ItemProperty -LiteralPath $tcpRegistry -Name Enabled -Value 1
    $changedSql = $true
    New-NetFirewallRule -DisplayName $firewallRule -Direction Inbound -Action Allow `
        -Protocol TCP -LocalPort 1433 -RemoteAddress 192.168.200.2 -Profile Any | Out-Null
    Restart-Service -Name MSSQLSERVER -Force
    (Get-Service MSSQLSERVER).WaitForStatus('Running', [TimeSpan]::FromSeconds(60))

    Connect-VMNetworkAdapter -VMName gpt_win11 -SwitchName Huawei
    $connectedVm = $true
    Start-Sleep -Seconds 3
    $vmCredential = Import-Clixml -LiteralPath $vmCredentialPath
    $session = New-PSSession -VMName gpt_win11 -Credential $vmCredential
    try {
        Invoke-Command -Session $session -ScriptBlock {
            $adapter = Get-NetAdapter |
                Where-Object MacAddress -eq '00-15-5D-64-9B-06' |
                Select-Object -First 1
            if ($null -eq $adapter) {
                throw 'Golden VM network adapter was not found.'
            }
            Set-NetIPInterface -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 -Dhcp Disabled
            Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 `
                -ErrorAction SilentlyContinue |
                Remove-NetIPAddress -Confirm:$false -ErrorAction SilentlyContinue
            New-NetIPAddress -InterfaceIndex $adapter.ifIndex -IPAddress '192.168.200.2' `
                -PrefixLength 24 | Out-Null
        }
        $remoteResult = Invoke-Command -Session $session -ScriptBlock {
            param($sqlCredential)
            $builder = New-Object System.Data.SqlClient.SqlConnectionStringBuilder
            $builder['Data Source'] = '192.168.200.1,1433'
            $builder['Initial Catalog'] = 'MesIngest_Ticket13_Golden'
            $builder['User ID'] = $sqlCredential.UserName
            $builder['Password'] = $sqlCredential.GetNetworkCredential().Password
            $builder['Encrypt'] = $true
            $builder['TrustServerCertificate'] = $true
            $builder['Connect Timeout'] = 10
            $sqlConnection = New-Object System.Data.SqlClient.SqlConnection $builder.ConnectionString
            try {
                $sqlConnection.Open()
                $sqlCommand = $sqlConnection.CreateCommand()
                $sqlCommand.CommandText = "SELECT CAST(SERVERPROPERTY('ProductMajorVersion') AS int), DB_NAME();"
                $sqlReader = $sqlCommand.ExecuteReader()
                [void]$sqlReader.Read()
                [pscustomobject]@{
                    Connected = $true
                    MajorVersion = $sqlReader.GetInt32(0)
                    Database = $sqlReader.GetString(1)
                }
            }
            finally {
                $sqlConnection.Dispose()
            }
        } -ArgumentList $credential
    }
    finally {
        Remove-PSSession $session
    }
    [pscustomobject]@{
        Status = 'READY'
        SqlService = (Get-Service MSSQLSERVER).Status
        TcpEnabled = (Get-ItemProperty $tcpRegistry).Enabled
        LoginMode = (Get-ItemProperty $sqlRegistry).LoginMode
        FirewallRemoteAddress = (Get-NetFirewallAddressFilter `
            -AssociatedNetFirewallRule (Get-NetFirewallRule -DisplayName $firewallRule)).RemoteAddress
        VmSwitch = (Get-VMNetworkAdapter -VMName gpt_win11).SwitchName
        VmSqlConnected = $remoteResult.Connected
        SqlMajorVersion = $remoteResult.MajorVersion
        Database = $remoteResult.Database
        CredentialPath = $credentialPath
    }
    Stop-Transcript | Out-Null
}
catch {
    $setupError = $_.Exception
    if ($connectedVm) {
        Disconnect-VMNetworkAdapter -VMName gpt_win11 -ErrorAction SilentlyContinue
    }
    Get-NetFirewallRule -DisplayName $firewallRule -ErrorAction SilentlyContinue |
        Remove-NetFirewallRule
    if ($changedSql) {
        Set-ItemProperty -LiteralPath $sqlRegistry -Name LoginMode -Value 1
        Set-ItemProperty -LiteralPath $tcpRegistry -Name Enabled -Value 0
        Restart-Service -Name MSSQLSERVER -Force -ErrorAction SilentlyContinue
    }
    try {
        Remove-DedicatedSqlObjects
    }
    catch {
    }
    Remove-Item -LiteralPath $credentialPath -Force -ErrorAction SilentlyContinue
    try {
        Stop-Transcript | Out-Null
    }
    catch {
    }
    throw $setupError
}
