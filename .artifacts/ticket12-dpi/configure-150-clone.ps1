$ErrorActionPreference = 'Stop'

$cloneVm = 'gpt_win11_ticket12_dpi150'
$credential = Import-Clixml -LiteralPath `
    "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"

$deadline = (Get-Date).AddMinutes(10)
do {
    Start-Sleep -Seconds 5
    try {
        $session = New-PSSession -VMName $cloneVm -Credential $credential -ErrorAction Stop
    }
    catch {
        $session = $null
    }
} while ($null -eq $session -and (Get-Date) -lt $deadline)
if ($null -eq $session) {
    throw "PowerShell Direct did not become available for $cloneVm."
}

try {
    Invoke-Command -Session $session -ScriptBlock {
        $desktop = 'HKCU:\Control Panel\Desktop'
        Set-ItemProperty -LiteralPath $desktop -Name Win8DpiScaling -Type DWord -Value 1
        Set-ItemProperty -LiteralPath $desktop -Name LogPixels -Type DWord -Value 144
        Restart-Computer -Force
    }
}
finally {
    Remove-PSSession $session -ErrorAction SilentlyContinue
}

$deadline = (Get-Date).AddMinutes(10)
do {
    Start-Sleep -Seconds 5
    try {
        $probe = New-PSSession -VMName $cloneVm -Credential $credential -ErrorAction Stop
    }
    catch {
        $probe = $null
    }
} while ($null -eq $probe -and (Get-Date) -lt $deadline)
if ($null -eq $probe) {
    throw "Clone did not return after DPI restart: $cloneVm"
}

try {
    Invoke-Command -Session $probe -ScriptBlock {
        [pscustomobject]@{
            ExplorerSessions = @(Get-Process explorer -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty SessionId)
            LogPixels = (Get-ItemProperty -LiteralPath 'HKCU:\Control Panel\Desktop').LogPixels
            Win8DpiScaling = (Get-ItemProperty -LiteralPath 'HKCU:\Control Panel\Desktop').Win8DpiScaling
        }
    }
}
finally {
    Remove-PSSession $probe
}
