[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$SourceRoot,
    [Parameter(Mandatory = $true)][string]$ArtifactsDirectory
)

$ErrorActionPreference = "Stop"
$project = Join-Path $SourceRoot "MesIngest.Watch.UiTests\MesIngest.Watch.UiTests.csproj"
New-Item -ItemType Directory -Path $ArtifactsDirectory -Force | Out-Null
$env:DOTNET_CLI_TELEMETRY_OPTOUT = "1"
$env:TESTINGPLATFORM_TELEMETRY_OPTOUT = "1"
$env:MESINGEST_WATCH_UI_ARTIFACTS = $ArtifactsDirectory

dotnet restore $project --ignore-failed-sources -p:NuGetAudit=false 2>&1 |
    Tee-Object -LiteralPath (Join-Path $ArtifactsDirectory "restore.log")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

try {
    $env:MESINGEST_WATCH_REQUIRE_JOURNEY_ENVIRONMENT = "1"
    dotnet run `
        --project $project `
        --configuration Release `
        --no-restore `
        -- `
        -culture zh-CN `
        -trait Category=watch-ui-environment `
        -parallel none 2>&1 |
        Tee-Object -LiteralPath (Join-Path $ArtifactsDirectory "environment-probe.log")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $env:MESINGEST_WATCH_RUN_REAL_WINDOWS = "1"
    dotnet run `
        --project $project `
        --configuration Release `
        --no-restore `
        -- `
        -culture zh-CN `
        -trait Category=watch-ui-journeys `
        -parallel none 2>&1 |
        Tee-Object -LiteralPath (Join-Path $ArtifactsDirectory "watch-ui-journeys.runner.log")
    exit $LASTEXITCODE
} finally {
    Remove-Item Env:MESINGEST_WATCH_REQUIRE_JOURNEY_ENVIRONMENT -ErrorAction SilentlyContinue
    Remove-Item Env:MESINGEST_WATCH_RUN_REAL_WINDOWS -ErrorAction SilentlyContinue
    Remove-Item Env:MESINGEST_WATCH_UI_ARTIFACTS -ErrorAction SilentlyContinue
}
