[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$baselinePath = Join-Path $repoRoot 'requirements\baselines\current-requirements-v1.0.0.md'
$pointerPath = Join-Path $repoRoot 'requirements\current-baseline.md'
$matrixPath = Join-Path $PSScriptRoot 'requirement-applicability-matrix.tsv'
$summaryPath = Join-Path $PSScriptRoot 'requirement-applicability-matrix-summary.md'

$expectedBaselineSha = '5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba'
$actualBaselineSha = (Get-FileHash -LiteralPath $baselinePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualBaselineSha -ne $expectedBaselineSha) {
    throw "Baseline SHA-256 mismatch. Expected $expectedBaselineSha, got $actualBaselineSha."
}

$pointer = Get-Content -LiteralPath $pointerPath -Raw
if ($pointer -notmatch [regex]::Escape($expectedBaselineSha)) {
    throw 'requirements/current-baseline.md does not point at the matrix baseline SHA-256.'
}

function New-IdSet {
    param([int[]]$Numbers)
    $set = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($number in $Numbers) { [void]$set.Add($number) }
    return ,$set
}

function Add-RangeToSet {
    param(
        [System.Collections.Generic.HashSet[int]]$Set,
        [int]$Start,
        [int]$End
    )
    foreach ($number in $Start..$End) { [void]$Set.Add($number) }
}

$direct = New-IdSet @(
    1, 26, 28, 29, 30, 31, 40, 79,
    146, 147,
    150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163,
    164, 169,
    183, 184, 186, 187,
    191, 192, 193, 200, 201, 204, 205, 207, 208, 209, 210,
    213,
    221, 222, 223, 224, 231,
    243, 244, 245, 246, 247, 248, 249,
    250, 258, 267, 269, 270,
    281,
    298, 302, 303, 305, 308,
    312, 313, 319,
    321, 322, 324, 325, 327, 329, 330, 331, 332, 333, 334, 335, 343, 344, 345
)
Add-RangeToSet $direct 221 224

$dependency = New-IdSet @(
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27,
    47, 51, 53, 54, 56, 78, 89,
    148, 149,
    165, 166, 167, 168,
    181, 182, 188,
    211,
    216, 218,
    225, 226, 227, 228, 229, 230,
    232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242,
    253, 255,
    257, 259, 262, 263, 264, 265,
    271, 272,
    282, 290,
    299, 300, 301, 304, 306, 309,
    314, 315,
    323, 336, 337, 338, 340, 341, 342, 347, 348
)

$deferred = New-IdSet @(
    37, 52, 55, 69, 70, 71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86, 87, 88,
    190, 194, 199, 203,
    212, 215,
    251, 252, 254, 256, 260, 261, 266, 268, 273, 274, 275, 276, 277, 278, 279, 280,
    307, 339, 346
)

$notApplicable = New-IdSet @()
Add-RangeToSet $notApplicable 32 36
Add-RangeToSet $notApplicable 38 39
Add-RangeToSet $notApplicable 41 46
Add-RangeToSet $notApplicable 48 50
Add-RangeToSet $notApplicable 57 68
Add-RangeToSet $notApplicable 90 145
Add-RangeToSet $notApplicable 170 180
foreach ($number in @(185, 189, 195, 196, 197, 198, 202, 206, 214, 217, 219, 220)) { [void]$notApplicable.Add($number) }
Add-RangeToSet $notApplicable 283 289
Add-RangeToSet $notApplicable 291 297
foreach ($number in @(310, 311, 316, 317, 318, 320, 326, 328)) { [void]$notApplicable.Add($number) }

$allSets = @($direct, $dependency, $deferred, $notApplicable)
for ($number = 1; $number -le 348; $number++) {
    $membershipCount = @($allSets | Where-Object { $_.Contains($number) }).Count
    if ($membershipCount -ne 1) {
        throw "REQ-$($number.ToString('0000')) belongs to $membershipCount classification sets; expected exactly one."
    }
}

function Get-Domain {
    param([int]$Number)
    switch ($Number) {
        { $_ -le 31 } { return 'MesIngest 目录与 Demand 事实' }
        { $_ -le 89 } { return 'MesIngest Watch、历史与运维' }
        { $_ -le 115 } { return 'MesIngestWatch AREA 配置编辑' }
        { $_ -le 145 } { return 'MesIngestWatch Inspector 交互' }
        { $_ -le 149 } { return 'RIoT 允许接口面' }
        { $_ -le 157 } { return 'Demand 身份、取消与抑制' }
        { $_ -le 163 } { return 'MES 只读与本地完成边界' }
        { $_ -le 180 } { return 'RIoT 订单状态与自动充电异常' }
        { $_ -le 188 } { return 'MES 候选、字段与机台端点' }
        { $_ -le 211 } { return '调度、容量与多任务规划' }
        { $_ -le 220 } { return '机台装货入口与服务端门禁' }
        { $_ -le 231 } { return '关卡卸货与完工后处置' }
        { $_ -le 249 } { return '故障、载货恢复与物理安全' }
        { $_ -le 256 } { return '人员身份、管理员与审计' }
        { $_ -le 267 } { return '仓位模型、IO 配置与投运' }
        { $_ -le 280 } { return '状态展示、日志与账号策略' }
        { $_ -le 297 } { return '电量、自动充电与空闲返回' }
        { $_ -le 309 } { return 'Map／Station 目录快照' }
        { $_ -le 320 } { return 'AGV 身份、归档与恢复' }
        default { return '机台／公共站点绑定与建单对账' }
    }
}

function Get-DecisionPointer {
    param([int]$Number)
    switch ($Number) {
        { $_ -le 31 } { return '决定 Demand 受理、执行身份与完成后防重边界 (../issues/02-decide-demand-acceptance-execution-identity-and-completion-deduplication.md)' }
        { $_ -le 145 } { return '最终批准 MVP 精确需求适用性清单 (../issues/12-approve-exact-mvp-requirement-applicability-profile.md)' }
        { $_ -le 149 } { return '决定 MVP RIoT 移动、建单对账与人工充电边界 (../issues/06-decide-riot-movement-order-reconciliation-and-manual-charging-boundary.md)' }
        { $_ -le 157 } { return '决定 Demand 受理、执行身份与完成后防重边界 (../issues/02-decide-demand-acceptance-execution-identity-and-completion-deduplication.md)' }
        { $_ -le 163 } { return '决定机台取货、多仓装货、关卡卸货与成功边界 (../issues/04-decide-pickup-loading-gate-unloading-and-success-boundary.md)' }
        { $_ -le 180 } { return '决定 MVP RIoT 移动、建单对账与人工充电边界 (../issues/06-decide-riot-movement-order-reconciliation-and-manual-charging-boundary.md)' }
        { $_ -le 188 } { return '决定机台取货、多仓装货、关卡卸货与成功边界 (../issues/04-decide-pickup-loading-gate-unloading-and-success-boundary.md)' }
        { $_ -le 211 } { return '决定单 Demand 选择、并发与等待策略 (../issues/03-decide-single-demand-selection-concurrency-and-waiting-policy.md)' }
        { $_ -le 231 } { return '决定机台取货、多仓装货、关卡卸货与成功边界 (../issues/04-decide-pickup-loading-gate-unloading-and-success-boundary.md)' }
        { $_ -le 280 } { return '决定 MVP 多仓容量、安全联锁与异常恢复最小集 (../issues/05-decide-minimum-multislot-safety-and-recovery-set.md)' }
        { $_ -le 297 } { return '决定 MVP RIoT 移动、建单对账与人工充电边界 (../issues/06-decide-riot-movement-order-reconciliation-and-manual-charging-boundary.md)' }
        { $_ -le 309 } { return '决定受控工厂试运行配置、执行顺序与验收证据 (../issues/11-decide-controlled-factory-pilot-configuration-and-acceptance-evidence.md)' }
        { $_ -le 320 } { return '决定 MVP 多仓容量、安全联锁与异常恢复最小集 (../issues/05-decide-minimum-multislot-safety-and-recovery-set.md)' }
        default { return '决定受控工厂试运行配置、执行顺序与验收证据 (../issues/11-decide-controlled-factory-pilot-configuration-and-acceptance-evidence.md)' }
    }
}

function Get-DependencyChain {
    param([int]$Number)
    switch ($Number) {
        { $_ -le 31 } { return 'MesIngest 完整轮次→ExternallyReadableDemandCatalog/CatalogRevision→AcceptedDemandSnapshot→本地执行身份' }
        { $_ -le 145 } { return 'MesIngest 运维/Watch 能力→真实目录可用性证据；不进入 ControlServer—OnboardHmi 主旅程' }
        { $_ -le 149 } { return 'RIoT 查询/建单/命令白名单→OrderIntent→结果未知对账→到站事实' }
        { $_ -le 157 } { return 'TransportDemandKey→DemandId/DemandRevision→本地终态→永久抑制/再现处理' }
        { $_ -le 163 } { return '真实装卸完成→8005 本地终态→释放车辆；MES/PDA 独立且无写回' }
        { $_ -le 180 } { return '车辆/订单新鲜事实→派车资格→移动或人工充电阻断→结果收敛' }
        { $_ -le 188 } { return '完整 WIRE_TO_GATE 行→AREA/EQP 与篮数事实→机台站/关卡站解析→装货准入' }
        { $_ -le 211 } { return '合格 Demand→单任务稳定选择→指定 AGV/仓位硬准入→不预绑忙车→OrderIntent' }
        { $_ -le 220 } { return '机台到站→操作员/Sublot 核对→服务端最终门禁→多仓装货指令' }
        { $_ -le 231 } { return '关卡到站→全部目标仓位卸空/锁闭→StopClosureCommit→本地完成' }
        { $_ -le 249 } { return 'StationOperationGuard→逐仓物理闭环→断联/故障收敛→可唯一解释恢复' }
        { $_ -le 256 } { return '人员身份/权限→敏感操作授权→不可改写审计→异常处置交接' }
        { $_ -le 267 } { return 'SlotModel/IO 配置身份→车载快照→投运核验→仓位资格与物理执行' }
        { $_ -le 280 } { return '当前事实/账号策略→HMI 状态与操作权限→日志/审计证据' }
        { $_ -le 297 } { return '电量事实→新任务准入或人工充电等待；自动充电/空闲返回在范围外' }
        { $_ -le 309 } { return 'RIoT Map/Station 全量快照→新鲜度门禁→冻结解析站点→移动建单' }
        { $_ -le 320 } { return 'AgvIdentity/RiotVehicleBinding/生命周期代次→业务就绪→会话与订单隔离' }
        default { return 'AREA 机台站/关卡公共功能绑定→不可变配置版本→TransportDemand 冻结→建单与结果对账' }
    }
}

function Get-Impact {
    param(
        [int]$Number,
        [string]$Classification
    )
    $none = '无首期实现影响；只保留为基线追溯，禁止误删原需求。'
    if ($Classification -eq '本场景不适用') {
        return @($none, $none, '不进入 ProtocolVersion 1；不得为范围外能力预留未定义消息。')
    }
    switch ($Number) {
        { $_ -le 31 } { return @('读取并冻结目录身份；不得重建 MES 事实。', '仅展示服务端已接受的 Demand 摘要，不自行读取 MES。', '需要携带已接受执行身份和必要来源修订，不复制 MesIngest DTO。') }
        { $_ -le 145 } { return @('仅在试运行门禁中消费健康/契约身份。', '无 MesIngestWatch 页面实现。', '通常无；健康身份只在诊断证据中引用。') }
        { $_ -le 149 } { return @('实现指定车辆的查询、建单、命令和对账边界。', '展示移动/到站/阻断事实，不直接调用 RIoT。', '服务端向车载发布可行动状态；不透传任意 RIoT API。') }
        { $_ -le 163 } { return @('持久化执行、取消、完成和抑制身份。', '显示唯一任务和本地完成；不显示或等待 PDA。', '任务快照、终态和去重关联必须版本化。') }
        { $_ -le 188 } { return @('执行 WIRE_TO_GATE 字段、站点和容量准入。', '在机台展示并核对 Sublot/篮数/端点。', '只传经服务端裁决的字段和错误码，不让车载二次分类。') }
        { $_ -le 211 } { return @('实现单任务选择、硬准入、等待与结构性阻断。', '只接收当前唯一任务/等待原因。', '需要任务分配、撤回/阻断和状态快照语义。') }
        { $_ -le 231 } { return @('掌握任务、仓位集和装卸业务承诺。', '掌握扫码、操作员交互和逐仓物理执行。', '需要装卸请求/结果、幂等身份、可靠事件与可替换快照。') }
        { $_ -le 249 } { return @('掌握业务阻断、恢复授权和任务/货物绑定。', '独占 IO、安全收尾、日志与恢复现场交互。', '需要断联收敛、逐仓结果、未知状态和 RecoveryHandshake 对账。') }
        { $_ -le 267 } { return @('提供身份、权限、审计和版本化仓位配置权威。', '执行身份核验并消费只读布局/IO 绑定。', '只交换最小身份、授权结果与配置身份，不同步管理界面。') }
        { $_ -le 280 } { return @('提供当前状态、权限裁决和审计留存。', '显示可行动状态并保存技术/执行日志。', '定义诊断/状态快照字段和敏感操作拒绝码。') }
        { $_ -le 297 } { return @('以电量门禁阻断新任务并提示人工充电。', '展示低电量等待与恢复业务就绪。', '只需要电量阻断/就绪状态；无自动充电或空闲返回消息。') }
        { $_ -le 309 } { return @('维护/验证 Map 与 Station 快照并冻结任务端点。', '展示服务端给出的站点，不自行同步 RIoT 目录。', '携带稳定站点身份、配置版本和新鲜度阻断码。') }
        { $_ -le 320 } { return @('掌握 AgvIdentity、RIoT 绑定和生命周期代次。', '使用 VehicleCredential 建会话并证明本车业务就绪。', '会话、命令和恢复消息绑定 AGV/代次/协议身份。') }
        default { return @('解析机台与关卡绑定，持久化配置/建单对账。', '按服务端冻结端点执行到站装卸。', '携带站点/绑定版本、OrderIntent 和对账结果身份。') }
    }
}

$specialReason = @{
    37 = '仅作为真实 MesIngest 试运行健康证据候选；完整 Current Attention 产品面不进入双仓库首期。'
    40 = 'ControlServer 必须通过版本化 Host API 发现并读取目录/健康事实，属于真实对端接入的直接门禁。'
    79 = '精确 contractVersion 整包兼容是 ControlServer 接入真实 MesIngest 的直接拒绝门禁。'
    89 = '旧部署状态不是验收证据；试运行前必须重新捕获目标 MesIngest build/contract 身份。'
    169 = '自动充电在范围外，但低电量阻断新任务并等待人工充电是地图已明确保留的直接边界。'
    185 = '旧排除 AREA 能力已由受控 Map/AREA 正向配置收敛，且单场景只接收 WIRE_TO_GATE；候选不进入首期，最终逐条批准时复核。'
    189 = '“同车多 Sublot/多 Demand”明确超出单 Demand/Sublot MVP；其中不合并与冲突保护条款可能仍是上游依赖，须在单 Demand 策略与最终清单中复核。'
    194 = '指定单车仍需最小硬准入，但多车软偏好和回退次序不属于首期；候选延后，避免把整条误当多车实现。'
    205 = '虽含在途车辆竞争语义，但“不预绑忙车、保留 backlog、状态恢复后重选”正是本地图待定的单车等待边界，候选直接纳入。'
    212 = 'MVP 已选扫码/输入 Sublot；运行时双入口配置能力不是首期所需，候选延后。'
    213 = 'OnboardHmi 扫码或输入 Sublot 是地图已明确的机台取货入口，直接纳入。'
    214 = 'Worklist 选择入口与已选 Sublot 扫码入口冲突，本场景候选不适用。'
    217 = '该条专属 WorklistTaskSelection 确认流；MVP 使用扫码核对，候选不适用，但服务端最终门禁由 REQ-0218 保留。'
    218 = '旧文案针对 worklistRevision，但“服务端最终裁决、车载不信任旧 UI 状态”是跨端安全依赖，须在消息面票中重述为扫码路径。'
    250 = '操作员工号和两个具名管理员身份是正常操作、异常恢复和试运行证据的直接身份边界。'
    267 = '八仓物理事实直接决定本 MVP 多仓容量、IO 核验和现场配置身份。'
    281 = '即使不做自动充电，也必须固定新任务电量准入与人工充电后恢复业务就绪的阈值关系。'
    290 = '单车仍需防止业务移动与人工充电/恢复动作并发争用；候选作为安全依赖，不实现完整自动用途调度。'
    312 = '指定 AGV 仍必须使用稳定 agvId，不能把 deviceKey 或网络地址当车辆身份。'
    313 = '真实 RIoT 指定车辆必须通过受控 RiotVehicleBinding 绑定，属于直接配置/建单身份。'
    319 = '试运行前必须以正面新鲜证据证明 VehicleCredential、会话、配置和物理状态业务就绪。'
    326 = '该条明确删除旧覆盖治理能力；MVP 不重建已被基线排除的覆盖流程。'
    328 = '单车 MVP 不发生释放原车后改选其它车辆；失去资格时应等待/阻断，故本条候选不适用。'
}

function Get-Classification {
    param([int]$Number)
    if ($direct.Contains($Number)) { return 'MVP 直接必须' }
    if ($dependency.Contains($Number)) { return 'MVP 交互／安全依赖' }
    if ($deferred.Contains($Number)) { return '首期延后' }
    if ($notApplicable.Contains($Number)) { return '本场景不适用' }
    throw "No classification for REQ-$($Number.ToString('0000'))."
}

function Get-Reason {
    param(
        [int]$Number,
        [string]$Classification,
        [string]$Domain,
        [string]$DecisionPointer
    )
    if ($specialReason.ContainsKey($Number)) { return $specialReason[$Number] }
    switch ($Classification) {
        'MVP 直接必须' { return "该条直接约束单 WIRE_TO_GATE 旅程的${Domain}；候选纳入首期，精确字段/状态仍由${DecisionPointer}收口。" }
        'MVP 交互／安全依赖' { return "不要求在首期重建该条全部产品面，但${Domain}中的事实、门禁或恢复语义是本旅程正确性/安全性的前置依赖；由${DecisionPointer}确认最小保留部分。" }
        '首期延后' { return "该条属于长期${Domain}能力或完整治理面，指定单车、单图、单 Demand 试运行无需先实现；若后续决策证明进入必要链再升级。" }
        '本场景不适用' { return "该条核心行为落在本地图已排除或未采用的${Domain}范围；不进入首期实现，但保留原基线身份并由${DecisionPointer}最终逐条复核。" }
    }
}

function Get-Risk {
    param(
        [string]$Classification,
        [string]$Domain
    )
    switch ($Classification) {
        'MVP 直接必须' { return "误删会使${Domain}主旅程或现场验收无法闭环，并可能造成重复执行、错误站点/仓位或不可证明完成。" }
        'MVP 交互／安全依赖' { return "误删可能让${Domain}出现权威分叉、物理状态猜测、断联后重复副作用或无法恢复；误当完整首期功能则扩大范围。" }
        '首期延后' { return "过早纳入会扩大首期和联调面；若后续证明它是安全/验收必要链却未升级，则会形成隐藏缺口。" }
        '本场景不适用' { return "误纳入会引入范围外状态、页面或协议消息；误把其中可复用的小型门禁一并删除，可能遗漏依赖，故仍需最终 HITL 复核。" }
    }
}

function Clean-TsvCell {
    param([AllowNull()][string]$Value)
    if ($null -eq $Value) { return '' }
    return (($Value -replace "`t", ' ' -replace "`r?`n", ' ') -replace '\s+', ' ').Trim()
}

$baselineText = Get-Content -LiteralPath $baselinePath -Raw
$blockPattern = '(?ms)^### `(?<id>REQ-\d{4})` — (?<title>.+?)\r?\n(?<body>.*?)(?=^---\r?$)'
$matches = [regex]::Matches($baselineText, $blockPattern)
if ($matches.Count -ne 348) {
    throw "Parsed $($matches.Count) requirement blocks; expected 348."
}

$rows = [System.Collections.Generic.List[object]]::new()
foreach ($match in $matches) {
    $id = $match.Groups['id'].Value
    $number = [int]$id.Substring(4)
    $body = $match.Groups['body'].Value
    $scopeMatch = [regex]::Match($body, '(?m)^- Scope: (?<scope>.+)$')
    $requirementMatch = [regex]::Match($body, '(?ms)^#### Current Requirement\r?\n\r?\n(?<requirement>.*?)(?=\r?\n\r?\n#### Verification Method)')
    if (-not $scopeMatch.Success -or -not $requirementMatch.Success) {
        throw "Could not parse Scope or Current Requirement for $id."
    }

    $classification = Get-Classification $number
    $domain = Get-Domain $number
    $decisionPointer = Get-DecisionPointer $number
    $impact = Get-Impact $number $classification
    $rows.Add([pscustomobject]@{
        RequirementId = $id
        Source = "../../../requirements/baselines/current-requirements-v1.0.0.md#$($id.ToLowerInvariant())"
        Title = Clean-TsvCell $match.Groups['title'].Value
        OriginalScope = Clean-TsvCell $scopeMatch.Groups['scope'].Value
        CandidateClassification = $classification
        CandidateReason = Clean-TsvCell (Get-Reason $number $classification $domain $decisionPointer)
        DependencyChain = Clean-TsvCell (Get-DependencyChain $number)
        MisclassificationRisk = Clean-TsvCell (Get-Risk $classification $domain)
        ControlServerImpact = Clean-TsvCell $impact[0]
        OnboardHmiImpact = Clean-TsvCell $impact[1]
        SharedProtocolImpact = Clean-TsvCell $impact[2]
        PendingHitlDecision = Clean-TsvCell $decisionPointer
    })
}

$ids = @($rows | ForEach-Object RequirementId)
$expectedIds = @(1..348 | ForEach-Object { 'REQ-' + $_.ToString('0000') })
if (@(Compare-Object $expectedIds $ids).Count -ne 0 -or @($ids | Sort-Object -Unique).Count -ne 348) {
    throw 'Requirement coverage is not exactly REQ-0001 through REQ-0348 with zero duplicates.'
}

$headers = @(
    'RequirementId', 'Source', 'Title', 'OriginalScope', 'CandidateClassification', 'CandidateReason',
    'DependencyChain', 'MisclassificationRisk', 'ControlServerImpact', 'OnboardHmiImpact',
    'SharedProtocolImpact', 'PendingHitlDecision'
)
$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add(($headers -join "`t"))
foreach ($row in $rows) {
    $lines.Add((@($headers | ForEach-Object { Clean-TsvCell ([string]$row.$_) }) -join "`t"))
}
[System.IO.File]::WriteAllLines($matrixPath, $lines, [System.Text.UTF8Encoding]::new($false))

$counts = $rows | Group-Object CandidateClassification | Sort-Object Name
$countLines = $counts | ForEach-Object { "| $($_.Name) | $($_.Count) |" }
$matrixSha = (Get-FileHash -LiteralPath $matrixPath -Algorithm SHA256).Hash.ToLowerInvariant()
$summary = @"
# WIRE_TO_GATE MVP 需求适用性证据矩阵摘要

- Source baseline: [current-requirements-v1.0.0.md](../../../requirements/baselines/current-requirements-v1.0.0.md)
- Source baseline SHA-256: ``$actualBaselineSha``
- Current pointer: [current-baseline.md](../../../requirements/current-baseline.md)
- Matrix: [requirement-applicability-matrix.tsv](requirement-applicability-matrix.tsv)
- Matrix SHA-256: ``$matrixSha``
- Generated by: [build-requirement-applicability-matrix.ps1](build-requirement-applicability-matrix.ps1)
- Coverage: ``REQ-0001``–``REQ-0348``，348 条，零重复、零遗漏。

## Candidate counts

| 候选分类 | 数量 |
| --- | ---: |
$($countLines -join "`n")

## Reading rules

- 本矩阵是候选路由和证据索引，不是用户批准的 MVP 精确适用性清单。
- ``MVP 直接必须`` 表示当前地图已足以看出该条直接约束单场景旅程；精确字段和状态仍由所指 HITL 票收口。
- ``MVP 交互／安全依赖`` 表示不必在首期重建整条产品面，但相关事实、门禁、恢复或权威边界不可静默丢失。
- ``首期延后`` 不修改原需求 Lifecycle，也不表示 deprecated；后续若进入必要链必须升级。
- ``本场景不适用`` 仅针对本地图的单车、单图、单 Demand ``WIRE_TO_GATE`` 目的地，不废弃基线条目。
- 每行保留原始 ID、标题、Scope、分类理由、依赖链、误分风险、三端影响和待 HITL 决策指针。详细规范文本与 Verification Method 只存在不可修改基线，通过 Source 列回看，避免复制漂移。

## Explicit conflict and narrowing flags

- ``REQ-0189`` 的多 Sublot/多 Demand 同车能力超出本地图；其“不合并/冲突保护”小条款仍须由“决定单 Demand 选择、并发与等待策略”复核。
- ``REQ-0194`` 的单车最小硬准入可能保留，但多车软偏好/回退延后。
- ``REQ-0205`` 的多车竞争主体不采用，但“不预绑忙车、保留 backlog、恢复后重选”直接进入候选。
- ``REQ-0212``–``REQ-0220`` 中只直接采用扫码/输入 Sublot；Worklist 入口与专属确认/审计流不进入本场景，服务端最终裁决原则作为依赖保留。
- ``REQ-0328`` 的换车分支不适用于指定单车；资格丢失时必须等待或阻断，不能借该条偷偷扩为多车。

## Validation

生成脚本会在写出前验证：当前指针包含基线 SHA-256；基线文件哈希一致；解析到 348 个规范块；每个 ID 恰好落入一个候选分类；最终 ID 集合连续、唯一且无遗漏。任何失败都会终止且不产出新矩阵。
"@
[System.IO.File]::WriteAllText($summaryPath, $summary, [System.Text.UTF8Encoding]::new($false))

Write-Output "Wrote $matrixPath"
Write-Output "Wrote $summaryPath"
Write-Output "Matrix SHA-256: $matrixSha"
Write-Output ($counts | ForEach-Object { "$($_.Name)=$($_.Count)" })
