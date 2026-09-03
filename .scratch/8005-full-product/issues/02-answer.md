# 票 02 决议：五条架构不变量作为重构／增量判据，16 条重构、46 条增量

Resolved: 2026-09-03
Resolves: `02-classify-rearchitecture-versus-incremental-and-ordering-rule.md`

## 结论一句话

**重构类不是「全新能力」，而是「推翻五条现行架构不变量之一」。**按此判据，AGV 主项目
62 条中 **16 条重构、46 条增量**；两类**不采用整体先后**，改用「每条增量不早于它所依赖
的那条不变量的推翻」；重构内部顺序为 **`B2 → (B1+B4 一起) → B3 → B5`**；**多车本身
不进协议 v2 冻结**，进 v2 的是 B3、B5、充电与等待点带来的 schema 变更。

用户 2026-09-03 对本票五个问题全部按推荐值批准。

## 判据：五条架构不变量

判据不是主观的「是否触及核心」。它是五条**有代码或契约位置**的现行不变量，逐条可复核，
且判定不依赖顺序（一个条目属哪一类是它的内在性质，不因先做后做而变）。

| 编号 | 不变量 | 现行证据 |
| --- | --- | --- |
| **I1** | 车辆占用必由一条 TransportDemand 引起 | `VehicleDispatchLeaseRow` 主键为 `DemandId`，`VehicleKey` 上过滤唯一索引 `ReleasedAt IS NULL`（`8005-agv-control-server/src/ControlServer.Infrastructure/Persistence/ControlServerDbContext.cs:44`）；获取路径 `WireToGateStore.cs:255-309` 在同一事务内查租约→建 Demand→建租约→建 OrderIntent |
| **I2** | 全系统至多一辆车、至多一条未收敛 journey | `JourneyRuntimeEngine.cs:84` `active.Length > 1` 抛 `BusinessIdentityConflictException`，`:108` 直接取 `active[0]`；车辆身份是 `JourneyRuntimeOptions.AgvId`／`VehicleKey` 标量（`JourneyRuntimeOptions.cs:11-12`）；选 Demand 排序键 `FirstSeenAt→CreatedAt→DemandId` **无任何车辆维度**（`JourneyRuntimeEngine.cs:297-301`）；数据库 37 个 `DbSet` 中**没有车辆注册表** |
| **I3** | 一次承诺 = 一条 Demand + 固定两段行程 | `JourneyRuntimeEngine.cs:1222-1228` 的 `Worklist(...)` 恒构造单元素数组；协议 `UpcomingStopPlanSnapshot.legs` `maxItems: 2`、`sequence` `maximum: 2`、`legType` enum 仅 `TO_PICKUP`／`TO_GATE`；`CurrentStopWorklistSnapshot.items` `maxItems: 1`、`stopRole` enum 仅 `PICKUP`／`GATE` |
| **I4** | 站点没有独占概念 | 固定站点只有 `gateStationId`／`gateStationRiotId`，pickup 站是运行期从 RIoT Map 目录按 AREA 解析（`MapStationResolver.cs`）；无充电桩表、无等待点、无站点级独占或预占 |
| **I5** | 车载对 Demand 是只读投影，绝不发现、选择或绑定 | `8005-agv-protocol/integration-slices/index.json:65` `NEVER_DISCOVER_SELECT_OR_BIND_DEMAND`；`:52` `onboardMode: "READ_ONLY_COMMITTED_PROJECTION"`；`vectors/CV-DEMAND-ACCEPT-TO-PICKUP/expected.json:19-21` 把 `onboard-demand-selection`／`onboard-demand-binding`／`onboard-mesingest-read` 列为 forbidden side effects；`tools/g1-validate.mjs:25` 断言 worklist 至多一条已承诺 Demand |

**重构判据 B1～B5：条目的实现要求推翻 I1～I5 中任一条，即为重构。**

- **B1** 车辆占用脱离 Demand —— 条目要求车辆被占用而不存在对应 TransportDemand。
- **B2** 车辆集合语义 —— 条目的判定结果依赖「存在多辆车」：在车辆之间排序、仲裁、改选，或要求并行的未收敛 journey。
- **B3** 计划形状 —— 条目要求一次承诺承载多条 Demand、超过两段行程，或允许已承诺计划被变更。
- **B4** 站点独占 —— 条目要求某站点在同一时刻只能被一辆车占用或预占。
- **B5** 车载选择 Demand —— 条目要求车载端产生对 Demand 的发现、选择或绑定。

**增量判据：五条都不推翻。**合法形态只有两种——（a）在 `ValidateDynamicFacts` 的
fail-closed 资格链上增加一个可独立求值的谓词（该链现有 11 个原因码，
`JourneyRuntimeEngine.cs:547-570`，是 append-only 的，加一条不改既有语义）；
（b）在核心之外新增表、审计、UI 或配置版本。

### 判据的代价，须明说

**这个判据会把大量「全新能力」判成增量。**充电 17 条里 13 条是增量，因为它们建立在
B4／B1 新建的原语之上，本身不推翻任何既有前提。如果期望的分类是「新能力 vs 已有能力的
扩展」，本判据给不出那个结果——但那个分类对排序没有指导价值，而本判据有：**它把「必须
先动的架构原语」压缩成 16 条，其余 46 条各自挂在它依赖的原语后面。**

### I5 是本票新增的第五条

票 02 正文只提到「ControlServer 选择与分配核心」。`REQ-0212`／`REQ-0214` 推翻的不是服务端
核心，而是**跨端只读投影契约**——那是唯一必须 Kun Wang 同步参与的一项。漏掉 I5 会让票 03
低估协作成本，也会让票 06 漏掉 `W2G-IS-01` 的 `definition` 与 forbidden side effects 需要
改动这件事。

## 逐问回答

### 问 1：每一簇归重构还是增量

**16 重构 / 46 增量。**逐条见下节表格，无未判定项。簇级汇总：

| 簇 | 总数 | 重构 | 增量 | 重构条目 |
| --- | --- | --- | --- | --- |
| FP-C1 自动充电桩调度与充电失败治理 | 17 | **4** | 13 | `REQ-0170` B4、`REQ-0172` B2、`REQ-0173` B1+B4、`REQ-0178` B2+B4 |
| FP-C2 多车与多任务调度 | 10 | **7** | 3 | `REQ-0189`／`0195`／`0196`／`0197`／`0198` B3、`REQ-0206`／`0328` B2 |
| FP-C3 车载 Worklist 选任务模式 | 6 | **2** | 4 | `REQ-0212`／`0214` B5 |
| FP-C4 空闲返回与等待点 | 8 | **3** | 5 | `REQ-0292` B1+B4、`REQ-0293` B4、`REQ-0294` B1 |
| FP-C5 AGV 归档恢复与身份连续性 | 6 | 0 | 6 | — |
| FP-C6 账号权限与密码治理 | 8 | 0 | 8 | — |
| FP-C7 配置生效治理与回滚 | 6 | 0 | 6 | — |
| FP-C8 看板与观测 | 1 | 0 | 1 | — |
| **合计** | **62** | **16** | **46** | |

票 02 正文点名的三处争议，判定结果：

- **空闲返回与等待点那 8 条**（`REQ-0289`～`0297`）——**争议成立，其中 3 条是重构**。
  `REQ-0292` 明文要求「基于同一份新鲜快照同时取得该车的 IDLE_RETURN `VehiclePurposeClaim`
  和具体等待点的 `WaitingPointExclusiveClaim`」，同时命中 B1 与 B4；`REQ-0293` 的连续单车
  独占命中 B4；`REQ-0294` 的空闲返回订单占用车辆而无 Demand，命中 B1。其余 5 条是增量。
- **车载 Worklist 那 6 条**（`REQ-0212`～`0220`）——**争议成立，其中 2 条是重构，但推翻的
  不是分配核心而是 I5 跨端契约**。`REQ-0212` 引入 `LoadTaskEntryMode` 与
  `WORKLIST_SELECTION` 能力，`REQ-0214` 定义车载从 worklist 选待装 `DemandId`，两条都命中
  B5。`REQ-0217`（禁止一点即开门）规定的是车载 UI 交互，`REQ-0219`（责任划分）与
  `REQ-0220`（审计）是 B5 之上的规则，三条均为增量。`REQ-0215`（模式按装货开始边界冻结）
  是配置版本语义，增量。
- **AGV 生命周期与归档恢复那 8 条**——**争议不成立，全部增量**。`REQ-0288` 已由票 01 移入
  FP-C1（讲的是充电桩不是车辆），`REQ-0287` 同理。剩下的 `REQ-0310`／`0311`／`0316`／
  `0317`／`0318`／`0320` 只在核心之外新增生命周期状态、权限与审计；`REQ-0317`
  （恢复后 `Disabled` 且 `VehicleBusinessReadiness = false`）是往资格链加一个谓词，
  不改任何不变量。**注意它们对 B2 是软依赖而非推翻**：单车系统里归档唯一一辆车等于停机，
  归档恢复要有运维意义须先有多车，但这是价值上的依赖，不是技术上的推翻。

### 问 2：两类的排序规则

**不采用「重构类整体先于增量类」。规则是：每条增量条目不早于它所依赖的那条不变量的推翻。**

理由是 46 条增量里有 **21 条（FP-C5 6 + FP-C6 8 + FP-C7 6 + FP-C8 1）完全不依赖任何不变量**
——它们只在核心之外新增表、审计、UI 与配置版本，而 `ValidateDynamicFacts` 的资格链是
append-only 的。让这 21 条等重构做完是白等，而它们恰好是最不需要现场车的部分，在一周
日历里是唯一能真正并行的一块。整体先后规则会把它锁死。

**可以并行或提前的增量（23 条）：**

| 条目 | 依赖 | 说明 |
| --- | --- | --- |
| FP-C5 全部 6 条 | 无 | 核心外的生命周期与审计 |
| FP-C6 全部 8 条 | 无 | 账号权限，完全在核心外 |
| FP-C7 全部 6 条 | 无 | 配置版本与激活治理 |
| FP-C8 `REQ-0268` | 无 | 看板从 ControlServer 取数，不走车载协议 |
| `REQ-0185` | 无 | 排除区域列表，单车下即可实现并验收 |
| `REQ-0202` | 无 | 只是把 FIFO 排序键换成优先级带，不改判定形状 |

**不得提前的增量（23 条）：**

| 条目 | 依赖 |
| --- | --- |
| FP-C1 的 13 条增量 | B4 + B1（充电周期本身） |
| FP-C4 的 5 条增量 | B1 + B4 |
| FP-C3 的 4 条增量 | B5 |
| `REQ-0203` | B2 —— 标定须报告「采样期车辆数」与完整周期分布，要 N 车现场数据 |

两条**数据前置**，无不变量依赖但有簇内次序：`REQ-0171`（独占充电桩名册）须先于
`REQ-0170`（候选集必须是名册子集）；`REQ-0289`（专用等待点登记）须先于 `REQ-0293`
（等待点独占）。两条都可以在重构开工前先做。

### 问 3：重构类内部顺序

**`B2 → (B1 + B4 一起) → B3 → B5`。**

先纠正票 02 正文推敲的方向。正文问的是「多车并发是否必须先于充电桩调度」，因为
「充电排队与待充电集合本身就是多车语义」，并注意到 3 车 3 桩使这个依赖变弱。
**查下来这个问题问偏了——充电真正依赖的是等待点，不是多车调度。**`REQ-0178` 明文：

> 正常任务完成、充电完成和充电失败共用地图等待点集合；即使当前只有一个点也按集合建模，
> 只选当前地图上身份有效、路线可达且未被占用或预占的点，多车原子预占。

清桩必须把车开到等待点。因此 **FP-C1 不能排在 FP-C4 之前**，与正文的假设相反。3 车 3 桩
使排队不触发这一点仍然成立，但它削弱的是 `REQ-0172`／`REQ-0173` 的现场可观测性
（验收问题，归票 08），不改变 C1 对 C4 的结构依赖。

四段顺序的理由：

1. **B2 最小，且是其余三项的语义前提。**改动是：`JourneyRuntimeOptions` 的标量车辆字段
   改成 N 车配置、拆掉 `JourneyRuntimeEngine.cs:84` 的 `active.Length > 1` 断言、给
   `:297-301` 的排序键加车辆维度。持久化层不必动——租约本来就按 `VehicleKey` 分行、
   `VehicleKey` 上就有过滤唯一索引，**单车假设集中在 Host 层两个文件约 1443 行**。
   B1／B3／B4 的价值与测试都只在多车下成立。
2. **B1 与 B4 必须一起做。**`REQ-0292` 要求「基于同一份新鲜快照同时取得」车辆
   `VehiclePurposeClaim` 与站点 `WaitingPointExclusiveClaim`，「任一取得失败都不形成承诺」。
   拆开做会造出一个能取得车辆而拿不到站点的中间态，那正是这条要禁止的。
3. **B3 改动量最大且是 B5 的前提。**它同时动 `JourneyExecutionPlan`、`JourneyRuntimeStage`
   状态机（现 8 个值，无空闲态）与五处协议硬约束。worklist 只有一项时「选任务」无意义，
   所以 B5 必须在 B3 之后。
4. **B5 最后**，因为它是唯一必须 Kun Wang 同步参与的一项，把它放在最后可以让前三项的
   服务端工作不被跨端评审节奏阻塞。

**B2 在 348 条里没有需求条目载体，这一点票 09 必须知道。**348 条中**没有任何一条要求
「系统支持多辆车」**。多车是现场 3 车的事实，加上 `REQ-0259`（新 AGV 先登记后投运）、
`REQ-0190`（`VehicleTaskTypeAdmission` 按 `agvId + taskType`）、`REQ-0194`
（`DispatchZoneVehicleAdmission`）三条**批次 0 已实施**的配置能力的结果。因此 B2 在
348 行剖面里不产生新行，但它是一项真实的工程任务，票 09 必须在批次里单列，不能因为
「没有对应需求」而遗漏。

### 问 4：判定结果对协议的含义

**「是否改协议」与「重构／增量」是两条正交的轴。**FP-C3 是增量却必改协议；B2 是重构
却不必改协议。票 06 须按协议轴取条目，不能按重构／增量轴取。

一条支配性事实：**协议没有任何可选字段**——`compatibility/report.json:11`：

> No optional payload fields exist in this candidate. Future optional fields require proof
> that omission and ignore preserve safety and business conclusions.

而 breaking 的定义包含 enum 与 meaning 变更——`docs/release-governance.md:11`：

> Required/type/enum/meaning/direction/delivery/dedup/persistence/recovery/error/side-effect
> changes are breaking and require a ProtocolVersion and release-major increase.

**因此任何需要新字段或新枚举值的条目都必须进 v2 冻结，没有「加个可选字段」这条路。**

**必须进票 06 的 v2 冻结：**

| 来源 | 具体变更 |
| --- | --- |
| **B3** | `UpcomingStopPlanSnapshot.legs` `maxItems: 2 → N`；`sequence` `maximum: 2 → N`；`legType` enum 加值；`CurrentStopWorklistSnapshot.items` `maxItems: 1 → N`；`stopRole` enum 加值；`tools/g1-validate.mjs:25` 那条「worklist 至多一条已承诺 Demand」的 G1 断言须改 |
| **B5** | 新增车载→服务端的 Demand 选择消息与其响应；`W2G-IS-01` 的 `definition` 中 `onboardMode`／`ownerResponsibilities.onboardHmi` 须改；`CV-DEMAND-ACCEPT-TO-PICKUP` 的 forbidden side effects 须改 |
| **FP-C1 充电** | `legType` 加 `TO_CHARGING_STATION`；`VehicleBusinessStateSnapshot.manualChargingHold` 的含义从「人工挂起」变为自动充电周期状态，属 **meaning change**，即使字段名不变也是 breaking；`REQ-0176`／`REQ-0179` 的人工确认落在哪一端决定是否要新增消息（票 04／票 05 交接） |
| **FP-C4 等待点** | `legType` 加 `TO_WAITING_POINT` |

**不必进 v2 冻结：**

- **B2 多车本身。**协议 54 个消息**每一个**的信封都必填 `agvId`
  （`schemas/envelope.schema.json:44-50, 79`），且该字段无 `const`、无 `enum`、无 `pattern`。
  协议从未限制系统内车辆总数为 1，握手模型是「一条会话服务一台车」，三台车三条会话即可。
- FP-C5、FP-C6、FP-C8 —— 服务端与管理面，不经车载协议。

**额外点名给票 06 一条，否则会漏：**`REQ-0316` 要求恢复后车载上报的 `SlotModelVersion`、
IO 配置版本与指纹、以及完整 `OnboardCapabilitySnapshot` 与归档前记录**完全一致**。现有
`CapabilitySnapshot` 消息是否已覆盖这些字段须逐字段核对；**若需加字段，因无可选字段政策，
它同样是 breaking**。这是 FP-C5 唯一可能碰协议的地方。

## 逐条归属表（62 条，无未判定项）

`判定` 列：**R** = 重构，**I** = 增量。`命中／依赖` 列：重构条目写命中的判据，增量条目写
它不得早于哪条不变量的推翻（`—` 表示无依赖，可从第一天并行）。

| RequirementId | 簇 | 判定 | 命中／依赖 | 依据 |
| --- | --- | --- | --- | --- |
| `REQ-0170` | FP-C1 | **R** | B4 | 候选链要求站点「占用/预占状态可确认且当前空闲」，I4 下无此概念 |
| `REQ-0171` | FP-C1 | I | —（须先于 `REQ-0170`） | 名册是新配置表 + 一个「候选集是子集」的谓词 |
| `REQ-0172` | FP-C1 | **R** | B2 | 待充车辆进同一排队集合按电量排序，单车下不存在该集合 |
| `REQ-0173` | FP-C1 | **R** | B1 + B4 | 站点原子预占且不可抢占；充电占用车辆而无 Demand |
| `REQ-0174` | FP-C1 | I | B4 + B1 | 「已确认充不上」的事实构成，建立在充电周期之上 |
| `REQ-0175` | FP-C1 | I | B4 + B1 | 异常分支归类规则 |
| `REQ-0176` | FP-C1 | I | B4 + B1 | 现场确认权限 |
| `REQ-0177` | FP-C1 | I | B4 + B1 | 在已存在的站点候选链上加暂停谓词 |
| `REQ-0178` | FP-C1 | **R** | B2 + B4 | 清桩明文要求等待点集合 + 多车原子预占；**C1 对 C4 的结构依赖出处** |
| `REQ-0179` | FP-C1 | I | B4 + B1 | 清桩完成证明与权限 |
| `REQ-0180` | FP-C1 | I | B4 + B1 | 资格链谓词 |
| `REQ-0283` | FP-C1 | I | B4 + B1 | 明文继承既有 `RoutineOrderCreationCall`／`RIoTRetryReconciliation` |
| `REQ-0284` | FP-C1 | I | B4 + B1 | 重试次数策略 |
| `REQ-0285` | FP-C1 | I | B4 + B1 | 两个 Hold 都是新候选链上的谓词 |
| `REQ-0286` | FP-C1 | I | B4 + B1 | 归因规则，不改任何不变量 |
| `REQ-0287` | FP-C1 | I | B4 + B1 | 失联时保持既有预占，不改独占语义 |
| `REQ-0288` | FP-C1 | I | B4 + B1 | 暂停分配 + 保留名册身份 |
| `REQ-0185` | FP-C2 | I | — | 排除区域列表，纯谓词，单车下可验收 |
| `REQ-0189` | FP-C2 | **R** | B3 | 一辆 AGV 同时承载多个 Sublot 与多个独立 Demand |
| `REQ-0195` | FP-C2 | **R** | B3 | 同图跨区连续区段，行程超过固定两段 |
| `REQ-0196` | FP-C2 | **R** | B3 | 已承诺计划允许受控追加 |
| `REQ-0197` | FP-C2 | **R** | B3 | 后续停靠有界删除或换序 |
| `REQ-0198` | FP-C2 | **R** | B3 | 最大晚到量约束，预设多 Demand 可变更计划 |
| `REQ-0202` | FP-C2 | I | — | 只是把 FIFO 排序键换成优先级带 |
| `REQ-0203` | FP-C2 | I | B2 | 标定须报告采样期车辆数与完整周期分布 |
| `REQ-0206` | FP-C2 | **R** | B2 | `VehicleMarginalRouteCost` 要求在车辆之间比较 |
| `REQ-0328` | FP-C2 | **R** | B2 | 释放原车改选其它车辆，新 `DispatchGeneration` |
| `REQ-0212` | FP-C3 | **R** | B5 | 引入 `LoadTaskEntryMode` 与 `WORKLIST_SELECTION` 能力 |
| `REQ-0214` | FP-C3 | **R** | B5 | 车载从最新 worklist 选待装 `DemandId` |
| `REQ-0215` | FP-C3 | I | B5 | 配置版本按装货开始边界冻结 |
| `REQ-0217` | FP-C3 | I | B5 | 车载 UI 交互规则（归 Kun Wang 实现） |
| `REQ-0219` | FP-C3 | I | B5 | 责任按控制链划分 |
| `REQ-0220` | FP-C3 | I | B5 | `WorklistTaskSelection` 审计 |
| `REQ-0289` | FP-C4 | I | —（须先于 `REQ-0293`） | 专用等待点的登记规则与 `WaitingPointVehicleScope` |
| `REQ-0291` | FP-C4 | I | B1 | `IdleReturnEligibility` 是资格链谓词 |
| `REQ-0292` | FP-C4 | **R** | B1 + B4 | 同一快照原子取得 `VehiclePurposeClaim` + `WaitingPointExclusiveClaim` |
| `REQ-0293` | FP-C4 | **R** | B4 | 从在途预占到在点占用的连续单车独占 |
| `REQ-0294` | FP-C4 | **R** | B1 | 空闲返回订单占用车辆而无对应 Demand |
| `REQ-0295` | FP-C4 | I | B1 + B4 | 到点的一致证据组合 |
| `REQ-0296` | FP-C4 | I | B1 + B4 | 失败分流与释放边界 |
| `REQ-0297` | FP-C4 | I | B4 | 配置拓扑变化不破坏既有预占引用 |
| `REQ-0310` | FP-C5 | I | — | 恢复只能沿用原 `agvId` |
| `REQ-0311` | FP-C5 | I | — | 恢复权限只属系统管理员 |
| `REQ-0316` | FP-C5 | I | —（**唯一可能碰协议的 C5 条目**） | 归档前配置作为恢复候选，须核对车载上报字段 |
| `REQ-0317` | FP-C5 | I | — | 恢复与投运分离，往资格链加谓词 |
| `REQ-0318` | FP-C5 | I | — | 车辆离线时可先恢复档案 |
| `REQ-0320` | FP-C5 | I | — | 恢复尝试的不可改写审计 |
| `REQ-0236` | FP-C6 | I | — | 异常处置权限按个人授予 |
| `REQ-0254` | FP-C6 | I | — | 票据 62 的专门权限并入管理员角色 |
| `REQ-0256` | FP-C6 | I | — | 账号生命周期与立即撤权 |
| `REQ-0273` | FP-C6 | I | — | 不建立泄露找回或强制重置流程 |
| `REQ-0274` | FP-C6 | I | — | 密码只能由系统管理员设置 |
| `REQ-0275` | FP-C6 | I | — | 首次改密仅用于部署初始化 |
| `REQ-0277` | FP-C6 | I | — | 设置新密码不联动当前会话 |
| `REQ-0280` | FP-C6 | I | — | 密码设置沿用不可改写审计 |
| `REQ-0260` | FP-C7 | I | — | 模板资料变更与硬件配置变更分开治理 |
| `REQ-0261` | FP-C7 | I | — | 整车维护态是车辆级阻断谓词 |
| `REQ-0266` | FP-C7 | I | — | 配置审计可还原全过程 |
| `REQ-0326` | FP-C7 | I | — | 否定性需求：覆盖治理不属当前需求，维持不实施 |
| `REQ-0339` | FP-C7 | I | — | 敏感生效动作要求新鲜二次认证 |
| `REQ-0346` | FP-C7 | I | — | 回滚是受控的新激活 |
| `REQ-0268` | FP-C8 | I | — | 看板 2 秒刷新，数据来自 ControlServer，不走车载协议 |

计数核验：R = 16（C1 4 + C2 7 + C3 2 + C4 3）；I = 46（C1 13 + C2 3 + C3 4 + C4 5 +
C5 6 + C6 8 + C7 6 + C8 1）；合计 62，与票 01 底稿的 `FP-C*` 行数一致。

## 对其他票据的影响

1. **新增票 12「决定空闲返回与等待点的独占语义与范围」**，承载 B1 + B4 这对必须一起做的
   原语。它是 FP-C1 的前置（`REQ-0178`），塞进票 03 会让多车票同时背四条不变量，塞进
   票 04 会把 C1 的前置埋在 C1 内部、票 09 排批次时看不见。票 04 与票 06 增加对票 12 的
   阻塞。
2. **票 03** 的 FP-C4 归属问题已解决——8 条全部去票 12，票 03 不再涵盖。票 03 剩下承载
   B2、B3、B5 三条不变量与 FP-C2、FP-C3 共 16 条。
3. **票 04** 须知道 C1 对 C4 的结构依赖出自 `REQ-0178`，且 C1 的 4 条重构条目分别命中
   B4／B2／B1，其余 13 条是建在原语之上的增量。
4. **票 05** 的 FP-C5 归属问题已解决——6 条全部增量，全部留在票 05。另新增一条输入：
   `REQ-0316` 是 C5 唯一可能碰协议的条目。
5. **票 06** 收到明确的输入清单（见问 4 的两张表），并须知道 B2 不进 v2。
6. **票 09** 须单列 B2 这项无需求条目载体的工程任务，并按「每条增量不早于它所依赖的那条
   不变量的推翻」排批次，而非按重构／增量两大块排。
7. **票 08** 收到一条已知难题的出处：3 车 3 桩使 `REQ-0172`／`REQ-0173` 在现场不触发，
   但两条是重构类条目、必须实现，证据怎么取由票 08 判，不得默认「不触发即通过」。

## 未派生新需求

本票不新增、不修改、不废弃任何需求条目。五条不变量是对**现行实现与契约**的描述，不是
需求；B1～B5 是判据，不是需求。

---

## 2026-09-03 修订：票 13 补充识别第六条架构不变量 I6

本票当时识别了五条不变量（I1～I5），对应判据 B1～B5。**票 13 在判定 `STAGING_TO_WIRE`
方向反转时补充识别了第六条**：

**I6 — 站点任务类型准入必在装货腿检查并冻结。**代码强制点：`WireToGateStore.cs:795-800` 明文
`"Only LOAD may carry a complete station/task admission identity."`；准入决策快照只在 LOAD 路径
按 `SlotOperationAttemptId` 冻结（`WireToGateStore.cs:852-871`）；UNLOAD 发布不传准入参数
（`JourneyRuntimeEngine.cs:751-765`）。而 `StationTaskTypeAdmission` 的键是「站点 × 任务类型」，
站点侧取 MES AREA 机台站——`STAGING_TO_WIRE` 下 AREA 机台站是**卸货端**，准入该检查的那一腿
恰好是被禁止携带准入身份的那一腿。

**这不推翻本票的任何定案。**62 条的 16 重构 / 46 增量划分不变，排序规则不变，重构内部顺序
`B2 → (B1+B4) → B3 → B5` 不变。I6 影响的是票 13 新移出批次 0 的条目：`STAGING_TO_WIRE` 相关的
实施是**重构类**而非增量类，票 09 的排序须据此把它排在准入归属重做之后。

**方法论上值得记的一点**：`CONTEXT.md` 里 `AllocationArchitectureInvariant` 的原措辞是
「完整产品语境下**已识别**五条」，不是穷举封闭的表述，因此这是补充识别而非推翻。**这是本图第二次
发现本票的判据集不完整**——第一次是本票自己查出 B2（多车）在 348 条里没有需求条目载体。
后续票据遇到「某条新能力似乎要重做既有实现」时，应先检查它是否推翻了一条尚未列出的不变量，
而不是默认它是增量。`CONTEXT.md` 的词条已相应改为六条并加了这条提醒。

详见 [票 13 决议](13-answer.md) 的 Q6 与 `CONTEXT.md` 的 `LoadLegAdmissionBinding` 词条。
