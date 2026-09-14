# 调研：v2 线补齐多需求累积的差距——MVP 线实现与旧规格批次 6 逐项对照

- 承接票：[program#67](https://github.com/trytoreachpeak0/8005-agv-program/issues/67)（地图 [#64](https://github.com/trytoreachpeak0/8005-agv-program/issues/64)），关联审计 [program#61](https://github.com/trytoreachpeak0/8005-agv-program/issues/61)
- 调研日期：2026-09-14。**只查事实，不做决定。**
- 做法：只读 git ref（`git show`／`git grep`／`git log`／`git diff --stat`），没有 checkout、编译或跑测试，没有连现场机器、SSH 或 RIoT。

## 0. 口径与引用写法

| 简称 | ref | 提交 |
| --- | --- | --- |
| `MVP` | `8005-agv-control-server` 的 `origin/ControlServer_MVP` | `6a8a688c`（2026-09-13） |
| `v2` | `8005-agv-control-server` 的 `origin/fp/v2-impl` | `d39983d7`（2026-09-14；#61 审计时是 `2b2aa51c`，之后又前进了） |
| `base` | 两线分叉点 `git merge-base` | `75ea9f60` |
| `main` | `8005-agv-program` 的 `origin/main` | `d0eaf5d5` |

引用写成 `ref:路径:行`。下面几个路径用简称：

| 简称 | 全路径 |
| --- | --- |
| `Engine` | `src/ControlServer.Host/Runtime/JourneyRuntimeEngine.cs` |
| `Options` | `src/ControlServer.Host/Runtime/JourneyRuntimeOptions.cs` |
| `Store` | `src/ControlServer.Infrastructure/Persistence/WireToGateStore.cs` |
| `DbContext` | `src/ControlServer.Infrastructure/Persistence/ControlServerDbContext.cs` |
| `Cfg/` | `src/ControlServer.Infrastructure/Persistence/Configurations/` |
| `appsettings` | `src/ControlServer.Host/appsettings.json` |
| `Spec` | `main:.scratch/8005-full-product/full-product-scope-and-sequence-specification.md` |
| `TSV` | `main:.scratch/8005-full-product/evidence/full-product-implementation-profile-draft.tsv`（行号含表头，第 10 列 `Batch`） |
| `Req` | `main:requirements/baselines/current-requirements-v1.1.0.md` |
| `T03`／`T12`／`T14` | `main:.scratch/8005-full-product/issues/03-answer.md`／`12-answer.md`／`14-answer.md` |
| `ADR0057` | `main:docs/adr/cross/0057-multi-demand-journey-departs-on-full-or-holding-timeout.md` |

形态三档：**完整**＝需求文本要求的行为在 MVP 上都有载体；**退化**＝有载体，但只在单车、单分区或单任务类型下成立，或缺需求点名的门禁；**未实现**＝需求点名的标识符或行为在 `MVP` 的 `src/` 里零命中。

---

## 1. 问题 1：MVP 线实现了批次 6 的哪些条目、以什么形态

### 1.1 结论

`TSV` 里 `Batch=BATCH-6` 共 17 行（`Spec:201` 记「`FP-C2` 其余 17」）。对照 `MVP`：

- **完整 3 条**：`REQ-0155`、`REQ-0156`、`REQ-0211`（限 `WIRE_TO_GATE` 一类，`REQ-0211` 有一处未复核）。
- **退化 6 条**：`REQ-0189`、`REQ-0195`、`REQ-0196`、`REQ-0197`、`REQ-0205`、`REQ-0208`。
- **未实现 8 条**：`REQ-0185`、`REQ-0198`、`REQ-0201`、`REQ-0202`、`REQ-0203`、`REQ-0206`、`REQ-0210`、`REQ-0328`。

票里点名的 `REQ-0200` 在 `TSV:201` 标的是 `BATCH-0`，不属于批次 6，另附一行。

`TSV` 的 `Batch0FormNote` 在 `REQ-0155`（`TSV:156`）写的是「`TransportDemandSuppression` 零命中」。那是对分叉前服务端的判断。`MVP` 已由 `557644a6` 实现，`v2` 仍然零命中。

### 1.2 逐条表

| REQ | 标题（`Req` 摘要） | TSV 行 | MVP 形态 | 事实 | 证据 |
| --- | --- | --- | --- | --- | --- |
| `REQ-0155` | 取消终态挂 DemandId，禁止再执行挂 TransportDemandKey | 156 | **完整** | 抑制表以 `TransportDemandKey` 为主键；候选评分命中即判 `TRANSPORT_DEMAND_SUPPRESSED`，新 DemandId 回来也挡得住 | `MVP:Cfg/TransportDemandSuppressionRowConfiguration.cs:11`；`MVP:Engine:312-313,346`；`MVP:Store:1224-1257`；提交 `557644a6`；`Req:8966` |
| `REQ-0156` | 抑制只由本地取消产生 | 157 | **完整** | 只有抑制类理由码能写入，其他码直接抛异常。`MVP` 写 5 个码，比基线列的 4 个多一个 `TERMINATED_BY_FAULT_CARGO_HANDOFF`。`MES_DISAPPEARED`／`GONE` 不写 | `MVP:Store:1210-1211,1231-1235`；`557644a6` 提交说明；`ADR0057:88-93`；`Req:9024` |
| `REQ-0185` | 共晶与低温共晶在选任务阶段排除 | 186 | **未实现** | `TransportExecutionExcludedArea` 在 `MVP` 的 `src/` 零命中 | `git grep` `MVP -- src`；`Req:10706` |
| `REQ-0189` | 多 Sublot 不合并 Demand | 190 | **退化** | 一趟旅程挂多条 `JourneyDemands`，每条有自己的状态、预留仓位、装卸命令与 attempt。但任务类型写死 `WIRE_TO_GATE`，`SublotTaskTypeConflict` 零命中，「同 Sublot 多任务类型阻断」没有载体 | `MVP:DbContext:535-563`；`MVP:Cfg/JourneyDemandRowConfiguration.cs:12-15`；`MVP:Engine:348-349`；`Req:10938` |
| `REQ-0195` | 同图跨区允许，不得往返摆动 | 196 | **退化** | 每条候选的分区都取配置里唯一的 `runtimeOptions.DispatchZone`，`allowedDispatchZones` 只有一个值。不存在 A→B→A，所以代码里没有连续性检查 | `MVP:Engine:385`；`MVP:Engine:907-908`；`MVP:appsettings:55,66`；`Req:11286` |
| `REQ-0196` | 执行途中只允许受控追加 | 197 | **退化** | 吸收只发生在装货阶段的停靠上（车刚到站、每个 LoadBatch 闭环后），行驶中不吸收，所以不会改动「当前下一站」。`LoadingClosedReason` 一旦有值就停止吸收。复用首次派车的评分与抑制表，但 `EnRoutePickupDeliveryDelay`、`VehicleTaskTypeAdmission` 零命中，没有分区连续性门禁 | `MVP:Engine:549,666,735`；`MVP:Engine:2691-2714`（`FillJourneyAsync`）；`MVP:Engine:2729-2821`（`TryTakeOnMoreCargoAsync`，`:2739` 停止条件）；`18a7e6ad`；`Req:11344` |
| `REQ-0197` | 后续停靠可以有界删除或换序 | 198 | **退化** | **换序没有**：追加停靠一律取当前最大取货序号 +1，关卡序号固定为 9。**删除是隐式的**：没有待装需求的停靠直接跳过；操作员在别的停靠录入范围内 SUBLOT 时，需求改挂到当前停靠，原停靠从计划投影里消失。「已装车的不丢」成立。持货超时会把未开装的需求终结为 `CANCELLED_BY_STOP_COMPLETE`。没有分区连续性和延迟保护 | `MVP:Engine:84-93`；`MVP:Engine:2785-2794`；`MVP:Engine:2859-2864`；`MVP:Engine:2627-2630,2841-2857`；`18a7e6ad` 提交说明第 4 点；`Req:11402` |
| `REQ-0198` | 顺路取货按既有 Demand 最大晚到量约束 | 199 | **未实现** | `EnRoutePickupDeliveryDelay` 零命中。`HoldingTimeout`（30 分钟）是另一条规则：整趟车从第一个 LoadBatch 安全闭环起的持货上限，不是逐条需求的晚到增量 | `MVP:Options:63-75`；`MVP:Engine:730,2677-2680`；`Req:11460` |
| `REQ-0201` | 任务年龄只用本地连续等待时间 | 202 | **未实现** | `TransportDemandWaitingAge`／`WaitingAge` 零命中。排序键是 `JourneyBacklog.FirstSeenAt` → `Snapshot.CreatedAt` → `DemandId` | `MVP:Engine:252-256`；`Req:11634` |
| `REQ-0202` | 任务类型初始优先级带 | 203 | **未实现** | 只受理 `WIRE_TO_GATE`，没有带 | `MVP:Engine:128,348-349`；`Req:11692` |
| `REQ-0203` | 防饥饿阈值按 DispatchZone 标定 | 204 | **未实现** | 没有等待年龄，也没有升级层 | 同上；`Req:11750` |
| `REQ-0205` | 空闲车与可合法追加的在途车共同竞争 | 206 | **退化** | 运行时是单车：存在两条以上未结旅程直接抛 `BusinessIdentityConflictException`。有在途旅程时只把候选吸收进这一趟，没有旅程时才新派车，不存在竞争对象。`VehicleTaskTypeAdmission`／`EnRoutePickupDeliveryDelay` 零命中 | `MVP:Engine:133-165`（`:137-140` 断言）；`Req:11866` |
| `REQ-0206` | 车辆主要按新增行程成本比较 | 207 | **未实现** | `VehicleMarginalRouteCost` 零命中，没有路网成本。`v2` 已有批次 2 轨 B 的 `RouteGraphCostRanker`，但不在 MVP 线 | `git grep` 两线；`v2:src/ControlServer.Host/Runtime/Dispatch/RouteGraphCostRanker.cs`；`Req:11924` |
| `REQ-0208` | 电量和仓位首先是硬资格 | 209 | **退化** | 电量比的是**当前值**与 `MinimumBatteryPercent`，不是「预计完成任务后的余量」。低于充电触发线判 `BATTERY_CHARGE_REQUIRED`，在充且未到恢复线判 `BATTERY_POLICY_NOT_SATISFIED`。仓位由服务端账本减去本趟已预留仓位，装不下下一个候选即记 `VEHICLE_FULL` | `MVP:Engine:928-947`；`MVP:Engine:2744-2759`；`TSV:209` 的 `Batch0FormNote`；`Req:12040` |
| `REQ-0210` | 正常积压与结构性无解分别升级 | 211 | **未实现** | `StructuralDispatchBlock` 在 `MVP` 零命中，只有逐候选的 `JourneyBacklog.ReasonCode`，没有分级告警（`v2` 的 `src/ControlServer.Host/Runtime/CreateGate/PreCreateGate.cs:30-33` 以常量 `CREATE_GATE_FROZEN_STATION_ABSENT` 承接 `REQ-0308` 的一种情形） | `MVP:Store:461-469`；`MVP:Engine:258-264`；`Req:12156` |
| `REQ-0211` | 同站取消沿用 DemandId 与永久抑制 | 212 | **完整**（一处未复核） | 装货前取消与装货中取消都终结为 `CANCELLED_BY_OPERATOR`，同时写抑制。多需求旅程里取消其中一条后，本站按批次收尾，其他需求照走。**未复核**：`ADR0057:94-95` 记「装货前取消走 `LoadCancellationResult` 空范围」当时未实现；车载端 `8888811` 之后实现了授权即终结（#61 §2），本调研没有逐行核对两端现状 | `MVP:Store:1269`（`CancelDemandBeforeLoadAsync`）；`MVP:Engine:655-682`；提交 `80f6b93d`、`946d460d`、`8be28b1c`；`Req:12214` |
| `REQ-0328` | 当前车不合格时释放并改派 | 329 | **未实现** | 单车，没有改派路径 | `MVP:Engine:137-140`；`Req:19000` |
| `REQ-0200`（附，`BATCH-0`） | 任务优先的分层字典序 | 201 | **退化** | 首次派车按任务稳定排序取第一条。单车下「先选任务再选车」与「先选车再选任务」分不出来。**吸收时车已固定**：先按这趟车剩余仓位评分，再从装得下的候选里取第一条 | `MVP:Engine:252-256`；`MVP:Engine:2744-2780`；`Req:11576` |

### 1.3 不变量 I3「单 Demand 两段固定行程」在 MVP 线上怎么绕开的

`Spec:369` 把 I3 列为 B3 的判据，批次 6 推翻它。`MVP` 没按规格顺序走，直接改了 I3 的代码载体：

1. **原载体**：`JourneyRuntimeRow` 以 `DemandId` 为主键，取货与关卡各有一组写死的列。`v2` 至今仍是这个形状：`v2:DbContext:143` `HasKey(row => row.DemandId)`，`v2:DbContext:556-605` 有 `PickupStationId`、`PickupMovementLegId`、`GateMovementLegId` 等固定列。
2. **`663f275a`（2026-09-08）拆成三张表**：
   - `JourneyRuntimes`：主键换成 `JourneyId`（`MVP:Cfg/JourneyRuntimeRowConfiguration.cs:10`），加了 `CurrentStopSequence`、`NextStopSequence`、`HoldingStartedAt`、`LoadingClosedReason`（`MVP:DbContext:435-482`）。
   - `JourneyStops`：主键 `(JourneyId, Sequence)`（`MVP:Cfg/JourneyStopRowConfiguration.cs:10`）。
   - `JourneyDemands`：主键 `(JourneyId, DemandId)`，`DemandId` 另有唯一索引（`MVP:Cfg/JourneyDemandRowConfiguration.cs:12-13`）。
   - 迁移 `20260908042817_MultiDemandJourneyStopSequence` 是手写的。提交说明写明它拒绝在有在途旅程时执行。
3. **旅程有了自己的身份**：由发起它的需求确定性派生，`StableGuid(demandId, "journey-{DispatchGeneration}")`（`MVP:Engine:2057`）。`OperationSessionId` 按旅程派生（`MVP:Engine:2068`）。
4. **状态机沿用 8 个 stage，改由停靠序号驱动**：`AwaitingPickupArrival` 变成「每到一个取货停靠一次」（`MVP:Engine:491,534-555,814-822`）。取货停靠占序号 1..8，关卡固定为 9（`MVP:Engine:84-93`）。
5. **车辆租约键改成旅程**：`VehicleDispatchLeases` 主键从 `DemandId` 换成 `JourneyId`，但**保留** `VehicleKey` 过滤唯一索引 `ReleasedAt IS NULL`（`MVP:Cfg/VehicleDispatchLeaseRowConfiguration.cs:10-14`）。所以「一车同时只有一趟未结旅程」这条 I2 仍由索引与引擎断言（`MVP:Engine:137-140`）共同保证，多需求靠「一趟装多条」实现，不需要一车多租约。
6. **`18a7e6ad` 补上运行中吸收**：`JoinJourneyAsync` 把需求挂进在途旅程，必要时追加停靠。它**不取租约、不建移动意图**，下一段腿在离站时才授权（`MVP:src/ControlServer.Application/DemandStorePorts.cs:21-32`；`MVP:Store:373-470`）。
7. **离站规则来自 ADR-cross-0057**：装满（`VEHICLE_FULL`）或持货 30 分钟（`HOLDING_TIMEOUT`）先到者结束装货阶段，普通情形记 `NO_FURTHER_CARGO`（`MVP:Engine:2660-2680,2758,2870`；`ADR0057:24-32`）。
8. **协议面同时放开**：`MVP` pin 在 `protocol-v0.3.0`，profile `WIRE_TO_GATE_MVP`、`protocolVersion` 3（`MVP:appsettings:2-11`）。录入范围改成集合 `expectedSublots`（`MVP:src/ControlServer.Host/Transport/OnboardJourneyPublisher.cs:137`）。`ADR0057:67-73` 记这是一次 breaking 协议发布。

**与规格硬链的关系**：`Spec:311` 定「严格串行的只有 `2轨B → 5 → 6 → 7`」。`MVP` 在没有 B2（多车）、B1（`VehiclePurposeClaims`）、B4（站点独占）的情况下推翻了 I3。它之所以不需要前三者，是因为保留了单车（I2），也没有统一的用途占有（见 2.2 第 1、3 行）。

---

## 2. 问题 2：MVP 线实现与批次 5、批次 6 定案是同形还是冲突

### 2.1 结论

**方向一致，数据模型与多个定案点不同形。**一致的是「一趟计划承载多个停靠、每个停靠多条 Demand、计划上限 8+1」。不同形的有 7 处：租约与唯一性、充电占用载体、停靠目的类别、`OperationSession` 粒度、推进模型（单车）、换序与停靠主键、协议腿类型与录入范围。离站规则（ADR-cross-0057）在规格与需求基线里都没有对应条目。

是否「推倒重来」属于决定，本文不下。下表只列每个定案点两边的形态和出处。

### 2.2 逐项对照

| # | 定案项 | 定案出处与内容 | MVP 形态 | 关系 |
| --- | --- | --- | --- | --- |
| 1 | B1 车辆占用载体 | `T12` Q3（`:184-208`）、`Spec:495-499`：新建 `VehiclePurposeClaims`，主键 `VehicleKey`，`Purpose` 四值（`TRANSPORT`／`CHARGING`／`CLEARING_MAINTENANCE`／`IDLE_RETURN`），**取代** `VehicleDispatchLeases` | 保留 `VehicleDispatchLeases`，主键 `JourneyId`，`VehicleKey` 过滤唯一（`MVP:Cfg/VehicleDispatchLeaseRowConfiguration.cs:10-14`）。充电用独立表 `AutoChargingRuns`（`MVP:DbContext:593-608`），与搬运的互斥靠引擎控制流：没有在途旅程时才轮到充电（`MVP:Engine:141-161`），电量低于触发线时拒单（`:945-947`）。充电腿借 `OrderIntent` 的 DemandId 位写 `CHARGE-{id}` 标记（`:1964-1980`） | **不同形** |
| 2 | 唯一性放在哪一层 | `T03` Q7（`:156-172`）：**删除** lease 表的 `VehicleKey` 过滤唯一索引，改在 `OrderIntents` 上按车建。`T12:318` 补充：用途层由 `VehiclePurposeClaims` 承担 | 索引保留，多需求靠旅程分组，不靠删索引 | **不同形** |
| 3 | 停靠目的类别 | `T12` Q5（`:237-262`）、`Spec:496-497`：充电与等待点**作为停靠进入计划**，停靠加 `StopPurposeCategory`（`BUSINESS`／`WAITING_POINT`／`CHARGER`） | 停靠只有 `Role` Pickup／Gate 与 `LegType` `TO_PICKUP`／`TO_GATE`（`MVP:DbContext:490-528`）。充电不在旅程计划里，是一条独立的 `TO_CHARGER` 移动。`v2` 已按定案对外发 `StopPurposeCategory`，常量 `BUSINESS`（`v2:src/ControlServer.Domain/WireToGateModels.cs:134`；`v2:Engine:1719-1727`） | **冲突** |
| 4 | B4 站点独占 | `T12` Q4（`:209-236`）：`(MapId, StationId)` 复合键、一行两状态 | 无（单车不需要） | 无对应 |
| 5 | 多车推进模型 | `T03` Q7 与 `Spec:417-421`：单 worker 按车串行，每车超时预算 | 单车断言（`MVP:Engine:137-140`），推进 `active[0]`（`:165`）。`v2` 已是按车循环（`v2:Engine:160-175`） | **冲突**：MVP 多需求代码建在单车假设上 |
| 6 | `OperationSession` 粒度 | `T03` Q11（`:227-236`）：**每 Demand 一个**，`operationSessionId` 下移到清单 `items[]` 每项 | **每旅程一个**（`MVP:Engine:2068`，`:1263-1274` 按旅程的 id 匹配录入）。`v2` 仍按 Demand 派生（`v2:Engine:1610`） | **冲突** |
| 7 | 途中追加与换序 | `T14`（`:7-12,180-189`）、`Spec:423-426`：三条按完整能力实施；边际成本用计划锚，由 `RouteGraphSnapshot` 自建图给出；可达性只认自建图；`REQ-0198` 延迟门禁；`REQ-0197` 删除与换序合一行 | 只在装货阶段追加到末尾，没有成本、没有换序、没有延迟门禁（见 1.2）。停靠序号是主键的一半，关卡固定为 9。代码注释写明改序号等于删了再插一行（`MVP:Engine:84-90`） | **不同形**：换序与 MVP 的主键设计相抵 |
| 8 | 计划上限 | `T03`（`:423-452`）：`legs.maxItems` 9、`items.maxItems` 8（8 取货 + 1 关卡） | `MaxPickupStops = 8`，关卡序号 9（`MVP:Engine:91-93`）。车载端 `14b51d0` 把 MVP 腿数上限设为 10，按 v1.0.0 应为 9（#61 §1.3 Q3） | **同形**（服务端数值一致） |
| 9 | 腿类型与停靠角色 | `T03:435,447` 定 B3 不改 enum；票 13 拆「取货／卸货」与「站点功能」（`T12:239`）。已发布的 `protocol-v1.0.0` 腿类型是 `TO_PICKUP`／`TO_DROPOFF` 加 `stopPurposeCategory`，没有 `TO_GATE`（`v2:src/ControlServer.Domain/WireToGateModels.cs:116`） | `TO_PICKUP`／`TO_GATE`／`TO_CHARGER`（v0.3.0） | **不同形**（协议面） |
| 10 | 录入范围 | `ADR0057:34-40` 与 FR-001 AC-3：操作员可录入派车范围内任意 SUBLOT | `expectedSublots` 集合（v0.3.0）。`protocol-v1.0.0` 仍是单值 `expectedSublot`（#61 §2 `0b65f05` 行，`SublotEntryRequested.schema.json:67`） | **冲突**（v1.0.0 已发布，改是协议变更） |
| 11 | 离站规则（装满或持货 30 分钟） | `ADR0057` 状态 accepted。`Spec` 全文 grep `0057`／`持货`／`装满` **零命中**；`Req` grep `持货`／`HOLDING_TIMEOUT`／`VEHICLE_FULL` **零命中** | 已实现（1.3 第 7 点），并在现场窗口触发过（4.2 第 2 行） | **规格与基线无对应条目** |
| 12 | 批次顺序 | `Spec:299-311`：`5 ← 2轨B`、`6 ← 5`，严格串行 `2轨B → 5 → 6 → 7` | MVP 在没有 B2／B1／B4 的情况下先做了 B3 形态。`v2` 已有 2 轨 B 的产物：`RouteGraph*` 表、`DispatchAdmission` 准入判据、车队 roster（`v2:DbContext:43-57`；`v2:src/ControlServer.Host/Runtime/Fleet/VehicleRoster.cs`） | MVP 的实施顺序与规格相反 |

---

## 3. 问题 3：把 MVP 线多需求累积搬到 v2 线的代价

### 3.1 #61 审计里 D 类「旅程改造」的提交

出处：#61 §1.3 Q1 与 §2、§3 各行。服务端 `src` 改动行数由本调研 `git show --numstat <c> -- src` 实测。

**服务端 10 条**（主线 3 条 + 跟随 7 条）：

| 提交 | 日期 | 标题 | `src` 改动（+/−，不含迁移 Designer） | #61 试算与依赖 |
| --- | --- | --- | --- | --- |
| `663f275a` | 09-08 | 旅程按自己的身份重建，改由停靠序列驱动 | `WireToGateModels.cs` +79/−9、`Engine` +733/−217、`Options` +22、`OnboardRecoveryCoordinator.cs` +41/−16、`DbContext` +134/−27、`Store` +252/−97；迁移 `20260908042817_MultiDemandJourneyStopSequence` +386 | 冲突 12 个文件。#61：「若做是按 v1.0.0 重写，不是移植」 |
| `18a7e6ad` | 09-08 | 运行中把新需求吸收进在途旅程，装满或持货 30 分钟才去关卡 | `Ports.cs` +13、`WireToGateOrchestration.cs` +79/−13、`Engine` +383/−123、`Store` +113 | 依赖 `663f275a` |
| `bc145629` | 09-08 | 切到 protocolVersion 2，批次录入按范围给、按 BR-013 录入后重算 | `ProtocolCandidateIdentity.cs` +21/−8、`WireToGateModels.cs` +19/−1、`Engine` +128/−1、`OnboardJourneyPublisher.cs` +53/−2 | 协议身份与 `expectedSublots` 属 C。录入后重算属基线缺口 |
| `80f6b93d` | 09-08 | 到站没货的两条出口，以及电量低了自己去充电 | `Engine` +311/−2、`Options` +56、`DbContext` +33、`Store` +95、`Coordinator` +28/−3、`appsettings` +6；迁移 `20260907174639_SublotWaitTimeoutAndBeforeLoadCancellation` +29、`20260907175328_AutoChargingRuns` +51 | 冲突 Engine、Options、ModelSnapshot |
| `557644a6` | 09-08 | 理由码对齐基线，取消写下按业务键的永久抑制 | `Engine` +11/−1、`Coordinator` +14/−6、`DbContext` +25、`Store` +66；迁移 `20260908020947_TransportDemandSuppression` +36 | #61：抑制部分可以不带多需求单独做 |
| `a370c1c2` | 09-08 | 充电桩现场身份到位，自动充电打开 | `appsettings` +2/−2 | 依赖 `80f6b93d`、`3c9ced41` |
| `3c9ced41` | 09-12 | 充电单带开始充电动作，桩解析不到或该充电时拒单 | `Engine` +48/−6、`Options` +11/−9、`HttpRiotMovementGateway.cs` +88/−11、`appsettings` +2/−2 | 与 `80f6b93d`、`a370c1c2` 同车 |
| `946d460d` | 09-09 | 取消在途装载后本站按批次收尾 | `Engine` +43、`Coordinator` +11 | 随 `663f275a`，否则 C |
| `8be28b1c` | 09-11 | 补偿清空或故障货物交接后多需求旅程不再停在 Blocked | `Coordinator` +39/−9 | 多需求进 v2 时必须带上 |
| `e08ab634` | 09-10 | SublotRejected 带上被拒 SublotSubmitted 的 messageId | `Engine` +1、`OnboardJourneyPublisher.cs` +9/−1 | 随 `bc145629` |

**车载端 4 条 D**：`8888811`（到站扫码前取消）、`54772ff`（清单项数上限）、`14b51d0`（腿数上限）、`b142152`（行程带）。另有 `0b65f05`（可录入子批改成集合），#61 判 C，但做多需求时要一并改 `WireToGateJourney.cs`、`MainViewModel.cs`、`OnboardController.cs`（#61 §2）。

**不属 Q1、但建在多需求结构上的其他提交**（#61 §2、§3）：

- `770447f5`（B）：store 那段用了 `JourneyDemands`，`v2` 编译不过。
- `c0e90361`、`80d7c65e`、`de3960e2`、`d36f11bc`（D，属 Q2）：依赖 `663f275a`／`80f6b93d`。
- `b56a9df9`（A）：「AwaitingSublot 结束本站后当轮判」那一半只属多需求。
- `25a298d4`（B）：「判过一次」那一半只属多需求。

### 3.2 依赖了 v2 上不存在的哪些表与结构

| 类别 | MVP 上有 | v2 上的现状 | 证据 |
| --- | --- | --- | --- |
| 表 | `JourneyStops`、`JourneyDemands`、`TransportDemandSuppressions`、`AutoChargingRuns` | 四张都没有 DbSet。`v2` 迁移 Designer 里残留的表定义来自批次 3 的 cherry-pick，`v2 13bbe4d2` 说明写「v0.3.0 线其余的表不带进来」 | `MVP:DbContext:32-36` 对 `v2:DbContext:9-57`；`git grep` 在 `v2` 的 `src` 只命中 `Migrations/20260909124757_Batch3GovernanceAndSlotConfiguration.Designer.cs`；#61 §1.3 |
| 主键 | `JourneyRuntimes` 主键 `JourneyId` | 主键 `DemandId`，取货与关卡是固定列 | `MVP:Cfg/JourneyRuntimeRowConfiguration.cs:10` 对 `v2:DbContext:143,556-605` |
| 主键 | `VehicleDispatchLeases` 主键 `JourneyId` | 主键 `DemandId`（同样有 `VehicleKey` 过滤唯一索引） | `MVP:Cfg/VehicleDispatchLeaseRowConfiguration.cs:10-14` 对 `v2:DbContext:73-76` |
| 列 | `CurrentStopSequence`、`NextStopSequence`、`HoldingStartedAt`、`LoadingClosedReason`、`LoadRound`、`SublotWaitStartedAt`、`LoadCommandedAt`／`UnloadCommandedAt` | 没有。`v2` 有自己的 `StationDepartureWaitStartedAt`（离站修正窗口，`6e8dea5a`） | `MVP:DbContext:435-563`；`v2:DbContext:602` |
| 端口 | `IDemandAcceptanceStore.JoinJourneyAsync` | 没有 | `MVP:src/ControlServer.Application/DemandStorePorts.cs:27`；`v2` grep 零命中 |
| 配置 | `HoldingTimeout`、`SublotWaitTimeout`、`AutoChargingEnabled`、`ChargerStationId`／`ChargerStationRiotId`、`ChargeTriggerBatteryPercent`、`ChargeResumeBatteryPercent` | 都没有；`v2` 有 `checkpointWaitBudget`、`stationDepartureWaitTimeout` | `MVP:Options:22-75`；`MVP:appsettings:44-69` 对 `v2:appsettings:44-65` |
| 迁移链 | 分叉后 MVP 独有 5 个：`20260907174639`、`20260907175328`、`20260908020947`、`20260908042817`、`20260912153533` | 分叉后 v2 独有 5 个：`20260904094629_ManualChargingReturnToService`、`20260907133250_Batch2CapabilityFoundation`、`20260910031132`、`20260910063725`、`20260913131725_StationDepartureWait`。只有 `20260909124757` 两线同名 | 两线 `git ls-tree .../Migrations/` |
| 引擎形状 | 单车，`Engine` 3004 行 | 多车（按车推进、车队 roster、`DispatchAdmission` 判据链、`RouteGraph`），`Engine` 2011 行 | `base` 时 `Engine` 1379 行。自 `base` 起四个核心文件：`MVP` +3042/−554，`v2` +1289/−299（`git diff --stat`） |
| 协议 | `protocol-v0.3.0`，`WIRE_TO_GATE_MVP`，`protocolVersion` 3，`TO_GATE`、`expectedSublots` 集合 | `protocol-v1.0.0`，`AGV_FULL_PRODUCT`，`protocolVersion` 2，`TO_DROPOFF` + `stopPurposeCategory`，`expectedSublot` 单值；没有 `TO_CHARGER`，也没有 `CV-LOAD-CANCELLATION-BEFORE-LOAD` 向量 | `MVP:appsettings:2-11` 对 `v2:appsettings:2-12`；#61 §1.3 |
| 车载端上限 | 腿数、清单项数随 schema 放开（`14b51d0`、`54772ff`） | `v2` 车载端仍是 `Legs.Count > 2`、`Items.Count > 1`，`OnboardController.cs:1682` 是 `SingleOrDefault` | #61 §1.3 Q3 |

**#61 已有的判断**（引述，不是本调研的新结论）：子审计判「多停靠与充电要按 v1.0.0 重做，不能移植」（#61 §1.3 Q1 第 2 问）。#61 的试算是逐提交单独做的，**不叠加前序**；文本合并干净也不等于能编译（#61 §0）。

---

## 4. 问题 4：「生产无倒退切 v2」至少要求 v2 具备哪些能力

### 4.1 「生产在用」的证据边界

- #61 断言「生产现在就在用多单和自动充电」（#61 §1.3 Q1 事实末条）。
- 本调研能读到的一手证据是 `MVP` 上的现场窗口提交与证据目录（`MVP:evidence/field/`）。窗口条件：真车 `agv01`（`老厂前线新多仓位1`）、生产 RIoT `172.19.206.222:8888`、数据库在 `factory01`、仓位 IO 是模拟器（`127.0.0.1:1502`），需求取自真实 MES（`123c5f9b` 记「本窗口永久抑制 4 条真实需求」）。
- `MVP:appsettings:45` 出厂 `JourneyRuntime.enabled=false`，`:59` `autoChargingEnabled=true`。`factory01` 上的实际配置与日常运行状态**离线读不到，未核实**。
- `origin/deploy/3b379bb-onboard-io52` 是 `MVP` 的祖先；`origin/field/w1-20260913` 不是。

### 4.2 MVP 线在现场用到、v2 当前缺的能力

| # | 能力 | MVP 现场证据 | v2 现状 | 规格排期 |
| --- | --- | --- | --- | --- |
| 1 | **多需求旅程**（一趟 5 个取货停靠加关卡） | `123c5f9b`（窗口一，旅程 `a72e0b81` 五个取货加关卡）；`f8d355e8`（窗口二 N 场景，旅程 `bcdaf0ee` 五条需求走通） | 一趟一单：`v2:DbContext:143`；`v2:docs/defects/20260913-no-pre-departure-correction-window.md:58`「v2 一趟旅程只有一条需求」 | 批次 6（`Spec:201`，`FP-IS-08`，`Spec:741`） |
| 2 | **持货超时截断**（`CANCELLED_BY_STOP_COMPLETE`） | `123c5f9b`：车 22:06 到停靠 3 时持货已超 30 分钟，三条需求被终结 | `LoadingClosedReason`／`HOLDING_TIMEOUT`／`VEHICLE_FULL` 零命中（#61 §3 `18a7e6ad` 行） | 规格与基线无条目（2.2 第 11 行） |
| 3 | **按业务键永久抑制** | `123c5f9b`：抑制 4 条真实需求 | 只按 `DemandId` 挡（`v2:src/ControlServer.Host/Runtime/Dispatch/Criteria/AlreadyAcceptedCriterion.cs:28`）；同一 SUBLOT 换新 DemandId 回来撞 `TransportDemandKey` 唯一索引（`v2:DbContext:71`；#61 §3 `557644a6` 行） | 批次 6（`REQ-0155`／`0156`／`0211`） |
| 4 | **自动充电**（move 212 → move 211 → act 78） | `f8d355e8`：窗口二充电短窗口 `FW-FL2` PASS/14，「自动充电现场第一次做成」 | 零命中；`v2:Engine:1725-1727` 注释「CHARGING is batch 8」；`VehicleDynamicFactsCriterion.cs:94` 充电中直接拒单。`v2` 有迁移 `ManualChargingReturnToService`（人工充电后恢复服务，行为未核） | 批次 8（`Spec:203,430-444`，`FP-C1` 19 条）。注意 `Spec:348` 写「三个充电桩物理上还没安装」，而 `f8d355e8` 在 `充电点1`／211 上充上了电，两者口径不一致 |
| 5 | **到站无货的出口**（站点等待超时取消、到站未装货取消） | `80f6b93d`；窗口一场景 A、B（`123c5f9b`） | `AwaitingSublot` 没有出口，也没有超时（#61 §1.3 Q1 第 3 问第 1 项） | 基线要求（ADR-cross-0046、0055），#61 列为「基线要求而 v2 缺」 |
| 6 | **ADR-cross-0058 确定失败与站点期限**（`STATION_TIMEOUT_DOOR_NOT_CLOSED`、`CANCELLED_BY_STATION_TIMEOUT`） | `123c5f9b`：窗口一场景 C、B；`MVP:Engine:691-719` | v2 车载端仍是超时即失败，服务端没有 `Failed` 分支（#61 §1.3 Q2） | 待 #61 Q2 裁定 |
| 7 | **BR-013 录入后重算与 `SublotRejected`** | `bc145629`、`e08ab634` 已实现；**现场窗口是否触发过，本调研未核** | `SublotRejected` 没有发送方（#61 §3 `bc145629` 行） | 基线要求，#61 列为「基线要求而 v2 缺」 |
| 8 | **车载端腿数与清单项数上限对齐 schema** | `14b51d0`、`54772ff`（MVP 2026-09-10 会话锁死之后修的） | `v2` 车载端仍是 `> 2`／`> 1`；一旦 v2 服务端能发多腿，会触发同样的锁死 | 待 #61 Q3 裁定 |

第 1～6 项有 MVP 现场窗口证据，第 7 项只有代码证据，第 8 项是第 1 项的车载端前提。另外，#61 §1.2 的 B 类 21 条（重连、恢复、取消与修正等）不属多需求，但同样是「切 v2 不倒退」的前置，见 #61。

---

## 5. 未查、未证与读法提醒

- 没有读车载端仓（`8005-agv-onboard-hmi`）与协议仓（`8005-agv-protocol`）的 ref。车载端提交与 `protocol-v1.0.0` 的 schema 事实都转引自 #61。
- `REQ-0211` 装货前取消走空范围 `LoadCancellationResult` 这一幕，两端现状未逐行复核（1.2 表）。
- `factory01` 上 `JourneyRuntime` 与 `autoChargingEnabled` 的实际值、生产日常是否持续开启，离线无法核实（4.1）。
- `v2` 的 `ManualChargingReturnToService` 只看了迁移名与表名，没有读行为。
- 所有「零命中」都是对 `src/` 做 `git grep` 的结果，排除了迁移目录；标识符改名后同义实现的情形不在其内。
