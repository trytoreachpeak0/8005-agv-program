param(
    [string]$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path,
    [string]$FixedHead = '1469d6309d00b0abb792f6cd686aed68286e638e',
    [string]$InventoryPath = (Join-Path $PSScriptRoot '..\material-inventory\material-inventory.tsv'),
    [string]$CorrectionPath = (Join-Path $PSScriptRoot 'git-status-corrections.tsv')
)

$ErrorActionPreference = 'Stop'

function Normalize-RepositoryPath {
    param([string]$Path)
    $normalized = $Path -replace '\\', '/'
    if ($normalized.StartsWith('./', [StringComparison]::Ordinal)) {
        return $normalized.Substring(2)
    }
    return $normalized
}

Push-Location -LiteralPath $RepositoryRoot
try {
    $inventoryRows = @(Import-Csv -Delimiter "`t" -LiteralPath $InventoryPath)
    $correctionRows = @(Import-Csv -Delimiter "`t" -LiteralPath $CorrectionPath)

    if ($correctionRows.Count -ne 58) {
        throw "Expected 58 corrections, found $($correctionRows.Count)."
    }
    if (@($correctionRows | Group-Object path | Where-Object Count -ne 1).Count -ne 0) {
        throw 'Correction table contains duplicate paths.'
    }

    $tracked = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    git -c core.quotepath=false ls-tree -r --name-only $FixedHead |
        ForEach-Object { [void]$tracked.Add((Normalize-RepositoryPath $_)) }
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read fixed HEAD $FixedHead."
    }

    $inventoryByPath = @{}
    foreach ($row in $inventoryRows) {
        $inventoryByPath[$row.path] = $row
    }
    $correctionByPath = @{}
    foreach ($row in $correctionRows) {
        $inventory = $inventoryByPath[$row.path]
        if ($null -eq $inventory) {
            throw "Correction path is absent from inventory: $($row.path)"
        }
        if ($inventory.git_status -ne $row.original_git_status) {
            throw "Original status mismatch for $($row.path): inventory=$($inventory.git_status), correction=$($row.original_git_status)"
        }
        if ($row.original_git_status -ne 'untracked' -or $row.corrected_git_status -ne 'tracked-clean') {
            throw "Unexpected correction transition for $($row.path)."
        }
        if (-not $tracked.Contains($row.path)) {
            throw "Correction path is absent from fixed HEAD: $($row.path)"
        }
        $actualBlob = (git rev-parse "$FixedHead`:$($row.path)").Trim()
        if ($LASTEXITCODE -ne 0 -or $actualBlob -ne $row.fixed_head_blob) {
            throw "Fixed HEAD blob mismatch for $($row.path)."
        }
        $correctionByPath[$row.path] = $row.corrected_git_status
    }

    $effectiveCounts = @{}
    $falseUntracked = [System.Collections.Generic.List[string]]::new()
    foreach ($row in $inventoryRows) {
        $status = if ($correctionByPath.ContainsKey($row.path)) {
            $correctionByPath[$row.path]
        }
        else {
            $row.git_status
        }
        if (-not $effectiveCounts.ContainsKey($status)) {
            $effectiveCounts[$status] = 0
        }
        $effectiveCounts[$status] += 1
        if ($status -eq 'untracked' -and $tracked.Contains($row.path)) {
            $falseUntracked.Add($row.path)
        }
    }

    if ($falseUntracked.Count -ne 0) {
        throw "False untracked paths remain: $($falseUntracked -join ', ')"
    }
    if ($effectiveCounts['tracked-clean'] -ne 1762 -or $effectiveCounts['untracked'] -ne 47) {
        throw "Unexpected effective counts: tracked-clean=$($effectiveCounts['tracked-clean']), untracked=$($effectiveCounts['untracked'])"
    }

    Write-Output "fixed_head=$FixedHead"
    Write-Output "corrections=$($correctionRows.Count)"
    Write-Output "false_untracked=$($falseUntracked.Count)"
    Write-Output "tracked-clean=$($effectiveCounts['tracked-clean'])"
    Write-Output "untracked=$($effectiveCounts['untracked'])"
}
finally {
    Pop-Location
}

