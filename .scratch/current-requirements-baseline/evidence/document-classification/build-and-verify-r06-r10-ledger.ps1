param(
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\..'))
$inventoryPath = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\material-inventory\material-inventory.tsv'
$correctionsPath = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\initial-snapshot\git-status-corrections.tsv'
$investigationsDir = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\investigations'
$ledgerPath = Join-Path $PSScriptRoot 'R06-R10-document-evidence-ledger.tsv'
$batchIds = @('R06', 'R07', 'R08', 'R09', 'R10')

function Normalize-Text {
    param([AllowEmptyString()][string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return ''
    }

    return (($Text -replace '<br\s*/?>', '; ' -replace '\r?\n', ' ' -replace '\s+', ' ').Trim())
}

function Get-MarkdownCells {
    param([Parameter(Mandatory)][string]$Line)

    return @($Line.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() })
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

$inventory = @(Import-Csv -LiteralPath $inventoryPath -Delimiter "`t" | Where-Object { $_.batch_id -in $batchIds })
if ($inventory.Count -ne 201) {
    throw "Expected 201 R06-R10 inventory rows, found $($inventory.Count)."
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
        throw "Report record is outside the R06-R10 inventory: $Path"
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
        record_id                          = "$($item.batch_id)-$Sequence"
        batch_id                           = $item.batch_id
        path                               = $item.path
        sha256                             = $item.sha256.ToLowerInvariant()
        bytes                              = $item.bytes
        inventory_snapshot_git_status      = $item.git_status
        effective_snapshot_git_status      = $effectiveGitStatus
        inventory_material_role            = $item.material_role
        document_class                     = Normalize-Text $DocumentClass
        source_type                        = Normalize-Text $SourceType
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

$reports = @(
    [PSCustomObject]@{ Batch = 'R06'; Name = 'R06-slot-hardware-fleet-test-cases.md'; Expected = 65 },
    [PSCustomObject]@{ Batch = 'R07'; Name = 'R07-traceability-and-nonfunctional-requirements.md'; Expected = 15 },
    [PSCustomObject]@{ Batch = 'R08'; Name = 'R08-cross-domain-vocabulary-and-decisions.md'; Expected = 57 },
    [PSCustomObject]@{ Batch = 'R09'; Name = 'R09-mes-sdk-decisions.md'; Expected = 18 },
    [PSCustomObject]@{ Batch = 'R10'; Name = 'R10-slot-simulator-materials.md'; Expected = 46 }
)

foreach ($report in $reports) {
    $reportPath = Join-Path $investigationsDir $report.Name
    $reportDirectory = Split-Path -Parent $reportPath
    $lineNumber = 0
    $matchedRows = 0

    foreach ($line in (Get-Content -LiteralPath $reportPath)) {
        $lineNumber++
        if ($line -notmatch '^\|') {
            continue
        }

        $path = ''
        switch ($report.Batch) {
            'R06' {
                $pathMatch = [regex]::Match($line, '`(?<path>requirement-documents/[^`:]+\.md)(?::[^`]*)?`')
                if ($pathMatch.Success) { $path = $pathMatch.Groups['path'].Value }
            }
            'R09' {
                $pathMatch = [regex]::Match($line, '`(?<path>docs/adr/[^`:]+\.md)(?::[^`]*)?`')
                if ($pathMatch.Success) { $path = $pathMatch.Groups['path'].Value }
            }
            default {
                $hrefMatch = [regex]::Match($line, '\[[^\]]+\]\((?<href>[^)]+)\)')
                if ($hrefMatch.Success) {
                    $candidate = Resolve-ReportLink -ReportDirectory $reportDirectory -Href $hrefMatch.Groups['href'].Value
                    if ($inventoryByPath.ContainsKey($candidate) -and $inventoryByPath[$candidate].batch_id -eq $report.Batch) {
                        $path = $candidate
                    }
                }
            }
        }

        if ([string]::IsNullOrWhiteSpace($path) -or -not $inventoryByPath.ContainsKey($path) -or $inventoryByPath[$path].batch_id -ne $report.Batch) {
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
            'R06' {
                if ($cells.Count -notin @(3, 4)) { throw "Unexpected R06 matrix width at line $lineNumber" }
                $classCell = $cells[-1]
                $codeMatch = [regex]::Match($classCell, '^\s*(?<code>[ADPI])；')
                if (-not $codeMatch.Success) { throw "R06 row has no A/D/P/I classification at line $lineNumber" }
                $code = $codeMatch.Groups['code'].Value
                $documentClass = "R06-$code"
                $sourceType = switch ($code) {
                    'A' { 'unapproved-internal-derived-test-case-draft' }
                    'D' { 'upstream-drifted-internal-test-case-draft' }
                    'P' { 'empty-test-domain-placeholder' }
                    'I' { 'test-library-index-and-writing-rule' }
                }
                $currentApplicability = "$classCell; no test execution evidence"
                $historyDerivation = if ($cells.Count -eq 4) { $cells[2] } else { 'repository test-library structure' }
                $atomicRoute = switch ($code) {
                    'A' { 'candidate-only-after-scenario-level-decomposition-deduplication-source-review-and-explicit-approval' }
                    'D' { 'blocked-until-upstream-version-drift-is-rewritten-or-explicitly-version-bound' }
                    default { 'do-not-extract-from-this-document' }
                }
                $evidencePointers = "$classCell; retain upstream FR/UC/BR pointers and R06 overlap/drift findings; execution evidence remains separate"
            }
            'R07' {
                if ($cells.Count -ne 4) { throw "Unexpected R07 matrix width at line $lineNumber" }
                $documentClass = $cells[3]
                if ($path -match '/nfr-00[12]-') {
                    $sourceType = 'unapproved-internal-derived-nonfunctional-requirement-draft'
                    $atomicRoute = 'candidate-only-after-fit-criterion-level-decomposition-source-review-and-explicit-approval'
                }
                elseif ($path -match 'traceability-matrix') {
                    $sourceType = 'derived-dynamic-traceability-query-definition'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                elseif ($path -match 'classification-rules') {
                    $sourceType = 'internal-classification-and-archiving-rule'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                elseif ($path -match 'template-guide') {
                    $sourceType = 'writing-and-recording-guidance'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                else {
                    $sourceType = 'empty-category-placeholder-or-library-index'
                    $atomicRoute = 'do-not-extract-from-this-document'
                }
                $currentApplicability = $cells[3]
                $historyDerivation = $cells[2]
                $evidencePointers = "$($cells[2]); $($cells[3]); preserve dynamic-query-versus-snapshot and metric-TBD boundaries"
            }
            'R08' {
                if ($cells.Count -ne 5) { throw "Unexpected R08 matrix width at line $lineNumber" }
                $historyCode = Normalize-Text $cells[2]
                $documentClass = $cells[3]
                $sourceType = switch ($historyCode) {
                    'H1' { 'ai-modified-current-vocabulary-and-domain-context-without-confirmation' }
                    'H2' { 'internal-adr-of-unknown-decision-source' }
                    'H3' { 'ai-generated-or-modified-internal-adr-without-confirmation' }
                    'H4' { 'legacy-vocabulary-carrier-of-unknown-decision-source' }
                    default { throw "Unexpected R08 history code '$historyCode' at line $lineNumber" }
                }
                $currentApplicability = $cells[4]
                $historyDerivation = "$historyCode; see R08 identity/history groups and any explicit supersession"
                if ($path -match '/0038-' -or $path -match '/0045-') {
                    $atomicRoute = 'do-not-extract-superseded-historical-material'
                }
                elseif ($documentClass -match 'BR\?|DM|PF|(^|\s)V(\s|$)') {
                    $atomicRoute = 'candidate-only-after-separating-vocabulary-domain-business-physical-and-design-claims-source-review-and-explicit-approval'
                }
                else {
                    $atomicRoute = 'do-not-extract-as-requirement; retain-for-separate-technical-decision-review'
                }
                $evidencePointers = "$($cells[4]); preserve R08 conflict, supersession, physical-evidence and dual-vocabulary-entry findings"
            }
            'R09' {
                if ($cells.Count -ne 3) { throw "Unexpected R09 matrix width at line $lineNumber" }
                $codeMatch = [regex]::Match($cells[2], '`(?<code>[RMLI])`')
                if (-not $codeMatch.Success) { throw "R09 row has no R/M/L/I classification at line $lineNumber" }
                $code = $codeMatch.Groups['code'].Value
                $documentClass = "R09-$code"
                $sourceType = switch ($code) {
                    'R' { 'internal-adr-containing-unapproved-business-or-external-constraint-candidates' }
                    'M' { 'internal-adr-mixing-local-design-with-unapproved-external-or-product-constraints' }
                    'L' { 'local-technical-design-decision-outside-requirement-baseline' }
                    'I' { 'adr-navigation-index' }
                }
                $currentApplicability = $cells[2]
                $historyDerivation = $cells[1]
                $atomicRoute = if ($code -in @('R', 'M')) {
                    'candidate-only-after-separating-business-external-safety-and-local-design-claims-source-review-and-explicit-approval'
                }
                else {
                    'do-not-extract-as-requirement; retain-for-separate-technical-decision-or-index-use'
                }
                $evidencePointers = "$($cells[1]); $($cells[2]); retain RIoT environment limits, customer SQL boundaries and implementation-versus-approval separation"
            }
            'R10' {
                if ($cells.Count -ne 5) { throw "Unexpected R10 matrix width at line $lineNumber" }
                $historyCode = Normalize-Text $cells[2]
                $documentClass = $cells[3]
                $sourceType = switch ($historyCode) {
                    'H-AI' { 'ai-modified-simulator-planning-material-without-confirmation' }
                    'H-U' { 'simulator-planning-material-of-unknown-source' }
                    'H-V' { 'third-party-vendor-manual-retained-for-lossless-identity-only' }
                    'H-D' { 'derived-vendor-excerpt-retained-for-lossless-identity-only' }
                    default { throw "Unexpected R10 history code '$historyCode' at line $lineNumber" }
                }
                $currentApplicability = "$($cells[4]); vendor-manual semantics excluded from this effort by user scope decision"
                $historyDerivation = "$historyCode; see R10 Git history, derivation and status-correction groups"
                if ($documentClass -match 'SIM-REQ') {
                    $atomicRoute = 'simulator-scope-candidate-only-after-separating-main-system-vendor-and-tool-claims-source-review-and-explicit-approval'
                }
                elseif ($documentClass -eq 'VENDOR' -or $documentClass -match '^DERIVED \+ VENDOR$') {
                    $atomicRoute = 'do-not-extract; vendor-material-content-is-out-of-scope-and-retained-only-for-lossless-identity-and-source-history'
                }
                else {
                    $atomicRoute = 'do-not-extract-as-requirement; retain-as-simulator-design-test-plan-index-or-evidence-request-pointer'
                }
                $evidencePointers = "$($cells[4]); preserve simulator-only scope, MAIN-LEAD evidence gaps, internal inconsistencies and vendor exclusion"
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
$expectedPerBatch = @{ R06 = 65; R07 = 15; R08 = 57; R09 = 18; R10 = 46 }
foreach ($batch in $batchIds) {
    $count = @($records | Where-Object { $_.batch_id -eq $batch }).Count
    if ($count -ne $expectedPerBatch[$batch]) {
        throw "Expected $($expectedPerBatch[$batch]) records for $batch, found $count."
    }
}

if (@($records | Where-Object { $_.document_approval_state -ne 'not-approved-by-this-classification' }).Count -ne 0) {
    throw 'A document classification was incorrectly promoted to approval.'
}

if (@($records | Where-Object { $_.batch_id -eq 'R10' -and $_.source_type -match 'vendor' -and $_.atomic_requirement_extraction_route -notmatch '^do-not-extract' }).Count -ne 0) {
    throw 'An R10 vendor-only record was incorrectly routed into requirement extraction.'
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
$candidateRoutes = @($records | Where-Object { $_.atomic_requirement_extraction_route -match 'candidate-only' }).Count
$blockedRoutes = @($records | Where-Object { $_.atomic_requirement_extraction_route -match '^blocked-' }).Count
$excludedVendor = @($records | Where-Object { $_.atomic_requirement_extraction_route -match 'vendor-material-content-is-out-of-scope' }).Count
Write-Output "R06-R10 ledger verified: total=$($records.Count); $($summary -join '; '); missing=0; duplicates=0; hash_drift=0; approved_by_classification=0; candidate_routes=$candidateRoutes; blocked_routes=$blockedRoutes; excluded_vendor_records=$excludedVendor"
