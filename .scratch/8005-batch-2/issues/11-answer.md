# 票 11 决议：两级事实模型落地，停稳只认组合证据，证不出来就当场升级

Resolved: 2026-09-08
Resolves: `11-fp-c11-fault-isolation-model.md`

## 结论一句话

「车出问题了」现在是一条可判定的事实，两级，**只有一条硬证据能自动进第二级**；进入任一级
立刻挡住派车并按住当前订单；**而「车停住了」必须由连续多次的运动采样正面证明，证不出来就
当场触发急停，不等任何超时**。

control-server `fp/v2-impl`，commit `9cdf1a4` ＋ `e8ed6da`。

| 项 | 值 |
| --- | --- |
| 运动观测端口 | `src/ControlServer.Application/VehicleFaultPorts.cs` |
| 适配器 | `HttpRiotMovementGateway` 增实现 `IVehicleMotionFacts`（新增 `SampleMotionAsync` ＋ `ReadMotion`） |
| 停稳判定 | `src/ControlServer.Host/Runtime/Faults/StopProof.cs`（纯函数 ＋ `VehicleMotionLedger`） |
| 两级模型与处置 | `src/ControlServer.Host/Runtime/Faults/VehicleFaultCoordinator.cs` |
| 判据参数 | `src/ControlServer.Host/Runtime/Faults/VehicleFaultOptions.cs`，配置节 `VehicleFault` |
| 派车阻断 | `src/ControlServer.Host/Runtime/Dispatch/Criteria/VehicleFaultBlockCriterion.cs`（Order 15） |
| 新增测试 | **83 条**（`VehicleFaultIsolationTests`） |
| 全量套件 | **534 passed / 0 failed / 0 skipped**（票 10 基准 451 ＋ 83） |
| L2 | `normal-load` PASS |
| 新增 migration | **零** |
| `Ports.cs` 改动 | **零** |
| 证据 | `evidence/fp-c11/20260908-ticket11/`、`evidence/l2/20260908-ticket11-normal-load-001/` |

## 白名单只有一条，而且不是调用方说了算

`REQ-0233` 逐字写着：能自动进 `VehicleFaultIsolation` 的**唯一**事实是新鲜的
`emergencyState=CAN_NOT_RECOVER`；`sysState`、`lastErrorCode`、`hardwareErrorCode`、
`faultCodesList` 要先绑定环境、build、车型／固件、语义、严重度与清除条件并**再次批准**才能加入。
那次批准没有发生，所以清单就一条。

**做法上有一处值得记：白名单判的是本次评估自己读到的状态，不是调用方传进来的证据码。**
`ObserveAsync(subject, symptomCode, …)` 先读一次急停状态，读到 `CAN_NOT_RECOVER` 才走第二级，
证据码由代码换成 `RIOT_EMERGENCY_CAN_NOT_RECOVER`；调用方就算把这个码原样传进来，读不到闩锁
也只能停在第一级（`ACallerClaimingTheHardEvidenceWithoutTheLatchStaysSuspected`）。

这样「新鲜」是**构造性**成立的——不需要给证据码配一个时间戳再去判它有没有过期，也就不存在
「谁来保证这个时间戳是真的」这个问题。

清单外的事实只有一条路进第二级：`ConfirmIsolationAsync`，要求身份 ＋ 异常处置会话号，缺一即拒。
它**不在**自动白名单上，`EvidenceOnAutoConfirmWhitelist` 落 `false`——那一列记的是「这次是不是
自动确认的」，人确认的不是。

## 四处自行定案

### 一、`movementState` 的「非移动」是两条，不是七条

行为实验室实测出现过七种取值。`MT_FINISHED` 与 `MT_PAUSED` 是「移动已经停下」的正面陈述，
进清单；`MT_NA` 是一个缺失；`MT_WAIT_FOR_CHECKPOINT`／`MT_WAIT_FOR_START`／`MT_IN_CANCEL`
描述的是一台正处在某件事中间的车，**都不排除它还在滚**。清单外一律读成 `Unknown`，而 `Unknown`
挡住证明，所以清单不全的代价是一次多余的升级——`REQ-0246` 要求往这个方向错。

**`MT_PAUSED` 必须在清单里，否则 `OrderHold` 这条路走不完。**`REQ-0234` 的流程是 Hold → 订单
`PAUSED` → 车停下，那时车侧大概率就是 `MT_PAUSED`；只认 `MT_FINISHED` 会让每一次故障都无法
证明停稳，于是每一次都升级成急停，`OrderHold` 形同虚设。

速度胜过状态字段：speed 非 0 一律 `Moving`，speed 读不到一律 `Unknown`——一个没读到的速度不能
成为「车是静止的」这个证明的一部分。

### 二、停稳判定的四个参数，以及为什么是「间隔区间」而不是三个独立的时间

`REQ-0247` 把「连续次数与时间窗口」交给监控新鲜度那份统一规则去定，本票把它落成四个可配置项：
`StopProofSampleCount`（默认 3）、`MinimumSampleInterval`（500 ms）、`MaximumSampleInterval`（5 s）、
`MaximumEvidenceAge`（3 s）。

**间隔写成一个上下界区间，是因为两端各挡一件不同的事：**

- **下界**挡的是「三次读取发生在同一瞬间」。没有下界，一个循环调三次就满足了「连续多次」，
  而那对一台需要几秒才滑停的车什么都没证明。
- **上界**挡的是 `REQ-0247` 最容易丢的那半句——「确认期间没有新的移动迹象」是对**整段区间**的
  断言。两次采样隔了半小时，车完全可以开走再回到同一个站，而每一次采样都会一致。

`MaximumEvidenceAge` 是另一件事：最新一次采样离现在多久。未来时间戳与过期同样处理——那意味着
两个时钟不一致，而用不一致的时钟算出来的年龄不能证明新鲜。

### 三、采样窗口在内存里，而且是有意的

票 06 没有为采样建表，本批次也不加 migration；但**就算能建也不该建**。跨重启拼出来的停稳证明，
是一句关于「一台在那期间没人看着的车」的断言。丢掉窗口的代价是多采几个周期，换来的是「每一次
证明都由做出它的那个进程亲眼看过」。

结论本身是持久的——它带着时刻写在故障事实上，急停监督器读的是那个。

**新 episode 一定从空窗口开始**：`ApplyAsync` 比较 generation，一变就 `Forget`。挂在 generation 上
而不是挂在「续行成功」这条路径上，是因为 `IVehicleFaultStore.ClearAsync` 从别处也够得到。

### 四、派车阻断做成被动的

`REQ-0234` 的「立即禁止新派车」不是进入故障时执行的一个动作，而是 `VehicleFaultBlockCriterion`
每一轮读一次故障事实。三个好处：进程重启照样挡；不存在「事实写进去了但还有谁要记得去执行」的
窗口；写事实的是谁都行——今天没有产品调用方在写（见缺口一），将来有了也不用改这一侧。

Order 15，排在 `AlreadyAcceptedCriterion`（10）之后、其余全部之前：一台故障车无论别的条件多好
都接不了活，所以更贵的检查都不该先跑。

**车辆身份解析不出来就挡。**故障事实按 8005 的 `agvId` 存，派车轮次跑的是 RIoT 的 `vehicleKey`，
两者不是同一个串。今天配置里只有一对，所以认不出的 `vehicleKey` 意味着这一轮在为一台**读不到
故障状态的车**做决定——而那正是这条判据要防的事。票 09 会换掉这个查找。

## `REQ-0246` 的三个条件我保留了全部三个，这很重要

条目是三个条件串联：(1) 仓门未证明锁闭**或**阻断／隔离已要求停车；(2) `OrderHold` 后无法**同时**
证明订单已 HELD 和车辆已停稳；(3) 车辆仍在移动**或**因监控失败无法排除继续移动。

第一版我差点把它简化成「停稳没证明就升级」。**那样 `OrderHold` 这条路永远走不完**：第一次评估
必然样本不足，于是每一次故障都立刻变成急停。

第三个条件正是挡住这件事的东西。一台读起来明确非移动、位置已知、采样新鲜的车，**没有任何一件
事说它在动**——窗口没填满只是扣住证明，不是主张移动。所以：

```
升级 = !(Hold 已确认 && 停稳已证明)
       && (最近一次采样不是 NotMoving || 位置未知 || 窗口内位置变过 || 证据不新鲜)
```

反过来，**沉默一律升级**：读不到运动状态、车停在两站之间没有站号、时间戳来自不一致的时钟——
每一条都是「监控失败且无法排除继续移动」，当场升级。这故意很贵：一台离线的车会升级，它的急停
也确认不了，于是报警把人叫到现场。**一台没人看得见的车，就是一台没人能说它停住了的车。**

顺带记一条实测事实：`GetVehicleCardAsync` 在车移动全程报 `station 0 / noStation`，到站才有站号
（Round 10）。所以**「没有位置」是移动中车辆的常态**，把它读成「位置没变」会让每一台停在轨道
中间的车都通过停稳判定。代码里 `PositionUnknown` 与 `PositionChanged` 是两个码，且位置未知时
不报后者——报告不能把「看不见」说成「看见了没动」。

## 一处自审改出来的东西

`StopProof.Evaluate` 第一版在样本不足时**短路**，只报 `TooFewSamples`。写测试时撞红两条，
看了一眼发现短路是错的：窗口里唯一那个样本是「读不到车」时，报告只说「采样不够」——而这两件事
要人做的动作相反，一个是继续等，一个是等不出来了。已改为不短路，样本不足与样本本身的问题一起报。

## `REQ-0238`／`REQ-0239` 的两处判断

**货物：「未装货但状态未知」与「已装货」同等对待。**`REQ-0238` 把两者放进同一个 hold，理由在
条目里就有——绑定是产品与 `DemandId` 的关联，恰恰在没人能确定哪个为真的时候不能丢。唯一不绑的
情况是「明确未装货且货物状态已知」，那是一台确知为空的车。一次 episode 只绑一次，重复观察不
累积行。

**续行：三者一致才走，且只有 `OrderContinue` 被确认之后才清故障、释放货物。**这个顺序是车能
自动恢复的前提——票 10 的 `ReleaseObstacles` 要求故障事实**真的**被 `ClearAsync`（`Level=None`
且 `ClearedAt` 有值）加上 `StopProven`，所以在订单恢复之前就清，等于为一件还没发生的事发放解除
许可。`AResumptionThatClearsTheFaultLetsTheEmergencyLatchBeReleased` 端到端走了一遍这条链。

`REQ-0239` 后半句「原订单已明确终结、相关阻断收敛且 8005 任务未终止时可重新建单」：故障清除之后
`VehicleFaultBlockCriterion` 不再挡，那条任务走的就是既有派车路径，本票没有为它另开一条路。

## 验收对账

| 票据条目 | 结果 |
| --- | --- |
| 两级模型落地，征兆与硬证据分别对应两级，级间跃迁有明确判据 | ✅ 跃迁由本次评估读到的闩锁状态决定；不降级，确认过的隔离只能被清除 |
| 自动进 `VehicleFaultIsolation` 的事实是封闭白名单，清单外一律停在疑似阻断 | ✅ 清单一条；`IsAutoConfirmable` 的封闭性有 10 例覆盖 |
| 进入任一级立即禁止新派车，并对当前执行订单自动 `OrderHold` | ✅ 阻断被动化；Hold 经票 10 的命令面并回读 HELD，**从不发 Cancel** |
| 已装货或货物状态未知时进 `FaultedVehicleCargo`，绑定不变 | ✅ 三种组合各一条，另有「确知为空不绑」与「不重复绑」 |
| 修复续行三者一致才走，任一不一致不续行 | ✅ 四种不一致各一条拒绝，另加「未确认的续行什么都不清」 |
| 无法证明停车时立即升级，不等待任何固定超时 | ✅ 升级发生在看见车在动的那一次评估，时钟一格未走 |
| 停稳要求组合证据且证据必须新鲜；三个单项证据各自单独出现判为未停稳 | ✅ `StopProof` 的入参里根本没有订单状态与闩锁；八个缺失事实码逐一有测试 |
| L1 新增覆盖：两级跃迁、白名单边界、停稳正负例 | ✅ 83 条，其中 29 条断言拒绝并断言原因码 |
| 无新增 migration | ✅ `Persistence/Migrations/`、`ControlServerDbContext`、`Ports.cs` 均零改动 |

九条全中，无偏离。

## 两处如实登记的缺口

### 一、协调器今天没有产品调用方

`VehicleFaultCoordinator.ObserveAsync` **只有测试在调**。谁去检测 `REQ-0232` 列的那四类征兆、
以什么节奏驱动，票 11 的验收里没有这一条，票据的冲突边界也只说「故障模型实现为独立文件」。

不自行接上运行时循环，三个理由：接上会改变每一轮派车的行为，需要重跑 L2 全套；「哪个信号算
离线」在服务端有多个候选来源，选哪个是一次没人授权的判断；票 09（B2 多车）本来就要重写车辆
循环，那时接更自然，而且它已经在读所需的车辆观测。

**这不影响 `REQ-0234` 的阻断**：判据已经挂在派车链上，只要故障事实存在就挡，无论那条事实是谁写的。

### 二、人工确认隔离只有策略，没有传输

与票 10 留下的「人发起急停的两条来源只有策略没有传输」是同一种形状。`REQ-0253` 的
`ExceptionRecoveryPermission` 权限模型在本批次不存在，所以没有入口调 `ConfirmIsolationAsync`。
身份与异常处置会话号目前落在日志里（EventId 9202），表上没有一等列——补它是三个列加一次
migration，**建议与票 10 记的那三个审计列并成同一次**。

## 给下游票的指针

1. **票 09（B2 多车）请顺手做两件事。**其一，`VehicleFaultBlockCriterion` 里 `vehicleKey → agvId`
   的查找目前读 `JourneyRuntimeOptions` 的那一对配置，多车时必须换成真正的映射表，否则除了配置里
   那台车之外全部落到 `VEHICLE_FAULT_IDENTITY_UNRESOLVED` 上（fail-closed，不会误放行，但会全挡）。
   其二，**驱动 `ObserveAsync` 的最佳位置就是它要重写的那个车辆循环**，见缺口一。
2. **`EvaluateAsync` 与 `ObserveAsync` 的节奏要配**。急停监督器的退避从审计流算，故障协调器每次
   `ObserveAsync` 采一个样本；采样间隔的上下界（默认 500 ms～5 s）就是对驱动节奏的约束——调得比
   500 ms 快，样本会因为「太密」被拒；比 5 s 慢，会因为「中间没人看」被拒。
3. **不要在别处再推一遍停稳。**结论落在 `IVehicleFaultStore.RecordStopProofAsync`，急停监督器读它。
   票 10 已经解释过为什么在监督器里重推是循环的，本票同理：`IRiotVehicleSafetyFacts` 的
   `MotionState` 对闩锁车永远是 `Unknown`，它回答的不是这个问题。这也是本票新开一个
   `IVehicleMotionFacts` 而不是复用它的全部理由。
4. **票 17（`FP-IS-00`～`07` 重证）注意**：本票新增的四个配置项在 `VehicleFault` 节，没有默认关闭
   开关——与 `REQ-0302` 一样，安全判据不给「关掉」这个选项。校验器会在启动时拒绝一个会削弱证明的
   配置（4 例覆盖）。
5. **票 19（W1 急停演练）**：`AResumptionThatClearsTheFaultLetsTheEmergencyLatchBeReleased` 是这条
   链在 L1 上的完整走位，演练脚本可以照它排步骤——进故障、证不出停稳、升级、拒绝解除并报
   `EMERGENCY_CAUSE_NOT_CLEARED`、三次采样证明停稳、续行确认、自动解除。
