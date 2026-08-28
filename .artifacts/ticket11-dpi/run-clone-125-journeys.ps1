[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Root)

$ErrorActionPreference = 'Stop'
$resultPath = Join-Path $Root 'dpi125-journeys-result.json'
$logPath = Join-Path $Root 'Results\dpi125-journeys.log'

try {
    $source = Join-Path $Root 'Source\mes\ingest\csharp'
    New-Item -ItemType Directory -Path (Join-Path $Root 'Results') -Force | Out-Null
    Set-Location -LiteralPath $source
    $env:NUGET_PACKAGES = 'C:\MesIngest\Ticket11\NuGetPackages'
    $env:NUGET_XMLDOC_MODE = 'skip'
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    $env:TESTINGPLATFORM_TELEMETRY_OPTOUT = '1'
    $env:DOTNET_NOLOGO = '1'
    $env:MesIngestWatch__RenderingMode = 'SoftwareOnly'

    & '.\Invoke-WatchUiTests.ps1' `
        -Configuration Release `
        -Suite watch-ui-journeys 2>&1 |
        Tee-Object -LiteralPath $logPath
    $exitCode = $LASTEXITCODE

    [pscustomobject]@{
        Status = if ($exitCode -eq 0) { 'PASSED' } else { 'FAILED' }
        ExitCode = $exitCode
        CompletedAt = [DateTimeOffset]::Now.ToString('O')
        Log = $logPath
    } | ConvertTo-Json | Set-Content -LiteralPath $resultPath -Encoding utf8
    exit $exitCode
}
catch {
    [pscustomobject]@{
        Status = 'FAILED'
        ExitCode = 1
        CompletedAt = [DateTimeOffset]::Now.ToString('O')
        Error = $_.Exception.Message
    } | ConvertTo-Json | Set-Content -LiteralPath $resultPath -Encoding utf8
    exit 1
}
