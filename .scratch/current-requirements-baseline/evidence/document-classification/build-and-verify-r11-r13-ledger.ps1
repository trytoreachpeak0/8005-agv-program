param(
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\..'))
$inventoryPath = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\material-inventory\material-inventory.tsv'
$correctionsPath = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\initial-snapshot\git-status-corrections.tsv'
$investigationsDir = Join-Path $repoRoot '.scratch\current-requirements-baseline\evidence\investigations'
$ledgerPath = Join-Path $PSScriptRoot 'R11-R13-document-evidence-ledger.tsv'
$batchIds = @('R11', 'R12', 'R13')

$reports = @{
    R11 = 'R11-mes-data-query-validation-constraints.md'
    R12 = 'R12-historical-local-specs-and-issues.md'
    R13 = 'R13-riot-interface-sdk-constraints.md'
}
foreach ($report in $reports.Values) {
    if (-not (Test-Path -LiteralPath (Join-Path $investigationsDir $report) -PathType Leaf)) {
        throw "Missing investigation report: $report"
    }
}

$inventory = @(Import-Csv -LiteralPath $inventoryPath -Delimiter "`t" | Where-Object { $_.batch_id -in $batchIds })
if ($inventory.Count -ne 87) {
    throw "Expected 87 R11-R13 inventory rows, found $($inventory.Count)."
}

$correctionsByPath = @{}
foreach ($correction in (Import-Csv -LiteralPath $correctionsPath -Delimiter "`t")) {
    if ($correctionsByPath.ContainsKey($correction.path)) {
        throw "Duplicate Git status correction path: $($correction.path)"
    }
    $correctionsByPath[$correction.path] = $correction
}

function New-Classification {
    param(
        [Parameter(Mandatory)][string]$DocumentClass,
        [Parameter(Mandatory)][string]$SourceType,
        [Parameter(Mandatory)][string]$CurrentApplicability,
        [Parameter(Mandatory)][string]$HistoryDerivation,
        [Parameter(Mandatory)][string]$AtomicRoute,
        [Parameter(Mandatory)][string]$EvidencePointers,
        [Parameter(Mandatory)][string]$InvestigationPointer
    )

    return [PSCustomObject]@{
        DocumentClass       = $DocumentClass
        SourceType          = $SourceType
        CurrentApplicability = $CurrentApplicability
        HistoryDerivation   = $HistoryDerivation
        AtomicRoute         = $AtomicRoute
        EvidencePointers    = $EvidencePointers
        InvestigationPointer = $InvestigationPointer
    }
}

function Get-R11Classification {
    param([Parameter(Mandatory)][string]$Path)

    $pointer = "$($reports.R11); section=逐文件调查台账"
    switch ($Path) {
        'mes/analysis/README.md' {
            return New-Classification 'R11-D/E' 'internal-offline-analysis-entry-and-current-state-evidence' 'Current-project offline PACKAGE coverage tooling only; does not prove capacity correctness or PACKAGE completeness.' 'Formed in 5718541 as an internal Python-standard-library analysis entry.' 'do-not-extract-as-requirement; retain-as-offline-analysis-and-current-state-evidence' 'Preserve input/output boundaries and the rule that analysis results describe only the supplied snapshot.' $pointer
        }
        'mes/catalog/queries.md' {
            return New-Classification 'R11-I' 'internal-query-catalog-and-navigation-index' 'Current repository QUERY_ID and SSOT navigation; last-evidence fields are stale and do not establish validation status.' 'Formed in 5718541; ffe1f49 added the sixth task type.' 'do-not-extract-from-this-document' 'Retain QUERY_ID/source pointers; bind any future evidence to run_id and SQL hash instead of catalog wording.' $pointer
        }
        'mes/docs/工厂首轮执行与回传清单.md' {
            return New-Classification 'R11-A/E' 'mixed-factory-acceptance-plan-and-limited-run-summary' 'Candidate acceptance conditions plus summaries of three 2026-07-24 runs; valid only for their SQL, environment and data time.' 'Formed in 5718541; ffe1f49 changed five branches to six, removed approval/hash requirements and backfilled observed results.' 'candidate-only-after-acceptance-condition-level-decomposition-run-evidence-review-and-explicit-approval' 'Preserve approval-versus-integrity rule conflict, run manifests, incomplete PACKAGE coverage and ticket 30 decision boundary.' $pointer
        }
        'mes/queries/mes-task-union/README.md' {
            return New-Classification 'R11-X/D/A' 'mixed-external-data-candidate-derived-query-design-and-behavior' 'Potential six-task Oracle data contract mixed with unified-column, UNION ALL, filtering and idempotency design.' 'Formed in 5718541 from customer SQL snapshots; ffe1f49 added WIRE_TO_NITROGEN.' 'candidate-only-after-separating-external-fields-filters-query-design-and-behavior-source-review-and-explicit-approval' 'Retain six source snapshot pointers, SQL hashes, environment scope and quality/performance run limits.' $pointer
        }
        'mes/queries/operator-identity/README.md' {
            return New-Classification 'R11-X/D/A' 'mixed-external-identity-query-candidate-and-product-boundary' 'Potential operator identity data contract mixed with no-result session behavior and the boundary that identity is not role authorization.' 'Formed in 5718541 from a stated 2026-07-16 customer-source snapshot; no independent run or approval binding.' 'candidate-only-after-separating-external-fields-identity-behavior-privacy-and-authorization-boundary-explicit-approval' 'Retain source SQL pointer; require duplicate/no-result/timeout, privacy and authorization evidence separately.' $pointer
        }
        'mes/queries/schema-introspection/README.md' {
            return New-Classification 'R11-D/E' 'internal-oracle-schema-introspection-design' 'Internal validation-query shape; only an actual bound run can evidence a specific database, Schema, user and time.' 'Formed in 5718541 for five types; 493ac5a expanded it to six.' 'do-not-extract-as-requirement; retain-as-validation-design-and-future-current-state-evidence-pointer' 'Do not infer business value ranges from declared lengths or sample maxima; preserve missing independent run.' $pointer
        }
        'mes/queries/sublot-box-count/README.md' {
            return New-Classification 'R11-X/D/A' 'mixed-external-box-count-query-candidate-and-loading-safety-behavior' 'Potential SUBLOT box-count contract mixed with ExpectedBasketCount and fail-closed loading behavior.' 'Formed in 5718541; 493ac5a replaced scan fallback with blocking on failure, non-positive result or ambiguous capacity.' 'candidate-only-after-separating-external-query-semantics-capacity-calculation-and-loading-safety-explicit-approval' 'Retain source SQL pointer, 2026-07-31 behavior change and absence of an independent run.' $pointer
        }
        'mes/README.md' {
            return New-Classification 'R11-I' 'internal-mes-repository-governance-and-navigation' 'Current repository organization, QUERY_ID and SQL SSOT guidance; not a customer requirement.' 'Formed in 5718541 as the MES material and execution entry point.' 'do-not-extract-from-this-document' 'Retain the rule that factory passage requires imported return evidence, without treating it as approved acceptance authority.' $pointer
        }
        'mes/reference/package-basket-capacity.csv' {
            return New-Classification 'R11-X/A' 'unapproved-migrated-package-capacity-rule-table' 'Twenty-eight external-data candidates and one matching-failure behavior; coverage is incomplete and must not be called exhaustive.' 'Formed in 5718541 as a stated 2026-07-16 customer-table migration without the original table or row reconciliation.' 'candidate-only-after-row-level-capacity-match-type-scope-source-review-and-explicit-approval' 'Retain 27 exact/1 prefix identity, TOLL- ambiguity, source-table gap, unmatched PACKAGE evidence and CSV SSOT role.' $pointer
        }
        'mes/reference/package-basket-capacity.md' {
            return New-Classification 'R11-I' 'generated-review-view-of-package-capacity-csv' 'Generated duplicate view of the CSV; not an independent rule source or approval record.' 'Formed in 5718541 and derived wholly from package-basket-capacity.csv.' 'do-not-extract-from-this-document' 'Preserve derivation and bind references to the CSV hash.' $pointer
        }
        'mes/reference/README.md' {
            return New-Classification 'R11-D/A/I' 'internal-capacity-schema-matching-and-safety-guidance' 'Current-project capacity matching and fail-closed guidance mixed with CSV navigation; does not prove the 28 values.' 'Formed in 5718541 around the stated customer-table migration.' 'candidate-only-after-separating-match-algorithm-safety-guardrails-and-source-data-explicit-approval' 'Retain exact-before-longest-prefix, case-sensitivity, no-fuzzy-inference, CSV SSOT and missing customer approval.' $pointer
        }
        default { throw "Unclassified R11 path: $Path" }
    }
}

function Get-R12Classification {
    param([Parameter(Mandatory)][string]$Path)

    $pointer = "$($reports.R12); section=分组调查矩阵"
    if ($Path -match '^\.scratch/mes-ingest-(phase-1|watch-operations)/spec\.md$') {
        $effort = if ($Path -match 'phase-1') { 'MesIngest Phase 1' } else { 'MesIngest Watch Operations' }
        return New-Classification 'R12-SPEC-MIXED' 'internal-implementation-spec-mixing-requirement-summaries-and-design' "$effort implementation spec; possible decision summaries are mixed with architecture, defaults, UI/API and delivery design." 'Created from internal planning and upstream MES/ADR material; ready-for-agent or confirmed wording is not a four-element approval record.' 'candidate-only-after-story-and-semantic-level-decomposition-upstream-source-review-current-applicability-check-and-explicit-approval' 'Retain user-story/domain-semantic/functional-requirement pointers; separate customer MES semantics, operational/UI preferences, API contracts and technical design.' $pointer
    }
    if ($Path -match '^\.scratch/mes-ingest-phase-1/issues/(?<n>\d{2})-') {
        $number = [int]$Matches.n
        if ($number -le 11) {
            return New-Classification 'R12-IMPLEMENTATION-TASK' 'completed-implementation-slice-derived-from-internal-spec' 'Historical Phase 1 implementation plan and completion evidence; does not independently preserve an original requirement.' 'Derived from the Phase 1 spec and later completed through implementation commits.' 'do-not-extract-from-this-document; trace-any-claimed-requirement-to-upstream-spec-and-primary-evidence' 'Retain build scope, acceptance checks and completion commit as implementation history only.' $pointer
        }
        return New-Classification 'R12-IMPLEMENTATION-DEVIATION-FIX' 'implementation-or-review-deviation-and-fix-record' 'Historical Phase 1 implementation deviation/current-state fix; upstream contract alone may become a candidate.' 'Created after implementation or review exposed a concrete deviation, then closed by a fix commit.' 'do-not-extract-from-this-document; retain-as-current-state-and-regression-evidence' 'Retain referenced upstream contract, repro, regression test and fix commit without promoting derived UI/data-model details.' $pointer
    }
    if ($Path -match '^\.scratch/mes-ingest-watch-operations/issues/') {
        return New-Classification 'R12-IMPLEMENTATION-TASK' 'completed-implementation-slice-derived-from-internal-spec' 'Historical Watch implementation, operations, database, UI or factory-validation task; not independent requirement authority.' 'Derived from the Watch Operations spec and completed through implementation commits.' 'do-not-extract-from-this-document; trace-any-claimed-requirement-to-upstream-spec-and-primary-evidence' 'Retain build scope, acceptance checks and completion commit as implementation history only.' $pointer
    }
    if ($Path -match '^\.scratch/mes-ingest-review-remediation/issues/') {
        return New-Classification 'R12-REVIEW-REMEDIATION' 'code-review-finding-and-regression-fix-record' 'Historical implementation-review finding and repair; authoritative only as evidence that an implementation diverged from an upstream contract at that time.' 'Created by code review, with parent/reference, repro, regression tests and a later fix.' 'do-not-extract-from-this-document; retain-as-current-state-and-regression-evidence' 'Retain upstream reference, repro, regression and fix history; new interaction/default/model choices remain derived design.' $pointer
    }
    throw "Unclassified R12 path: $Path"
}

function Get-R13Classification {
    param([Parameter(Mandatory)][string]$Path)

    $pointer = "$($reports.R13); section=26/26 覆盖与哈希终检"
    if ($Path -eq 'rcs/01-rcs-intro.md') {
        return New-Classification 'R13-PN' 'unapproved-project-integration-note' 'Project-local access/API note with unbound environment and unsafe example credentials; not a production configuration or project authorization.' 'Present by the initial 2026-07-13 commit and changed on 2026-07-16; no named approver or target-build binding.' 'candidate-only-after-separating-environment-configuration-access-and-security-claims-controlled-snapshot-and-explicit-approval' 'Preserve 172.19.206.222 versus 172.10.1.72 environment gap and prohibit promoting admin/admin.' $pointer
    }
    if ($Path -match '^rcs/riot_documents/.+\.pdf$') {
        return New-Classification 'R13-IGN' 'third-party-vendor-manual-retained-for-lossless-identity-only' 'Out of scope by user direction on 2026-08-03; content is ignored for the current baseline.' 'Tracked in fixed HEAD after Git-status correction; PDF readability was verified before scope exclusion.' 'do-not-extract; vendor-manual-content-is-out-of-scope-and-retained-only-for-lossless-identity-and-source-history' 'Retain path, hash, bytes, corrected Git identity and completed PDF QA record only.' $pointer
    }
    if ($Path -match '^rcs/riot_ithing_model/.+物模型枚举问题清单\.md$') {
        return New-Classification 'R13-LA' 'local-thing-model-analysis-and-provisional-design-boundary' 'Local analysis of missing/inconsistent enums plus provisional SDK/application handling; not an authoritative TSL or approved project rule.' 'Present by the initial 2026-07-13 commit; Git identity corrected to tracked-clean.' 'candidate-only-after-separating-observed-gaps-defensive-design-and-business-handling-authoritative-tsl-review-and-explicit-approval' 'Retain productKey, missing-enum questions, ticket 38 evidence gap and ticket 39 decision dependency.' $pointer
    }
    if ($Path -match '^rcs/riot_swagger/.+\.json$') {
        return New-Classification 'R13-SS' 'uncontrolled-static-openapi-schema-snapshot' 'Static OpenAPI 3.0.3 schema with missing info.version; not yet bound to a verified RIoT build, project environment or permitted API set.' 'Captured around 2026-07-06 and committed by 2026-07-13 without a controlled capture manifest.' 'candidate-only-after-controlled-environment-version-snapshot-binding-operation-level-decomposition-api-allowlist-and-explicit-approval' 'Retain raw schema hash, server snapshot, missing version, ticket 36 environment binding and ticket 37 API safety boundary.' $pointer
    }
    if ($Path -match '^rcs/riot-sdk/specs/\.(normalized)/') {
        return New-Classification 'R13-ND' 'local-normalized-schema-generation-input' 'Local preprocessing artifact; its default info.version=1.0.0 is not a RIoT product/API version.' 'Untracked at the fixed snapshot and currently ignored; derived from raw imap schema.' 'do-not-extract-as-requirement-or-external-contract; retain-as-sdk-generation-state-evidence' 'Preserve raw-versus-normalized operation counts and prevent default version promotion.' $pointer
    }
    if ($Path -match '^rcs/riot-sdk/specs/.+\.json$') {
        return New-Classification 'R13-SD' 'byte-identical-sdk-copy-of-uncontrolled-raw-schema' 'SDK-local schema copy, not an independent source or approval record.' 'Created during SDK work and byte-identical to the corresponding raw Swagger snapshot.' 'do-not-extract-from-this-duplicate; route-external-contract-review-to-the-raw-schema-record' 'Preserve byte-identical hash relationship and avoid double-counting external candidates.' $pointer
    }
    if ($Path -match '^rcs/riot-sdk/(README\.md|docs/.+\.md)$') {
        return New-Classification 'R13-DS' 'internal-sdk-design-or-test-guidance' 'SDK scope, facade or smoke-test design; passing or skipping smoke does not prove target-environment availability.' 'Formed during SDK implementation between 2026-07-15 and 2026-07-27.' 'do-not-extract-as-project-requirement; retain-for-separate-technical-design-and-current-state-review' 'Preserve facade/non-goal, CallApiKey, sample-base-url and offline/skip semantics without inferring project API scope.' $pointer
    }
    throw "Unclassified R13 path: $Path"
}

$records = @()
$sequenceByBatch = @{ R11 = 0; R12 = 0; R13 = 0 }
foreach ($item in ($inventory | Sort-Object batch_id, path)) {
    $sequenceByBatch[$item.batch_id]++
    $classification = switch ($item.batch_id) {
        'R11' { Get-R11Classification $item.path }
        'R12' { Get-R12Classification $item.path }
        'R13' { Get-R13Classification $item.path }
    }

    $absolutePath = Join-Path $repoRoot $item.path
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) {
        throw "Fixed inventory file is missing: $($item.path)"
    }
    $actualHash = (Get-FileHash -LiteralPath $absolutePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $item.sha256.ToLowerInvariant()) {
        throw "Hash drift for $($item.path). Inventory=$($item.sha256), current=$actualHash"
    }

    $effectiveGitStatus = $item.git_status
    if ($correctionsByPath.ContainsKey($item.path)) {
        $correction = $correctionsByPath[$item.path]
        if ($correction.original_git_status -ne $item.git_status) {
            throw "Git status correction does not match inventory for $($item.path)"
        }
        $effectiveGitStatus = $correction.corrected_git_status
    }

    $record = [PSCustomObject][ordered]@{
        record_id                           = '{0}-{1:D2}' -f $item.batch_id, $sequenceByBatch[$item.batch_id]
        batch_id                            = $item.batch_id
        path                                = $item.path
        sha256                              = $item.sha256.ToLowerInvariant()
        bytes                               = $item.bytes
        inventory_snapshot_git_status       = $item.git_status
        effective_snapshot_git_status       = $effectiveGitStatus
        inventory_material_role             = $item.material_role
        document_class                      = $classification.DocumentClass
        source_type                         = $classification.SourceType
        current_applicability               = $classification.CurrentApplicability
        history_or_derivation               = $classification.HistoryDerivation
        approval_named_authorizer           = 'not-found'
        approval_date                       = 'not-found'
        approval_scope                      = 'not-found'
        approval_version_binding            = 'not-found'
        document_approval_state             = 'not-approved-by-this-classification'
        atomic_requirement_extraction_route = $classification.AtomicRoute
        evidence_or_conflict_pointers       = $classification.EvidencePointers
        investigation_pointer               = $classification.InvestigationPointer
    }
    foreach ($property in $record.PSObject.Properties) {
        if ([string]::IsNullOrWhiteSpace([string]$property.Value)) {
            throw "Empty required field '$($property.Name)' for $($item.path)"
        }
    }
    $records += $record
}

$expectedPerBatch = @{ R11 = 11; R12 = 50; R13 = 26 }
foreach ($batch in $batchIds) {
    $count = @($records | Where-Object { $_.batch_id -eq $batch }).Count
    if ($count -ne $expectedPerBatch[$batch]) {
        throw "Expected $($expectedPerBatch[$batch]) records for $batch, found $count."
    }
}
if (@($records.path | Group-Object | Where-Object Count -ne 1).Count -ne 0) {
    throw 'Duplicate ledger path detected.'
}
if (@($records | Where-Object { $_.document_approval_state -ne 'not-approved-by-this-classification' }).Count -ne 0) {
    throw 'A document classification was incorrectly promoted to approval.'
}
if (@($records | Where-Object { $_.batch_id -eq 'R13' -and $_.document_class -eq 'R13-IGN' -and $_.atomic_requirement_extraction_route -notmatch '^do-not-extract' }).Count -ne 0) {
    throw 'An ignored R13 vendor manual was routed into extraction.'
}
if (@($records | Where-Object { $_.batch_id -eq 'R12' -and $_.document_class -ne 'R12-SPEC-MIXED' -and $_.atomic_requirement_extraction_route -notmatch '^do-not-extract' }).Count -ne 0) {
    throw 'An R12 implementation ticket was incorrectly routed into atomic requirement extraction.'
}
if (@($records | Where-Object { $_.batch_id -eq 'R13' -and $_.document_class -eq 'R13-SD' -and $_.atomic_requirement_extraction_route -notmatch '^do-not-extract' }).Count -ne 0) {
    throw 'An R13 duplicate SDK schema was incorrectly double-counted as an external candidate.'
}

if ($VerifyOnly) {
    if (-not (Test-Path -LiteralPath $ledgerPath -PathType Leaf)) {
        throw "Ledger does not exist: $ledgerPath"
    }
    $persisted = @(Import-Csv -LiteralPath $ledgerPath -Delimiter "`t")
    if ($persisted.Count -ne $records.Count) {
        throw "Persisted ledger row count mismatch. expected=$($records.Count), actual=$($persisted.Count)"
    }
    for ($i = 0; $i -lt $records.Count; $i++) {
        foreach ($property in $records[$i].PSObject.Properties.Name) {
            if ([string]$persisted[$i].$property -ne [string]$records[$i].$property) {
                throw "Persisted value mismatch at row $($i + 1), field $property"
            }
        }
    }
}
else {
    $records | Export-Csv -LiteralPath $ledgerPath -Delimiter "`t" -NoTypeInformation -Encoding utf8
}

$summary = $records | Group-Object batch_id | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Count)" }
$candidateRoutes = @($records | Where-Object { $_.atomic_requirement_extraction_route -match '^candidate-only' }).Count
$implementationOnly = @($records | Where-Object { $_.batch_id -eq 'R12' -and $_.document_class -ne 'R12-SPEC-MIXED' }).Count
$schemaPending = @($records | Where-Object { $_.document_class -eq 'R13-SS' }).Count
$ignoredVendor = @($records | Where-Object { $_.document_class -eq 'R13-IGN' }).Count
$correctionCount = @($records | Where-Object { $_.inventory_snapshot_git_status -ne $_.effective_snapshot_git_status }).Count
Write-Output "R11-R13 ledger verified: total=$($records.Count); $($summary -join '; '); missing=0; duplicates=0; hash_drift=0; approved_by_classification=0; candidate_routes=$candidateRoutes; implementation_only_records=$implementationOnly; schema_snapshot_pending=$schemaPending; ignored_vendor_records=$ignoredVendor; git_status_corrections=$correctionCount"
