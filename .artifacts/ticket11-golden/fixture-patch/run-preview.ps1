[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$Root)

$ErrorActionPreference = "Stop"
$resultPath = Join-Path $Root "preview-result.json"
$logPath = Join-Path $Root "Results\four-page-previews.log"

try {
    $source = Join-Path $Root "Source\mes\ingest\csharp"
    $artifacts = Join-Path $Root "Results\four-page-previews"
    New-Item -ItemType Directory -Path $artifacts -Force | Out-Null
    Set-Location -LiteralPath $source

    $env:NUGET_PACKAGES = "C:\MesIngest\Ticket11\NuGetPackages"
    $env:NUGET_XMLDOC_MODE = "skip"
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = "1"
    $env:TESTINGPLATFORM_TELEMETRY_OPTOUT = "1"
    $env:DOTNET_NOLOGO = "1"
    $env:MESINGEST_WATCH_RUN_REAL_WINDOWS = "1"
    $env:MESINGEST_WATCH_UI_ARTIFACTS = $artifacts

    if ([string]::IsNullOrWhiteSpace($env:SESSIONNAME)) {
        $sessionId = [Diagnostics.Process]::GetCurrentProcess().SessionId
        $explorer = Get-Process explorer -ErrorAction SilentlyContinue |
            Where-Object SessionId -eq $sessionId |
            Select-Object -First 1
        if ($null -eq $explorer) {
            throw "No Explorer process exists in interactive session $sessionId."
        }
        $env:SESSIONNAME = "Console"
    }

    dotnet run `
        --project .\MesIngest.Watch.UiTests\MesIngest.Watch.UiTests.csproj `
        --configuration Release `
        --no-restore `
        -- `
        -trait Category=watch-ticket11-previews `
        -parallel none 2>&1 | Tee-Object -LiteralPath $logPath
    $exitCode = $LASTEXITCODE

    [pscustomobject]@{
        Status = if ($exitCode -eq 0) { "PASSED" } else { "FAILED" }
        ExitCode = $exitCode
        CompletedAt = [DateTimeOffset]::Now.ToString("O")
        Artifacts = $artifacts
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
} finally {
    Remove-Item Env:MESINGEST_WATCH_RUN_REAL_WINDOWS -ErrorAction SilentlyContinue
    Remove-Item Env:MESINGEST_WATCH_UI_ARTIFACTS -ErrorAction SilentlyContinue
}
