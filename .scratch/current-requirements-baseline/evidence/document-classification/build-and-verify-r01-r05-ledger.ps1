param(
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\..'))
$inventoryPath = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\material-inventory\material-inventory.tsv'
$correctionsPath = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\initial-snapshot\git-status-corrections.tsv'
$investigationsDir = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\investigations'
$ledgerPath = Join-Path $PSScriptRoot 'R01-R05-document-evidence-ledger.tsv'
$batchIds = @('R01', 'R02', 'R03', 'R04', 'R05')

function Normalize-Text {
    param([AllowEmptyString()][string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return ''
    }

    return (($Text -replace '\r?\n', ' ' -replace '\s+', ' ').Trim())
}

function Resolve-ReportLink {
    param(
        [Parameter(Mandatory)][string]$ReportDirectory,
        [Parameter(Mandatory)][string]$Href
    )

    $decoded = [Uri]::UnescapeDataString($Href)
    $absolute = [IO.Path]::GetFullPath((Join-Path $ReportDirectory $decoded))
    return [IO.Path]::GetRelativePath($repoRoot, $absolute).Replace('\', '/')
}

function Get-MarkdownCells {
    param([Parameter(Mandatory)][string]$Line)

    return @($Line.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() })
}

function Get-R01-Bullet {
    param(
        [Parameter(Mandatory)][string]$Body,
        [Parameter(Mandatory)][string[]]$Labels
    )

    foreach ($line in ($Body -split '\r?\n')) {
        foreach ($label in $Labels) {
            if ($line -match ('^- \*\*' + [regex]::Escape($label) + '：\*\*\s*(?<value>.*)$')) {
                return Normalize-Text $Matches.value
            }
        }
    }

    return ''
}

$inventory = @(Import-Csv -LiteralPath $inventoryPath -Delimiter "`t" | Where-Object { $_.batch_id -in $batchIds })
if ($inventory.Count -ne 202) {
    throw "Expected 202 R01-R05 inventory rows, found $($inventory.Count)."
}

$inventoryByPath = @{}
foreach ($item in $inventory) {
    if ($inventoryByPath.ContainsKey($item.path)) {
        throw "Duplicate inventory path: $($item.path)"
    }
    $inventoryByPath[$item.path] = $item
}

$correctionsByPath = @{}
foreach ($correction in (Import-Csv -LiteralPath $correctionsPath -Delimiter "`t")) {
    if ($correctionsByPath.ContainsKey($correction.path)) {
        throw "Duplicate Git status correction path: $($correction.path)"
    }
    $correctionsByPath[$correction.path] = $correction
}

$recordsByPath = @{}

function Add-LedgerRecord {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Sequence,
        [Parameter(Mandatory)][string]$DocumentClass,
        [Parameter(Mandatory)][string]$SourceType,
        [Parameter(Mandatory)][string]$CurrentApplicability,
        [Parameter(Mandatory)][string]$HistoryDerivation,
        [Parameter(Mandatory)][string]$AtomicExtractionRoute,
        [Parameter(Mandatory)][string]$EvidenceOrConflictPointers,
        [Parameter(Mandatory)][string]$InvestigationPointer
    )

    if (-not $inventoryByPath.ContainsKey($Path)) {
        throw "Report record is outside the R01-R05 inventory: $Path"
    }
    if ($recordsByPath.ContainsKey($Path)) {
        throw "Duplicate report classification for: $Path"
    }

    $item = $inventoryByPath[$Path]
    $absolutePath = Join-Path $repoRoot $Path
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) {
        throw "Fixed inventory file is missing: $Path"
    }

    $actualHash = (Get-FileHash -LiteralPath $absolutePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $item.sha256.ToLowerInvariant()) {
        throw "Hash drift for $Path. Inventory=$($item.sha256), current=$actualHash"
    }

    $effectiveGitStatus = $item.git_status
    if ($correctionsByPath.ContainsKey($Path)) {
        $correction = $correctionsByPath[$Path]
        if ($correction.original_git_status -ne $item.git_status) {
            throw "Git status correction does not match inventory for $Path"
        }
        $effectiveGitStatus = $correction.corrected_git_status
    }

    $record = [PSCustomObject][ordered]@{
        record_id                         = "$($item.batch_id)-$Sequence"
        batch_id                          = $item.batch_id
        path                              = $item.path
        sha256                            = $item.sha256.ToLowerInvariant()
        bytes                             = $item.bytes
        inventory_snapshot_git_status     = $item.git_status
        effective_snapshot_git_status     = $effectiveGitStatus
        inventory_material_role           = $item.material_role
        document_class                    = Normalize-Text $DocumentClass
        source_type                       = Normalize-Text $SourceType
        current_applicability              = Normalize-Text $CurrentApplicability
        history_or_derivation              = Normalize-Text $HistoryDerivation
        approval_named_authorizer          = 'not-found'
        approval_date                      = 'not-found'
        approval_scope                     = 'not-found'
        approval_version_binding           = 'not-found'
        document_approval_state            = 'not-approved-by-this-classification'
        atomic_requirement_extraction_route = Normalize-Text $AtomicExtractionRoute
        evidence_or_conflict_pointers       = Normalize-Text $EvidenceOrConflictPointers
        investigation_pointer              = Normalize-Text $InvestigationPointer
    }

    foreach ($property in $record.PSObject.Properties) {
        if ([string]::IsNullOrWhiteSpace([string]$property.Value)) {
            throw "Empty required field '$($property.Name)' for $Path"
        }
    }

    $recordsByPath[$Path] = $record
}

# R01 uses one headed section per fixed file rather than a Markdown matrix.
$r01Name = 'R01-customer-project-source-materials.md'
$r01Path = Join-Path $investigationsDir $r01Name
$r01Text = Get-Content -LiteralPath $r01Path -Raw
$r01Pattern = '(?ms)^### R01-(?<sequence>\d{2}) `(?<path>[^`]+)`\r?\n(?<body>.*?)(?=^### |^## |\z)'
$r01Matches = [regex]::Matches($r01Text, $r01Pattern)
if ($r01Matches.Count -ne 19) {
    throw "Expected 19 R01 report sections, found $($r01Matches.Count)."
}

foreach ($match in $r01Matches) {
    $sequence = $match.Groups['sequence'].Value
    $path = $match.Groups['path'].Value
    $body = $match.Groups['body'].Value
    $classMatch = [regex]::Match($body, '文档级分类：\*\*(?<class>[^*]+)\*\*')
    if (-not $classMatch.Success) {
        throw "R01 section has no explicit document classification: $path"
    }

    $sourceHistory = Get-R01-Bullet -Body $body -Labels @('来源/时间/历史', '来源/形成与捕获', '来源/形成与历史', '来源/历史')
    $relationship = Get-R01-Bullet -Body $body -Labels @('版本/重复关系', '版本/关系', '版本/重复/派生关系')
    $approvalScope = Get-R01-Bullet -Body $body -Labels @('批准/范围/适用', '具名批准/范围/适用', '具名批准/批准范围', '批准/范围', '具名批准/范围', '具名批准/批准范围/适用')
    $missingEvidence = Get-R01-Bullet -Body $body -Labels @('缺失证据与分类')
    $atomicPointer = Get-R01-Bullet -Body $body -Labels @('原子指针')
    if ([string]::IsNullOrWhiteSpace($atomicPointer)) {
        throw "R01 section has no atomic pointer: $path"
    }

    $atomicRoute = if ($atomicPointer -match '^(不从本文件提取|不提取需求|不重复生成需求条目|不提取示例为需求)|README 本身不生成') {
        'do-not-extract-from-this-document'
    }
    else {
        'candidate-only-after-atomic-decomposition-evidence-review-and-explicit-approval'
    }

    Add-LedgerRecord `
        -Path $path `
        -Sequence $sequence `
        -DocumentClass $classMatch.Groups['class'].Value `
        -SourceType $classMatch.Groups['class'].Value `
        -CurrentApplicability "$approvalScope $missingEvidence" `
        -HistoryDerivation "$sourceHistory $relationship" `
        -AtomicExtractionRoute $atomicRoute `
        -EvidenceOrConflictPointers "$atomicPointer; detailed evidence gaps and any conflict candidates: $r01Name section R01-$sequence" `
        -InvestigationPointer "$r01Name#R01-$sequence"
}

$tableReports = @(
    [PSCustomObject]@{ Batch = 'R02'; Name = 'R02-requirements-framing-and-business-rules.md'; Expected = 27 },
    [PSCustomObject]@{ Batch = 'R03'; Name = 'R03-use-cases.md'; Expected = 48 },
    [PSCustomObject]@{ Batch = 'R04'; Name = 'R04-functional-requirements.md'; Expected = 41 },
    [PSCustomObject]@{ Batch = 'R05'; Name = 'R05-site-operation-acceptance-scenarios.md'; Expected = 67 }
)

foreach ($report in $tableReports) {
    $reportPath = Join-Path $investigationsDir $report.Name
    $reportDirectory = Split-Path -Parent $reportPath
    $lineNumber = 0
    $matchedRows = 0

    foreach ($line in (Get-Content -LiteralPath $reportPath)) {
        $lineNumber++
        if ($line -notmatch '^\|' -or $line -notmatch '\[[^\]]+\]\((?<href>[^)]+)\)') {
            continue
        }

        $path = Resolve-ReportLink -ReportDirectory $reportDirectory -Href $Matches.href
        if (-not $inventoryByPath.ContainsKey($path) -or $inventoryByPath[$path].batch_id -ne $report.Batch) {
            continue
        }

        $cells = Get-MarkdownCells -Line $line
        $matchedRows++
        $sequence = $matchedRows.ToString('00')
        $documentClass = ''
        $sourceType = ''
        $currentApplicability = ''
        $historyDerivation = ''
        $atomicRoute = ''
        $evidencePointers = ''

        switch ($report.Batch) {
            'R02' {
                if ($cells.Count -ne 5) { throw "Unexpected R02 matrix width at line $lineNumber" }
                $sequence = $cells[0].PadLeft(2, '0')
                $classMatch = [regex]::Match($cells[4], '\*\*(?<class>[^*]+)\*\*')
                $documentClass = if ($classMatch.Success) { $classMatch.Groups['class'].Value } else { 'document-level-investigation-classification' }
                $sourceType = $documentClass
                $historyDerivation = "$($cells[1]); $($cells[2])"
                $currentApplicability = $cells[4]
                $number = [int]$sequence
                $atomicRoute = if ($number -in @(1, 2, 3, 4, 5, 6, 25, 27)) {
                    'do-not-extract-from-this-document'
                }
                else {
                    'candidate-only-after-atomic-decomposition-evidence-review-and-explicit-approval'
                }
                $evidencePointers = "$($cells[3]); $($cells[4]); detailed record: $($report.Name) matrix row $sequence"
            }
            'R03' {
                if ($cells.Count -ne 3) { throw "Unexpected R03 matrix width at line $lineNumber" }
                $codeMatch = [regex]::Match($cells[2], '`(?<code>[CIGT])`')
                if (-not $codeMatch.Success) { throw "R03 row has no classification code at line $lineNumber" }
                $code = $codeMatch.Groups['code'].Value
                $documentClass = "R03-$code"
                $sourceType = switch ($code) {
                    'C' { 'unapproved-use-case-candidate-for-human-review' }
                    'I' { 'unapproved-internal-design-exploration' }
                    'G' { 'writing-guide' }
                    'T' { 'empty-placeholder-or-todo' }
                }
                $historyDerivation = "$($cells[0]); $($cells[1])"
                $currentApplicability = $cells[2]
                $atomicRoute = switch ($code) {
                    'C' { 'candidate-only-after-flow-level-decomposition-evidence-review-and-explicit-approval' }
                    'I' { 'split-business-design-interface-and-safety-claims-before-evidence-review-and-explicit-approval' }
                    default { 'do-not-extract-from-this-document' }
                }
                $evidencePointers = "$($cells[2]); detailed record: $($report.Name) line $lineNumber"
            }
            'R04' {
                if ($cells.Count -ne 4) { throw "Unexpected R04 matrix width at line $lineNumber" }
                $sequence = $cells[0].PadLeft(2, '0')
                $number = [int]$sequence
                if ($number -le 31) {
                    $documentClass = 'internal-derived-draft-functional-requirement-candidate'
                    $sourceType = 'unapproved-internal-derived-functional-requirement'
                    $atomicRoute = 'candidate-only-after-acceptance-criterion-level-decomposition-evidence-review-and-explicit-approval'
                }
                elseif ($number -le 39) {
                    $documentClass = 'placeholder-or-completeness-index'
                    $sourceType = 'empty-domain-placeholder'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                elseif ($number -eq 40) {
                    $documentClass = 'writing-guide'
                    $sourceType = 'recording-guidance'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                else {
                    $documentClass = 'directory-index'
                    $sourceType = 'navigation-index'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                $historyDerivation = "$($cells[1]); $($cells[2])"
                $currentApplicability = $cells[3]
                $evidencePointers = "$($cells[3]); detailed record: $($report.Name) matrix row $sequence"
            }
            'R05' {
                if ($cells.Count -ne 5) { throw "Unexpected R05 matrix width at line $lineNumber" }
                $codeMatch = [regex]::Match($cells[4], '(?<code>C[12])')
                if (-not $codeMatch.Success) { throw "R05 row has no C1/C2 classification at line $lineNumber" }
                $code = $codeMatch.Groups['code'].Value
                $documentClass = "R05-$code"
                $sourceType = if ($code -eq 'C1') {
                    'unapproved-acceptance-draft-derived-from-draft-FR-AC'
                }
                else {
                    'unapproved-acceptance-draft-mixing-FR-AC-with-internal-design'
                }
                $historyDerivation = "$($cells[1]); derived object: $($cells[2])"
                $currentApplicability = "$($cells[3]); $($cells[4]); not executed"
                $atomicRoute = if ($code -eq 'C1') {
                    'candidate-only-after-scenario-level-evidence-review-and-explicit-approval'
                }
                else {
                    'split-business-acceptance-from-design-interface-and-safety-claims-before-explicit-approval'
                }
                $evidencePointers = "$($cells[2]); $($cells[4]); detailed record: $($report.Name) line $lineNumber; execution evidence remains separate"
            }
        }

        Add-LedgerRecord `
            -Path $path `
            -Sequence $sequence `
            -DocumentClass $documentClass `
            -SourceType $sourceType `
            -CurrentApplicability $currentApplicability `
            -HistoryDerivation $historyDerivation `
            -AtomicExtractionRoute $atomicRoute `
            -EvidenceOrConflictPointers $evidencePointers `
            -InvestigationPointer "$($report.Name):$lineNumber"
    }

    if ($matchedRows -ne $report.Expected) {
        throw "Expected $($report.Expected) $($report.Batch) matrix rows, found $matchedRows."
    }
}

if ($recordsByPath.Count -ne $inventory.Count) {
    $missing = @($inventory | Where-Object { -not $recordsByPath.ContainsKey($_.path) } | ForEach-Object { $_.path })
    $extra = @($recordsByPath.Keys | Where-Object { -not $inventoryByPath.ContainsKey($_) })
    throw "Coverage mismatch. records=$($recordsByPath.Count), inventory=$($inventory.Count), missing=[$($missing -join '; ')], extra=[$($extra -join '; ')]"
}

$records = @($recordsByPath.Values | Sort-Object batch_id, record_id, path)
$expectedPerBatch = @{ R01 = 19; R02 = 27; R03 = 48; R04 = 41; R05 = 67 }
foreach ($batch in $batchIds) {
    $count = @($records | Where-Object { $_.batch_id -eq $batch }).Count
    if ($count -ne $expectedPerBatch[$batch]) {
        throw "Expected $($expectedPerBatch[$batch]) records for $batch, found $count."
    }
}

if (@($records | Where-Object { $_.document_approval_state -ne 'not-approved-by-this-classification' }).Count -ne 0) {
    throw 'A document classification was incorrectly promoted to approval.'
}

if ($VerifyOnly) {
    if (-not (Test-Path -LiteralPath $ledgerPath -PathType Leaf)) {
        throw "Ledger does not exist: $ledgerPath"
    }
    $persisted = @(Import-Csv -LiteralPath $ledgerPath -Delimiter "`t")
    if ($persisted.Count -ne $records.Count) {
        throw "Persisted ledger row count mismatch. expected=$($records.Count), actual=$($persisted.Count)"
    }

    $persistedByPath = @{}
    foreach ($row in $persisted) {
        if ($persistedByPath.ContainsKey($row.path)) { throw "Duplicate persisted path: $($row.path)" }
        $persistedByPath[$row.path] = $row
    }

    foreach ($expected in $records) {
        if (-not $persistedByPath.ContainsKey($expected.path)) { throw "Persisted ledger misses: $($expected.path)" }
        $actual = $persistedByPath[$expected.path]
        foreach ($property in $expected.PSObject.Properties.Name) {
            if ([string]$actual.$property -ne [string]$expected.$property) {
                throw "Persisted value mismatch for $($expected.path), field $property"
            }
        }
    }
}
else {
    $records | Export-Csv -LiteralPath $ledgerPath -Delimiter "`t" -NoTypeInformation -Encoding utf8
}

$summary = $records | Group-Object batch_id | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Count)" }
Write-Output "R01-R05 ledger verified: total=$($records.Count); $($summary -join '; '); missing=0; duplicates=0; hash_drift=0; approved_by_classification=0"
