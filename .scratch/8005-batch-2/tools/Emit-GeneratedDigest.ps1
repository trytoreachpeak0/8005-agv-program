#Requires -Version 7
param(
    [Parameter(Mandatory)][string]$Generator,
    [Parameter(Mandatory)][string]$OutFile
)
$ErrorActionPreference = 'Stop'

$gen = Join-Path $env:TEMP ("fp-gen-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
try {
    node $Generator $gen | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "generate failed: $LASTEXITCODE" }

    $lines = Get-ChildItem -Recurse -File -LiteralPath $gen | ForEach-Object {
        $rel = [IO.Path]::GetRelativePath($gen, $_.FullName).Replace('\', '/')
        "$rel`t$((Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash)"
    }
    $sorted = $lines | Sort-Object
    [IO.File]::WriteAllLines($OutFile, $sorted)
    "wrote $($sorted.Count) entries to $OutFile"
}
finally {
    Remove-Item -Recurse -Force $gen -ErrorAction SilentlyContinue
}
