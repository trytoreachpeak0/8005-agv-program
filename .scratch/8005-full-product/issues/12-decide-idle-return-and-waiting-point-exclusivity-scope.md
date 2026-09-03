# 决定空闲返回与等待点的独占语义与范围

Type: grilling
Status: open
Blocked by: 02
Blocks: 04, 06

## Question

在票 02 定下的判据与排序规则内，决定完整产品的空闲返回与等待点做到哪一档，并定下 **B1
（车辆占用脱离 Demand）与 B4（站点独占）这对原语的落地形态**。

本票由票 02 从票 03 拆出。拆出的理由不是条目多，而是**这 8 条承载的两条不变量同时是自动
充电（`FP-C1`）的前置**：`REQ-0178` 明文要求充电失败清桩「共用地图等待点集合……多车原子
预占」。塞进票 03 会让多车票同时背四条不变量（B2／B3／B5 再加 B1／B4），塞进票 04 会把
`FP-C1` 的前置埋在 `FP-C1` 内部、票 09 排批次时看不见。见 [票 02 决议](02-answer.md)。

MVP 的边界是：行程终点硬编码为 `TO_PICKUP` → `TO_GATE` 两段，之后 journey 直接进
`Completed`，车辆停在关卡站不动。代码中 `IdleReturn`／`WaitingPoint`／`Park` 全仓零命中，
协议中同样零命中。本簇 `FP-C4` 共 **8 条**，票 02 判定 **3 条重构、5 条增量**：

| 条目 | 票 02 判定 | 说明 |
| --- | --- | --- |
| `REQ-0289` | 增量（须先于 `REQ-0293`） | 首版只允许专用等待点，以 RIoT 地图 + 站点登记，不得兼任业务或充电角色，沿用 `WaitingPointVehicleScope` |
| `REQ-0291` | 增量（依赖 B1） | `IdleReturnEligibility` 是严格兜底资格 |
| `REQ-0292` | **重构 B1 + B4** | 同一份新鲜快照**原子取得** `IDLE_RETURN VehiclePurposeClaim` 与 `WaitingPointExclusiveClaim`，任一失败都不形成承诺 |
| `REQ-0293` | **重构 B4** | 从在途预占到在点占用的连续单车独占，离点确认后才释放 |
| `REQ-0294` | **重构 B1** | 只用 `RoutineOrderCreationCall` 建单段 move，禁止 RIoT「一键停靠」与 `parkConfig` |
| `REQ-0295` | 增量（依赖 B1 + B4） | 到点必须由一致证据组合确认，单值 `currentPosition` 不足 |
| `REQ-0296` | 增量（依赖 B1 + B4） | 失败按「是否可能已有订单或仍在运动」分流 |
| `REQ-0297` | 增量（依赖 B4） | 配置和拓扑变化不破坏既有预占引用 |

现场规模由票 11 定案（用户 2026-09-03 确认）：**3 台 AGV、n 个等待点，全部在唯一作业图
`mapId` 25（`老厂前线new`）上，等待点数量必须可配置**。`REQ-0289` 的等待点登记已覆盖该
配置能力，**不派生新需求**。**`n` 的具体数量用户尚未给出**，本票须问到。

须回答：

1. **B1 的落地形态：`VehicleDispatchLease` 怎么从 Demand-keyed 推广为 purpose-keyed。**
   现状 `VehicleDispatchLeaseRow` 主键是 `DemandId`、`VehicleKey` 上有过滤唯一索引
   `ReleasedAt IS NULL`（`ControlServerDbContext.cs:44`）。空闲返回占用车辆时没有 Demand。
   是给租约加一个 `purpose` 维度并放宽主键，还是另建一张 claim 表？无论哪种，
   「一辆车同一时刻只有一个用途」这条唯一性必须由数据库约束而非应用逻辑保证——现状那条
   过滤唯一索引就是这么做的，新形态不得退化为应用层检查。
2. **B4 的落地形态：站点独占表的键与生命周期。**独占的键是「地图 + 站点」还是站点身份？
   预占与占用是同一行的两个状态还是两行？`REQ-0293` 要求「在途预占 → 在点占用」连续不
   中断，且**离点确认后才释放，不能在下达离点订单时提前释放**——这条对释放路径的要求
   同现有租约的三处释放点（`WireToGateStore.cs:988`／`:1478`、`OnboardRecoveryCoordinator.cs:807`）
   语义不同，须说明新形态怎么表达。
3. **B1 与 B4 的原子取得怎么实现。**`REQ-0292` 要求「基于同一份新鲜快照同时取得」两者。
   现状承诺路径是 `WireToGateStore.AcceptCoreAsync`（`:197-310`）一个事务内查租约→建
   Demand→建租约→建 OrderIntent，**且未显式设置隔离级别**（全仓无 `IsolationLevel`
   出现，用 SQLite provider 默认值）。3 车并发下这条路径是否仍然正确，要不要显式指定
   隔离级别或改用唯一约束冲突捕获，本票须判。
4. **空闲返回的触发档位。**`REQ-0291` 要求「启用空闲返回或激活新版等待点配置时，立即
   重评所有当前满足条件的车辆」。完整产品是全量实现这条重评，还是先做「任务收敛后触发
   一次」的更小档？两档的差别在于是否需要一个独立于 journey tick 的重评入口。
5. **行程第三段怎么表达。**空闲返回是 `byDefaultMissions` 单段 move，不是 journey 的第三
   段——但车载 HMI 要显示车辆正在去等待点。这需要协议 `UpcomingStopPlanSnapshot.legType`
   加 `TO_WAITING_POINT`（enum 变更即 breaking，输入给票 06），还是用别的表达？本票只输出
   「哪些业务能力必须由协议承载」，不改协议消息面。
6. **等待点数量 `n` 是多少**，以及等待点的现场值（地图 + 站点标识）从哪里来。三个 8005
   独占充电桩的名册由票 04 处理，等待点登记归本票。若现场值尚未确定，本票须说明它属实施
   图的哪一步，且不得让规格假定某个具体数量。
7. **`REQ-0294` 的禁止项怎么落到验收上。**该条明文「生成的 RIoT『一键停靠』和 `parkConfig`
   客户端不构成授权，现有白名单也明确禁止这些调用」。这是一条否定性约束，证据形态
   （静态检查白名单？运行期断言？）本票给意见，最终归票 08。

### 票 03 定下的、与本票相关的两件事

**第一，`legType` enum 的扩值是本票与票 04 的责任，不是 B3 的。**票 02 曾把
「`legType` enum」列进 B3 要动的五处协议硬约束，[票 03 决议](03-answer.md)查实后**纠正了这一判断**：
档 2 下每一段仍是「去某个取货点」或「去关卡」，`["TO_PICKUP", "TO_GATE"]` 两个值够用。
真正要给它加值的是**空闲返回去等待点**（本票）与**去充电桩**（票 04）。`stopRole` 的 enum
同理。**本票不要假设票 06 已经从 B3 那里收到了这个改动。**

位置：`schemas/messages/UpcomingStopPlanSnapshot.schema.json:75-81`（`legType`）与
`schemas/messages/CurrentStopWorklistSnapshot.schema.json:92-98`（`stopRole`）；两处 enum
在整个 `schemas/` 下**各只出现一次**。按 `docs/release-governance.md:11`，enum 变更是 breaking。

**第二，B3 已把计划形状从「单 Demand 两段固定行程」改成多停靠计划。**票 03 定的上限是
`legs.maxItems` 9（8 个取货停靠 + 1 个关卡停靠）、`sequence.maximum` 9、`items.maxItems` 8。
本票若要在计划里插入等待点停靠，**是在这个新形状里插，不是在原来的两段里插**，上限数值要
连同本票的需求一并算给票 06。

另：票 03 已删除 `IX_VehicleDispatchLeases_VehicleKey ... WHERE ReleasedAt IS NULL` 并把
唯一性下移到 `OrderIntents` 的按 `VehicleKey` 过滤唯一索引。**本票在设计站点独占（B4）的
持久化形态时，不要再假设 lease 表上有那条索引。**

### 已知边界

- 本票不改协议消息面。等待点带来的消息面变化由票 06 一次冻结。
- 本票不决定批次归属与顺序，那是票 09。
- 本票不决定车载端实现方式；车载端归 Kun Wang，其仓库对本工作区只读。
- 本票不决定自动充电的任何范围。`REQ-0178` 只作为「清桩要用等待点」这一依赖的出处被引用，
  充电失败治理的范围归票 04。
- 跨图约束不覆盖等待点（票 11 查明：没有任何一条要求等待点与车辆同图）。当前全部在
  `mapId` 25 上使这个缺口无害，**本票不为它派生新需求，但不得在范围表述中假定「同图」是
  已被规定的不变量**。
