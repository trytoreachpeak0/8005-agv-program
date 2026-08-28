[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$InventoryRoot = Split-Path -Parent $PSCommandPath
$EffortRoot = Split-Path -Parent (Split-Path -Parent $InventoryRoot)
$SnapshotPath = Join-Path $EffortRoot 'evidence\initial-snapshot\candidate-documents.tsv'
$InventoryPath = Join-Path $InventoryRoot 'material-inventory.tsv'
$SummaryPath = Join-Path $InventoryRoot 'batches.md'

$BatchCatalog = [ordered]@{
    R01 = @{ Title = '客户、项目协议与原始需求输入'; FollowUp = 'yes'; Purpose = '核实客户/项目原稿、讨论稿、需求确认与附件的来源、版本、批准范围及重复关系。' }
    R02 = @{ Title = '需求库框架、愿景、干系人与业务规则'; FollowUp = 'yes'; Purpose = '核实结构化需求库的形成历史、模板/索引性质，以及愿景、干系人和业务规则的来源与批准状态。' }
    R03 = @{ Title = '用例'; FollowUp = 'yes'; Purpose = '按用例集合核实来源链、适用范围、确认状态与未决项，不因编号或格式推定权威。' }
    R04 = @{ Title = '功能需求'; FollowUp = 'yes'; Purpose = '按功能需求集合核实原子条目来源、批准证据、适用范围及与上游用例/规则的派生关系。' }
    R05 = @{ Title = '现场操作验收场景'; FollowUp = 'yes'; Purpose = '核实现场操作测试案例是否是已批准验收标准、派生验证材料或草稿。' }
    R06 = @{ Title = '仓位、硬件、车队及其余测试案例'; FollowUp = 'yes'; Purpose = '核实其余测试案例和占位索引的来源、批准状态、覆盖范围及派生关系。' }
    R07 = @{ Title = '追溯规则与非功能需求'; FollowUp = 'yes'; Purpose = '核实追溯规则、矩阵及非功能要求的来源、可批准粒度和适用范围。' }
    R08 = @{ Title = '跨域词汇与架构决定'; FollowUp = 'yes'; Purpose = '核实 CONTEXT、术语表和跨域 ADR 的决定来源、批准主体、版本适用性；不得把 accepted 外观当成批准证据。' }
    R09 = @{ Title = 'MES 与 SDK 架构决定'; FollowUp = 'yes'; Purpose = '核实 MES/SDK ADR 的来源、批准证据和适用范围，并区分需求决定与设计决定。' }
    R10 = @{ Title = '仓位模拟器需求与决定'; FollowUp = 'yes'; Purpose = '核实模拟器愿景、需求、决定、设计和测试计划是否属于本系统需求基线及其批准范围。' }
    R11 = @{ Title = 'MES 数据、查询与工厂验证约束'; FollowUp = 'yes'; Purpose = '核实 MES 业务说明、查询契约、参考数据和现场验证清单的来源、版本、范围及证据状态。' }
    R12 = @{ Title = '历史本地 spec 与实施票据'; FollowUp = 'yes'; Purpose = '核实既有 .scratch spec/issue 的来源、完成状态、批准证据与对当前版本的适用性。' }
    R13 = @{ Title = 'RIoT 外部接口与 SDK 约束'; FollowUp = 'yes'; Purpose = '核实厂商文档、物模型、OpenAPI 快照和 SDK 规格的版本身份、适用环境及其只能证明的约束范围。' }
    E01 = @{ Title = '需求库与编辑器配置现状证据'; FollowUp = 'no'; Purpose = '仅记录 Obsidian 等配置现状，不作为需求或批准证据；相关候选批次需要时按哈希引用。' }
    E02 = @{ Title = 'MES 实验、实现、样本与运行证据'; FollowUp = 'no'; Purpose = '仅记录查询实现、实验、样本、配置、日志与执行结果现状，供 R01/R11 调查按需引用。' }
    E03 = @{ Title = 'RIoT 行为实验与配置现状证据'; FollowUp = 'no'; Purpose = '仅记录行为实验、fixture、配置、日志和观察结果现状，供 R13 调查按需引用。' }
    E04 = @{ Title = 'RIoT SDK 实现与接口转储现状证据'; FollowUp = 'no'; Purpose = '仅记录 SDK 实现、生成/转储材料现状，不据此反推正确需求。' }
    E05 = @{ Title = '根目录事件转储现状证据'; FollowUp = 'no'; Purpose = '仅记录事件转储现状，不作为需求、业务决定或批准证据。' }
    G01 = @{ Title = '仓库代理、流程与工具元数据'; FollowUp = 'no'; Purpose = '记录代理技能、追踪器说明、文件命名和工具锁定等仓库治理现状；不纳入系统需求候选。' }
}

function New-Route {
    param(
        [Parameter(Mandatory)] [string] $Batch,
        [Parameter(Mandatory)] [string] $Role,
        [Parameter(Mandatory)] [string] $Reason
    )

    [pscustomobject]@{
        batch_id = $Batch
        material_role = $Role
        route_reason = $Reason
    }
}

function Get-Route {
    param([Parameter(Mandatory)] [string] $Path)

    switch -Regex ($Path) {
        '^project_agreements/' { return New-Route R01 'candidate-source' '项目协议、指令书或其附件；可能携带批准或范围证据。' }
        '^requirement-documents/07-customer-deliverables/' { return New-Route R01 'candidate-source' '客户交付/讨论材料及附件；须核实版本与批准状态。' }
        '^requirement-documents/(简易需求文档|FR的可能来源|user case)\.md$' { return New-Route R01 'candidate-source' '需求库根部的早期输入或来源说明。' }
        '^mes/(宿迁长电AGV项目MES数据接口需求确认|AGV系统业务与MES任务模型)\.md$' { return New-Route R01 'candidate-source' 'MES 根部需求/业务说明副本；须检查与其他位置的重复和版本关系。' }
        '^mes/docs/(待处理事项清单-MES-RIOT-应用|宿迁长电AGV项目MES数据接口需求确认|AGV系统业务与MES任务模型)\.(md|docx)$' { return New-Route R01 'candidate-source' 'MES 需求确认、业务模型或待处理事项输入。' }
        '^mes/sources/customer/' { return New-Route R01 'candidate-source' '客户来源快照；保留为来源证据，不自动视为已批准需求。' }

        '^requirement-documents/\.obsidian/' { return New-Route E01 'current-state-evidence' '编辑器/插件配置，只证明盘点时仓库工具状态。' }
        '^requirement-documents/_templates/' { return New-Route R02 'template-or-index' '需求记录模板，只定义记录形态，不独立表达获批需求。' }
        '^requirement-documents/(00-vision|01-stakeholders|02-business-rules)/' { return New-Route R02 'candidate-requirement' '愿景、干系人或业务规则候选，等待来源与批准核实。' }
        '^requirement-documents/README\.md$' { return New-Route R02 'template-or-index' '需求库入口与组织说明。' }
        '^requirement-documents/03-use-cases/' { return New-Route R03 'candidate-requirement' '用例或用例索引/指南，等待逐份核实。' }
        '^requirement-documents/04-functional-requirements/' { return New-Route R04 'candidate-requirement' '功能需求或其索引/指南，等待原子条目核实。' }
        '^requirement-documents/05-test-cases/01-site-operations/' { return New-Route R05 'candidate-acceptance' '现场操作测试案例，可能表达验收标准。' }
        '^requirement-documents/05-test-cases/' { return New-Route R06 'candidate-acceptance' '测试案例或索引，可能表达验收标准。' }
        '^requirement-documents/(06-traceability|08-non-functional-requirements)/' { return New-Route R07 'candidate-requirement' '追溯治理或非功能要求候选。' }

        '^CONTEXT\.md$' { return New-Route R08 'candidate-vocabulary' '领域词汇候选；地图明确禁止未核实时自动认权。' }
        '^glossary/' { return New-Route R08 'candidate-vocabulary' '术语材料候选；须核实来源和适用范围。' }
        '^docs/adr/cross/' { return New-Route R08 'candidate-decision' '跨域 ADR 决定候选；accepted 状态本身不是批准证据。' }
        '^docs/adr/(mes|sdk)/' { return New-Route R09 'candidate-decision' 'MES/SDK ADR 决定候选；须区分需求决定与设计决定。' }
        '^docs/adr/README\.md$' { return New-Route R09 'template-or-index' 'ADR 索引/说明，不独立证明业务批准。' }

        '^slots-simulator/AGENTS\.md$' { return New-Route G01 'repository-governance' '子项目代理规则，不是系统需求。' }
        '^slots-simulator/' { return New-Route R10 'candidate-requirement' '模拟器愿景、需求、决定、设计、测试或参考材料，须核实其基线范围。' }

        '^mes/docs/工厂首轮执行与回传清单\.md$' { return New-Route R11 'candidate-acceptance' '现场验证清单可能表达验收条件，须核实批准与适用范围。' }
        '^mes/(analysis|catalog|queries|reference)/' { return New-Route R11 'candidate-data-constraint' 'MES 查询/参考材料可能表达外部数据约束。' }
        '^mes/README\.md$' { return New-Route R11 'template-or-index' 'MES 资料入口及材料边界说明。' }
        '^mes/docs/工厂环境配置说明\.md$' { return New-Route E02 'current-state-evidence' '环境配置说明只证明盘点时的部署/操作现状。' }
        '^mes/(evidence|experiments|ingest|samples|tools)/' { return New-Route E02 'current-state-evidence' 'MES 实验、实现、样本、工具或执行结果，只作现状证据。' }
        '^mes/sources/legacy-program-sql/' { return New-Route E02 'current-state-evidence' '旧程序 SQL 快照只证明历史实现现状。' }

        '^\.scratch/(mes-ingest-phase-1|mes-ingest-review-remediation|mes-ingest-watch-operations)/' { return New-Route R12 'candidate-decision' '既有本地 spec/issue 记录；须核实来源、批准与当前适用性。' }

        '^rcs/01-rcs-intro\.md$' { return New-Route R13 'candidate-external-constraint' '项目 RIoT 接入说明，须核实来源与适用版本。' }
        '^rcs/riot_documents/' { return New-Route R13 'candidate-external-constraint' '厂商接口文档，可能约束集成但须核实版本与项目适用性。' }
        '^rcs/riot_ithing_model/' { return New-Route R13 'candidate-external-constraint' '物模型快照，可能约束集成但须核实环境和版本。' }
        '^rcs/riot_swagger/' { return New-Route R13 'current-state-evidence' 'OpenAPI/配置快照只证明被采集接口现状，不能自动成为正确需求。' }
        '^rcs/riot-sdk/(README\.md|docs/|specs/)' { return New-Route R13 'candidate-external-constraint' 'SDK 说明/规格可能表达接口约束，须核实其来源和批准范围。' }
        '^rcs/riot-sdk/' { return New-Route E04 'current-state-evidence' 'SDK 实现或生成产物只证明当前实现。' }
        '^rcs/(_endpoints_dump|_imap_dump)\.txt$' { return New-Route E04 'current-state-evidence' '接口转储只证明采集时现状。' }
        '^rcs/riot-behavior-lab/' { return New-Route E03 'current-state-evidence' '行为实验、fixture、配置、日志、观察或研究记录只作现状证据。' }

        '^events_dump\.txt$' { return New-Route E05 'current-state-evidence' '事件转储只证明采集时现状。' }
        '^\.agents/' { return New-Route G01 'repository-governance' '代理技能与配置，不是项目系统需求。' }
        '^docs/agents/' { return New-Route G01 'repository-governance' '代理/追踪器工作规则，不是项目系统需求。' }
        '^AGENTS\.md$' { return New-Route G01 'repository-governance' '根代理规则，不是项目系统需求。' }
        '^skills-lock\.json$' { return New-Route G01 'repository-governance' '工具锁定元数据，不是项目系统需求。' }
        '^file-naming-convention/' { return New-Route G01 'repository-governance' '文件命名治理说明，不是系统行为需求。' }
        default { return New-Route 'UNCLASSIFIED' 'unclassified' '没有命中路由规则。' }
    }
}

$SnapshotRows = @(Import-Csv -LiteralPath $SnapshotPath -Delimiter "`t")
if ($SnapshotRows.Count -eq 0) {
    throw 'Initial snapshot is empty.'
}

$DuplicatePaths = @($SnapshotRows | Group-Object path | Where-Object Count -ne 1)
if ($DuplicatePaths.Count -ne 0) {
    throw "Initial snapshot has duplicate paths: $($DuplicatePaths.Name -join ', ')"
}

$InventoryRows = foreach ($Row in $SnapshotRows) {
    $Route = Get-Route -Path $Row.path
    $Batch = $BatchCatalog[$Route.batch_id]
    if ($null -eq $Batch) {
        throw "Unknown batch '$($Route.batch_id)' for '$($Row.path)'."
    }

    [pscustomobject]@{
        path = $Row.path
        git_status = $Row.git_status
        sha256 = $Row.sha256
        bytes = $Row.bytes
        last_write_utc = $Row.last_write_utc
        material_role = $Route.material_role
        batch_id = $Route.batch_id
        batch_title = $Batch.Title
        follow_up_ticket = $Batch.FollowUp
        route_reason = $Route.route_reason
    }
}

$Unclassified = @($InventoryRows | Where-Object material_role -eq 'unclassified')
if ($Unclassified.Count -ne 0) {
    throw "Unclassified snapshot rows: $($Unclassified.path -join ', ')"
}
if ($InventoryRows.Count -ne $SnapshotRows.Count) {
    throw "Row count mismatch: snapshot=$($SnapshotRows.Count), inventory=$($InventoryRows.Count)."
}
if (@($InventoryRows | Group-Object path | Where-Object Count -ne 1).Count -ne 0) {
    throw 'Inventory contains duplicate paths.'
}

$InventoryRows | Export-Csv -LiteralPath $InventoryPath -Delimiter "`t" -NoTypeInformation -Encoding utf8

$RoleLines = $InventoryRows |
    Group-Object material_role |
    Sort-Object Name |
    ForEach-Object { "| ``$($_.Name)`` | $($_.Count) |" }

$BatchLines = foreach ($BatchId in $BatchCatalog.Keys) {
    $Rows = @($InventoryRows | Where-Object batch_id -eq $BatchId)
    if ($Rows.Count -eq 0) {
        continue
    }
    $RoleSummary = ($Rows | Group-Object material_role | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join '; '
    $TotalBytes = ($Rows | Measure-Object -Property bytes -Sum).Sum
    "| $BatchId | $($BatchCatalog[$BatchId].Title) | $($Rows.Count) | $TotalBytes | $($BatchCatalog[$BatchId].FollowUp) | $RoleSummary |"
}

$CandidateCount = @($InventoryRows | Where-Object { $_.batch_id -like 'R*' }).Count
$EvidenceCount = @($InventoryRows | Where-Object { $_.batch_id -like 'E*' }).Count
$GovernanceCount = @($InventoryRows | Where-Object { $_.batch_id -like 'G*' }).Count

$Summary = @"
# 当前需求性材料无损清单批次

## 口径

- 唯一输入是已固定的 **../initial-snapshot/candidate-documents.tsv**；本清单没有重新扫描工作区，也没有读取后续变化覆盖快照身份。
- **material-inventory.tsv** 对快照的每一路径一对一保留 **git_status**、**sha256**、**bytes**、**last_write_utc**，再追加材料角色、批次与路由理由。
- **candidate-\*** 只表示值得调查，不表示真实、当前、适用、无冲突或已批准。
- **current-state-evidence** 包括实现、测试/实验、配置、日志、样本、转储和运行结果；它们只能证明观察到的现状，不得反推正确需求。
- **template-or-index** 和 **repository-governance** 不独立形成系统需求；前者可提供结构/指针，后者保留完整盘点但不进入系统需求候选调查。
- 路由按来源群组和单次调查规模组织；同一批次仍须逐文件、逐原子条目核实，不能整批批准。

## 对账

- 初始快照：$($SnapshotRows.Count) 条。
- 清单：$($InventoryRows.Count) 条；路径重复 0，未分类 0，漏项 0。
- 候选调查批次：$CandidateCount 条；现状证据批次：$EvidenceCount 条；仓库治理元数据：$GovernanceCount 条。

## 材料角色

| 角色 | 数量 |
|---|---:|
$($RoleLines -join "`n")

## 批次

| 批次 | 名称 | 文件数 | 字节数 | 建立调查票 | 角色构成 |
|---|---|---:|---:|---|---|
$($BatchLines -join "`n")

## 调查约束

每个 **follow_up_ticket=yes** 批次的调查都必须记录：来源身份、捕获/形成时间、版本或历史关系、具名批准证据、批准适用范围、当前版本适用性、重复/派生关系和仍缺少的证据。调查只能做文档级证据分类；遇到真实冲突时另建逐项 HITL 票，遇到可独立批准的需求时留待后续原子需求分类与批准票。

现状证据批次不单独升级为需求调查票。候选批次可按路径和哈希引用它们来验证实现、环境或外部接口事实，但代码行为、测试通过、配置存在、日志/实验观察均不构成批准。
"@

Set-Content -LiteralPath $SummaryPath -Value $Summary -Encoding utf8

Write-Output "snapshot_rows=$($SnapshotRows.Count)"
Write-Output "inventory_rows=$($InventoryRows.Count)"
Write-Output "candidate_rows=$CandidateCount"
Write-Output "evidence_rows=$EvidenceCount"
Write-Output "governance_rows=$GovernanceCount"
Write-Output "unclassified_rows=$($Unclassified.Count)"
