# 票 09 决议：多车执行已落地，形态仍是单 worker 按车串行

Resolved: 2026-09-08
Resolves: `09-b2-multi-vehicle-execution.md`

## 结论一句话

**三台车能同时建会话、同时被派单、同时推进旅程，而调度仍然是一个 worker 按车串行。**
五件事全部落地，八条验收里六条通过、一条改写后通过、一条无从执行（第六条，见下）。

证据：**L1 557 passed / 0 failed**（票 11 基准 534 ＋ 23）；**L2 七条合成场景全 PASS**，其中
`three-synthetic-peers` 的断言按它自己注释里预告的方式**从「服务端只持有第一台车的会话」翻成
「三台都有、逐台 Ready」**。零新增 migration，零 `Ports.cs` 改动。

证据目录：`8005-fp/8005-agv-control-server/evidence/b2/20260908-ticket09/SUMMARY.md`。

## 落在哪

| 文件 | 内容 |
| --- | --- |
| `Runtime/Fleet/VehicleRoster.cs` | 车队名册 ＝ `vehicleKey ↔ agvId` 的登记处 |
| `Runtime/Fleet/VehicleDispatchPolicyAccess.cs` | 配置 → 票 06 三张表，按内容指纹幂等；占用申领/释放的门面 |
| `Runtime/Fleet/CheckpointWaitLedger.cs` | 检查点等待时长（进程内），＋ `RiotMovementStates.WaitForCheckpoint` |
| `Dispatch/Criteria/VehicleTaskTypeAdmissionCriterion.cs` | order 25，`agvId × taskType` |
| `Dispatch/Criteria/DispatchZoneVehicleCriterion.cs` | order 65，区→车 |
| `Transport/OnboardPeer.cs` | 按 `agvId` 持 N 条连接，按信封里的 `agvId` 路由 |
| `Transport/OnboardTcpServer.cs` | 并发 accept，有并发上限 |
| `Runtime/JourneyRuntimeEngine.cs` | 按车迭代、按车预算、按车会话、占用申领、检查点处置 |
| `Runtime/JourneyRuntimeOptions.cs` | `Fleet[]`、`CheckpointWaitBudget`，及其校验 |
| `tests/.../MultiVehicleExecutionTests.cs` | 23 条 L1 |

判据链现在 13 条（原 11 ＋ 2）：

| Order | 判据 | 本票新增 |
| --- | --- | --- |
| 10 | `AlreadyAcceptedCriterion` | |
| 15 | `VehicleFaultBlockCriterion` | 身份解析改了 |
| 20 | `WorkTypeScopeCriterion` | |
| **25** | **`VehicleTaskTypeAdmissionCriterion`** | ✅ |
| 30／40／50 | `RequiredMesFacts`／`AreaScope`／`AreaEqpUnique` | |
| 60 | `StationResolutionCriterion` | |
| **65** | **`DispatchZoneVehicleCriterion`** | ✅ |
| 70／80／90／100 | `PackageCapacity`／`VehicleDynamicFacts`／`StationTaskType`／`SlotCapacity` | |
| 110／120／130 | 路网可达／目录可用／建单前门 | |

两条新判据都是**必需参数**而不是可选尾参，理由与票 11 给 `faultStore` 的一样：一条调用方可以
省掉的 fail-closed 规则，会被最需要它的那个调用方省掉。

## 五件事各自怎么落的

### 1. `OnboardPeer.Attach` 的 N 会话

两处都得改，缺一不可：

- **`OnboardPeer` 原本只持一条连接**，第二台车 `Attach` 直接抛。现在按 `agvId` 分槽，
  **同一个 `agvId` 的第二条连接仍然抛**——那是歧义，不是车队。
- **`OnboardTcpServer` 的 accept 循环原本是串行的**（`await HandleClientAsync` 写在 `while`
  里），处理完一条连接才接下一条。这才是真正卡死车队的那一处：`OnboardPeer` 就算能分槽，第二
  台车也还在 listen backlog 里等第一台的会话结束。现在每条连接一个任务，`ServeAsync` 兜住这
  条连接的所有异常（一台车的协议错不能掀掉共用的 accept 循环），并发数由新配置
  `OnboardTransport:MaxConcurrentSessions`（默认 8）封顶，超出的连接立刻关掉而不是排队。

**路由靠信封里的 `agvId`，不是靠给 `IOnboardPeer` 加参数。**`SerializeWire` 给每一条出站信封
都写了 `agvId`，收件人本来就在消息里；读它比再加一个可能与载荷不一致的参数更实在，而且
`Ports.cs` 一行不用动（票 06 的承诺）。找不到收件人就抛 `IOException`，与原来「没有连接」同
一个形状——**不广播、不静默丢弃**。

### 2. `MT_WAIT_FOR_CHECKPOINT` 识别与处置

**识别**：`RiotMovementStates.WaitForCheckpoint` 具名，`AdvanceAsync` 在两个「还没到站」的分支
里采一次运动样本，认出这个状态。

**处置**：预算内报 `VEHICLE_WAITING_AT_CHECKPOINT`，超过 `CheckpointWaitBudget`（默认 5 分钟）
改报 `VEHICLE_CHECKPOINT_WAIT_EXCEEDED` 并记 Warning 日志；车一走就清掉等待时钟、并把这两个
原因码从 `BlockReasonCode` 上撤掉（只撤自己写的那两个）。

等待时长存在一个进程内的 ledger 里，**不持久化**，理由与票 11 的 `VehicleMotionLedger` 一字
不差：跨重启带过来的时长是在替没人看着的那段时间说话。

**它没有被加进 `NotMovingStates`。**票 11 的交接已经点了这一条，本票确认它是对的：在检查点
等待不排除车还在滑行，加进去就是用削弱 `REQ-0247` 的停稳证明来换一个好看的词。

### 3. 单 worker 按车串行 ＋ 每车超时预算

循环骨架是票 05 的，本票只把 `DispatchVehicleKeys()` 那一行换成名册，外加两件事：

- **每车一个 `CancellationTokenSource`**（预算来自策略表的 `RoundTimeoutMilliseconds`）包住
  `DispatchForVehicleAsync`。超时只丢这台车这一轮，日志记 agvId 与预算，**下一轮照常服务**——
  超时不被记住，因为它描述的是那一轮的一次读，不是这台车的状态。
- **超时后 `dbContext.ChangeTracker.Clear()`。**这一句才是「一台车不拖垮其余车」真正生效的地
  方：预算只是停住了工作，被半途放弃的那些 tracked 改动如果留着，会在下一台车的
  `SaveChangesAsync` 里被一起写出去。清完之后重建 backlog 字典。

### 4／5. `agvId × taskType` 与区→车

两条判据都读**本轮一次性取到的** `VehicleDispatchPolicy`（挂在 `DispatchRoundFacts.Policy`
上）。每条判据两个不同的拒绝原因码，因为它们要人做的事不一样：

| 原因码 | 含义 |
| --- | --- |
| `VEHICLE_NOT_IN_DISPATCH_POLICY` | 策略里根本没有这台车——运维漏配 |
| `VEHICLE_TASK_TYPE_NOT_ADMITTED` | 配了，这个任务类型不在允许集里——策略正常工作 |
| `DISPATCH_ZONE_HAS_NO_VEHICLES` | 这个区没有任何车服务——运维漏配 |
| `VEHICLE_NOT_ADMITTED_IN_ZONE` | 区配了，这台车不在里面——策略正常工作 |

## 五处需要单独交代的判断

### 一、`Fleet` 为空＝那一台车，这不是宽松默认

`JourneyRuntimeOptions.Fleet` 为空时，名册与策略都从既有的单车字段推出来一条：
`AgvId`／`VehicleKey`／`AgvLifecycleGeneration`，允许的任务类型取 `AllowedWorkTypes`，服务的
区取 `DispatchZone`。

这不是「未配置时放行」——那几个字段**本来就是配置**，而且都是显式列举的。把它读成空策略才是
错的：那会把唯一那台配置好的车挡在每一个候选之外，fail-closed 且与事实不符。真正的
fail-closed 在别处：**不在名册里的车根本不进循环**，不在策略里的车被 order 25 挡掉。

代价是：现有部署升级到这个 build 不用改任何 appsettings，行为逐字不变。

`Fleet` 显式写出来时，校验器要求它**必须包含主 `AgvId`/`VehicleKey` 那一对**——否则地图、关卡
站、调度代次这些仍然全局的字段就在描述一台名册里没有的车，是两份互相矛盾的配置。

### 二、策略按内容指纹同步，不设人工版本号

`VehicleDispatchPolicyAccess.EnsureCurrentAsync` 每轮读一次库里的策略，与配置算出来的比
`ConfigurationVersion`——而那个串是**策略内容自己的 SHA-256 指纹**（长度前缀拼接，理由同票 06
的边组指纹：agvId、区名、任务类型里可以出现任何分隔符）。

不用人工版本号，是因为它的失效方向很难看：运维改了名册忘了升版本，库里的表就与他正在读的
文件静默不一致。指纹让「改了必写、没改必不写」成为结构性质。

写入用票 06 的 `ReplacePolicyAsync`（整体替换，两次 `SaveChanges`）。稳态一轮零写入。

### 三、一轮内被前车拿走的需求必须立刻消失——这是多车最先炸的地方

三台车面对同一份目录、用同一个全序（`FirstSeenAt` → `CreatedAt` → `DemandId`）排序，
**必然选中同一个需求**。第二台车进 intake 时会撞上 `AcceptedDemands` 的唯一性或 lease 表，整
轮 fail-closed。

所以 `DispatchRoundFacts.AcceptedDemandIds` 从「本轮开始时的快照」改成**一轮之内会长大的活
集合**：一台车决定要某个需求，就在调 intake **之前**把它加进去（之前而不是之后——下面每一条
拒绝路径都已经把这个需求绑在这次尝试上了）。

这么做是安全的，**而且它安全的理由正是「单 worker 按车串行」本身**：没有任何一段在别人写的
时候读它。这条依赖关系写进了 `DispatchRoundFacts` 的文档注释——如果哪天有人想把车辆循环改成
并发，这里会立刻不成立。

### 四、「只能有一个未完成旅程」从服务端级降为车辆级

`ExecuteOnceAsync` 原来是 `if (active.Length > 1) throw`。单车时「服务端只有一个旅程」与「每
台车只有一个旅程」是同一句话；多车时不是，照旧读就是拒绝跑车队。现在按 `AgvId` 分组，**同一
台车两个未完成旅程仍然抛**，异车不抛。

顺带确认单车行为逐字不变：先推进已有旅程，再为空闲车辆发现新需求；`active.Length == 1` 时空
闲车辆为零，直接返回（＝原来的「只推进」）；`active.Length == 0` 时空闲车辆是那一台，走孤儿
检查 ＋ 发现（＝原来的「只发现」）。**孤儿检查的位置也因此没变**：它原来只在「没有活跃旅程」
时跑，现在在「有车空闲、即将接活」时跑，单车下这两句话相等。

### 五、票 11 的 `vehicleKey → agvId` 查找换成了名册解析的结果

`VehicleFaultBlockCriterion` 原来把 `evaluation.Vehicle.VehicleKey` 与配置里那一对比较，对不上
就 `VEHICLE_FAULT_IDENTITY_UNRESOLVED`。多车下那会把除配置那台之外的每一台都挡掉（fail-closed
但全挡）。

现在身份在**判据链跑之前**由名册解析好，`DispatchVehicleFacts` 同时带 `VehicleKey` 与
`AgvId`，判据读后者。**守卫保留**：`AgvId` 为空串就是「身份从未被解析」，仍然阻断——一条相信
调用方的安全判据是脆的。票 11 那条测试改成传空串，语义与命名都还对得上。

`ReadOnboardFactsAsync` 同样从读 `runtimeOptions.AgvId` 改成读入参：里面每一次读（会话行、两
份快照、最后一条入站消息）都是会话作用域的，用配置那台车的会话去放行另一台，正是按车迭代要
防的那种串。

## 占用唯一性：开关打开了

票 06 把唯一性下移到 `OrderIntents`（`VehicleOccupancyClaimedAt IS NOT NULL AND
VehicleOccupancyReleasedAt IS NULL` 上的 filtered unique index），但当时没有任何代码写那两个
时刻，所以每一行都落在索引之外。本票开始写：

- **申领**：intake 接受之后，用 `plan.PickupUpperId` 调 `TryClaimVehicleOccupancyAsync`。占用
  **骑在旅程的第一张订单上并持有整程**——关卡腿是同一台车的第二张 `OrderIntent`，让它也申领就
  是让车跟自己撞。
- **释放**：旅程置为 `Completed` 之后，在同一次 `SaveChanges` 里释放，所以崩在中间不会留下
  「已完成但仍占着车」的状态。
- **申领被拒**＝有第二个写入方插了进来。这时**报出来而不是绕过去**：日志 Error ＋ 旅程
  `Block("VEHICLE_OCCUPANCY_CONFLICT")`。旅程已经存在了，运维必须看到是哪台车被双占。

lease 表的检查保留不动，两者不冲突：lease 是一个 Demand 的占用（决策前读），occupancy 是一台
车的在途订单（写入瞬间由数据库判定）。

## 三件与票据不同的事

### 一、`DispatchUniquenessGuard` 这条验收无从执行（第三次记录）

票 09 的第六条验收是「`DispatchUniquenessGuard` 源码零改动且其测试仍绿」。**这个符号在
`8005-agv-control-server` 里不存在**——票 06 决议第一条与票 05 决议都已经查证过，本票再次
`grep` 确认（`src/`、`tests/`、`*.md` 全部零命中）。既没有源码可保持不变，也没有「其测试」可
保持绿。

它想保护的不变量是真实存在的，由两样东西承载：`VehicleDispatchLeases` 上
`HasIndex(VehicleKey).IsUnique().HasFilter("ReleasedAt IS NULL")`，以及本票开始写的
`OrderIntents` 占用索引。这条验收因此按票 06 的建议改写为「占用唯一性生效且有测试」，并以
`ADispatchedVehicleHoldsItsOccupancyUntilTheJourneyEnds` 兑现。

**这是同一个不存在的符号第三次出现在验收里。**建议票 17／18 写验收前照旧先 grep。

### 二、`MT_WAIT_FOR_CHECKPOINT` 没有接进故障模型，这是有依据的拒绝

票 11 的交接建议在车辆循环里驱动 `VehicleFaultCoordinator.ObserveAsync`，并说明接不接是本票的
判断。**本票判断为不接**，而且理由是具体的，不是嫌麻烦：

1. **从检查点等待接进去，会把每一次长时间等待变成急停。**
   `VehicleFaultCoordinator.RequiresEscalation` 的条件是
   `latest.Reading != NotMoving || !latest.HasKnownPosition || …`。在检查点等待的车读成
   `Unknown`，第一个条件**按构造成立**，于是第一次 `ObserveAsync` 就会升级并发急停。等在检查
   点是多车下的正常交通行为，不该以急停收场。
2. **从 `VEHICLE_OFFLINE` 接进去，会给没有在途订单的车留下清不掉的闩锁。**
   `REQ-0232` 把「车辆离线」列为症状，接进去看似顺理成章；但故障事实的清除路径是
   `ResumeAsync`，它要求一个仍然 HELD 的订单在。一台空闲的车瞬时掉线一次，会被记上
   `SuspectedBlocked` 而**没有任何路径把它清掉**——从此再也派不出去。

两条都是「接上去反而更糟」，不是「来不及做」。**票 11 决议的缺口一（`ObserveAsync` 无产品调用
方）因此仍然开着**，本票把它的两条障碍具体化了：要接，得先有一个不依赖在途订单的清除路径
（`REQ-0253` 的权限模型那条线），以及一个能把「交通性等待」与「不动了」区分开的症状来源。

### 三、`three-synthetic-peers` 的断言方向被翻过来

那条 L2 场景是票 03 留下的，它在自己注释里写着：票 09 之后「这条会红，而它红得对：它在提醒
边界已经移动，把它改掉即可」。照办了：三台车都等 READY，`L2-3P-06` 从「只有第一台」改成三台，
`L2-3P-07` 改成逐台断言 Ready。**PASS**——服务端确实同时持有三条 Ready 会话。

## 验收清单

- [x] 三台车能同时建立会话并各自推进，会话与旅程状态互不串
      （L1 4 条 ＋ L2 `three-synthetic-peers` 三条 Ready 会话）
- [x] 调度是单 worker 按车串行，同一轮内不并发写同一份快照
      （一轮一次目录决策读、车辆读不交错；一轮内前车拿走的需求对后车立即消失）
- [x] 每车有独立超时预算，一台车超时不影响其余车在本轮被服务
- [x] `MT_WAIT_FOR_CHECKPOINT` 被正确识别并有对应处置（且仍读成 `Unknown`，停稳证明未削弱）
- [x] `agvId × taskType` 与区→车两条判据在判据链里，配置驱动，未配置时 fail-closed
- [~] `DispatchUniquenessGuard` 源码零改动且其测试仍绿 —— **无从执行**，符号不存在；
      改以占用唯一性生效兑现，见上文
- [x] L1 新增覆盖：多车下的会话隔离、按车串行、超时预算各有测试（23 条）
- [x] 无新增 migration（`git status` 里没有 migration 文件，`ControlServerDbContext` 未动）

## 遗留

1. **`VehicleFaultCoordinator.ObserveAsync` 仍然没有产品调用方**（票 11 缺口一）。本票查明了两
   条具体障碍，见上文「三件与票据不同的事」第二条。
2. **三车端到端（派单→装货→关卡→卸货）尚未在 L2 上跑过**——那是票 18 的出口。本票的 L2 只证
   到会话这一层；三车同轮成单在 L1 上有覆盖。
3. **`OnboardPeer` 的路由靠解析每条出站信封的第一行 JSON。**缓冲区里多条信封共用第一行的收件
   人，没有逐行复核。当前每个调用方都是为一个会话构造缓冲区，所以复核只会花掉一次 JSON 解析
   去发现一个没人能犯的错；如果将来出现跨车批量发送，这一条要重新看。
4. **`MaxConcurrentSessions` 默认 8**，没有随名册大小自动调整。车队超过 8 台时要一起改。

## 给下游票的指针

1. **票 18（三车 L2 出口）**——`three-synthetic-peers` 现在证到「三条 Ready 会话」为止，端到端
   要在它基础上加派单与装卸。编排器侧多对端已经就绪（`OnboardPeers` 数组、每台一个进程一个控
   制面）。**注意 `Invoke-L2Query` 的返回形状**：它以 `return , $rows` 返回整张结果集，调用处
   **不要**再包一层 `@()`，否则拿到的是「一个元素、那个元素是整张结果集」，`$_.X` 会走成员展
   开。单行时这个错完全看不出来，多行时才现形——本票就是这么撞上的。
2. **票 17（`FP-IS-00`～`07` 重证）**——本票新增两个配置项：`JourneyRuntime:Fleet`（数组，为空
   即单车，校验器要求包含主 `AgvId`/`VehicleKey` 对）与 `JourneyRuntime:checkpointWaitBudget`
   （默认 5 分钟，已写进 `appsettings.json`），另有
   `OnboardTransport:MaxConcurrentSessions`（默认 8）。三个都没有「关掉」开关。
3. **票 19（W1 急停演练）**——本票**没有**给急停链新增触发点，票 11 的走位仍然是唯一那条。
   演练脚本不需要考虑多车预算或检查点等待。
4. **任何要改车辆循环并发度的人**——`DispatchRoundFacts.AcceptedDemandIds` 在一轮之内会长大，
   它的正确性依赖「按车串行」。改成并发的那一刻这条就不成立了，文档注释里写了。
5. **任何要给 `NotMovingStates` 加值的人**——`MT_WAIT_FOR_CHECKPOINT` 已经被识别并处置了，
   **不需要**为了让报告好看而把它加进去。加它会削弱 `REQ-0247`，那是一次需要论证的判断。
