# 票 12 决议：空闲返回与等待点的独占语义与范围，及 B1／B4 的落地形态

日期：2026-09-03。批准人：用户（本图默认且唯一最终批准人），八问全部取推荐值。

## 一、事实基础

本票开工前先做了三组事实核查，两组由子 agent 执行（控制服务端持久化与独占现状、RIoT 建单
与停靠 API 面），一组自查（需求基线全文标识符扫描、mapId 25 站点实测枚举）。**核查推翻或
补正了本票原文的三处前提**，逐条记在下面；`REQ-0290` 那条改变了本票的形状。

### 1.1 `REQ-0290` 是 B1 的定义条款，而它一直在批次 0 —— 本图第五次「能力藏在批次 0」

`REQ-0290` 的正文是**「所有用途通过唯一 `VehiclePurposeClaim` 原子争用车辆。已开始或结果
未知的搬运、充电、清桩/维护和空闲返回保持现有占有，不允许新用途抢占……」**。它规定了四种
用途共用一个占有槽、三级优先级（强制充电 > 普通搬运 > 空闲返回）与「空闲返回不预留未来
车辆」。这正是票 12 第 1 问要落地的原语。

它在剖面里归 `FP-B0 批次 0 候选`，`MvpFinalClassification` 是「MVP 交互／安全依赖」，
`ControlServerImpact` 写的是**「以电量门禁阻断新任务并提示人工充电」**——MVP 剖面只读到了
本条后半句的 `MandatoryChargeEntryThreshold`，把整条判成了电量阻断，前半句的用途争用完全
没有进入判定。

代码侧：`VehiclePurposeClaim` 在 `8005-agv-control-server/src/` 下**零命中**；现存的
`VehicleDispatchLeaseRow`（`ControlServerDbContext.cs:150-156`）主键是 `DemandId`，四列
`DemandId`／`VehicleKey`／`AcquiredAt`／`ReleasedAt`，只表达搬运一种用途。

票据侧：**`REQ-0290` 与 `REQ-0147` 在本图 01～15 号票据中从未被提及过一次。**票 02 判 B1
时用的是 `REQ-0292`（原子取得车辆与等待点）与 `REQ-0294`（返回订单占用车辆而无 Demand），
两条都是**使用**这个原语的条目；定义它的那条因为标着批次 0 而根本没进 62／81 条的视野。

**这是本图第五次「能力藏在批次 0」**，与前四次同构：MVP 只有搬运一种用途，「唯一用途原子
争用」退化为「一个 Demand 一个租约」，判定**在单一用途形态下没错**。交接文档预告的「第五次
的最强线索」指向配置与告警面的六个零命中标识符——**第五次实际出现在别处**，这说明那六个
标识符仍是未验证线索，票 09 逐条复核时不得因本次已找到第五次而放松。

### 1.2 票 03 删掉 lease 表唯一索引后留下一个空窗，只有 `REQ-0290` 能补

票 03 的 Q7 定：删除 `IX_VehicleDispatchLeases_VehicleKey ... WHERE ReleasedAt IS NULL`，
唯一性下移到 `OrderIntents` 的按 `VehicleKey` 过滤唯一索引（未终结订单每车至多一条），
并论证 `DispatchUniquenessGuard` 一字不改仍成立。

**这个推理在订单层是对的，但它不覆盖用途层。**用途跨越多个订单：一次搬运从接单到卸货有
2 个订单（B3 之后 2～9 个），车在两个订单之间——例如刚到取货点、去关卡的单尚未建立——
`OrderIntents` 上没有活跃行，此刻每车唯一索引约束不到任何东西。现状靠 lease 表那条过滤唯一
索引挡住，票 03 删掉它就出现空窗。

两条唯一性是不同层次，`CONTEXT.md:898` 的 `DispatchUniquenessGuard` 措辞本身就说明了这点
（「每辆 AGV 同时只能被一个未确认或未终结的**本项目订单**占用」——约束的是订单）。
**`VehiclePurposeClaim` 是用途层，`DispatchUniquenessGuard` 是订单层，两者并存不冗余。**

### 1.3 两处代码现状与票据记载不一致，须纠正

1. **`IX_VehicleDispatchLeases_VehicleKey` 现在还在**（`ControlServerDbContext.cs:45-48`，
   模型快照 `ControlServerDbContextModelSnapshot.cs:1565-1567`）。票 12 正文写「票 03 已删除
   ……本票不要再假设 lease 表上有那条索引」——票 03 的删除是**决策**不是现状，本票的设计以
   「删除后」为起点是对的，但描述现状时不能说它已经不在。
2. **`OrderIntents` 上没有任何 `VehicleKey` 索引**（该表主键 `MovementLegId`，三条唯一索引
   分别在 `UpperId`、`CreateAttemptId`、`ExperimentalCreateAuthorizationId`）。票 03 要建的
   那条同样是待实施决策。

### 1.4 站点独占在代码里完全不存在，不是「另有一套叫法」

`SingleBerthStationClaim`、`StationExclusive`、`StationClaim`、`WaitingPointExclusiveClaim`、
`VehiclePurposeClaim`、`StationReservation`、`BerthClaim`、`PublicStationIncumbentPreference`
在 `src/` 下**全部零命中**。放宽到子串 `Claim` 在 `src/` 下**一条都没有**；`Exclusive` 的三处
是迁移类名 `ExclusiveVehicleDispatchLease`（指车辆租约）与一个英文副词；`Reserv` 的三处是
`preserve`、`PreserveNewest` 与一句提到车上槽位的注释。

**B4 是纯新建，没有任何既有实现可以改造。**

### 1.5 journey 走完两段之后，代码什么都不做

进入 `Completed` 在 `JourneyRuntimeEngine.cs:525`，`SetStage` 只写 `Stage`／
`BlockReasonCode=null`／`UpdatedAt`（`:1277-1282`），随即 `break` 到 `:535` 的
`SaveChangesAsync` 结束方法。下一 tick 的 `ExecuteOnceAsync` 用
`.Where(row => row.Stage != JourneyRuntimeStage.Completed)`（`:80-82`）把已完成 journey 过滤掉，
去找新需求。**车辆此后停在关卡站，代码里没有任何把它移走的路径。**
`IdleReturn`／`WaitingPoint`／`Park`／`Dock`／`Standby` 在 `src/` 下均零命中。

### 1.6 mapId 25 上当前没有等待点，也没有充电桩

来源：`rcs/riot-behavior-lab/evidence/rounds/2026-09-03-round-43/runs/004-stations-map-25.json`
（本图最新一次实测，票 14 的 Round 43 同一批数据）。206 个站：

| 事实 | 值 |
| --- | --- |
| `type` 字段 | 全部 = 1，**无第二个取值** |
| `desc`／`param`／`user_define_properties` | **全部为空** |
| 站名形态 | `N#-#` 119 个、`T##-##` 86 个、`关卡` 1 个，共 206 |
| `id` 范围 | 1–210（4 个 id 空洞） |
| `removedStation/25` | `result: []`（无移除站点） |

**没有任何一个站是等待点或充电桩，RIoT 的 Station 也不携带角色信息。**这坐实了票 11 证据
文件「事实 3」的方向（此前是从 `205 + 1 = 206` 的计数推出的，现在是直接观测），并与
`CONTEXT.md` 的 `_Avoid_: RIoT 原生业务站点类型、按名称识别等待点或充电点` 吻合——基线早就
知道角色只能在 8005 侧登记。

### 1.7 `REQ-0294` 要的建单能力，批次 0 已经实现了

`REQ-0147`（**批次 0，MVP 直接必须**）的正文：「常规建单：只允许
`POST /api/order/v1/add/byDefaultMissions` 创建指定车辆、地图和站点的**单段 move**；须使用
稳定 `upperId`，并先验证车辆 `ON_LINE`、`RouteCost` 可达且该车未占用 RIoT 车辆订单名额。
模板建单、订单组合、改单不获批。」

控制服务端已在用：`HttpRiotMovementGateway.cs:93` 调
`riotSession.Order.CreateMoveOrderAsync(upperId, vehicleKey, mapId, destinationStationId, upperId, ct)`，
SDK 填 `Mission = [{ Type="move", MapId, Destination }]` 单元素数组。请求体 schema
`OrderRecordDTO对象` 唯一必填字段是 `mission`（数组），元素 `MissionDTO` 唯一必填字段是
`type`（`move`／`act`），`mapId`／`destination` 均为可选。

**空闲返回不需要任何新的建单能力，只是复用。**`REQ-0294` 的工程量全在「占用与释放」那一侧，
不在「怎么建单」。

**一处措辞纠正**：`byDefaultMissions` 是 **URL 路径段**，不是请求体字段。请求体字段叫
`mission`（单数、数组），响应侧才叫 `missions`（`OrderSnapshot.Missions`，控制服务端在
`HttpRiotMovementGateway.cs:299-307` 读它校验「必须恰好一段 move」）。基线 `REQ-0294`
与 `CONTEXT.md:751` 都写「创建 `byDefaultMissions` 单段 move」，在代码语境下会被读成字段名。
本图不改基线，此处只记录该措辞的正确读法。

### 1.8 `RoutineOrderCreationCall` 的白名单是纯文档，且 `Raw` 逃逸舱是 public 的

- RIoT **确实有一键停靠端点** `POST /api/task/vehicles/park`（summary 字面「一键停靠」，
  operationId `parkUsingPOST`），外加 6 条 `parkConfig` 路径。**生成客户端在 vendored 包里
  全部在场**——`RIoT.Sdk.Generated.dll` 里 16 个 `Park*` 类型。
- **`OrderClient.Raw`／`TaskClient.Raw`／`MapClient.Raw` 三个属性都是 public**。因此
  `riotSession.Tasks.Raw.Api.TaskNamespace.Vehicles.Park.PostAsync(...)` **能直接编译通过**。
  控制服务端当前 `.Raw` 在 `src/` 与 `tests/` 均零命中——**是没用，不是不能用**。
- 真正的白名单是一份纯文档：`.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md:15-23`，
  按业务后果分五层封闭列举获批调用，`:23` 明写「一键停靠、放行、指定充电、……、`RawEscape`、
  生成客户端和其它未具名调用全部不授权」。**执行方式是人工审批，编译期、运行期、测试期
  三处都没有守卫。**
- 现有测试只有**正向**断言（`HttpRiotMovementGatewayTests.cs` 逐个断言 6 条实际调用的路径）
  与供应链完整性（`RiotSdkPackageProvenanceTests.cs` 比对包哈希）。**没有一条断言「不得调用
  其它端点」。**

**这条同时消解了票 14 遗留的残余风险。**map 的 Not-yet-specified 记「`riot-sdk` vendored 包
的残余风险只剩『连 `Raw` 通道都不给』」——**不成立**，三个 client 的 `Raw` 都是 public。

---

## 二、逐问定案

### Q1 — 等待点属现场未测绘，`n` 不写进规格

**取 (a)：等待点物理上在厂区，但尚未测绘进 RIoT 地图。**票 11 记载的用户确认「3 车 3 桩
n 等待点全在 mapId 25 上」说的是物理布置，Round 43 的实测说的是 RIoT 地图内容，两者不冲突——
**冲突的是「已确认在图上」这个此前未经检验的读法**。

**与票 13 的 `FP-C9a` 同构：机制一次建齐，投运待现场测绘。**具体形态：

1. **`n` 不进规格。**`REQ-0289` 的等待点登记做成配置驱动（`MapWaitingPointPool` 是一个可为
   空的集合），规格中不假定任何具体数量。
2. **空集合时 fail-closed 且静默。**没有合格等待点时车辆进入 `IdleReturnPending`（该词
   `CONTEXT.md` 已有），不取得任何 claim、不建单、不告警——这正是 `REQ-0289` 未部署时的
   自然状态，与 `REQ-0294` 的「无合格点时原地排队并告警」不同（后者是 `REQ-0178` 清桩场景，
   有合格点集合但全被占用）。**区分二者是实施图的事，本票只定「空集合 ≠ 异常」。**
3. **验收期无法在现场真实触发空闲返回。**出口条件归票 08，与票 13 的「验收期只有
   `WIRE_TO_GATE` 能现场触发」是同一类问题，处置方式应当一致。
4. **不得归入 `证据受限实施`。**理由与票 13 的 `FP-C9a` 完全相同：这里证据不可得是现场
   尚未测绘造成的，补测绘后**无需改代码**。`证据受限实施` 要求的是判据依赖的外部证据恒不可得
   而门禁恒走保守分支；等待点集合为空只是配置为空。

**票 04 会撞上同一堵墙。**三个 8005 独占充电桩同样不在 mapId 25 的 206 个站里（`REQ-0171`
的桩名册也是「地图 + 站点」标识）。票 04 定案时应当采用同一形态，否则同一类现场事实会在
两个簇里得到两种处置。

### Q2 — `REQ-0290` 改判出批次 0，并入 `FP-C4`，判为重构类 B1

**改判成立。**判据与前四次相同：MVP 判定在单一用途形态下正确，完整产品语境下该形态是退化的。

- `FullProductCluster`：`FP-B0 批次 0 候选（MVP 已覆盖）` → `FP-C4 空闲返回与等待点`
- 分类：**重构类，判据 B1**（车辆占用脱离 Demand）
- `Batch0FormNote` 已写入，记录批次 0 判定在什么形态下成立

**票 02 的 B1 判定结论不变**，改判补上的是**需求载体**：`Purpose` 的四值枚举、三级优先级、
「空闲返回不预留未来车辆」这三条约束此前没有任何票据承载。票 02 用 `REQ-0292`／`REQ-0294`
判 B1 是对的，但那两条只说「空闲返回要取得占有」，没说**占有槽本身是什么、有几种用途、
谁压过谁**。

**`FP-C4` 由 9 条增至 10 条**，内部分类变为 **5 条重构（`REQ-0290` B1、`REQ-0292` B1+B4、
`REQ-0293` B4、`REQ-0294` B1、`REQ-0204` B4）／5 条增量**（`REQ-0289`、`REQ-0291`、
`REQ-0295`、`REQ-0296`、`REQ-0297`）。

### Q3 — B1 取甲档：`VehiclePurposeClaims` 新表取代 lease 表

**新建 `VehiclePurposeClaims`，主键 `VehicleKey`（一车一行）**，`VehicleDispatchLeases`
随 B3 一并废弃。

| 项 | 定案 |
| --- | --- |
| 主键 | `VehicleKey`，**唯一性由主键保证，不用过滤唯一索引** |
| `Purpose` | 四值枚举一次定全：`TRANSPORT`／`CHARGING`／`CLEARING_MAINTENANCE`／`IDLE_RETURN` |
| 用途相关引用 | 可空，按 `Purpose` 取不同含义（搬运指向计划、充电指向目标桩、空闲返回指向等待点） |
| 历史 | 独立审计表，不在业务表里软删除 |

三个理由：

1. **`DemandId` 主键在 B3 之后必废**——票 03 定的多停靠计划使「一次承诺 = 一条 Demand」
   不再成立，改造现有表等于同一张表连改两次。
2. **主键强于过滤唯一索引**。`HasFilter("ReleasedAt IS NULL")` 是 provider 相关语法，
   现状只有 SQLite（`Program.cs:25`），主键约束在任何 provider 上语义一致。
3. **`REQ-0297` 要求保留全过程证据**（「所有承诺、预占、建单、对账、到点、离点、失败与人工
   处置均保留车辆、地图、站点、配置版本、订单、时间和结果证据」），审计本来就得单独一张表；
   把软删除留在业务表里两头不到岸——既不是干净的当前态，也不是完整的审计。

**四值枚举一次定全是本票与票 04 的接口。**`CLEARING_MAINTENANCE`（清桩/维护）与 `CHARGING`
的语义归票 04，但**枚举本身在本票定死**，否则票 04 会再改一次同一张表的同一列。

### Q4 — B4 取「`(MapId, StationId)` 复合键 + 一行两状态 + 离点证据释放」

**三个子项分别定案：**

**键 —— `(MapId, StationId)` 复合键。这是事实决定的，不是选择。**RIoT 的 `stationId` 是
**图内唯一**的整数（Round 43 实测 mapId 25 上 id 范围 1–210），跨图会撞号。

**状态 —— 一行两状态**（`Reserved` → `Occupied`）。两行会产生「预占行已删、占用行未建」的
中间态，直接违反 `REQ-0293` 的「**连续**单车独占」。同一行状态跃迁在一个事务内完成，中间
不存在无主时刻。

**释放 —— 取 (ii)，由离点证据组合确认，并写成对称于 `REQ-0295` 的一致证据组合。**四项
同时成立才判离点：

1. `currentMap` 仍是本图（换图是另一类事件，不能当作离点）
2. `currentPosition` **不再**精确匹配该等待点
3. 车辆处于运动态
4. 全部证据新鲜且无冲突

不取 (i)「由下一段行程的到点反推」：车可能长时间停在等待点不动，独占永不释放。不取 (iii)
「新订单已建立且车辆已开始移动」：`REQ-0293` 明文「不能在下达离点订单时提前释放」，(iii) 把
建单事件混进了判据。

**离点确认是一个新领域词，且它没有需求条目载体。**基线只定了到点（`REQ-0295`），离点侧
只有 `REQ-0293` 一句「确认车辆实际离点后才释放」，没有规定证据构成。这与票 02 发现的
「B2 无需求条目载体」是同一类情况。**本图不改基线**，因此该证据组合在最终规格中作为实施
决策加注，不表述为需求。词条已写入 `CONTEXT.md`（见第五节）。

### Q5 — 空闲返回取甲档：加第三个正交维度「停靠目的类别」

票 13 已定 `stopRole`／`legType` 拆成「取货/卸货」与「站点功能」两个正交概念。等待点两个
维度都不属于——它既不装卸，也不是五个 `PublicStationFunction` 之一。

**给停靠加第三个正交维度：停靠目的类别，三值 `BUSINESS`／`WAITING_POINT`／`CHARGER`。**
空闲返回作为一个停靠进入 `UpcomingStopPlanSnapshot`。

依据是 `REQ-0292` 的原话：「形成承诺后，返回成为车辆**当前已承诺下一站**，沿用
`PlannedStopMutationBoundary`」——「已承诺下一站」与 `PlannedStopMutationBoundary` 两个词
都是计划语义，基线已经把空闲返回放进计划里了。

**这同时是 B1 的实质表达：计划里可以有不由 `TransportDemand` 引起的停靠。**票 03 定的
多停靠计划（`MultiStopExecutionPlan`）此前每个停靠都对应至少一条 Demand，等待点停靠是第一个
反例，充电桩停靠是第二个。

**给票 06 的输入**（本票不改协议消息面）：

| 项 | 内容 |
| --- | --- |
| 新增维度 | 停靠目的类别，三值 `BUSINESS`／`WAITING_POINT`／`CHARGER` |
| 位置 | `UpcomingStopPlanSnapshot`（现 `legType` 处，`schemas/messages/UpcomingStopPlanSnapshot.schema.json:75-81`）与 `CurrentStopWorklistSnapshot`（现 `stopRole` 处，`:92-98`） |
| 与票 13 的关系 | 票 13 已要求把这两处拆开取货卸货与站点功能；本票要求的是**第三个**维度，三者正交，票 06 一次冻结 |
| 与票 04 的关系 | `CHARGER` 值由本票定，语义归票 04；票 04 不应再向票 06 提第四个值 |
| 计划上限 | 票 03 定 `legs.maxItems` 9／`sequence.maximum` 9／`items.maxItems` 8。等待点停靠**不叠加上限**——它是行程收敛之后的独立承诺，不与业务停靠同时在计划里 |

### Q6 — `REQ-0291` 的全量重评全量实现

`REQ-0291` 明文要求「启用空闲返回或激活新版等待点配置时，**立即重评所有当前满足这些条件的
车辆**」。本图的「不做」只有延后与范围外两种合法形态，砍它等于不做 `REQ-0291`。

**全量实现。**3 车规模下这是一个由配置激活事件触发的重评入口，不是循环扫描。真正的成本是
**它必须独立于 journey tick 存在**：`JourneyRuntimeEngine` 现在只有 `ExecuteOnceAsync` 一个
入口，由 `PeriodicTimer` 驱动。

**这个「独立重评入口」是票 09 排序时看得见的工程量。**它不大，但不为零，且与
`FP-C7`（配置生效治理）有接口——「激活新版等待点配置」是一次配置生效事件。

### Q7 — 不加隔离级别，改为捕获主键/唯一约束冲突

事实：`AcceptCoreAsync` 用 `BeginTransactionAsync(cancellationToken)` 无隔离级别
（`WireToGateStore.cs:255`）；`src/` 下 `IsolationLevel` 与 `ExecutionStrategy` **均零命中**；
7 处 `BeginTransactionAsync` 全部无隔离级别参数；provider **只有 SQLite**（`Program.cs:25`）。
SQLite 的写事务全局串行，加上票 03 已定「单 worker 按车串行」，并发窗口极窄。

**定案：不显式指定隔离级别，在 `VehiclePurposeClaims` 与站点独占表两处写唯一约束冲突捕获。**

理由是**把正确性放在数据库层而不依赖 provider 语义**——SQLite 的串行写是实现属性不是契约，
而 `REQ-0292` 要的「任一取得失败都不形成承诺」正是「冲突即整体回滚」。代价诚实说：两处都要
写冲突捕获路径，比加一行 `IsolationLevel.Serializable` 麻烦。

**注意这条与票 03 的一处相关事实**：`AcceptCoreAsync` 的 lease 前置检查（`:256-265`）是事务内
**纯读**、非 `SELECT ... FOR UPDATE`，票 03 已指出「单 worker 串行下这没问题；票 09 排批次时
不得把模型甲当作可替换的实现细节」。**本票的冲突捕获使这条依赖减弱但不消失**——唯一约束
兜住了写冲突，但「读到的快照是否新鲜」仍由单 worker 串行保证，而 `REQ-0292` 明文要求
「基于**同一份新鲜快照**同时取得」。

### Q8 — `REQ-0294` 的否定性约束取甲档：架构测试

**加一条架构测试**，断言两件事：产品代码 `src/` 下 `.Raw` 命中数为 0；对 Facade 的调用方法
集合是获批清单的子集。测试期失败，CI 就能挡。

**两条限定必须写进规格：**

1. **这条约束的作用域远大于空闲返回。**它保护的是全部 RIoT 调用面，`REQ-0294` 只是唯一一条
   把它写进需求文本的条目。**不该只为空闲返回建这个机制**——票 09 排批次时把它作为一条
   **独立的横切工程**，不要挂在 `FP-C4` 下面，否则 `FP-C4` 延后会连带把整个 RIoT 调用面的
   守卫一起延后。
2. **不叠加运行期 DelegatingHandler。**乙档看着更强其实更晚——`Raw` 走同一个 HttpClient，
   路径拦截确实拦得住，但那是运行时才发现，甲档在 CI 就挡住。3 车规模下叠加的增益不抵成本。

丙档（维持纯文档 + 人工审批）的代价现在是量化的：**从「写一行 `.Raw`」到「打到一键停靠」
中间隔着零道自动关卡**，而 vendored 包里 16 个 `Park*` 类型全部在场。

---

## 三、对其他票据的影响

| 票据 | 影响 |
| --- | --- |
| **票 02** | B1 判定结论不变，但**需求载体补上了 `REQ-0290`**。这是本图**第三次**发现票 02 判据集或其载体不完整（第一次 B2 无载体，第二次票 13 补 I6，第三次是本次）。票 02 决议已追加修订说明。 |
| **票 03** | Q7「唯一性下移到 `OrderIntents`」在**订单层**成立，但不覆盖**用途层**的跨订单空窗。`VehiclePurposeClaims` 补上这个空窗，二者并存不冗余。票 03 决议已追加修订说明。 |
| **票 04** | 三条硬输入：(a) `Purpose` 四值枚举已在本票定死，票 04 不得再改这一列；(b) B1+B4 是充电簇 13 条增量的前置，本票已定形态，票 04 在其上工作；(c) **充电桩同样不在 mapId 25 的 206 个站里**，票 04 应采用与 Q1 相同的「机制建齐待测绘」形态。 |
| **票 06** | 停靠目的类别三值 `BUSINESS`／`WAITING_POINT`／`CHARGER`，与票 13 要求的两个维度正交，一次冻结。`CHARGER` 值由本票定，票 04 不再提第四个值。等待点停靠不叠加票 03 的计划上限。 |
| **票 08** | 两条：(a) **等待点在验收期无法现场真实触发**，出口条件须与票 13 的「其余五类不能现场触发」一致处置；(b) `REQ-0294` 的验收形态取架构测试（甲档），但**它是横切工程不属 `FP-C4`**。 |
| **票 09** | 五条：(a) `REQ-0290` 改判使批次 0 由 167 降至 **166**、待排期由 81 增至 **82**、`FP-C4` 由 9 增至 **10**；(b) `FP-C4` 内部 5 重构／5 增量；(c) **独立重评入口**是可见工程量，与 `FP-C7` 有接口；(d) **RIoT 调用白名单守卫是独立横切工程**，不挂 `FP-C4`；(e) **第五次「能力藏在批次 0」出现在别处**，交接预告的六个零命中标识符仍是未验证线索，不得因此放松逐条复核。 |
| **票 10** | 三条须在规格中如实表述：(a) `n` 不写进规格，等待点登记是配置驱动的可空集合；(b) **离点确认证据组合没有需求条目载体**，作为实施决策加注，不表述为需求；(c) `byDefaultMissions` 是路径段不是字段，基线措辞的正确读法须记录。 |
| **票 15** | 无直接影响。但本票的 `REQ-0290` 是**第三个**「批次 0 条目与完整产品语境不符」的实例（前两个是票 11 的跨 Map、票 13 撞见的 `REQ-0298`），**且它的解法与前两个都不同**——不是 Out of scope，也不是需求变更，而是**剖面判定错误、需求文本本身没问题**。票 15 判「是否对 348 条做专门冲突复核」时应把这第三种形态算进去。 |

## 四、剖面影响

| 项 | 变更前 | 变更后 |
| --- | --- | --- |
| 总行数 | 348 | 348（不变） |
| 批次 0（`FP-B0`） | 167 | **166** |
| 待排期（`FP-C*`） | 81 | **82** |
| Out of scope（`OOS-*`） | 100 | 100（不变） |
| `FP-C4 空闲返回与等待点` | 9 | **10** |

`evidence/full-product-implementation-profile-draft.tsv` 11 列不变，行尾 LF 口径不变
（CRLF 计数 0）。新 SHA-256：

```
bf6cae31432dcaaebcb0b6e5b668ddeb5ee7155d315a1c779d946f737e2a84e4
```

## 五、写回 `CONTEXT.md` 的领域词

三个词条，全部写入末尾「实施范围与顺序」一节：

1. **`WaitingPointDepartureConfirmation`（等待点离点确认）** —— 新造。Q4 定的四项一致证据
   组合。它对称于 `REQ-0295` 的到点确认，但**基线没有对应条款**，是本票的实施决策。
2. **`StopPurposeCategory`（停靠目的类别）** —— 新造。Q5 定的第三个正交维度。
3. **`VehiclePurposeClaim` 词条补注** —— 该词条（`CONTEXT.md:1647`）已存在且措辞正确，但
   未说明它与 `DispatchUniquenessGuard` 的层次关系。补一句：前者是**用途层**、跨多个订单，
   后者是**订单层**，二者并存不冗余。

## 六、未证明项与悬着的事

1. **等待点的现场值全部未知。**数量、在图上的位置、`WaitingPointVehicleScope` 白名单配置，
   三者都要现场测绘后才有。属实施图的现场准备步骤，本工作区查不到。
2. **离点确认的「车辆处于运动态」用哪个 RIoT 字段判，未查。**Q4 定的是证据构成，不是字段
   映射。`GetVehicleExecutionFactsAsync` 与 `GetVehicleCardAsync` 是候选来源面，属实施图。
3. **RIoT 调用白名单文档的位置是脆弱的。**它在
   `.scratch/current-requirements-baseline/issues/37-...md`，是**另一张已完成地图的工作票据**，
   不是产品文档。`REQ-0294` 正文引用「现有白名单」指的就是它。那份 scratch 若被清理，白名单
   就没有权威副本了。属文档治理，本票不处置，记给票 10。
4. **vendored 包的溯源已断**（票 03 已记，本次复核确认）：`vendor/nuget/riot-sdk/0.1.0-controlserver.2/README.md:5-7`
   记的 commit `e708f874…` 在 2026-09-02 历史重写后不存在，而
   `RiotSdkPackageProvenanceTests.cs:10` 仍在断言这个 hash 出现在 nuspec 里——该断言只比对
   包内元数据字符串、不解析 commit，**所以仍会通过**。这不是本票要处置的，但它说明那条
   供应链测试证明的是「包没被换掉」，不是「包来源可追」。
5. **交接预告的第五次「能力藏在批次 0」线索仍未验证。**
   `TransportDemandSuppression`、`LoadPreparationAlert`、`UnassignedDemandBacklog`、
   `AreaEqpUniquenessMonitor`、`DispatchZoneAreaAssignment`、`EnRoutePickupDeliveryDelay`
   六个零命中标识符**不是**本次找到的第五次，它们指向的批次 0 条目本票未复核。票 09 照旧
   逐条查。

## 七、复核副产品

1. **`REQ-0147` 是 `RoutineOrderCreationCall` 的真正需求载体，且它在批次 0。**本图此前没有
   任何票据引用过它。它的正文把白名单写死了（「模板建单、订单组合、改单不获批」），是
   `REQ-0294` 那句「现有白名单也明确禁止这些调用」在需求基线内的对应物。
2. **`REQ-0323` 明文「地图可以包含公共业务点、等待点、充电点及其它普通 Station」**，且它在
   批次 0。这条与 Round 43 的实测（206 站全是机台与关卡）不矛盾——它规定的是**解析规则**
   （非 AREA 命名不算解析失败），不是断言这些站点已存在。
3. **RIoT 的 Station `type` 字段在 mapId 25 上恒为 1。**这意味着即使将来测绘了等待点，
   **RIoT 侧也不会给出角色区分**，角色只能在 8005 侧登记——`REQ-0289` 的「以明确的 RIoT
   地图 + 站点登记」指的是**用地图与站点标识来指认**，不是「RIoT 里有一个等待点类型」。
   `CONTEXT.md` 的 `_Avoid_: RIoT 原生业务站点类型` 早已写明，此处是实测确认。
