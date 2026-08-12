[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Root)

$ErrorActionPreference = "Stop"
$resultPath = Join-Path $Root "xaml-stability-result.json"
$logPath = Join-Path $Root "Results\xaml-stability.log"
$diagnostics = Join-Path $Root "Results\xaml-stability-diagnostics"

try {
    $source = Join-Path $Root "Source\mes\ingest\csharp"
    New-Item -ItemType Directory -Path (Join-Path $Root "Results") -Force | Out-Null
    Set-Location -LiteralPath $source

    $env:NUGET_PACKAGES = "C:\MesIngest\Ticket11\NuGetPackages"
    $env:NUGET_XMLDOC_MODE = "skip"
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = "1"
    $env:TESTINGPLATFORM_TELEMETRY_OPTOUT = "1"
    $env:DOTNET_NOLOGO = "1"
    $env:MES_INGEST_WATCH_BASELINE_DIRECTORY = Join-Path $source `
        "MesIngest.Watch.UiTests\Baselines\SelectedUi"

    # Copied golden runs must not retain CallerFilePath/project-directory constants
    # embedded by an earlier run. A clean rebuild makes Verify write only below Root.
    dotnet clean ".\MesIngest.Watch.UiTests\MesIngest.Watch.UiTests.csproj" `
        -c Release | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "clean failed: $LASTEXITCODE" }
    dotnet restore ".\MesIngest.Watch.UiTests\MesIngest.Watch.UiTests.csproj" `
        --packages $env:NUGET_PACKAGES `
        --ignore-failed-sources | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "restore failed: $LASTEXITCODE" }
    dotnet build ".\MesIngest.Watch.UiTests\MesIngest.Watch.UiTests.csproj" `
        -c Release `
        --no-restore | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "build failed: $LASTEXITCODE" }

    & "C:\Program Files\PowerShell\7\pwsh.exe" `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -STA `
        -File (Join-Path $source "Test-WatchXamlBaselineStability.ps1") `
        -Configuration Release `
        -Runs 10 `
        -DiagnosticsDirectory $diagnostics 2>&1 | Tee-Object -LiteralPath $logPath
    $exitCode = $LASTEXITCODE

    $candidateDirectory = Join-Path $source "MesIngest.Watch.UiTests\Baselines\SelectedUi"
    $received = @(Get-ChildItem $candidateDirectory -Filter "*.received.*" -File -ErrorAction SilentlyContinue)
    [pscustomobject]@{
        Status = if ($exitCode -eq 0) { "PASSED" } else { "FAILED" }
        ExitCode = $exitCode
        CompletedAt = [DateTimeOffset]::Now.ToString("O")
        ReceivedCount = $received.Count
        ReceivedPngCount = @($received | Where-Object Extension -eq ".png").Count
        ReceivedXmlCount = @($received | Where-Object Extension -eq ".xml").Count
        CandidateDirectory = $candidateDirectory
        Diagnostics = $diagnostics
        Log = $logPath
    } | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $resultPath -Encoding utf8
    exit $exitCode
} catch {
    [pscustomobject]@{
        Status = "FAILED"
        ExitCode = 1
        CompletedAt = [DateTimeOffset]::Now.ToString("O")
        Error = $_.Exception.Message
    } | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $resultPath -Encoding utf8
    exit 1
}
