<#
.SYNOPSIS
  Live smoke: login + list devices via the C# Facade.
#>
$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..")
$env:RIOT_SMOKE = "1"
if (-not $env:RIOT_BASE_URL) { $env:RIOT_BASE_URL = "http://172.19.206.222:8888" }
if (-not $env:RIOT_USERNAME) { $env:RIOT_USERNAME = "admin" }
if (-not $env:RIOT_PASSWORD) { $env:RIOT_PASSWORD = "admin" }

Write-Host "Smoke against $($env:RIOT_BASE_URL) as $($env:RIOT_USERNAME)"
dotnet test (Join-Path $repo "csharp/RIoT.Sdk.Tests") --filter FullyQualifiedName~Smoke
