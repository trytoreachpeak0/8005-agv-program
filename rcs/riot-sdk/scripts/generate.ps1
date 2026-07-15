<#
.SYNOPSIS
  Normalize OpenAPI specs and regenerate C# / Python Kiota clients for device/task/order.
#>
[CmdletBinding()]
param(
  [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

function Assert-Command([string]$Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $Name"
  }
}

Assert-Command kiota
Assert-Command python

$specsDir = Join-Path $RepoRoot "specs"
$normalizedDir = Join-Path $specsDir ".normalized"
$modules = @(
  @{ Name = "device"; Client = "DeviceClient"; CsNs = "RIoT.Sdk.Generated.Device"; PyNs = "riot_sdk.generated.device"; CsOut = "csharp/RIoT.Sdk.Generated/Device"; PyOut = "python/riot_sdk/generated/device" },
  @{ Name = "task";   Client = "TaskClient";   CsNs = "RIoT.Sdk.Generated.TaskApi"; PyNs = "riot_sdk.generated.task";   CsOut = "csharp/RIoT.Sdk.Generated/TaskApi"; PyOut = "python/riot_sdk/generated/task" },
  @{ Name = "order";  Client = "OrderClient";  CsNs = "RIoT.Sdk.Generated.Order";  PyNs = "riot_sdk.generated.order";  CsOut = "csharp/RIoT.Sdk.Generated/Order";  PyOut = "python/riot_sdk/generated/order" }
)

$inputs = @()
foreach ($m in $modules) {
  $path = Join-Path $specsDir "$($m.Name).json"
  if (-not (Test-Path $path)) { throw "Missing spec: $path" }
  $inputs += $path
}

Write-Host "==> Preprocess OpenAPI specs"
python (Join-Path $PSScriptRoot "preprocess_openapi.py") @inputs -o $normalizedDir
if ($LASTEXITCODE -ne 0) { throw "preprocess_openapi.py failed" }

foreach ($m in $modules) {
  $spec = Join-Path $normalizedDir "$($m.Name).json"
  $csOut = Join-Path $RepoRoot $m.CsOut
  $pyOut = Join-Path $RepoRoot $m.PyOut

  Write-Host "==> Generate C# $($m.Name) -> $($m.CsOut)"
  kiota generate `
    -l CSharp `
    -d $spec `
    -o $csOut `
    -c $m.Client `
    -n $m.CsNs `
    --clean-output
  if ($LASTEXITCODE -ne 0) { throw "Kiota C# generation failed for $($m.Name)" }

  Write-Host "==> Generate Python $($m.Name) -> $($m.PyOut)"
  kiota generate `
    -l Python `
    -d $spec `
    -o $pyOut `
    -c $m.Client `
    -n $m.PyNs `
    --clean-output
  if ($LASTEXITCODE -ne 0) { throw "Kiota Python generation failed for $($m.Name)" }
}

# Ensure package markers exist after --clean-output
$initPaths = @(
  (Join-Path $RepoRoot "python/riot_sdk/generated/__init__.py"),
  (Join-Path $RepoRoot "python/riot_sdk/generated/device/__init__.py"),
  (Join-Path $RepoRoot "python/riot_sdk/generated/task/__init__.py"),
  (Join-Path $RepoRoot "python/riot_sdk/generated/order/__init__.py")
)
foreach ($p in $initPaths) {
  if (-not (Test-Path $p)) {
    New-Item -ItemType File -Path $p -Force | Out-Null
  }
}

Write-Host "==> Done. Regenerated device/task/order for C# and Python."
