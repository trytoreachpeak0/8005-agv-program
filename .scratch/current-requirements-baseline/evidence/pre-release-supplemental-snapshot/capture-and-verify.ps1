param(
    [string]$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
)

$ErrorActionPreference = 'Stop'
$captureStartedLocal = Get-Date
$captureStartedUtc = $captureStartedLocal.ToUniversalTime()
$outputDirectory = $PSScriptRoot
$outputRelativePrefix = '.scratch/current-requirements-baseline/evidence/pre-release-supplemental-snapshot/'
$initialManifestPath = Join-Path $RepositoryRoot '.scratch/current-requirements-baseline/evidence/initial-snapshot/candidate-documents.tsv'

function Normalize-RepositoryPath {
    param([string]$Path)
    $normalized = $Path -replace '\\', '/'
    if ($normalized.StartsWith('./', [StringComparison]::Ordinal)) {
        return $normalized.Substring(2)
    }
    return $normalized
}

function New-PathSet {
    param([string[]]$Paths)
    $set = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($path in $Paths) {
        if (-not [string]::IsNullOrWhiteSpace($path)) {
            [void]$set.Add((Normalize-RepositoryPath $path))
        }
    }
    return ,$set
}

function New-GitObjectMap {
    param([string[]]$Lines)
    $map = [System.Collections.Generic.Dictionary[string,string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($line in $Lines) {
        if ($line -match '^[0-7]{6} (?:blob )?([0-9a-f]{40})(?: [0-9]+)?\t(.+)$') {
            $map[(Normalize-RepositoryPath $Matches[2])] = $Matches[1]
        }
    }
    return $map
}

function Get-MaterialClassification {
    param([string]$Path)

    switch -Regex ($Path) {
        '^\.scratch/(new-mes-ingest|mes-ingest-bounded-storage-low-memory|mes-ingest-watch-area-live-sync|demand-series-inspector-e)/spec\.md$' {
            return @('normative-candidate', 'user-approved bound specification source', '8005 MesIngest/Watch scope fixed by ticket 84; item-level baseline approval still required')
        }
        '^\.scratch/current-requirements-baseline/' {
            return @('support-approval-evidence', 'local wayfinding governance and approval record', 'baseline provenance, approval, classification, or supporting evidence; not automatically a system requirement')
        }
        '^\.scratch/(new-mes-ingest|mes-ingest-bounded-storage-low-memory|mes-ingest-watch-area-live-sync|demand-series-inspector-e)/(issues|evidence)/' {
            return @('implementation-acceptance-evidence', 'local implementation tracker or generated validation evidence', 'proves implementation, review, or acceptance state only; cannot establish a requirement by itself')
        }
        '^\.scratch/(mes-ingest-phase-1|mes-ingest-watch-v2|mes-ingest-watch-v2-implementation|mes-ingest-watch-operations|mes-ingest-review-remediation|mes-ingest-watch-fluent-refinement)/' {
            return @('historical-superseded', 'local historical specification, prototype, or implementation record', 'historical evidence only unless an obligation is explicitly carried forward by a current approved source')
        }
        '^\.scratch/' {
            return @('implementation-acceptance-evidence', 'local planning, implementation, or validation record', 'review as supporting evidence only; no automatic requirement or approval upgrade')
        }
        '^(project_agreements/|requirement-documents/|mes/docs/|mes/analysis/|mes/catalog/|mes/queries/|mes/reference/|rcs/01-rcs-intro\.md$|rcs/riot_documents/|rcs/riot_ithing_model/|rcs/riot-sdk/(README\.md|docs/|specs/))' {
            return @('normative-candidate', 'repository requirement, acceptance, business, or external-constraint material', 'candidate only; source, applicability, supersession, and item-level approval must be verified')
        }
        '^(CONTEXT\.md$|docs/adr/)' {
            return @('support-approval-evidence', 'domain vocabulary or architectural decision record', 'supports terminology or decision provenance; not automatically an approved requirement')
        }
        '^(AGENTS\.md$|\.agents/|docs/agents/|skills-lock\.json$|file-naming-convention/)' {
            return @('support-approval-evidence', 'repository governance material', 'agent and repository process boundary only; outside product requirement content')
        }
        default {
            return @('implementation-acceptance-evidence', 'repository working material or observed artifact', 'current-state evidence only unless separately classified and approved')
        }
    }
}

function Write-Utf8Lines {
    param([string]$Path, [string[]]$Lines)
    if ($null -eq $Lines -or $Lines.Count -eq 0) {
        [IO.File]::WriteAllText($Path, '', [Text.UTF8Encoding]::new($false))
        return
    }
    [IO.File]::WriteAllLines($Path, $Lines, [Text.UTF8Encoding]::new($false))
}

function Write-Tsv {
    param([string]$Path, [object[]]$Rows)
    Write-Utf8Lines -Path $Path -Lines @($Rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation)
}

Push-Location -LiteralPath $RepositoryRoot
try {
    $branch = (git branch --show-current).Trim()
    $head = (git rev-parse HEAD).Trim()
    $upstream = (git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>$null)
    if ($LASTEXITCODE -ne 0) { $upstream = '(none)' } else { $upstream = $upstream.Trim() }

    $tracked = New-PathSet @(git -c core.quotepath=false ls-files)
    $staged = New-PathSet @(git -c core.quotepath=false diff --cached --name-only 2>$null)
    $modified = New-PathSet @(git -c core.quotepath=false diff --name-only 2>$null)
    $indexObjects = New-GitObjectMap @(git -c core.quotepath=false ls-files -s)
    $headObjects = New-GitObjectMap @(git -c core.quotepath=false ls-tree -r HEAD)

    $worktreeStatus = @(git -c core.quotepath=false status --porcelain=v1 --branch --untracked-files=all)
    Write-Utf8Lines -Path (Join-Path $outputDirectory 'worktree-status.txt') -Lines $worktreeStatus

    $excludedGlobs = @(
        '!.git/**', '!**/bin/**', '!**/obj/**', '!**/node_modules/**', '!**/packages/**',
        '!**/dist/**', '!**/.dist/**', '!**/build/**', '!**/coverage/**', '!**/TestResults/**',
        '!**/.vs/**', '!**/.idea/**', '!**/.vscode/**', '!**/.cache/**', '!**/.cache',
        '!**/.pytest_cache/**', '!**/.pytest_cache', '!**/artifacts/**', '!**/artifact/**',
        "!$outputRelativePrefix**"
    )
    $rgArguments = @('--files', '--hidden', '--no-ignore')
    foreach ($glob in $excludedGlobs) { $rgArguments += @('-g', $glob) }

    $errorTemporaryPath = Join-Path $env:TEMP ("agv-pre-release-snapshot-rg-{0}.txt" -f [guid]::NewGuid().ToString('N'))
    $allPaths = @(& rg @rgArguments 2> $errorTemporaryPath)
    $rgExitCode = $LASTEXITCODE
    $discoveryErrors = if (Test-Path -LiteralPath $errorTemporaryPath) { @(Get-Content -LiteralPath $errorTemporaryPath) } else { @() }
    if (Test-Path -LiteralPath $errorTemporaryPath) { Remove-Item -LiteralPath $errorTemporaryPath }
    Write-Utf8Lines -Path (Join-Path $outputDirectory 'discovery-errors.txt') -Lines $discoveryErrors
    if ($rgExitCode -notin @(0, 1)) { throw "rg discovery failed with exit code $rgExitCode." }

    $candidateExtensions = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    @(
        '.md', '.markdown', '.adoc', '.rst', '.txt', '.rtf', '.pdf', '.doc', '.docx',
        '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.tsv', '.html', '.htm', '.xml',
        '.json', '.yaml', '.yml', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg', '.drawio', '.trx'
    ) | ForEach-Object { [void]$candidateExtensions.Add($_) }

    $currentCandidatePaths = @(
        $allPaths |
            ForEach-Object { Normalize-RepositoryPath $_ } |
            Where-Object {
                -not $_.StartsWith($outputRelativePrefix, [StringComparison]::OrdinalIgnoreCase) -and
                $candidateExtensions.Contains([IO.Path]::GetExtension($_))
            } |
            Sort-Object -Unique
    )

    $nonTracked = @($currentCandidatePaths | Where-Object { -not $tracked.Contains($_) })
    $ignoredPaths = if ($nonTracked.Count -gt 0) { @($nonTracked | git -c core.quotepath=false check-ignore --stdin) } else { @() }
    if ($LASTEXITCODE -notin @(0, 1)) { throw "git check-ignore failed with exit code $LASTEXITCODE." }
    $ignored = New-PathSet $ignoredPaths

    $initialRows = @(Import-Csv -LiteralPath $initialManifestPath -Delimiter "`t")
    $initialByPath = [System.Collections.Generic.Dictionary[string,object]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($row in $initialRows) { $initialByPath[$row.path] = $row }
    $currentPathSet = New-PathSet $currentCandidatePaths

    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($relativePath in $currentCandidatePaths) {
        $absolutePath = Join-Path $RepositoryRoot ($relativePath -replace '/', [IO.Path]::DirectorySeparatorChar)
        $item = Get-Item -LiteralPath $absolutePath
        $sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $absolutePath).Hash.ToLowerInvariant()
        $initial = if ($initialByPath.ContainsKey($relativePath)) { $initialByPath[$relativePath] } else { $null }
        $changeKind = if ($null -eq $initial) { 'added' } elseif ($initial.sha256 -ne $sha256) { 'modified' } else { 'unchanged' }
        if ($changeKind -eq 'unchanged') { continue }

        $gitStatus = if ($tracked.Contains($relativePath)) {
            $parts = [System.Collections.Generic.List[string]]::new()
            if ($staged.Contains($relativePath)) { $parts.Add('staged') }
            if ($modified.Contains($relativePath)) { $parts.Add('modified') }
            if ($parts.Count -eq 0) { 'tracked-clean' } else { 'tracked-' + ($parts -join '+') }
        } elseif ($ignored.Contains($relativePath)) { 'ignored-untracked' } else { 'untracked' }

        $classification = Get-MaterialClassification -Path $relativePath
        $rows.Add([pscustomobject]@{
            path = $relativePath
            change_kind = $changeKind
            git_status = $gitStatus
            head_blob = if ($headObjects.ContainsKey($relativePath)) { $headObjects[$relativePath] } else { '' }
            index_blob = if ($indexObjects.ContainsKey($relativePath)) { $indexObjects[$relativePath] } else { '' }
            sha256 = $sha256
            initial_sha256 = if ($null -ne $initial) { $initial.sha256 } else { '' }
            bytes = $item.Length
            last_write_utc = $item.LastWriteTimeUtc.ToString('o')
            classification = $classification[0]
            source = $classification[1]
            applicability = $classification[2]
            approval_effect = 'none-by-capture'
        })
    }

    foreach ($initial in $initialRows) {
        if ($currentPathSet.Contains($initial.path)) { continue }
        $classification = Get-MaterialClassification -Path $initial.path
        $rows.Add([pscustomobject]@{
            path = $initial.path
            change_kind = 'deleted'
            git_status = 'absent-from-worktree'
            head_blob = if ($headObjects.ContainsKey($initial.path)) { $headObjects[$initial.path] } else { '' }
            index_blob = if ($indexObjects.ContainsKey($initial.path)) { $indexObjects[$initial.path] } else { '' }
            sha256 = ''
            initial_sha256 = $initial.sha256
            bytes = 0
            last_write_utc = ''
            classification = $classification[0]
            source = $classification[1]
            applicability = $classification[2]
            approval_effect = 'none-by-capture'
        })
    }

    $sortedRows = @($rows | Sort-Object path)
    Write-Tsv -Path (Join-Path $outputDirectory 'supplemental-evidence-manifest.tsv') -Rows $sortedRows

    $approvedSources = @(
        [pscustomobject]@{ path='.scratch/new-mes-ingest/spec.md'; expected_blob='9104575426c60f71ed8020d3d231c3332e2c0589'; expected_sha256='bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f' },
        [pscustomobject]@{ path='.scratch/mes-ingest-bounded-storage-low-memory/spec.md'; expected_blob='099feeef433a0b356c41c90e221ee7d5bafcface'; expected_sha256='23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6' },
        [pscustomobject]@{ path='.scratch/mes-ingest-watch-area-live-sync/spec.md'; expected_blob='c6050a6102abc6b24f330187af7010fad15736b4'; expected_sha256='8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0' },
        [pscustomobject]@{ path='.scratch/demand-series-inspector-e/spec.md'; expected_blob='2b4a2b326a3df2635e56977b22feb8686d0c0cca'; expected_sha256='c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657' }
    )
    $validationRows = foreach ($source in $approvedSources) {
        $absolutePath = Join-Path $RepositoryRoot ($source.path -replace '/', [IO.Path]::DirectorySeparatorChar)
        $actualSha256 = if (Test-Path -LiteralPath $absolutePath) { (Get-FileHash -Algorithm SHA256 -LiteralPath $absolutePath).Hash.ToLowerInvariant() } else { '' }
        $actualBlob = if (Test-Path -LiteralPath $absolutePath) { (git hash-object -- $source.path).Trim() } else { '' }
        $headBlob = if ($headObjects.ContainsKey($source.path)) { $headObjects[$source.path] } else { '' }
        [pscustomobject]@{
            path = $source.path
            expected_blob = $source.expected_blob
            actual_worktree_blob = $actualBlob
            head_blob = $headBlob
            expected_sha256 = $source.expected_sha256
            actual_sha256 = $actualSha256
            blob_match = ($source.expected_blob -eq $actualBlob).ToString().ToLowerInvariant()
            sha256_match = ($source.expected_sha256 -eq $actualSha256).ToString().ToLowerInvariant()
            approval_binding_valid = (($source.expected_blob -eq $actualBlob) -and ($source.expected_sha256 -eq $actualSha256)).ToString().ToLowerInvariant()
        }
    }
    Write-Tsv -Path (Join-Path $outputDirectory 'approved-source-validation.tsv') -Rows @($validationRows)

    $supersessionRows = @(
        [pscustomobject]@{ layer_order=1; source_path='.scratch/new-mes-ingest/spec.md'; relationship='base-current-source'; supersedes_source='old Phase 1, old V2, old database/contract/Watch/IngestAlert semantics'; effective_scope='8005 MesIngest service, projection, SQL storage, versioned API/OpenAPI, Watch, external readable catalog'; approval_pointer='issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md' },
        [pscustomobject]@{ layer_order=2; source_path='.scratch/mes-ingest-bounded-storage-low-memory/spec.md'; relationship='partial-later-layer'; supersedes_source='.scratch/new-mes-ingest/spec.md'; effective_scope='GONE detail, error history, raw evidence retention, recovery, capacity, and low-memory storage boundaries only'; approval_pointer='issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md' },
        [pscustomobject]@{ layer_order=3; source_path='.scratch/mes-ingest-watch-area-live-sync/spec.md'; relationship='partial-later-layer'; supersedes_source='.scratch/new-mes-ingest/spec.md'; effective_scope='AreaFilterProfile editing, live synchronization, conflict, and post-deletion scope snapshot only'; approval_pointer='issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md' },
        [pscustomobject]@{ layer_order=4; source_path='.scratch/demand-series-inspector-e/spec.md'; relationship='partial-later-layer'; supersedes_source='.scratch/new-mes-ingest/spec.md'; effective_scope='DemandSeries detail information architecture only; domain contracts remain unchanged'; approval_pointer='issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md' },
        [pscustomobject]@{ layer_order=5; source_path='.scratch/current-requirements-baseline/issues/81-reconcile-mes-ingest-watch-v2-operability-definitions.md'; relationship='explicit-cross-version-carry-forward'; supersedes_source='conflicting old V2 operability rules'; effective_scope='single read-only Host, generation isolation, preserve-and-mark last success, non-actionable alerts, and Watch failures not becoming business alerts'; approval_pointer='issues/81-reconcile-mes-ingest-watch-v2-operability-definitions.md' }
    )
    Write-Tsv -Path (Join-Path $outputDirectory 'pre-baseline-source-supersession.tsv') -Rows $supersessionRows

    $captureCompletedLocal = Get-Date
    $captureCompletedUtc = $captureCompletedLocal.ToUniversalTime()
    $changeSummary = @($sortedRows | Group-Object change_kind | Sort-Object Name | ForEach-Object { "- $($_.Name): $($_.Count)" })
    $classificationSummary = @($sortedRows | Group-Object classification | Sort-Object Name | ForEach-Object { "- $($_.Name): $($_.Count)" })
    $driftRows = @($validationRows | Where-Object approval_binding_valid -ne 'true')
    $discoverySummary = if ($discoveryErrors.Count -eq 0) { 'None.' } else { "$($discoveryErrors.Count) line(s); see discovery-errors.txt." }
    $driftSummary = if ($driftRows.Count -eq 0) { 'None; all four approved sources match both bound Git blob and SHA-256.' } else { "$($driftRows.Count) approved source(s) drifted; their current bytes are not approved and require a new approval entry." }

    $summaryLines = @(
        '# PreReleaseSupplementalEvidenceSnapshot', '',
        'This is a capture and classification record, not an automatic requirement or approval upgrade. It does not modify source materials.', '',
        '## Capture identity', '',
        "- Started (local): $($captureStartedLocal.ToString('o'))", "- Started (UTC): $($captureStartedUtc.ToString('o'))",
        "- Completed (local): $($captureCompletedLocal.ToString('o'))", "- Completed (UTC): $($captureCompletedUtc.ToString('o'))",
        "- Repository root: $RepositoryRoot", "- Branch: $branch", "- HEAD: $head", "- Upstream: $upstream",
        '- Window baseline: initial snapshot completed 2026-08-03T10:50:48.2268823+08:00 at HEAD 1469d6309d00b0abb792f6cd686aed68286e638e.',
        "- Supplemental changed/new/deleted files: $($sortedRows.Count)", "- Discovery errors: $discoverySummary", "- Approved-source drift: $driftSummary", '',
        '## Change counts', ''
    ) + $changeSummary + @('', '## Classification counts', '') + $classificationSummary + @(
        '', '## Classification boundary', '',
        '- `normative-candidate` is eligible for item-level baseline formation only after its source, scope, conflicts, supersession, and atomic approval are verified.',
        '- `support-approval-evidence` proves provenance, governance, vocabulary, or a decision; its presence does not promote the whole file to a system requirement.',
        '- `implementation-acceptance-evidence` proves implementation, test, review, or observed state only.',
        '- `historical-superseded` remains immutable historical evidence and cannot be presented as current.',
        '- Every captured row has `approval_effect=none-by-capture`.', '',
        '## Freeze rule', '',
        'Any requirement-shaped material added or changed after the Completed timestamp above is outside this frozen supplemental snapshot. Before v1.0.0 final approval it must reopen this snapshot and revalidate affected bytes and approvals; otherwise it enters the post-release change gate for a later version.', '',
        '## Assets', '',
        '- `supplemental-evidence-manifest.tsv`: every document-shaped file added, changed, or deleted relative to the immutable initial snapshot, with Git/worktree identity, SHA-256, source, applicability, classification, and approval effect.',
        '- `approved-source-validation.tsv`: bound Git blob and SHA-256 verification for the four approved current specification sources.',
        '- `pre-baseline-source-supersession.tsv`: approved source layering and PreBaselineSourceSupersession scope.',
        '- `worktree-status.txt`: raw Git status at capture.',
        '- `discovery-errors.txt`: discovery stderr; empty means no errors.',
        '- `capture-and-verify.ps1`: repeatable capture and verification method. Re-running creates a new observation and therefore requires intentional review of its new cutoff.'
    )
    Write-Utf8Lines -Path (Join-Path $outputDirectory 'snapshot.md') -Lines $summaryLines

    Write-Output "supplemental_rows=$($sortedRows.Count)"
    Write-Output "approved_source_drift=$($driftRows.Count)"
    Write-Output "discovery_errors=$($discoveryErrors.Count)"
    if ($driftRows.Count -ne 0) { exit 2 }
}
finally {
    Pop-Location
}
