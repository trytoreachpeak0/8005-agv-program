[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Root)

$ErrorActionPreference = "Stop"
$resultPath = Join-Path $Root "journeys-result.json"
$logPath = Join-Path $Root "Results\watch-ui-journeys.log"

try {
    $source = Join-Path $Root "Source\mes\ingest\csharp"
    New-Item -ItemType Directory -Path (Join-Path $Root "Results") -Force | Out-Null
    Set-Location -LiteralPath $source

    $env:NUGET_PACKAGES = "C:\MesIngest\Ticket11\NuGetPackages"
    $env:NUGET_XMLDOC_MODE = "skip"
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = "1"
    $env:TESTINGPLATFORM_TELEMETRY_OPTOUT = "1"
    $env:DOTNET_NOLOGO = "1"

    .\Invoke-WatchUiTests.ps1 `
        -Configuration Release `
        -Suite watch-ui-journeys 2>&1 | Tee-Object -LiteralPath $logPath
    $exitCode = $LASTEXITCODE

    [pscustomobject]@{
        Status = if ($exitCode -eq 0) { "PASSED" } else { "FAILED" }
        ExitCode = $exitCode
        CompletedAt = [DateTimeOffset]::Now.ToString("O")
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
