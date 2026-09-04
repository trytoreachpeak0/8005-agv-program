# 票 04 决议：自动充电桩调度与充电失败治理的范围

日期：2026-09-04。批准人：用户本人（本图默认且唯一最终批准人）。

十一问全部定案：Q2 后半段与 Q3 由用户直接给出现场事实并改判，其余九问取本票推荐值。

## 一、事实基础

### 1.1 `FP-C1` 在控制服务端是整簇零实现，比票据原先设想的更彻底

20 个充电标识符在 `8005-agv-control-server/src/` 下**全部零命中**：`ChargeHangReassign`、
`ProjectExclusiveChargingStationRegistry`、`ChargingStationExclusiveReservation`、
`ChargingStationAllocationHold`、`VehicleChargingEligibilityHold`、
`ConfirmedChargingInterruption`、`ConfirmedChargingNoProgress`、`ConfirmedUnableToCharge`、
`ChargingProgressObservationPolicy`、`ChargingRIoTVehicleObservationLoss`、
`ChargingBatteryTelemetryLoss`、`ChargingStationRecoveryConfirmation`、
`MandatoryChargeEntryThreshold`、`ChargingCompletionThreshold`、`ChargingPolicyVersion`、
`DispatchBatteryEligibility`、`RouteCostEquivalenceBand`、`NearStationQuery`、
`DeterministicDispatchTieBreak`、`407802`。

整个 `src/` 里含 `Charg`（大小写不敏感）的只有 **3 行**，分布在 3 个文件：
`ControlServer.Domain/WireToGateModels.cs:92`、
`ControlServer.Host/Runtime/JourneyRuntimeEngine.cs:563`（字符串常量 `"CHARGING"`，是 RIoT 的
电池状态取值）、`ControlServer.Host/Transport/OnboardJourneyPublisher.cs:87`。

### 1.2 MVP 的「电量门禁」是一个标量，且「提示人工充电」根本不存在

实际存在的是 `JourneyRuntime:minimumBatteryPercent`（`ControlServer.Host/appsettings.json:57`，
当前值 30；代码默认值同为 30，见 `Runtime/JourneyRuntimeOptions.cs:20`）。它在
`Runtime/JourneyRuntimeEngine.cs:561-565` 的 `ValidateDynamicFacts` 里被使用：

```
561	        if (vehicle.BatteryPercent is null || string.IsNullOrWhiteSpace(vehicle.BatteryState))
562	            return "BATTERY_FACT_UNKNOWN";
563	        if (string.Equals(vehicle.BatteryState, "CHARGING", StringComparison.Ordinal) ||
564	            vehicle.BatteryPercent < runtimeOptions.MinimumBatteryPercent)
565	            return "BATTERY_POLICY_NOT_SATISFIED";
```

「阻断新任务」不是一段独立分支，而是这个返回值让候选落不进 `eligible` 列表
（`JourneyRuntimeEngine.cs:277-281` 把 reason 写进 `JourneyBacklog`，`:286-289` 候选为空即返回）。

**「提示人工充电」这段代码不存在。**`src/` 下没有任何把 `BATTERY_POLICY_NOT_SATISFIED` 或
`BATTERY_FACT_UNKNOWN` 转成人工充电提示、告警或车载消息的路径，这两个值只落进 backlog 的
reason 字段。`docs/RELEASE-CANDIDATE.md` 全文**不提充电、电量或 battery**——MVP 的 RC 从未
把任何充电行为纳入范围。

### 1.3 `ManualChargingHold` 没有生产者，是协议 payload 上的占位字段

赋值点只有两处，**两处都是硬编码 `false` 字面量**：`JourneyRuntimeEngine.cs:669` 与 `:736`
（`new VehicleBusinessProjection(revision, "READY", false, "SUFFICIENT", [])`）。同一处的
`BatteryState` 硬编码 `"SUFFICIENT"`，与 `:561` 从 RIoT 读到的真实 `vehicle.BatteryState`
**没有任何连接**。`src/` 下没有任何代码读取或消费 `ManualChargingHold`。

协议侧的对应事实：`VehicleBusinessStateSnapshot.schema.json:64-90` 的 `manualChargingHold`
（boolean）与 `batteryState`（enum `SUFFICIENT`/`LOW`/`UNKNOWN`）都是 `required`；
`common/types.schema.json:94` 有错误码 `MANUAL_CHARGING_HOLD_ACTIVE`。

### 1.4 协议 v1 已有一对完整的充电人工确认消息，且控制服务端零实现

`ManualChargingReturnToServiceRequested` / `ManualChargingReturnToServiceResult` 在
`manifest/release.json` 的 **54 条消息面之内**（`denylistedMessageTypes` 的 11 条里没有它们），
并有完整正反向量（`examples/invalid/ManualChargingReturnToServiceRequested/` 下十余个）。

其 payload 形态是本票要复用的范式：`requestId`（幂等）+ `administrator`（`OperatorContext`）
+ `administratorRole`（enum **`MAINTENANCE_ADMINISTRATOR` / `SYSTEM_ADMINISTRATOR`**）
+ `reason` + `observedBatteryPercent`。`correlationId: null` 表明它是发起消息，方向是车载 → 服务端。

**控制服务端 `src/` 与 `tests/` 对 `ManualChargingReturnToService` 零命中。**协议承诺了、有向量、
两端没实现。本票只记录该事实并交票 06 与票 08，**不开缺陷**——MVP 收尾属本图 Out of scope。

### 1.5 RIoT 有专门的充电 API 面，但 8005 不用它；本票一度断言错误

**本票初查时断言「RIoT 没有任何充电专用接口」，那是错的**，原因是只查了 vendored Facade 层的
符号表。穷举四份 OpenAPI 描述（`task` 86 条、`order` 30 条、`imap` 34 条、`device` 36 条，
共 186 条路径）后，充电相关的路径是：

| 方法 | 路径 | summary |
| --- | --- | --- |
| POST | `/api/task/v1/order/charge/{vehicleKey}` | 指定车辆充电 |
| GET/POST | `/api/task/v1/chargeConfig`（含 `/delete/{id}`、`/getAgvGroup`、`/getDefaultConfig`、`/{id}`，共 6 条） | 自定义充电配置管理 |
| POST | `/api/task/v1/statistics/chargeCount`、`/chargeLocationCount` | 充电统计 |
| GET | `/api/imap/v1/mapInfo/getStationCustomAttributes/{mapId}?stationType=CHARGE_POSITION` | 按 `CHARGE_POSITION` 列出站点 |

这正是 map Notes 第 23 条那条教训的第二次实例——**穷举来源面，不要只看最像的那一层**。

**但 8005 不使用这套。**已有的边界决定见 Round 24 与 Round 25 的计划与日志
（`rcs/riot-behavior-lab/evidence/rounds/2026-07-21-round-24/round-plan.md:5`「MES/业务不能用
RCS 自带充电功能，需用订单两段任务」、`:18`「不调用 RCS 充电桩/自动充电接口」；round-25 的
`execution-log.md:42`「RIoT 自动充电未启用；充电由 MES 订单触发」）。`REQ-0294` 对一键停靠与
`parkConfig` 的禁止是同一条边界的另一半。

### 1.6 充电订单不是单段 move，而是 `move(目标站) + act(78, param1=1)`

Round 24 实测（`rcs/riot-behavior-lab/hypotheses/open-questions.md:264-289`，Q-033）：

- `act` 的模板动作是 RIoT 里现成的：`actionId=78`，`actionParam1=1` 为「开始充电」、
  `actionParam1=2` 为「结束充电」，`actionParam2` 均为 0（实测响应
  `evidence/rounds/2026-07-21-round-24/runs/PROBE-action78.json`，两条模板均 2023-08-30 由 admin 建）
- **离桩靠再下一张订单**，RIoT 在队首**自动插入** `act(78,2,0)`（round-25 `execution-log.md:37`）
- 接上充电器后 `batteryState` 由 `NO_CHARGE` 转 `CHARGING`，act 结束，订单 SUCCESS（同上 `:31`）

而 vendored facade 的建单方法**建不出这种订单**：`OrderClient.CreateMoveOrderAsync`
（`riot-sdk/csharp/RIoT.Sdk.Facade/OrderClient.cs:18-43`）内部写死了单元素 `Mission` 数组、
`Type = "move"`，没有 act 参数也没有重载。控制服务端当前唯一的建单路径
（`ControlServer.Infrastructure/Adapters/HttpRiotMovementGateway.cs:93-99`）就是它。

**`CONTEXT.md:752` 的 `RoutineOrderCreationCall` 词条把「前往充电桩」写进了「单段移动意图」，
与这条现场事实矛盾。**本票改这条词条（见第五节）。

### 1.7 充电桩在 8005 的自建机制下是普通站点，RIoT 侧无任何字段能标识它们

**这一条由用户 2026-09-04 直接给出，取代了本票原先基于 `type=2` 的推断。**

- 若要用 RIoT 本体的充电机制，站点**必须**设置成充电桩 type；
- 若自建充电机制（普通订单里加移动与充电动作，即 1.6 的形态），**不需要充电站 type，普通站点即可**；
- map 25 当前**还没有设置充电桩站点**——桩本身还没安装好，装好后它们会是**普通站点**；
- **装完之后想知道哪些 id 是充电桩，只能问用户，不能通过查 `type` 找到。**

这比票 12 记的「现场尚未测绘」更强：不是「现在观测不到、补测绘后能观测到」，而是
**8005 选定的机制决定了充电桩身份永远不可从 RIoT 观测中推导**。

它同时收窄了此前两条实测的可推广性。Round 43 实测 map 25 的 206 个站 `type` 恒为 1、
`user_define_properties` 全空（`evidence/rounds/2026-09-03-round-43/runs/004-stations-map-25.json`，
本票独立复核：206 个对象字段完全一致的 28 个字段，`type=1` 206/206、`desc=""` 206/206、
`param=0` 206/206、`user_define_properties={}` 206/206）。Round 42 实测 map 19 上充电桩确实
以 `type=2` + `user_define_properties.enter_exit` 出现
（`evidence/rounds/2026-08-04-round-42/runs/020-map-19-stations.json`，id 30「充电桩」、
294「充电桩5」、378「充电桩-新」；`type` 分布 `{1: 441, 2: 3}`），且 `type=2` 并不充分——
id 308「夹抱充电桩」是 `type=1` 而 `enter_exit` 有值。**这两条实测的正确读法是：`type=2` 是
RIoT 本体充电机制的标记，而 8005 不走那条路，所以它对本项目没有判别力。**

### 1.8 站点占用无法从 RIoT 按站点查询，且「无人正前往」原则上不可观测

穷举四份 spec：`reserv*` / `busy*` / `free*` **零命中**；`occup` 只有
`机器人卡片返回对象.occupyDevices`（「被交管的车辆」）；`lock` 只有车辆级的 `lockStatus`。
站点侧只有 `ListStationsAsync` / `ListStationsStrictAsync`，返回目录不含占用状态。

最接近的是交管资源面 8 条（`/api/task/v1/traffic/*`），但其 key 是 deviceKey 与
node/edge 资源标识（实测形态 `node-map-11.4`、`edge-map-11.36`，
`evidence/rounds/2026-07-21-round-26/round-plan.md:19`），**不是 stationId**。

已成契约的硬上界是 `BC-VEH-006`（`rcs/riot-behavior-lab/knowledge/behavioral-contracts.md:415-426`）：
车侧 `(currentMap, currentPosition)` 可辅助证明「**已经**占用」，但
**「不能把未见本地预占解释为『空闲且无人正前往』」**（`:426`）；`currentPosition=0` 同时出现在
在线离站、移动中与断线/定位错误三种车辆上，只能判未知（`:421`）。

**车辆规模的记载须纠正**：18 台车是 Round 42 在 `RIOT-CROSS-PROJECT-TEST`（build 2.2.0.30，
`172.10.1.72:8888`）上观测的，当时 8005 生产环境不可达（`round-42/execution-log.md:7`）。
Round 43 打到了生产环境 `RIOT-8005-RUNTIME`（2.2.0.14，`172.19.206.222:8888`）但只做地图与
路由只读，**没有采车辆列表**。8005 生产 RIoT 上有多少台车，本图未知。

### 1.9 RIoT 订单命令面全在，8005 一条都没接

vendored `RIoT.Sdk.Facade 0.1.0-controlserver.2` 的符号表里 39 个 `*Async` 方法全在场，包含
`REQ-0148` 批准的全部四个命令：`CancelOrderAsync`、`OrderHoldAsync`、`OrderContinueAsync`、
`HangContinueAsync`，以及底层的 `PostOrderCommandAsync`。另有
`GetDispatchableVehiclesAsync`、`ListDevicesAsync`、`QueryNearestEndAsync`、
`QueryNearestStartAsync`、`GetRouteCostAsync`、`DispatchEnableAsync`/`DispatchDisableAsync`
等控制服务端未使用的能力。**同一张符号表里 `Charg*` 一个都没有**——充电能力在 Generated 层与
spec 里，不在 Facade 层，这正是 1.5 那次误判的成因。

控制服务端这侧：`IRiotMovementGateway` 只有 `ReconcileByUpperIdAsync` 与 `CreateAsync`
两个方法（`ControlServer.Application/Ports.cs:14`、`:16`），`riotSession.` 的全部调用点只有
6 处（`HttpRiotMovementGateway.cs:51`、`:93`、`:154`、`:190`、`:230`、`:232`），
**没有任何一个是命令**。`src/` 下向 RIoT 取消订单的路径**零命中**。

取消的端点与终态已由实测确定（`knowledge/behavioral-contracts.md:171-181` BC-ORDER-003）：
`POST /api/task/v1/order/command/{orderKey}` 带 `{"commandType":"CMD_ORDER_CANCEL"}`，
对执行中单段 move 可达 `orderState=2 CANCELLED`（`missionState=4`），车侧回 `IDLE`。

**全图此前无人认领这个面**：15 张票据里 `CANCEL` 只出现在票 04 自己的问 4，
七张已闭决议里 `CANCEL`／`取消订单`／`CMD_ORDER`／`REQ-0148` **全部零命中**。

## 二、逐问定案

### Q1 — `REQ-0281` 与 `REQ-0282` 改判出批次 0，并入 `FP-C1`，均判增量类

**改判成立，判据与票 12 改判 `REQ-0290` 完全相同。**

检出手段是**按 MVP 剖面的 `ControlServerImpact` 分组**：串为
「以电量门禁阻断新任务并提示人工充电。」的条目**恰好 3 条**——`REQ-0281`、`REQ-0282`、
`REQ-0290`，三条的 `OnboardHmiImpact` 与 `SharedProtocolImpact` 也逐字相同。票 12 已据同一
判据把 `REQ-0290` 改判出批次 0，**另两条仍标着 `FP-B0`**。这是一个封闭枚举：充电这一簇的
批次 0 判定全部出自这一个影响串，三条现已全部处置完毕。

| 条目 | 基线要求 | 代码现状 | 批次 0 判定在什么形态下成立 |
| --- | --- | --- | --- |
| `REQ-0281` | 三个阈值 + 硬关系 `完成 > 强制入口 >= 任务后余量`；「达到完成阈值不等于订单收敛、离桩或释放预占」 | **一个**标量比当前电量；`ChargingCompletionThreshold`／`DispatchBatteryEligibility` 零命中 | 单一固定行程 + 无充电周期。MVP 只有一条固定路线，故「预计任务后余量」可折叠进一个常量；无充电周期则完成阈值无所指、三方硬关系空转 |
| `REQ-0282` | `ChargingPolicyVersion` 受证据批准、按周期冻结、既有周期用原快照、无已批准版本不得投运 | 一个 `appsettings.json` 整数，无版本、无批准记录、无快照 | 单参数单车下「部署时那个配置文件即已批准版本」。完整产品有多参数、多车、并发充电周期，快照隔离与「无批准版本不得投运」那道门在代码里不存在 |

分类：**两条均判增量类**。它们建立在 B1（`VehiclePurposeClaims`）与 B4（站点独占）之上，
不推翻 I1～I6 中任何一条——与票 02 定的「全新能力不等于重构」一致。

`REQ-0208`（`FP-B0`，「电量和仓位首先是硬资格」）有同样的形态依赖：代码比的是**当前**电量而
非「预计完成任务后的最低余量」，该折叠只在单一固定行程下成立。**但它属 `FP-C2`、票 03 已闭，
本票不改判它**，只带证据标为候选交票 09 复核（见第三节）。

### Q2 — 充电桩占位取「项目独占为现场前提」，轮询其它车辆降级为辅助告警

**用户 2026-09-04 确认：不会有其它项目的车占用 8005 的充电桩。**

原先考虑的「轮询全部车辆比位置」被 `BC-VEH-006` 证明**单独不成立**——它只能证明「已占用」，
永远证不出「空闲且无人正前往」，而 `ChargingStationOccupancy` 要的恰恰是后者
（_Avoid_ 明列「仅凭当前无车占位推定为项目独占」）。

**定案：**

1. **占位判据只覆盖本项目车辆 + 8005 自己的 B4 预占表。**依据是 `REQ-0171` 名册的全称就是
   「项目**独占**充电桩名册」，而 `ChargingStationOccupancy` 的 _Avoid_ 把「共享桩、归属未知桩」
   挡在名册准入之外——**「独占」本身就是那条现场前提，不是需要另外观测的事实**。
2. **发现非本项目车辆占位时告警并 fail-closed 排除该桩**，但这条路径是辅助防御，不是资格判据；
   它不因无法穷举全部车辆而阻断自动充电。
3. **`ChargingStationOccupancy` 因此不是 `证据受限实施`。**该形态要求判据依赖的外部证据恒不可得
   而门禁恒走保守分支；这里的证据是可得的（本项目三台车的 `(currentMap, currentPosition)`
   已在用），只是不覆盖非本项目车辆，而现场前提使那部分不必覆盖。

### Q3 — 不做探测；充电桩身份永远只能来自名册，不能从 RIoT 推导

**用户 2026-09-04 直接给出事实并否决探测**（见 1.7）。这条回答改变了这件事的**性质**，不只是
它的证据来源：

**定案：**

1. **`ProjectExclusiveChargingStationRegistry` 是充电桩身份的唯一来源，且不可与 RIoT 交叉校验。**
   名册里的 `(mapId, stationId)` 无法用 RIoT 的任何字段验证「这个 id 真的是一个充电桩」。
   这正是 `StationOperationalRole` 词条已写的「角色不能由站点名称、坐标或现场习惯猜测」，
   现在它对充电桩是**唯一可能**，不是保守选择。
2. **名册录入是人工口述输入。**`REQ-0171` 要求的「批准/变更记录」因此不是形式主义——**它是
   唯一的可追溯性来源**。本票不另加机制，以 `REQ-0171` 的批准记录本身作为录入门禁。
3. **录错一个 id 的失效模式必须写进实施图。**车会开到一个普通工作站去执行 `act(78,1,0)`，
   那正是 Round 24 场景 S1（不接充电器）的形态，结果是 HANG + 407802 →
   `ConfirmedUnableToCharge` → `ChargingStationAllocationHold` 暂停一个**根本不是桩的站点**，
   同时把一台车卡进清桩流程。
4. **三态划分（照本票推荐值）：**
   - **名册为空 = 功能未部署** → 退化到 `ManualChargingHold` + `ManualChargingReturnToService`，
     即 MVP 现有的那条路，**不静默**；
   - **名册非空但当前无合格桩** → 保持在待充电排队集合、告警、不猜站点（与 `REQ-0178` 的
     「无合格点时原地排队并告警」同构）；
   - **名册非空且有合格桩** → 正常自动周期。
5. **第一态是投运第一天的真实状态，不是边角情况。**桩物理上还没装好，名册必然为空，且会持续到
   安装完成为止。故 `FP-C1` 的验收出口条件必须含「充电桩安装完成 + 名册录入」这个现场前置
   （交票 08），批次排期不得假定投运即可自动充电（交票 09）。
6. **`n` 不写进规格**，桩数配置驱动，与票 12 的等待点一致。
7. **不得归入 `证据受限实施`。**理由与票 12 的 Q1、票 13 的 `FP-C9a` 相同：证据不可得是设备
   尚未安装造成的，装好并录入名册后**无需改代码**。

**这条同时消掉了本票与票 12 之间的一处不对称。**票 12 只定了「等待点空集合 ≠ 异常」且静默；
充电这边空名册**不静默**，因为到阈值的车既不能充也不能接搬运，静默会让运力无声下降。两者的
差别不是处置不一致，而是后果不同：等待点空集合车原地不动无害，充电桩空名册等于车退出服务。

### Q4 — 全链路自动，不主动腾桩；释放预占用票 12 的 B4 离点证据

**自动化边界：**从 `MandatoryChargeEntryThreshold` 触发、待充电排队、选桩、
`ChargingStationExclusiveReservation` 原子预占、建单、物理充电、到 `ChargingCompletionThreshold`
**全部自动**；人工只出现在三个「系统事实不足」的确认点（Q8）。

**释放预占取票 12 已定的 B4 离点证据四项**，充电桩不另立一套：`currentMap` 仍是本图 +
`currentPosition` 不再精确匹配该桩 + 车辆处于运动态 + 全部证据新鲜且无冲突。这正是
`REQ-0281`「达到完成阈值不等于订单收敛、车辆离桩或预占释放」落到实现上的形态。

**不主动腾桩**，而且这不只是政策选择——**RIoT 的机制就长这样**：离桩由下一张订单触发，
`act(78,2,0)` 由 RIoT 在队首自动插入（1.6），8005 没有单独的「离桩」动作可下。所以：

- 充电完成后释放 `CHARGING` 用途占有，走 `REQ-0290` 的用途优先级重评；
- 车**因为取得了新用途**（搬运，或其次空闲返回）才离桩，不因为充满了；
- 这与 `MapWaitingPointPool` 的 _Avoid_「达到充电完成阈值即返回」一致，不违反基线。

**代价要交票 08 与实施图：桩数 < 车数时，充满的车占着桩会饿死低电车。**当前 3 桩 3 车不触发，
但桩数可配置意味着这是一条现场配置约束；建议名册校验加一条「桩数 < 车数」告警。

### Q5 — 共用一个分配核心，但排序键不合并：先判用途，再选资源

两套独立选择器会在同一张 `VehiclePurposeClaims` 表的同一行上竞争，而票 12 已把原子性定为
「捕获主键冲突」——两套选择器就等于靠冲突重试来仲裁优先级，会把「强制充电高于普通搬运」变成
时序问题。

**定案的三步形态：**

1. 每轮先对**尚无占有**的车按 `REQ-0290` 的三级优先级判本轮用途（强制充电 > 普通搬运 >
   空闲返回）；
2. 再按用途分头选资源——`CHARGING` 走桩选择（在已过滤桩集合上算最近，按 `REQ-0172` 的
   **当前电量**排序决定谁先取桩）；`TRANSPORT` 走票 03 定的选单选车（成本档 β）；
   `IDLE_RETURN` 走票 12 的等待点选择；
3. 两个排序键（充电按当前电量、搬运按新增行程成本）**作用在不相交的车辆子集上，因此永不需要
   合并**。

这一步正是 `REQ-0290`「电量允许时先执行 `TaskFirstDispatchSelection`，只有没有合法搬运用途时
才评估空闲返回」的实现形态。**抢占同一台车不存在**——用途占有由主键唯一保证，先取得者胜，
后者本轮不派。

### Q6 — 清桩闭环一次做完，不拆子集

`REQ-0178` 的「旧充电订单必须在清桩前确认取消终态，取消结果未知时继续对账而不完成清桩」与
`REQ-0179` 的两种完成证明是**同一个状态机的两条出边**，拆开会造出「已确认充不上但没有腾桩
路径」的中间态——那正是 `ChargingStationClearancePending` 词条 _Avoid_ 里禁止的
「订单已取消、充电桩已恢复、车辆已就绪」误解。

而且 `ChargingStationAllocationHold` 一触发就把桩移出运行时候选，3 桩 3 车下等于损失三分之一
运力，**没有闭环就没有恢复路径**。

前置可满足：`CancelOrderAsync` 在 vendored 包里在场（1.9），取消终态已由 BC-ORDER-003 实测。

### Q7 — `ChargeHangReassign` 进本期；选桩走票 14 的自建图，不调 `queryNearEnd`

**进本期**，三条理由：

1. 改派用的候选链**就是 `REQ-0170` 的那条链**，而 `REQ-0170` 是重构类 B4 必须做，改派只多一个
   「排除刚失败的站点」的过滤项——**延后它不省工程量，只省一个过滤条件**。
2. 不做改派的话，第一次充电失败就 `ChargingStationAllocationHold` 原桩、该车进
   `VehicleChargingEligibilityHold` 且无处可充，3 桩 3 车下直接损失一台车。
3. 与票 03 分配核心的耦合点只有一个——改派车辆按 `REQ-0172` 进**同一个**待充电排队集合、
   按当前电量排序、不取得独立优先级，**而这正是 Q5 已定的形态，不引入第二个耦合点**。

**选桩用票 14 的 `RouteGraphSnapshot` 自建图算成本，不调 RIoT 的 `queryNearEnd`。**两条理由：
其一，`queryNearEnd` 入参只有 `mapId` + 起点 + 候选列表，**没有任何空闲/占用过滤**，返回单个
int 也带不出状态；其二，Round 43 实测——候选集合或起点含一个有向图不可达站点时，整个查询抛
`java.lang.NullPointerException`（`code=00002`，栈帧 `WorldRoute.queryNearestEnd:293`，
契约 BC-ROUTE-002）。这与票 14 的 Q1 已定的「`getRouteCostsBy` 与 `queryNearEnd` 一律退出产品
代码路径」一致，**不是本票新开的口子**。

`REQ-0170` 的「`NearStationQuery` 只对这个已过滤集合计算，不得从全图或失败站点中回填」因此
读作：过滤在前、成本计算在后，而成本计算的权威是自建图。

### Q8 — 名册走受控预置配置；四个人工动作按「对象里有没有车」分端

**名册：受控预置配置 + 版本化审计表，不做 UI，不进票 05 的治理面。**依据是 `REQ-0288` 把名册
变更限定为「只有永久拆除、改名、换地图或退出 8005 才修改名册」——极低频，物理拆装才改。
运行期真正高频的是暂停与恢复分配，而 `REQ-0288` 明文那**不是**名册变更（「不临时删除名册身份」）。

**四个人工动作的分端判据是：动作的对象里有没有车。**有车说明人就在现场、在车旁、要看着那台车
那个桩；只有桩说明车可能不在、三台车都可能不在。

| 动作 | 对象 | 落点 |
| --- | --- | --- |
| `UnableToChargeFieldConfirmation`（充不上现场确认，`REQ-0176`） | 车 + 桩 | **车载 HMI**，新协议消息对 |
| `ManualStationClearanceConfirmation`（人工清桩确认，`REQ-0179`） | 车 + 桩 | **车载 HMI**，新协议消息对 |
| `ChargingStationAllocationHold`（授权维修触发的暂停，`REQ-0288`） | 只有桩 | **ControlServer 侧，不进协议** |
| `ChargingStationRecoveryConfirmation`（桩恢复确认，`REQ-0288`） | 只有桩 | **ControlServer 侧，不进协议** |

**这把协议面增量压到两对消息（4 条）**，形状照抄 1.4 已有的
`ManualChargingReturnToServiceRequested`/`Result`。

**与票 05 的交接点是一条本票新发现的硬约束（见第三节）：`REQ-0254` 不得单独砍。**

### Q9 — RIoT 订单命令面立为跨簇工程大件，不归 `FP-C1`

它同时服务三个簇：`FP-C1`（`REQ-0178` 清桩前确认取消终态、`REQ-0170` 改派前 CANCEL 旧 HANG）、
`FP-C2`（`REQ-0197` 有界删除停靠——已建单的停靠被删除需要取消）、`FP-C4`（`REQ-0296` 空闲返回
已确认失败后的释放）。

**定案：照票 14 处置 `RouteGraphSnapshot` 的先例，由本票命名为一个跨簇工程大件，票 09 排期，
不计入 `FP-C1` 的条目数。**它的内容不只是「加一个 `CancelAsync`」——`REQ-0178` 要的是
「取消结果未知时继续对账而不完成清桩」，即命令面必须继承 `RIoTRetryReconciliation` 的对账
语义，与建单侧同构。

`REQ-0148`（`FP-B0`，`ControlServerImpact` 写「实现指定车辆的查询、建单、**命令**和对账边界」）
标为「批次 0 判定只在『MVP 从不需要发命令』这一形态下成立」的候选改判，证据交票 09——
**本票不改判它，它不属 `FP-C1`**。

### Q10 — 删 `ChargingStationReservation`，保留 `ChargingStationExclusiveReservation`

两条是同一个概念的两个词条（`CONTEXT.md:1095` 与 `:1631`），**且两个都不在基线里**（基线用
中文散文「原子预占」表达，四个候选标识符 `ChargingStationReservation`、
`ChargingStationExclusiveReservation`、`ChargingStationOccupancy`、`SingleBerthStationClaim`
在 348 条全文里各 0 命中）。

保留 `ChargingStationExclusiveReservation`：定义更完整，且 `ChargeHangReassign` 词条正文
（`CONTEXT.md:1092`）引用的是它。删除不动基线。

另加一条层次补注：**B4 的三个角色化名——`SingleBerthStationClaim`（公共业务点）、
`WaitingPointExclusiveClaim`（等待点）、`ChargingStationExclusiveReservation`（充电桩）——
是同一个原语在三种站点角色上的实例**，票 12 已定它们共用同一张 `(MapId, StationId)` 表。
做法与票 12 给 `VehiclePurposeClaim` 和 `DispatchUniquenessGuard` 加层次补注一致。

### Q11 — 充电建单扩为 `RoutineOrderCreationCall` 的第二种获批形态

`RoutineOrderCreationCall` 的「单段 move」形态**表达不了充电订单**（1.6），三条路里取 (i)：

- **(i) 扩为第二种获批形态「`move(目标桩) + act(78,1,0)`」**，仍用稳定 `upperId`、仍先确认
  车辆可调度与目标站可达、仍完整继承 `RIoTRetryReconciliation`；
- (ii) 改用 RIoT 自带的 `POST /api/task/v1/order/charge/{vehicleKey}` —— **否决**。它与
  Round 24/25 已记录的边界决定「MES/业务不能用 RCS 自带充电功能」冲突；它零实测（返回体、
  选桩规则、失败码全未知）；**而且用户已明确指出走这条路要求把站点设成充电桩 type**，那与
  Q3 定的「充电桩是普通站点」互斥；
- (iii) 不做自动充电、`FP-C1` 整簇延后 —— 否决，基线要求自动充电，且 3 桩已在采购安装中。

**(i) 是唯一同时满足「基线要求自动充电」「不启用 RCS 自带调度」「调用面可白名单化」的形态。**

三件附带的事：

1. **这是给票 10 白名单问题的新条目**——获批调用从一种形态变两种，而白名单当前是另一张已完成
   地图 scratch 里的一份纯文档（票 12 的 Q8 已记）。
2. **实现路径属实施图**：facade 缺这个方法，走 `Raw`（票 12 已确认 `OrderClient.Raw` 是 public）
   还是给 `riot-sdk` 加一个 `CreateChargeOrderAsync` 再切新 vendored 包，本票不定。
3. **`CONTEXT.md:752` 的 `RoutineOrderCreationCall` 词条要改**——它把「前往充电桩」写成单段
   移动意图是错的（见第五节）。

## 三、对其他票据的影响

**票 05（治理面增量）—— 一条硬约束：`REQ-0254` 不得单独砍。**

`REQ-0254` 是本票四个人工动作里三个的**唯一有效身份模型载体**，而它在 map Notes 列的十条可砍
权限条目里。事实链：

- `REQ-0176` 写「只有 R-11 可补充现场确认」、`REQ-0179` 写「『人工清桩』权限初始授予 R-11 与
  R-13」；
- `REQ-0254`（`FP-C6`）明文「票据 62 的专门权限并入管理员角色……这些能力**不再引用 R-11/R-13
  系统角色**，也不另建可独立分配的权限」，且它的来源票据 71 晚于 62（批准批次 `V1-APP-069`
  对 `V1-APP-047`／`V1-APP-048`）；
- `REQ-0270`（批次 0）另外明文「不恢复 R-12/R-13 为系统授权角色」；
- 批次 0 的权限骨架（`REQ-0250` 三种访问身份、`REQ-0251`／`REQ-0336` 两级管理员）里**没有
  R-11**；
- 协议 v1 已实装 `REQ-0254` 的模型——`administratorRole` 枚举就是
  `MAINTENANCE_ADMINISTRATOR`／`SYSTEM_ADMINISTRATOR`。

**砍掉它的后果不对称**：`REQ-0176` 写的是「R-11 **或等效维护权限人员**」，有退路；`REQ-0179`
写的是「初始授予 R-11 与 R-13」，**没有退路**——人工清桩确认会失去任何可授予的身份。

**这是 map Notes 里 `REQ-0311`／`REQ-0339` 之外的第三条跨簇耦合，且方向不同**：前两条是
「另一簇能力的安全前提」，这一条是「另一簇能力的唯一身份模型」。

另注：基线里同一个模式还有一处，但它是安全的——`REQ-0236`（`FP-C6`）把异常处置权限授予
R-09/R-11/R-13，而退役它的 `REQ-0253` 在**批次 0**，不在可砍清单里。

**票 06（协议 v2 冻结）—— 确定输入清单：**

1. **两对新消息（4 条）**：充不上现场确认、人工清桩确认，各一对请求/结果，形状照抄
   `ManualChargingReturnToServiceRequested`/`Result`（`requestId` + `administrator` +
   `administratorRole` 两值枚举 + `reason`）。
2. **`legType` 增 `TO_CHARGING_STATION`**（`UpcomingStopPlanSnapshot.schema.json:75-81`，
   当前 `["TO_PICKUP","TO_GATE"]`）；**`stopRole` 增充电桩取值**
   （`CurrentStopWorklistSnapshot.schema.json:92-98`，当前 `["PICKUP","GATE"]`）。
   `StopPurposeCategory` 的 `CHARGER` 值由票 12 定，本票不再提第四个值。
3. **不改 `manualChargingHold` 的含义。**本票 Q3 把「名册为空」定为退化到 `ManualChargingHold`，
   该字段因此保留原义作为那一态的载体，**充电周期状态另立字段**。含义变更在字段名不变时两端都
   静默编译，是最坏的一种 breaking；本票避开它。
4. **`ManualChargingReturnToServiceRequested`/`Result` 在 v1 的 54 条消息面里但控制服务端零
   实现**（1.4）。票 06 冻结 v2 时要决定它们是实现还是进 denylist。
5. `batteryState` 当前枚举 `SUFFICIENT`/`LOW`/`UNKNOWN` 三值是否够用，由票 06 连同 3 一并判。

**票 08（验收边界）—— 三条硬输入：**

1. **`FP-C1` 的验收出口条件必须含「充电桩安装完成 + 名册录入」的现场前置**（Q3 第 5 点）。
   桩当前尚未安装，投运第一天名册必然为空。
2. **`REQ-0174` 引的 407802 只在测试环境验证过**，见第六节。`REQ-0174` 要求的是「已经**目标
   build/契约验证**的失败码」，目标 build 上没验过。
3. **3 桩 3 车使 `REQ-0172`／`REQ-0173` 的排队与抢占语义在现场自然不触发**（票 02 已指出），
   验收证据怎么取归票 08；本票只指出，不替它判。另加一条同类：**桩数 < 车数时充满的车占桩会
   饿死低电车**（Q4），当前配置不触发。

**票 09（批次与依赖）—— 五条：**

1. **剖面变更**：`REQ-0281`、`REQ-0282` 改判进 `FP-C1`（第四节）。
2. **「RIoT 订单命令面」是一个跨簇工程大件**，服务 `FP-C1`／`FP-C2`／`FP-C4`，不计入任一簇的
   条目数，必须先于清桩、改派与有界删除停靠上线（Q9）。
3. **`REQ-0148` 是候选改判**，理由「批次 0 判定只在『MVP 从不需要发命令』这一形态下成立」，
   证据见 1.9。**本票不改判，它不属 `FP-C1`。**
4. **`REQ-0208` 是候选改判**，理由「代码比的是当前电量而非预计任务后余量，该折叠只在单一固定
   行程下成立」，属 `FP-C2`。**本票不改判。**
5. **`FP-C1` 依赖 `FP-C4` 的路径比票据原先记的多一条**：不只清桩要等待点，**正常充电完成后
   离桩也要靠取得新用途**（Q4），其中一条新用途就是空闲返回。故 `FP-C1` 不能排在 `FP-C4`
   之前这一点不变，理由加强。

**票 10（汇编）—— 一条：**获批的 RIoT 建单调用**从一种形态变为两种**（Q11），而白名单本身是
另一张已完成地图 scratch 里的纯文档（票 12 的 Q8 已记为「需求文本引用位置不稳的外部身份」
第三例）。票 10 汇编前须一并有结论。

**票 15（`REQ-0298` 冲突）—— 一条：**本票的 `REQ-0281`／`REQ-0282` 是「需求文本没问题、剖面
判定错误」这一形态的**第二与第三个实例**（第一个是票 12 的 `REQ-0290`）。票 15 第 3 问要判
「专门复核要复核哪一种」时，这个形态现在有三个实例，且**三个都是同一个 `ControlServerImpact`
串**——说明按影响串分组是这一形态的有效检出手段，可与票 13 加的第 11 列 `Batch0FormNote` 配合。
另一形态（逐条读基线文本找禁止性约束，如 `REQ-0298`）仍无票据系统性覆盖，本票未改变这一点。

## 四、剖面影响

| 项 | 前 | 后 |
| --- | --- | --- |
| 批次 0（`FP-B0`） | 166 | **164** |
| 待排期（`FP-C*`） | 82 | **84** |
| `FP-C1 自动充电桩调度与充电失败治理` | 17 | **19**（4 重构／15 增量） |

`FP-C1` 的重构 4 条不变（`REQ-0170` B4、`REQ-0172` B2、`REQ-0173` B1+B4、`REQ-0178` B2+B4），
增量由 13 增至 15（新增 `REQ-0281`、`REQ-0282`）。

Out of scope 的 100 条不变。TSV 改动两行三列（`FullProductCluster`、`ClusterBasis`、
`Batch0FormNote`），348 行 11 列与 LF 口径不变（349 个 LF、0 个 CRLF）。

`evidence/full-product-implementation-profile-draft.tsv` 的新 SHA-256：
`6eb323d47fe06c6f126b7eecbcdb9f85b1462c00823250d279bad7f5045c5fb0`（192,647 字节）。

## 五、写回 `CONTEXT.md` 的领域词

本票**不新增词条**——`FP-C1` 的约二十个词条基线制定期已经建齐。本票只做三处修正与补注：

1. **删除重复词条 `充电桩预占（ChargingStationReservation）`**（原 `CONTEXT.md:1631`），
   保留 `充电桩独占预占（ChargingStationExclusiveReservation)`（Q10）。
2. **修正 `RoutineOrderCreationCall`**：它把「前往充电桩」写进「单段移动意图」与现场事实矛盾
   （1.6）。改为区分两种获批形态：普通搬运与空闲返回是单段 move，前往充电桩是
   `move(目标桩) + act(78,1,0)`（Q11）。
3. **给 `站点业务角色（StationOperationalRole）` 加一条补注**：8005 自建充电机制下充电桩是
   普通站点，RIoT 侧无任何字段能标识它，名册是唯一身份来源，不能靠查 `type` 找到（Q3）。
   同时在该处记下 B4 三个角色化名共用同一原语的层次关系（Q10）。

## 六、未证明项与悬着的事

1. **`REQ-0174` 引的失败码 407802 只在测试环境验证过。**出处只有 Round 24
   （`evidence/rounds/2026-07-21-round-24/runs/S1b-hang-detail.json:115-116`，
   `"resultStr": "未知类型错误,导致订单挂起:错误编码为:407802"`；`:136` 的 `taskState`
   把它绑到 `7,78,1,0` 即 `act 78 param1=1`），而那一轮的范围写着「仅测试车；map30
   （api测试2）」，不是 `RIOT-8005-RUNTIME`。两个 SDK 仓库都没有错误码表，RIoT 自己也只回
   「未知类型错误」。`REQ-0174` 要求的是「已经**目标 build/契约验证**的失败码」——**目标 build
   上没验过**。已交票 08。
2. **8005 生产 RIoT 上有多少台车，本图未知**（1.8）。这不影响本票的任何定案（Q2 取现场独占
   前提，不依赖车辆规模），但它是此前「现场有 18 台车」这一说法的纠正。
3. **RIoT 的 `chargeConfig` 实测值是测试配置，不是 8005 的。**
   `evidence/rounds/2026-07-21-round-24/runs/PROBE-chargeConfig.json` 是真响应
   （`code:"0"`，`batteryLevelCritical:40`／`FullyRecharged:85`／`SufficientlyRecharged:50`／
   `enableIdleCharge:true`），但配置名是「新潮尊阳测试」、组名「测试」。8005 现场这些阈值的
   实际取值未知——**且本票取 (i) 自建机制后它们与本项目无关**，`ChargingPolicyVersion` 是
   8005 自己的策略，不读 RIoT 的 `chargeConfig`。
4. **充电桩的现场值全部未知**——数量、图上站点 id、名册配置，三者都要等桩安装完成后由用户
   给出（Q3）。属实施图的现场准备步骤，与票 12 记的等待点同类。
5. **`POST /api/task/v1/order/charge/{vehicleKey}` 与 6 条 `chargeConfig` 路径本票判为不使用**，
   故它们的返回体、选桩规则与失败码是否可知，本图不再追。
6. **票 12 记的「vendored `Generated.dll` 里 16 个 `Park*` 类型」口径应为 12**——按 `riot-sdk`
   的 C# 生成源码里 `public class/enum` 声明计数是 12，16 那个数大概来自 dll 反射。这不改变
   票 12 的 Q8 结论（一键停靠编译期可达、无守卫），只是计数口径。
7. **`useChargeLocationAsParkingLot`（「充电桩可作停靠站点」）是 RIoT `parkConfig` 的字段**，
   与 `REQ-0289`「等待点不得同时承担业务或充电角色」方向相反。当前无影响——8005 不用
   `parkConfig`（`REQ-0294` 明文禁止），但若将来有人开启 RIoT 本体停靠，两套角色定义会冲突。

## 七、复核副产品

1. **按 MVP 剖面的 `ControlServerImpact` 分组，是「能力藏在批次 0」这一形态的有效检出手段。**
   充电这一簇的批次 0 判定全部出自同一个影响串「以电量门禁阻断新任务并提示人工充电。」，
   恰好 3 条，现已全部处置。**票 09 逐条复核 164 条时可直接用这个手段**：同一个影响串下的
   条目，其批次 0 判定成立于同一个形态，一条被推翻则同串全部要重判。
2. **`docs/RELEASE-CANDIDATE.md` 全文不提充电**，而 MVP 剖面的 `ControlServerImpact` 写着
   「提示人工充电」。**剖面的影响列是范围制定期写的摘要，可能超出 RC 实际承诺的范围**——
   下断言时以 RC 与代码为准，不以剖面列为准。这与票 12 的方法论第 2 条（「票据里写的『已 X』
   可能是决策不是现状」）是同一类陷阱的另一面。
3. **只查一层抽象就断言能力不存在，会漏。**本票初查时因只看 vendored **Facade** 层的符号表
   （39 个 `*Async` 方法里 `Charg*` 零命中）而断言「RIoT 没有充电接口」，实际能力在 Generated
   层与 OpenAPI spec 里（1.5）。这是 map Notes 第 23 条的第二次实例，**第一次是票 03 的
   `getRouteCostsBy`**。教训收窄为一句：**穷举来源面时，「面」包括抽象层次，不只是命名空间。**
4. **协议 v1 里有已冻结、有向量、两端零实现的消息。**`ManualChargingReturnToService*` 在 54 条
   之内、不在 denylist、有完整正反向量，而控制服务端 `src/` 与 `tests/` 零命中。票 06 冻结 v2
   时要处置；本图不开缺陷。
