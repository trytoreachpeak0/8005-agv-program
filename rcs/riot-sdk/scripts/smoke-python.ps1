<#
.SYNOPSIS
  Live smoke: login + list devices via the Python Facade.
#>
$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..")
$pyRoot = Join-Path $repo "python"
$env:RIOT_SMOKE = "1"
if (-not $env:RIOT_BASE_URL) { $env:RIOT_BASE_URL = "http://172.19.206.222:8888" }
if (-not $env:RIOT_USERNAME) { $env:RIOT_USERNAME = "admin" }
if (-not $env:RIOT_PASSWORD) { $env:RIOT_PASSWORD = "admin" }

$python = Join-Path $pyRoot ".venv/Scripts/python.exe"
if (-not (Test-Path $python)) {
  throw "Python venv missing. Run: cd python; python -m venv .venv; .\.venv\Scripts\pip install -e `".[dev]`""
}

Write-Host "Smoke against $($env:RIOT_BASE_URL) as $($env:RIOT_USERNAME)"
Set-Location $pyRoot
& $python -m pytest -q -k smoke --tb=short
