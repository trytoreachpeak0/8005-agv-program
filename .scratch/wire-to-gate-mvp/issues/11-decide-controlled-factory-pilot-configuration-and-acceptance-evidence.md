# 决定受控工厂试运行配置、执行顺序与验收证据

Type: grilling
Status: resolved
Blocked by: 03, 04, 05, 06, 08, 10

## Question

最终受控试运行前必须锁定哪些 MesIngest 契约与连接身份、ControlServer 和 OnboardHmi 构建 commit、protocol release、AGV/VehicleCredential、Map、EQP/AREA 机台站解析、关卡 FixedTaskStation、仓位配置、RIoT 车辆/站点/建单凭证和真实 Sublot 物料？

离线模拟、双 Fake 契约测试、静态环境核对、空车不开仓彩排、受控真实物料旅程与失败后清场应以什么顺序执行，并以哪些结构化证据证明只执行一次、不重复建单、不遗失载货状态、不等待 MES PDA 且全部安全门禁有效？

由于用户在[验证 OnboardHmi 单场景操作原型](08-validate-onboard-single-scenario-interaction-prototype.md)中明确豁免了车载端开发同事的原型评审，本票还必须决定如何在实施门禁、目标车载硬件或等效校准环境和受控试运行中验证获选 A“旅程导引台”的真实分辨率／缩放无裁切、关键状态无需危险滚动、触控尺寸与误触隔离、扫码枪焦点与键盘备用输入、现场距离和光照下的安全／断联／UNKNOWN 文案可读性，以及状态与动作在车载实现框架中的可实现性。失败必须作为实施缺陷或需用户重新裁决的设计偏差处理，不得把当前原型票误述为车载端开发同事已经批准。

## Answer

### 决策依据与授权记录

本票依据用户对本 Wayfinder 后续各票采用推荐值的明确授权，在重新核对根 `CONTEXT.md`、`docs/adr/cross/`、地图 Notes、全部前置已解决票、A“旅程导引台”原型及其 README 后，采用下列全部推荐值。该授权替代逐题等待，不表示用户曾逐项回答，也不表示车载端开发同事、ControlServer 开发者、现场人员、工厂 IT、RIoT 管理方或任何法定／第三方人员已经确认真实环境、凭证、物料、构建、协议 release 或试运行。

当前项目目录没有可供本票确认的 ControlServer／OnboardHmi 候选构建、真实 `ProtocolReleaseIdentity`、G3 运行、现场凭证、目标车载硬件校准结果或真实 Sublot 证据。因此以下决定固定的是执行前置门禁、顺序、责任和证据格式；具体身份必须在未来执行时从真实来源取得，缺失即不得开始，不能由 AI、默认值、截图、口头确认或本票推荐值补齐。

### 完整候选与推荐值

❓ **Q1 — 试运行配置如何冻结**：候选 A 为现场清单和口头核对；候选 B 只锁两端软件版本，其余使用运行时“当前值”；候选 C 为创建不可改写的 `FactoryPilotConfigurationSnapshot`，绑定全部构建、协议、环境、车辆、地图、站点、仓位、凭证引用、物料资格和前置证据。

➡️ **推荐 C。** A 无法重现，B 会让地图、凭证、RIoT 绑定和物料漂移；C 能在不保存秘密的前提下证明实际运行的精确输入。任一绑定字段变化都建立新快照并重过受影响门禁，不能在原快照上手改。

❓ **Q2 — 谁对哪些事实负责**：候选 A 为用户单人替所有技术和现场事实批准；候选 B 为现场集体口头同意；候选 C 为按权威来源分别具名证明，并保留不可由任何角色豁免的身份、安全与恢复门禁。

➡️ **推荐 C。** 用户负责产品范围和是否启动试运行；两名真实开发者本人按票据 09 治理确认共同协议 release，且双方候选构建负责人分别证明 build 与 G2/G3 身份；系统管理员／部署负责人证明非秘密部署配置和 secret reference；工厂 IT 或 MesIngest 责任人证明 MES 只读契约与目标环境；RIoT 责任人证明目标环境、车辆绑定、站点和建单权限；车载端开发同事证明 A 到生产实现的映射及可实现性；具名现场试运行负责人掌握开始／中止口令；实际执行断电、抱闸、机械开锁等动作的人仍须具备相应现场资质。没有任何一项把 AI 变成批准人，也不新增法定批准结论。

❓ **Q3 — 执行阶段如何排序**：候选 A 为真实物料先跑、失败再补门禁；候选 B 为离线、现场和物料步骤并行；候选 C 为严格串行的 P0～P7，任一步 FAIL／INCONCLUSIVE 都阻断后续步骤。

➡️ **推荐 C。** 顺序固定为：P0 配置和具名证明冻结；P1 G0～G3 离线／双 Fake／真实对真实门禁；P2 静态环境与只读连通核对；P3 目标硬件、生产 UI、输入设备及八仓维护资格核对；P4 空车不开仓彩排；P5 临行 go/no-go 重新核验；P6 一次受控真实物料旅程；P7 结束后对账、清场和封存证据。后一步不能为前一步补证。

❓ **Q4 — A“旅程导引台”怎样取得真实可用性证据**：候选 A 为沿用原型票通过；候选 B 为开发机截图或等效环境单次检查；候选 C 为先做原型到生产的逐项映射，在等效校准环境找缺陷，最终仍在实际目标车载硬件、实际分辨率／缩放、实际扫码枪／键盘、实际触控方式及代表性现场距离和光照下通过完整状态矩阵。

➡️ **推荐 C。** 原型票只定方向。真实门禁要求：所有规定状态无裁切、遮挡或重叠；当前安全、通信／业务就绪、`UNKNOWN`、主要指引和本车急停无需滚动即可看见；关键正常动作保持单一，急停与普通动作具有明显空间和视觉隔离；每个允许动作及相邻禁止动作都在实际触控方式下执行且不得误触；配置的扫码终止符、焦点切换、连续扫码、异常输入和完整键盘备用路径均保持“一次输入只形成一次提交”；安全／断联／恢复文案在记录的最不利观察距离与实测光照边界可辨识；四维状态和八仓事实能由生产框架的真实投影稳定驱动。等效环境可以提前找问题，但 P6 前必须在目标硬件复验。任何失败都是实施缺陷，或由用户重新裁决且重新构建／重验的设计偏差；不得称为“原型已批准”或作轻微视觉豁免。若未来正式验证落入本仓 Golden WPF tier 2/3 范围，仍须另行取得用户授权，不由本票触发。

❓ **Q5 — 空车不开仓彩排证明什么**：候选 A 为把 Fake happy path 当现场彩排；候选 B 为在生产环境注入虚构 MES Demand；候选 C 为把彩排拆成同一证据包中的两项受控活动：目标车载硬件在隔离 harness 下重放生产状态轨迹，以及由 RIoT 责任人使用既有获准的调试／投运能力让指定空车验证精确 Map、机台 Station、关卡 Station、停稳与路线，不发仓位操作、不创建虚假生产事实。

➡️ **推荐 C。** 它验证人员顺序、UI、扫码设备、车辆路线和站点身份，同时不污染真实 MesIngest、TransportDemand、RIoT 业务订单或仓位状态。若现场没有获准的空车路线验证能力，不得临时绕过 ControlServer 或直控车辆；P4 保持阻塞，先由真实 RIoT 责任人提供合规手段。

❓ **Q6 — 真实物料跑几次、是否注入故障**：候选 A 为没有前置门禁时反复试到成功；候选 B 为携带真实物料主动注入断联、崩溃、传感器故障和结果未知；候选 C 为前置负向／恢复轨迹全部在确定性 harness、双 Fake 和 G3 中完成，现场只要求一个全门禁后的正常真实 Sublot 旅程；意外失败按真实失败处理，新 runId 重来，不以“最佳一次”覆盖。

➡️ **推荐 C。** Destination 要求证明一次受控旅程，不授权用真实货物制造危险故障。一个 PASS 旅程足够满足本地图，但所有先前失败和 INCONCLUSIVE 永久保留；任何再次尝试都使用新的 `FactoryPilotRunIdentity`，且只有问题闭合、清场完成、配置身份仍有效时才可重跑。

❓ **Q7 — 什么证据足以验收**：候选 A 为视频加签字；候选 B 为应用日志和最终完成页；候选 C 为机器可读时间线、跨系统持久事实、物理／视觉证据和人工证明共同组成的不可改写证据包，并逐项证明正向结果和禁止副作用。

➡️ **推荐 C。** 视频、照片和签字只作辅证，不能代替构建、协议、RIoT 订单、幂等、仓位及审计事实。证据必须能由 `FactoryPilotRunIdentity` 找回精确配置快照、所有前置 run、原始证据哈希和判定规则。

❓ **Q8 — 失败后如何清场**：候选 A 为删除任务／订单／日志后重来；候选 B 为等待超时自动释放；候选 C 为立即停止进入下一阶段，保留 Guard、Demand、订单、车辆、仓位和货物绑定，先按既有安全与恢复语义对账，再由具名人员走批准的异常路径和实物交接；只有安全、业务和物理事实都收敛后才解除现场。

➡️ **推荐 C。** 不得以改库、换 ID、清日志、人工标记 EMPTY／SAFE／COMPLETE、PDA/MES 后续操作或时间经过代替收敛。无法电子证明空仓／锁闭／输出复位时进入 `ForcedMechanicalCargoRecovery` 等既有路径，业务交接不证明车辆恢复；清场结果及后续修复 runId 必须回链原失败。

❓ **Q9 — 如何判定、保存和批准结果**：候选 A 为现场负责人可手工把失败改成通过；候选 B 为最后一次绿灯覆盖历史；候选 C 为每个运行只取 `PASS|FAIL|INCONCLUSIVE`，安全／身份／持久化／恢复／UNKNOWN／禁止副作用没有手工豁免，证据在 ControlServer 产品验收记录形成单一索引，并把试运行 PASS 与最终发布批准分开。

➡️ **推荐 C。** PASS 只说明精确身份的一次受控试运行满足本票标准，不自动批准生产发布、不批准其它构建／配置、不替代票据 14 的用户与车载端开发同事本人确认。FAIL／INCONCLUSIVE 及红色证据永久保留，秘密只保存版本化 secret reference 和核验结果。

### 1. `FactoryPilotConfigurationSnapshot` 的强制内容

P0 必须形成一个不可改写、可重算 SHA-256 的结构化 snapshot；显示名称、分支、`latest`、口头“当前配置”和未版本化截图均不能作为身份。至少包含：

1. **MES／MesIngest**：目标环境和实例非秘密标识；MesIngest repository、完整 commit、build digest；已发布读契约身份；`FactoryMesTaskQueryVersion` 的提供方、接收日期和 SHA-256；`SUBLOT_BOX_COUNT` 契约与 `package-basket-capacity.csv` 哈希；预计使用的 `HistoryEpoch` 获取方式；只读凭证的 secret reference、版本和权限探测结果。P6 最终读取时再冻结实际 `HistoryEpoch + CatalogRevision + DemandRevision + AcceptedDemandSnapshot`，不能预造。
2. **两端与协议**：ControlServer、OnboardHmi 的 repository、完整 commit、artifact SHA-256、构建配置和部署摘要；完整 `ProtocolReleaseIdentity`；双方适用 Fake 身份；W2G-IS-00～07 的 G1、双方 G2 和同一精确候选 G3 `ConformanceRunIdentity` 指针。G0 必须存在真实、可核验且与身份一致的两名开发者本人批准；原型豁免、用户推荐值授权和 AI 审查均不能替代。
3. **AGV 与连接**：稳定 `agvId`、`AgvLifecycleGeneration`、目标 Onboard 硬件身份、固件／OS／运行时摘要；`VehicleCredential` secret reference 与版本、服务端 TLS pin 指纹；连接身份错配负向检查；当前 `RiotVehicleBinding` 版本和目标 `deviceKey`。不得把真实 secret、私钥或认证证明写入 snapshot。
4. **RIoT**：环境、build、OpenAPI／SDK 身份与已批准接口兼容结论；会话 secret reference；建单、查询、OrderHold／Continue 和必要急停接口的权限探测；指定车辆、Map、Station 与当前绑定；所有未结／未知订单清单及清零证明。跨 build 兼容只能沿用 `CONTEXT.md` 的局部假设，发现差异即阻断对应能力。
5. **Map 与站点**：新鲜 `MapStationCatalogSnapshot` 的 revision、来源 build、内容指纹和观测时间；唯一目标 `mapId`；真实 Sublot 所属 `EQP + AREA`、`AreaEqpUniquenessMonitor` 结果与解析出的机台 `mapId + stationId`；关卡 `FixedTaskStation`、`TaskTypePublicStationRuleVersion`、`PublicStationBindingSetVersion`；两段当前 RouteCost、无同坐标角色歧义及 `SingleBerthStationClaim` 可用事实。任一目录过期、解析非唯一、跨图、绑定暂停或路线不可达都阻断。
6. **八仓与安全**：八仓配置版本／指纹、1～8 号稳定身份、DO1～DO8、DI1～DI16、信号极性、500 ms 脉冲、能力快照、逐仓 SlotOperability；锁反馈、光幕、输出回读和 IO 在线性的维护核验；日志容量；以将用于 P6 的最小／最不利真实花篮尺寸和放置姿态证明 `DetectableLoadConstraint`。维护资格核对必须在停车和隔离条件下完成，不得把管理员身份当安全覆盖。
7. **人员与现场**：用户 go/no-go、两名开发者协议批准、两端候选负责人、部署负责人、工厂 IT／MesIngest 负责人、RIoT 负责人、车载端开发同事、现场试运行负责人、装货操作员、异常处置管理员及所需现场资质人员的身份和各自 attestation 指针；至少一个不共享的个人管理员账号已验证可用。这里记录责任，不替任何人员签名。
8. **物料候选和证据基础设施**：获准用于试运行的真实 Sublot 选择规则、PACKAGE、预计 `ExpectedBasketCount`、1～8 篮边界、花篮可检测性、数量及接管／返还责任；时间同步状态、证据目录可写性、容量、180 天服务端业务／管理员审计与 30 天车载技术日志保留能力。具体 Sublot 和最终篮数只在 P5/P6 从真实事实核验后进入 run identity。

任一 commit、artifact、protocol release、Fake、runner、向量、MesIngest 契约、credential version、RIoT 环境／binding、Map／Station、仓位配置、目标硬件、物料或影响判定的环境字段变化，都必须建立新 snapshot，并重跑受影响的 P1～P5；不得“只改附件”。

### 2. P0～P7 严格执行顺序

1. **P0 — 冻结候选与责任。** 收齐上述真实身份和 attestation，生成 snapshot，验证无 secret 泄露、全部指针可读、哈希可重算。任何待确认项均为 INCONCLUSIVE，不排期 P6。
2. **P1 — 离线与跨仓门禁。** G0、G1、双方 G2、精确两端候选 G3 全部 PASS，W2G-IS-00～07 无未关闭 FAIL／INCONCLUSIVE。身份必须与 snapshot 完全一致；Fake PASS 不能替代 G3，G3 不能替代现场。
3. **P2 — 静态环境核对。** 只读验证 MesIngest 契约、SQL／容量身份、凭证权限、连接和 `HistoryEpoch`；只读验证 RIoT build／API、车辆绑定、Map／Station、RouteCost 和无未结订单；核对八仓、管理员、日志、时钟和证据存储。不得创建 TransportDemand、RIoT 订单、开仓、写 MES 或改配置来“证明”静态核对。
4. **P3 — 目标硬件与维护资格。** 生产 OnboardHmi 在目标车载硬件完成 A 映射、全状态 UI／触控／扫码／键盘／可读性验证；停车隔离下完成八仓 IO 与 `DetectableLoadConstraint` 资格核对。P3 可以使用经批准的无生产业务测试工装或可检测花篮，但不执行真实 TransportDemand。
5. **P4 — 空车不开仓彩排。** 在目标 HMI 的隔离 harness 中重放旅程、断联、UNKNOWN 和恢复状态；另由获准 RIoT 投运手段验证空车沿精确机台与关卡路线、到站、IDLE、停稳和无角色歧义。全过程不开仓、不注入虚构 MES Demand、不触碰生产任务，不得把两部分合称生产端到端通过。
6. **P5 — 临行 go/no-go。** 在预先声明的短时间窗口内重新核对 snapshot 全部新鲜度和无漂移事实；选择一个真实、完整 `WorkType = WIRE_TO_GATE` 候选，证明未命中 suppression／completion／活动执行，预计篮数在 1～8 且合格仓位足够，物料和现场人员已就位。用户只在全部绿灯后授权启动；授权不能覆盖安全门禁。
7. **P6 — 一次受控真实物料旅程。** 从车辆空载、八仓 `EMPTY + 锁闭 + 输出复位`、无未结订单、连接恢复完成且 `VehicleBusinessReadiness` 成立开始；系统最终重读并只受理一个真实 Demand，严格执行 TO_PICKUP、可信机台到站、扫码、完整多仓装货、新鲜发车安全检查、TO_GATE、可信关卡到站、自动批量卸货和本地原子完成。现场不主动注入故障，不等待、不读取、不回写 PDA/MES；目的站责任人仍独立承担其既有流程。
8. **P7 — 结束对账与封存。** 核对所有仓位为空并安全锁闭、输出复位、Guard 和操作收敛、两段 RIoT 订单及调用结果明确、Demand 只有一个本地成功和一个 `TransportDemandCompletion`、车辆状态可解释；导出并哈希全部证据，形成 verdict。未完成 P7 的运行即使页面显示成功也为 INCONCLUSIVE。

任一阶段失败都停止推进，保留当时现场和系统绑定并按第 5 节清场；修复后以新身份从最早受影响阶段重来。

### 3. `FactoryPilotRunIdentity` 与结构化证据

每次 P3、P4 或 P6 尝试均产生独立 run；P6 的 `FactoryPilotRunIdentity` 至少绑定：`runId`、run kind、`FactoryPilotConfigurationSnapshot` 身份与 SHA-256、两端 build identity、`ProtocolReleaseIdentity`、全部适用 `ConformanceRunIdentity`、agvId／生命周期／RIoT binding、Map 与两站身份、仓位配置指纹、真实 AcceptedDemandSnapshot／DemandId／TransportDemandKey／DemandRevision、Sublot／PACKAGE／ExpectedBasketCount、参与人员 attestation 指针、开始／结束时间、结果及证据清单哈希。任何分量变化产生新 runId；失败重跑不得覆盖旧身份。

建议由 ControlServer 产品验收记录保存单一索引：`requirements/acceptance/wire-to-gate/factory-pilot/<runId>/`。本票只规定结构，不创建不存在的现场证据。目录至少包含：

- `run-manifest.json`：身份、verdict、配置 snapshot、前置门禁和 evidence inventory；
- `timeline.ndjson`：统一时间轴上的 MesIngest 读取、承诺事务、协议消息、RIoT 调用／回查、仓位命令／结果、安全快照、业务提交和人员动作摘要；
- `assertions.json`：每条验收不变量、证据指针、expected／actual 和 PASS／FAIL／INCONCLUSIVE；
- `artifacts/`：服务端业务审计、车载技术日志、RIoT 订单快照、持久事实导出、UI 状态矩阵、屏幕／输入／光照／距离核对、照片或视频等原始证据及 SHA-256；
- `cleanup.json`：最终车辆、订单、Guard、仓位、货物交接和异常状态，及失败时的修复 run 链。

证据只保存 secret reference、版本、权限结果和脱敏摘要；VehicleCredential、RIoT／MES 密钥、私钥、人员密码、badge 原值与会话令牌不得进入索引、日志、截图或视频。

### 4. P6 必须全部通过的验收不变量

1. **只受理和执行一次。** 一个最终重读只形成一个 AcceptedDemandSnapshot、一个 DemandId 和一个车辆排他绑定；没有第二个活动 Demand、影子队列绑定或同键新执行。
2. **RIoT 不重复建单。** TO_PICKUP 与 TO_GATE 各自只有一个 MovementLegId／DispatchGeneration／稳定且互不相同的 upperId；超时或重试沿原号对账，RIoT 订单目录证明每段至多一个实际订单，且两段严格串行。
3. **仓位范围不漂移。** `ExpectedBasketCount` 来源、完整目标仓位集和 SlotOperationAttemptId 在 OperationCommitPoint 后不变；恰好一篮一仓，没有替代仓、额外开锁或部分 LoadBatch 成功。正常的相反占用态纠正必须可区分于重复命令副作用。
4. **移动前安全证据完整。** 每次移动使用新的、在有效窗口内的 PreDepartureSafetyCheck；当时所有相关仓门锁闭、输出复位、IO 有效、无未结仓位操作和 Guard。ArrivalAtStation 单独不能开放作业，机台和关卡都通过完整 StationOperationArrivalGate。
5. **载货状态没有遗失。** 从装货前、逐仓装货、LoadBatch、TO_GATE、逐仓卸货到最终空仓，每个检查点都能把 Demand、Sublot、目标仓位、业务状态和车侧物理事实连成一条无冲突链；任何 UNKNOWN 都会阻断而非被人员覆盖。
6. **本地完成唯一且原子。** 全部目标仓位 `EMPTY + 锁闭 + 输出复位` 后，同一事务只形成一次 `UnloadBatch + StopClosureCommit + Demand 成功终态 + TransportDemandCompletion`；服务重读、MesIngest 持续可见、GONE／再现或页面刷新不能形成第二次完成或派车。
7. **PDA/MES 非门禁。** timeline 证明 8005 本地完成不等待目的站 PDA/MES，且所有 8005 组成部分没有 MES 写调用、代办流程、接收确认或后续状态轮询依赖。现场后续流程的时间只可作为独立背景，不进入 PASS 条件。
8. **UI 与输入真实可用。** P3 的目标硬件状态矩阵与 P6 的实际关键状态均满足 Q4；扫码一次只提交一次，键盘备用路径可用，安全／断联／UNKNOWN 和急停无需危险滚动且可辨识。车载端开发同事必须本人确认生产实现映射与可实现性，原型票豁免不适用。
9. **日志和审计可追溯。** 服务端业务／管理员审计和车载技术日志覆盖整个 run，时钟关系可解释，原始证据哈希可重算，保留能力满足既有 180 天／30 天要求；任何证据缺口使相关断言 INCONCLUSIVE。
10. **禁止副作用为零。** 没有额外 Demand、额外 RIoT 订单、扩大 ActiveUnlockSet、越权开仓、人工改写 EMPTY／SAFE／COMPLETE、自动充电、换车、跨图、MES 写回或以 PDA 结果倒推成功。

### 5. 中止、失败清场和重跑

现场试运行负责人可以在任何不确定、人员风险、地图／车辆异常、身份漂移或证据丢失时中止；系统安全联锁仍可自动停车。中止只停止新增副作用，不取消既有事实：

1. 立即禁止新 Demand、下一移动段和未发送开锁组；保留原 DemandId、OrderIntent、upperId、SlotOperationAttemptId、Guard、目标仓位和货物绑定。
2. 已知本系统移动按既有 OrderHold／停车证明处理；来源未知、急停结果未知或无法证明停稳时升级既有最高优先级现场隔离，不靠一次 API 成功推定安全。
3. ActiveUnlockSet 只执行 `SafelyFinishActiveUnlockSet`，不扩大集合。连接、命令、RIoT 或结果未知沿原身份完成恢复握手和对账。
4. 可以唯一修复时在原 ExceptionRecoverySession 范围内 `RESUME_AFTER_REPAIR`；无法继续装货时完整清空并补偿；故障车载货时执行具名 `FAULT_CARGO_HANDOFF`；电子状态无法证明时由合格人员在物理隔离后走 `FORCED_MECHANICAL_RECOVERY`。实物交接不能证明电子空仓、仓门安全或车辆恢复。
5. 清场只有在人员安全、货物去向、全部订单、所有 Guard／操作、逐仓物理与业务状态、输出回读和车辆隔离／可用状态都明确后才能关闭。若仍有未知，运行保持 FAIL 或 INCONCLUSIVE，现场保持阻断。
6. 原证据永久保存。修复、更换构建／配置或重新尝试均建立新 snapshot／runId，并从最早受影响阶段重跑；不得删除数据库事实、复用业务 ID、手工改绿或以新的 PASS 覆盖旧红色结果。

### 6. verdict 与本票边界

- `PASS`：P0～P7 全部完成，十项验收不变量均有可重算证据，且没有未关闭 FAIL／INCONCLUSIVE 或身份漂移。
- `FAIL`：任一断言明确不符合，包括任何身份、安全、重复副作用、仓位／货物链、恢复、PDA 非门禁或 UI 真实可用性失败。
- `INCONCLUSIVE`：环境中断、证据缺失、时间线无法关联、人员 attestation 缺失或事实不能唯一解释；不得按 PASS 使用。

安全、身份、持久化、恢复、UNKNOWN 对账和禁止副作用没有手工豁免。确属协议或向量错误只能按票据 09 由两名开发者本人批准新 release；确属实现／视觉缺陷须修复候选；确属设计偏差须由用户重新裁决；确属环境问题须修复并新 run 重验。

本票没有创建或发布协议 release，没有运行 G0～G3、目标硬件验证、空车路线或真实物料旅程，没有读取或保存任何真实 credential，也没有取得车载端开发同事、现场或第三方批准。一次 FactoryPilot PASS 仍只是精确候选和配置的试运行证据；最终进入实施／发布仍须完成后续《最终批准 MVP 精确需求适用性清单》、交接包及《确认 WIRE_TO_GATE MVP 规格与实施交接》的真实批准。

### Key evidence

- [WIRE_TO_GATE 单场景 MVP 与双仓库协作路线图](../map.md)及已解决的[决定单 Demand 选择、并发与等待策略](03-decide-single-demand-selection-concurrency-and-waiting-policy.md)、[决定机台取货、多仓装货、关卡卸货与成功边界](04-decide-pickup-loading-gate-unloading-and-success-boundary.md)、[决定 MVP 多仓容量、安全联锁与异常恢复最小集](05-decide-minimum-multislot-safety-and-recovery-set.md)、[决定 MVP RIoT 移动、建单对账与人工充电边界](06-decide-riot-movement-order-reconciliation-and-manual-charging-boundary.md)、[验证 OnboardHmi 单场景操作原型](08-validate-onboard-single-scenario-interaction-prototype.md)、[决定共享协议仓库的发布内容与变更治理](09-decide-shared-protocol-repository-release-and-change-governance.md)及[决定双仓库一致性门禁、模拟对端与联调切片](10-decide-cross-repository-conformance-harness-and-integration-slices.md)。
- [`CONTEXT.md`](../../../CONTEXT.md)中的 VehicleCredential、ProtocolReleaseIdentity、ConformanceRunIdentity、RIoTOnlyVehicleControlBoundary、MapStationCatalogSnapshot、AreaNamedMachineStation、FixedTaskStation、StationOperationArrivalGate、DetectableLoadConstraint、CurrentMesReadOnlyBoundary 和 TransportDemandCompletion。
- [`ADR-cross-0003`](../../../docs/adr/cross/0003-onboard-disconnect-safe-finish-and-server-resume.md)、[`ADR-cross-0004`](../../../docs/adr/cross/0004-onboard-hmi-exclusive-io-authority.md)、[`ADR-cross-0009`](../../../docs/adr/cross/0009-fresh-safety-check-before-each-movement.md)、[`ADR-cross-0014`](../../../docs/adr/cross/0014-durable-command-acceptance-and-same-operation-reconciliation.md)、[`ADR-cross-0018`](../../../docs/adr/cross/0018-project-wide-operator-verification-enabled.md)、[`ADR-cross-0019`](../../../docs/adr/cross/0019-onboard-technical-logs-server-business-audit.md)、[`ADR-cross-0024`](../../../docs/adr/cross/0024-per-agv-connection-credential.md)、[`ADR-cross-0025`](../../../docs/adr/cross/0025-pinned-self-signed-tls-and-per-agv-secret.md)、[`ADR-cross-0028`](../../../docs/adr/cross/0028-connected-session-requires-explicit-business-readiness.md)、[`ADR-cross-0029`](../../../docs/adr/cross/0029-unified-five-step-recovery-handshake.md)、[`ADR-cross-0035`](../../../docs/adr/cross/0035-server-orders-slots-onboard-executes-array-order.md)、[`ADR-cross-0040`](../../../docs/adr/cross/0040-internal-light-curtain-is-slot-occupancy-evidence.md)及 [`ADR-cross-0053`](../../../docs/adr/cross/0053-onboard-upcoming-stop-plan-and-vehicle-overview.md)。
