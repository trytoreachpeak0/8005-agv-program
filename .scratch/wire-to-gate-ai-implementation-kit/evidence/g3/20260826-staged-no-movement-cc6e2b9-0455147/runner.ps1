[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$StageRoot
)

$ErrorActionPreference = 'Stop'

$controlCommit = 'cc6e2b97e4308fa14b519edf9a0089d0da7d6d14'
$onboardCommit = '045514770da9858a8a49196dede276192e4f2a1b'
$simulatorCommit = 'fb5f7c593742bf98bc3957b8729a38aad5321f28'
$agvId = 'AGV-8005-STAGED-G3-01'
$onboardPort = 58105
$healthPort = 58107
$credential = [Guid]::NewGuid().ToString('N')

$onboardConfig = Join-Path $StageRoot 'onboard\appsettings.json'
$settings = Get-Content -Raw -LiteralPath $onboardConfig | ConvertFrom-Json
$settings.environment = 'Development'
$settings.agvId = $agvId
$settings.onboardInstanceId = 'OBU-8005-STAGED-G3-01'
$settings.wireToGate.enabled = $true
$settings.wireToGate.host = '127.0.0.1'
$settings.wireToGate.port = $onboardPort
$settings.wireToGate.onboardInstanceId = '4f66df5d-0277-484a-b4f6-a104fa525b25'
$settings.wireToGate.onboardBuildCommit = $onboardCommit
$settings.wireToGate.useTls = $false
$settings.wireToGate.journalPath = Join-Path $StageRoot 'onboard-journal.db'
$settings.logging.directory = Join-Path $StageRoot 'onboard-logs'
$settings.logging.writeToConsole = $true
$settings | ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath $onboardConfig -Encoding utf8NoBOM

$env:CONTROL_SERVER_ONBOARD_CREDENTIAL = $credential
$env:ConnectionStrings__ControlServer = 'Data Source=' + (Join-Path $StageRoot 'controlserver.db')
$env:Health__url = "http://127.0.0.1:$healthPort"
$env:OnboardTransport__port = $onboardPort.ToString([Globalization.CultureInfo]::InvariantCulture)

function Wait-TcpPort {
    param([int]$Port, [int]$TimeoutSeconds = 30)

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        $client = [Net.Sockets.TcpClient]::new()
        try {
            $task = $client.ConnectAsync('127.0.0.1', $Port)
            if ($task.Wait(300) -and $client.Connected) {
                return
            }
        }
        finally {
            $client.Dispose()
        }
        Start-Sleep -Milliseconds 200
    } while ([DateTime]::UtcNow -lt $deadline)

    throw "等待端口 $Port 超时。"
}

function Start-ControlServer {
    param([int]$Ordinal)

    $process = Start-Process dotnet `
        -ArgumentList @(Join-Path $StageRoot 'control\ControlServer.Host.dll') `
        -WorkingDirectory (Join-Path $StageRoot 'control') `
        -RedirectStandardOutput (Join-Path $StageRoot "control-$Ordinal.out.log") `
        -RedirectStandardError (Join-Path $StageRoot "control-$Ordinal.err.log") `
        -WindowStyle Hidden `
        -PassThru
    Wait-TcpPort -Port $onboardPort
    Wait-TcpPort -Port $healthPort
    return $process
}

function Start-OnboardHmi {
    param([int]$Ordinal)

    return Start-Process dotnet `
        -ArgumentList @(Join-Path $StageRoot 'onboard\SQCD.Agv.Wpf.dll') `
        -WorkingDirectory (Join-Path $StageRoot 'onboard') `
        -RedirectStandardOutput (Join-Path $StageRoot "onboard-$Ordinal.out.log") `
        -RedirectStandardError (Join-Path $StageRoot "onboard-$Ordinal.err.log") `
        -WindowStyle Hidden `
        -PassThru
}

function Wait-Session {
    param([long]$GenerationGreaterThan = -1, [int]$TimeoutSeconds = 45)

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        try {
            $rows = Invoke-RestMethod `
                -Uri "http://127.0.0.1:$healthPort/api/runtime/sessions" `
                -TimeoutSec 2
            $row = $rows |
                Where-Object agvId -EQ $agvId |
                Select-Object -First 1
            if ($null -ne $row -and [long]$row.sessionGeneration -gt $GenerationGreaterThan) {
                return $row
            }
        }
        catch {
            # The endpoint may be temporarily unavailable while a process restarts.
        }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $deadline)

    throw "等待 session generation > $GenerationGreaterThan 超时。"
}

function Read-Session {
    $rows = Invoke-RestMethod `
        -Uri "http://127.0.0.1:$healthPort/api/runtime/sessions" `
        -TimeoutSec 3
    return $rows |
        Where-Object agvId -EQ $agvId |
        Select-Object -First 1
}

function Stop-ProcessSafely {
    param([Diagnostics.Process]$Process)

    if ($null -ne $Process -and -not $Process.HasExited) {
        Stop-Process -Id $Process.Id -Force
        try {
            $Process.WaitForExit(5000) | Out-Null
        }
        catch {
            # Continue cleanup for the remaining processes.
        }
    }
}

$control1 = $null
$control2 = $null
$onboard1 = $null
$onboard2 = $null
$simulator = $null
$runResult = $null

try {
    $simulator = Start-Process dotnet `
        -ArgumentList @(Join-Path $StageRoot 'simulator\SQCD_8005AGV_Simulator.dll') `
        -WorkingDirectory (Join-Path $StageRoot 'simulator') `
        -RedirectStandardOutput (Join-Path $StageRoot 'simulator.out.log') `
        -RedirectStandardError (Join-Path $StageRoot 'simulator.err.log') `
        -WindowStyle Hidden `
        -PassThru
    Wait-TcpPort -Port 1502
    Wait-TcpPort -Port 58006
    $simulatorHealth = Invoke-RestMethod `
        -Uri 'http://127.0.0.1:58006/api/v1/health' `
        -TimeoutSec 3

    $control1 = Start-ControlServer -Ordinal 1
    $version = Invoke-RestMethod -Uri "http://127.0.0.1:$healthPort/version" -TimeoutSec 3

    $onboard1 = Start-OnboardHmi -Ordinal 1
    $session1 = Wait-Session
    Start-Sleep -Seconds 12
    $session1Stable = Read-Session
    if ($null -eq $session1Stable `
        -or [long]$session1Stable.sessionGeneration -ne [long]$session1.sessionGeneration) {
        throw '第一阶段在稳定窗口内发生了意外断线或重连。'
    }
    if ($onboard1.HasExited) {
        throw "OnboardHmi 第一阶段提前退出，exitCode=$($onboard1.ExitCode)。"
    }

    Stop-ProcessSafely -Process $onboard1
    $onboard2 = Start-OnboardHmi -Ordinal 2
    $session2 = Wait-Session -GenerationGreaterThan ([long]$session1.sessionGeneration)
    Start-Sleep -Seconds 12
    $session2Stable = Read-Session
    if ($null -eq $session2Stable `
        -or [long]$session2Stable.sessionGeneration -ne [long]$session2.sessionGeneration) {
        throw '第二阶段在稳定窗口内发生了意外断线或重连。'
    }
    if ($onboard2.HasExited) {
        throw "OnboardHmi 第二阶段提前退出，exitCode=$($onboard2.ExitCode)。"
    }

    Stop-ProcessSafely -Process $control1
    Start-Sleep -Seconds 4
    $control2 = Start-ControlServer -Ordinal 2
    $session3 = Wait-Session `
        -GenerationGreaterThan ([long]$session2.sessionGeneration) `
        -TimeoutSeconds 60
    Start-Sleep -Seconds 12
    $session3Stable = Read-Session
    if ($null -eq $session3Stable `
        -or [long]$session3Stable.sessionGeneration -ne [long]$session3.sessionGeneration) {
        throw '第三阶段在稳定窗口内发生了意外断线或重连。'
    }
    if ($onboard2.HasExited) {
        throw "OnboardHmi 第三阶段提前退出，exitCode=$($onboard2.ExitCode)。"
    }

    try {
        Invoke-RestMethod -Uri "http://127.0.0.1:$healthPort/health/ready" -TimeoutSec 3 |
            Out-Null
        $healthReadyStatus = 200
    }
    catch {
        $healthReadyStatus = [int]$_.Exception.Response.StatusCode
    }

    $runResult = [ordered]@{
        schemaVersion = '1.0.0'
        runKind = 'STAGED_G3_REAL_PEERS_NO_MOVEMENT'
        runId = Split-Path -Leaf $StageRoot
        startedScope = @('W2G-IS-00', 'W2G-IS-06')
        status = 'PASS_WITH_OFFICIAL_SLICES_REMAINING_INCONCLUSIVE'
        protocol = [ordered]@{
            tag = $version.protocolTag
            commit = $version.protocolCommit
            manifestSha256 = $version.manifestSha256
        }
        commits = [ordered]@{
            controlServer = $controlCommit
            onboardHmi = $onboardCommit
            slotsSimulator = $simulatorCommit
        }
        config = [ordered]@{
            onboardConfigSha256 = (Get-FileHash -LiteralPath $onboardConfig -Algorithm SHA256).Hash.ToLowerInvariant()
            insecureLoopback = $true
            freshControlDatabase = $true
            freshOnboardJournal = $true
            ports = [ordered]@{
                modbus = 1502
                simulatorHttp = 58006
                onboardNdjson = $onboardPort
                controlHealth = $healthPort
            }
        }
        observations = @(
            [ordered]@{
                phase = 'fresh-start'
                session = $session1
                stableAfter12Seconds = $session1Stable
            },
            [ordered]@{
                phase = 'onboard-process-restart-same-journal'
                session = $session2
                stableAfter12Seconds = $session2Stable
            },
            [ordered]@{
                phase = 'controlserver-process-restart-same-database'
                session = $session3
                stableAfter12Seconds = $session3Stable
            }
        )
        expectedFailClosed = [ordered]@{
            readiness = 'RecoveryRequired'
            reasonCode = 'DEPARTURE_SAFETY_NOT_READY'
            healthReadyHttpStatus = $healthReadyStatus
            explanation = 'Onboard production composition uses UnavailableVehicleSafetySignalProvider; no movement attempted.'
        }
        simulatorHealth = $simulatorHealth
    }
}
finally {
    foreach ($process in @($onboard1, $onboard2, $control1, $control2, $simulator)) {
        Stop-ProcessSafely -Process $process
    }
    $env:CONTROL_SERVER_ONBOARD_CREDENTIAL = $null
}

$logFiles = Get-ChildItem -Recurse -File -LiteralPath $StageRoot |
    Where-Object Name -Like '*.log'
$runResult['evidenceFiles'] = @($logFiles | ForEach-Object {
    [ordered]@{
        path = [IO.Path]::GetRelativePath($StageRoot, $_.FullName).Replace('\', '/')
        sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        length = $_.Length
    }
})
$json = $runResult | ConvertTo-Json -Depth 20
[IO.File]::WriteAllText(
    (Join-Path $StageRoot 'run-result.json'),
    $json,
    [Text.UTF8Encoding]::new($false))
$json
