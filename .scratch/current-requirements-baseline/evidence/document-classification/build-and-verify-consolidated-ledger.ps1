[CmdletBinding()]
param(
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$scriptDir = $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $scriptDir '..\..\..\..')).Path
$inventoryPath = Join-Path $scriptDir '..\material-inventory\material-inventory.tsv'
$correctionPath = Join-Path $scriptDir '..\initial-snapshot\git-status-corrections.tsv'
$ledgerPath = Join-Path $scriptDir 'R01-R13-document-evidence-ledger.tsv'
$groupPath = Join-Path $scriptDir 'R01-R13-candidate-groups.tsv'
$sourcePaths = @(
    (Join-Path $scriptDir 'R01-R05-document-evidence-ledger.tsv'),
    (Join-Path $scriptDir 'R06-R10-document-evidence-ledger.tsv'),
    (Join-Path $scriptDir 'R11-R13-document-evidence-ledger.tsv')
)

$canonicalColumns = @(
    'record_id', 'batch_id', 'path', 'sha256', 'bytes',
    'inventory_snapshot_git_status', 'effective_snapshot_git_status',
    'inventory_material_role', 'document_class', 'source_type',
    'current_applicability', 'history_or_derivation',
    'approval_named_authorizer', 'approval_date', 'approval_scope',
    'approval_version_binding', 'document_approval_state',
    'atomic_requirement_extraction_route', 'evidence_or_conflict_pointers',
    'investigation_pointer'
)

$expectedCounts = [ordered]@{
    R01 = 19; R02 = 27; R03 = 48; R04 = 41; R05 = 67
    R06 = 65; R07 = 15; R08 = 57; R09 = 18; R10 = 46
    R11 = 11; R12 = 50; R13 = 26
}

$groupDefinitions = [ordered]@{
    R01 = @{
        title = '客户、项目协议与原始输入候选'
        ticket = '拆分并分类客户、项目协议与原始输入的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '按独立声明拆分，保留客户来源、讨论稿、内部推导和待确认的差异；不把自称关闭或未签署协议当作批准。'
    }
    R02 = @{
        title = '需求框架、愿景与业务规则候选'
        ticket = '拆分并分类需求框架、愿景与业务规则的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '只处理已路由候选文档；结构模板、导航索引和纯参考目录不从自身提取。'
    }
    R03 = @{
        title = '用例与流程候选'
        ticket = '拆分并分类用例与流程的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '按流程和可独立判断的行为拆分，先分离业务候选与内部设计推演。'
    }
    R04 = @{
        title = '功能需求候选'
        ticket = '拆分并分类功能需求的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '按功能声明和验收条件拆分，保留上游 UC/BR 指针并在批准前去重。'
    }
    R05 = @{
        title = '现场操作验收场景候选'
        ticket = '拆分并分类现场操作验收场景的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '按场景级验收声明拆分，将业务验收与接口、安全及内部设计主张分开。'
    }
    R06 = @{
        title = '仓位、硬件与车队验收候选'
        ticket = '拆分并分类仓位、硬件与车队验收的原子候选'
        gate = '合并并核验文档级证据分类账；4 份上游漂移旧稿不在候选组内'
        boundary = '只处理 52 份未阻塞测试草案；4 份漂移旧稿继续隔离，直到重写或明确绑定上游版本。'
    }
    R07 = @{
        title = '非功能需求候选'
        ticket = '拆分并分类非功能需求的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '按 fit criterion 拆分仅 2 份候选；追溯、索引和空占位不从自身提取。'
    }
    R08 = @{
        title = '跨域词汇、业务与物理事实候选'
        ticket = '拆分并分类跨域词汇、业务与物理事实的原子候选'
        gate = '合并并核验文档级证据分类账；确定领域词汇唯一入口与旧术语表关系'
        boundary = '必须把词汇、领域事实、业务规则、物理约束和设计决定分开；获批词汇走 CONTEXT.md 闭环。'
    }
    R09 = @{
        title = 'MES 与 SDK 业务/外部约束候选'
        ticket = '拆分并分类 MES 与 SDK 业务及外部约束的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '先分离业务、外部契约、安全主张与本地设计；纯技术决定不进入需求批准。'
    }
    R10 = @{
        title = '仓位模拟器范围需求候选'
        ticket = '拆分并分类仓位模拟器范围需求的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '仅拆分模拟器自身候选；主系统、供应商、设计、测试与实施计划不从规划文本反推。'
    }
    R11 = @{
        title = 'MES 数据、查询与工厂验证候选'
        ticket = '拆分并分类 MES 数据、查询与工厂验证的原子候选'
        gate = '合并并核验文档级证据分类账；决定工厂 MES 验证的批准与完整性证据门槛'
        boundary = '将外部数据契约、查询设计、容量与装载安全、验收条件及限定环境现状分开。'
    }
    R12 = @{
        title = '历史本地 spec 中的需求摘要候选'
        ticket = '拆分并分类历史本地 spec 需求摘要的原子候选'
        gate = '合并并核验文档级证据分类账'
        boundary = '仅处理 2 份混合 spec，按 story/语义拆分并追溯上游；48 张实施与修复票只作历史证据。'
    }
    R13 = @{
        title = 'RIoT 受控接口、集成与物模型候选'
        ticket = '拆分并分类 RIoT 受控接口、集成与物模型的原子候选'
        gate = '补齐 RIoT 目标环境与受控接口快照证据；决定 RIoT 项目 API 白名单与调用安全边界；补齐 standard.oasis.300ul 物模型枚举证据；决定未知物模型枚举值的项目处理规则'
        boundary = '14 份 schema 必须先绑定受控环境与版本并获得 API 白名单；物模型与集成笔记分离外部事实、项目行为及本地设计。'
    }
}

function Add-Error {
    param([System.Collections.Generic.List[string]]$Errors, [string]$Message)
    $Errors.Add($Message)
}

function Get-RouteClass {
    param([string]$Route)
    if ($Route -like 'candidate-*' -or $Route -like 'split-*' -or $Route -like 'simulator-scope-candidate-*') { return 'candidate' }
    if ($Route -like 'blocked-*') { return 'blocked' }
    if ($Route -like 'do-not-*') { return 'excluded' }
    return 'invalid'
}

function Convert-ToLedgerRecord {
    param([object]$Row)
    $record = [ordered]@{}
    foreach ($column in $canonicalColumns) { $record[$column] = [string]$Row.$column }
    $routeClass = Get-RouteClass ([string]$Row.atomic_requirement_extraction_route)
    $record['route_class'] = $routeClass
    $record['candidate_group_id'] = if ($routeClass -eq 'candidate') { [string]$Row.batch_id } else { '' }
    [pscustomobject]$record
}

function Compare-Records {
    param(
        [object[]]$Expected,
        [object[]]$Actual,
        [string[]]$Columns,
        [string]$Label,
        [System.Collections.Generic.List[string]]$Errors
    )
    if ($Expected.Count -ne $Actual.Count) {
        Add-Error $Errors "$Label row count mismatch: expected=$($Expected.Count), actual=$($Actual.Count)"
        return
    }
    for ($i = 0; $i -lt $Expected.Count; $i++) {
        foreach ($column in $Columns) {
            if ([string]$Expected[$i].$column -cne [string]$Actual[$i].$column) {
                Add-Error $Errors "$Label mismatch at row=$($i + 1), column=$column"
                break
            }
        }
    }
}

$errors = [System.Collections.Generic.List[string]]::new()
$rows = @()
foreach ($sourcePath in $sourcePaths) {
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        Add-Error $errors "Missing source ledger: $sourcePath"
        continue
    }
    $sourceHeader = ((Get-Content -LiteralPath $sourcePath -TotalCount 1) -split "`t") | ForEach-Object { $_.Trim('"') }
    if (($sourceHeader -join "`t") -cne ($canonicalColumns -join "`t")) {
        Add-Error $errors "Canonical field order mismatch: $sourcePath"
    }
    $rows += @(Import-Csv -Delimiter "`t" -LiteralPath $sourcePath)
}

$inventory = @(Import-Csv -Delimiter "`t" -LiteralPath $inventoryPath | Where-Object { $_.batch_id -match '^R(0[1-9]|1[0-3])$' })
$corrections = @(Import-Csv -Delimiter "`t" -LiteralPath $correctionPath)
$inventoryByPath = @{}
foreach ($item in $inventory) {
    if ($inventoryByPath.ContainsKey($item.path)) { Add-Error $errors "Duplicate candidate path in fixed inventory: $($item.path)" }
    $inventoryByPath[$item.path] = $item
}
$correctionByPath = @{}
foreach ($item in $corrections) { $correctionByPath[$item.path] = $item }

if ($rows.Count -ne 490) { Add-Error $errors "Consolidated source count mismatch: expected=490, actual=$($rows.Count)" }
if ($inventory.Count -ne 490) { Add-Error $errors "Fixed candidate inventory count mismatch: expected=490, actual=$($inventory.Count)" }

$duplicateIds = @($rows | Group-Object record_id | Where-Object Count -gt 1)
$duplicatePaths = @($rows | Group-Object path | Where-Object Count -gt 1)
if ($duplicateIds.Count -gt 0) { Add-Error $errors "Duplicate record ids: $($duplicateIds.Name -join ', ')" }
if ($duplicatePaths.Count -gt 0) { Add-Error $errors "Duplicate paths: $($duplicatePaths.Name -join ', ')" }

$allowedInventoryRoles = @(
    'candidate-acceptance', 'candidate-data-constraint', 'candidate-decision',
    'candidate-external-constraint', 'candidate-requirement', 'candidate-source',
    'candidate-vocabulary', 'current-state-evidence', 'template-or-index'
)
$allowedSnapshotStatuses = @('tracked-clean', 'untracked')
$approvalColumns = @('approval_named_authorizer', 'approval_date', 'approval_scope', 'approval_version_binding')
$requiredTextColumns = @('document_class', 'source_type', 'current_applicability', 'history_or_derivation', 'atomic_requirement_extraction_route', 'evidence_or_conflict_pointers', 'investigation_pointer')

foreach ($batch in $expectedCounts.Keys) {
    $count = @($rows | Where-Object batch_id -eq $batch).Count
    if ($count -ne $expectedCounts[$batch]) { Add-Error $errors "$batch count mismatch: expected=$($expectedCounts[$batch]), actual=$count" }
}

foreach ($row in $rows) {
    if (-not $expectedCounts.Contains($row.batch_id)) { Add-Error $errors "Invalid batch enum at $($row.record_id): $($row.batch_id)" }
    if ($row.record_id -notmatch ('^' + [regex]::Escape($row.batch_id) + '-\d{2}$')) { Add-Error $errors "Record id does not match batch: $($row.record_id)" }
    if (-not $inventoryByPath.ContainsKey($row.path)) {
        Add-Error $errors "Path missing from fixed candidate inventory: $($row.path)"
        continue
    }
    $item = $inventoryByPath[$row.path]
    foreach ($pair in @(
        @('batch_id', 'batch_id'), @('sha256', 'sha256'), @('bytes', 'bytes'),
        @('inventory_snapshot_git_status', 'git_status'), @('inventory_material_role', 'material_role')
    )) {
        if ([string]$row.($pair[0]) -cne [string]$item.($pair[1])) {
            Add-Error $errors "Inventory mismatch at $($row.record_id): $($pair[0])"
        }
    }
    if ($allowedSnapshotStatuses -notcontains $row.inventory_snapshot_git_status) { Add-Error $errors "Invalid inventory git-status enum at $($row.record_id)" }
    if ($allowedSnapshotStatuses -notcontains $row.effective_snapshot_git_status) { Add-Error $errors "Invalid effective git-status enum at $($row.record_id)" }
    if ($allowedInventoryRoles -notcontains $row.inventory_material_role) { Add-Error $errors "Invalid material-role enum at $($row.record_id): $($row.inventory_material_role)" }
    $expectedEffectiveStatus = if ($correctionByPath.ContainsKey($row.path)) { $correctionByPath[$row.path].corrected_git_status } else { $item.git_status }
    if ([string]$row.effective_snapshot_git_status -cne [string]$expectedEffectiveStatus) { Add-Error $errors "Effective git-status correction mismatch at $($row.record_id)" }
    foreach ($column in $approvalColumns) {
        if ([string]$row.$column -cne 'not-found') { Add-Error $errors "Approval evidence overstatement at $($row.record_id): $column=$($row.$column)" }
    }
    if ([string]$row.document_approval_state -cne 'not-approved-by-this-classification') { Add-Error $errors "Document approval state overstatement at $($row.record_id)" }
    foreach ($column in $requiredTextColumns) {
        if ([string]::IsNullOrWhiteSpace([string]$row.$column)) { Add-Error $errors "Missing required classification text at $($row.record_id): $column" }
    }
    if ((Get-RouteClass ([string]$row.atomic_requirement_extraction_route)) -eq 'invalid') { Add-Error $errors "Invalid extraction-route enum at $($row.record_id): $($row.atomic_requirement_extraction_route)" }
    $fullPath = Join-Path $repoRoot ($row.path -replace '/', '\')
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        Add-Error $errors "Current file missing: $($row.path)"
    } else {
        $currentHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $fullPath).Hash.ToLowerInvariant()
        if ($currentHash -cne ([string]$row.sha256).ToLowerInvariant()) { Add-Error $errors "Current hash drift: $($row.path)" }
    }
}

$ledgerRows = @($rows | ForEach-Object { Convert-ToLedgerRecord $_ })
$routeCounts = @{}
foreach ($routeClass in @('candidate', 'blocked', 'excluded', 'invalid')) {
    $routeCounts[$routeClass] = @($ledgerRows | Where-Object route_class -eq $routeClass).Count
}
if ($routeCounts.candidate -ne 301) { Add-Error $errors "Candidate-route count mismatch: expected=301, actual=$($routeCounts.candidate)" }
if ($routeCounts.blocked -ne 4) { Add-Error $errors "Blocked-route count mismatch: expected=4, actual=$($routeCounts.blocked)" }
if ($routeCounts.excluded -ne 185) { Add-Error $errors "Excluded-route count mismatch: expected=185, actual=$($routeCounts.excluded)" }
if ($routeCounts.invalid -ne 0) { Add-Error $errors "Invalid-route count: $($routeCounts.invalid)" }

$groupRows = @()
foreach ($batch in $expectedCounts.Keys) {
    $batchRows = @($ledgerRows | Where-Object batch_id -eq $batch)
    $candidateRows = @($batchRows | Where-Object route_class -eq 'candidate')
    $definition = $groupDefinitions[$batch]
    $groupRows += [pscustomobject][ordered]@{
        candidate_group_id = $batch
        candidate_group_title = $definition.title
        batch_id = $batch
        total_documents = $batchRows.Count
        candidate_documents = $candidateRows.Count
        blocked_documents = @($batchRows | Where-Object route_class -eq 'blocked').Count
        excluded_documents = @($batchRows | Where-Object route_class -eq 'excluded').Count
        candidate_record_ids = ($candidateRows.record_id -join ',')
        required_gate = $definition.gate
        proposed_ticket_title = $definition.ticket
        processing_boundary = $definition.boundary
    }
}

if ((($groupRows | Measure-Object total_documents -Sum).Sum) -ne 490) { Add-Error $errors 'Candidate-group total does not reconcile to 490 documents' }
if ((($groupRows | Measure-Object candidate_documents -Sum).Sum) -ne 301) { Add-Error $errors 'Candidate-group total does not reconcile to 301 candidates' }
if ((($groupRows | Measure-Object blocked_documents -Sum).Sum) -ne 4) { Add-Error $errors 'Candidate-group blocked total does not reconcile to 4 documents' }
if ((($groupRows | Measure-Object excluded_documents -Sum).Sum) -ne 185) { Add-Error $errors 'Candidate-group excluded total does not reconcile to 185 documents' }

if ($errors.Count -gt 0) {
    throw ("Consolidated ledger verification failed:`n- " + ($errors -join "`n- "))
}

if ($VerifyOnly) {
    if (-not (Test-Path -LiteralPath $ledgerPath -PathType Leaf)) { throw "Missing consolidated ledger: $ledgerPath" }
    if (-not (Test-Path -LiteralPath $groupPath -PathType Leaf)) { throw "Missing candidate-group summary: $groupPath" }
    $actualLedger = @(Import-Csv -Delimiter "`t" -LiteralPath $ledgerPath)
    $actualGroups = @(Import-Csv -Delimiter "`t" -LiteralPath $groupPath)
    $compareErrors = [System.Collections.Generic.List[string]]::new()
    Compare-Records $ledgerRows $actualLedger ($canonicalColumns + @('route_class', 'candidate_group_id')) 'Consolidated ledger' $compareErrors
    Compare-Records $groupRows $actualGroups @('candidate_group_id','candidate_group_title','batch_id','total_documents','candidate_documents','blocked_documents','excluded_documents','candidate_record_ids','required_gate','proposed_ticket_title','processing_boundary') 'Candidate groups' $compareErrors
    if ($compareErrors.Count -gt 0) { throw ("Generated artifact verification failed:`n- " + ($compareErrors -join "`n- ")) }
} else {
    $ledgerRows | Export-Csv -Delimiter "`t" -UseQuotes Always -NoTypeInformation -Encoding utf8NoBOM -LiteralPath $ledgerPath
    $groupRows | Export-Csv -Delimiter "`t" -UseQuotes Always -NoTypeInformation -Encoding utf8NoBOM -LiteralPath $groupPath
}

$batchSummary = ($expectedCounts.Keys | ForEach-Object { "$_=$($expectedCounts[$_])" }) -join '; '
$correctionCount = @($rows | Where-Object { $correctionByPath.ContainsKey($_.path) }).Count
Write-Output "R01-R13 consolidated ledger verified: total=490; $batchSummary; missing=0; duplicates=0; hash_drift=0; approved_by_classification=0; candidates=301; blocked=4; excluded=185; candidate_groups=13; git_status_corrections=$correctionCount"
