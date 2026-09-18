# 操作员不作为时装卸站自行收敛，只有传感器不可信才进人工恢复

操作员到站后长时间不录入 SUBLOT、开了仓门不放料、放完不关门，这三种不作为都不允许把流程停在
需要管理员介入的状态上。**这不是一条新决策，而是 ADR-cross-0040 与 ADR-cross-0055 已经规定、
但 WIRE_TO_GATE 路径尚未实现的行为**；本 ADR 记录该差距，并补上基线唯一没有覆盖的那一格——
站点期限到期而仓门仍未闭合时的结局。

## 触发本条的现场事实

2026-09-08 车载端首次切到真实 Modbus IO 模块（`192.168.71.150:502`）实跑，`agv01`，
demand `Q26091238-17`。1 号仓开锁脉冲于 10:29:22.986 发出，锁 DI 由 1 变 0 确认弹开，
操作员在 17 秒后才开始动作，其间光幕 DI 反复跳变但仓门始终未闭；10:31:22 车载端 119 秒超时，
整个 station operation 判为 `LOAD_RESULT_REQUIRES_RECOVERY`，服务端 journey 转 Blocked。
HMI 显示「1、2 号仓操作失败或状态未知，服务端已收到结果，等待管理员恢复」，而
`wireToGate.recoveryResumeEnabled` 出厂为 `false`，恢复入口根本不会出现。唯一出路是从控制端
运行 `12-reset-journey-state.ps1` 清空两端状态重跑——那是测试台手段，不是产线出路。

值得注意的是 2 号仓当时**一次都没有打开过**，却和 1 号仓一起被标记为失败：车载端在超时分支里把
`command.Slots` 中所有未完成的仓位一并写成 `NOT_STARTED` + `UNKNOWN`。

## 基线规定了什么

**ADR-cross-0040** 已经把「人没放料」和「传感器不可信」分成了两件事，并给了不同出口：

> 若读到明确相反状态，当前仓位不记为完成，车载端自动再次输出开锁脉冲使仓门弹开，并提示操作员
> 重新放入或取出；关闭后重复核对，直到达到预期状态，**不设置「超过若干次便强制通过」的上限**。
> SlotOccupancyState 为 UNKNOWN、锁闭反馈无效或开锁输出无法确认复位时，不执行自动重开循环，
> 而是暂停当前操作并进入恢复；**软件不得把传感器故障当成「放错/漏取」**。

**ADR-cross-0055** 则把「不能无限占站」交给服务端：车辆进入 StationDepartureWaiting 后由
StationDepartureWaitTimeout（默认 5 分钟）计时，到期以 StopClosureCommit 原子结束本站，未开始的
待装 DemandId 记 `CANCELLED_BY_STATION_TIMEOUT`；**部分装货无进展达到同一时长时只告警**，
且「活动仓位操作阻断倒计时离站」。

**ADR-cross-0015** 规定装卸不对称：装货整批物理清空后可经 LoadTaskCancellation 终结，
**卸货采用 UnloadCompletionRequired，不存在取消分支**，异常时只能暂停、排障并继续，直到目标仓位
取空、锁闭并可靠上报。**ADR-cross-0016** 规定 `SlotOperationCommand` 一经发出不可撤回。

两条合起来的图景是完整的：仓位层面靠目标态闭环反复纠正，站点层面靠服务端期限收口，人工恢复
只留给传感器不可信。

## 本文档比对的是哪个版本

**这一节是后加的，因为第一版把本地代码当成了线上现状，三条结论因此是错的。**

线上 ControlServer 部署自 commit `75ea9f6`（`D:\zhengyushao\ControlServer\release-manifest.json`，
2026-09-04 构建，`worktreeCleanAtStart: true`），`/version` 报 `protocolVersion: 1` /
`protocol-v0.1.1`。而本地 `ControlServer_MVP` 分支已在实施 ADR-cross-0057——两个
`feat(journey)!` 提交把旅程切到 protocolVersion 2，HEAD 之外还有约 900 行未提交改动。

下面这些**只存在于本地，线上一行都没有**，全部经 `git show 75ea9f6:` 与线上库逐项核对：

| 机制 | 线上 `75ea9f6` | 线上数据库 |
| --- | --- | --- |
| `JourneyRuntimeOptions.SublotWaitTimeout` | 不存在 | — |
| `TryTimeOutSublotWaitAsync` | 0 处 | `JourneyRuntimes` 无 `SublotWaitStartedAt` 列 |
| 迁移 `20260907174639_SublotWaitTimeoutAndBeforeLoadCancellation` | 当时尚未创建 | 未应用（线上最新是 `20260903110052_...`） |
| `TransportDemandSuppressions` | 0 处 | 表不存在 |
| `CancelDemandBeforeLoadAsync` | 0 处 | — |

反过来，`WireToGateStore.ApplyOperationResultAsync` 的 `completedSafely` 二值判定在
`75ea9f6` 里就是现在这样（1455、1461 行），未变。车载端 `OperationTimeoutMs = 120_000`
由实测佐证：2026-09-08 首趟真车超时发生在开锁后 119 秒。

**因此「不录入 SUBLOT 会在 5 分钟后被取消」在线上是不成立的。**线上的真实行为是服务端每
2 秒无限重发 `SublotEntryRequested`，旅程停在 `AwaitingSublot`，车一直占着取货站，没有任何
机制会解救它——这正是本 ADR 要消除的那类卡死，而且是其中最容易发生的一种。

## 实现差距

WIRE_TO_GATE 的仓位操作走 `WireToGateSlotOperationExecutor`，与之并存的 `OnboardController`
（规则服务器路径）才是带重开循环的那条——`MaxReopenAttempts`（默认 2）只在 `OnboardController`
中被引用。WIRE_TO_GATE 路径的实际形状是：

| 项 | 实现现状 | 与基线的差距 |
| --- | --- | --- |
| 仓位目标态闭环 | 无。`WaitForLockerAsync` 等不到预期就抛 `TimeoutException` | ADR-0040 的自动重开循环在此路径**完全缺失** |
| 车载端期限 | `OperationTimeoutMs` 默认 120000 ms，**整条命令共享**（`deadline = started + OperationTimeout`），非每仓位各一份 | 基线不设仓位重试上限，站点时长归服务端；这个期限本身即偏离 |
| 超时结局 | `overallOutcome = "UNKNOWN"`，仓位 `outcome = "UNKNOWN"`，`reasonCode = ACTION_NOT_ALLOWED_IN_STATE` | 把「明确相反状态」当成了 UNKNOWN，正是 ADR-0040 禁止的那种混淆 |
| 服务端判定 | `completedSafely` 二值：非完美完成一律 `RecoveryRequired` | 缺「确定失败」这一档 |
| 站点期限 | **线上一个期限都没有。**无 StationDepartureWaiting，也无 sublot 录入超时——不录入就无限期停在 `AwaitingSublot`。本地新增了 `SublotWaitTimeout`（默认 5 分钟），尚未部署 | ADR-0055 的 StopClosureCommit 未实现；线上连本地那半个替代品都还没有 |
| 契约 `FAILED` | `overallOutcome` 与 SlotResult 的 `outcome` 枚举均已含 `FAILED`，两端**一次都没用过** | 表达能力已在契约里，实现未取用 |

契约侧不需要改动即可表达「确定的失败」：`overallOutcome: FAILED` 配合
`finalPhysicalState: EMPTY | OCCUPIED`、`lockState: LOCKED`、`unlockOutputState: RESET`
足以陈述「这次装货没完成，仓位是空的，门锁好了」这一完全确定的事实。

## 硬件能力边界

`ModbusTcpIoModuleClient` 只实现三个 function code：`0x01` 读线圈、`0x02` 读离散输入、
`0x05` 写单线圈；而 `0x05` **仅用于 `PulseUnlockAsync`**，向开锁 DO 写 `0xFF00`，硬件自动复位。
**不存在关门或锁门的输出。** 仓门由操作员手动闭合，锁为机械式。

这条约束决定了收敛的上界：仓门开着时软件无法使其回到确定状态，而 ADR-cross-0011 与
ADR-cross-0012 的离站安全约束又不允许车辆带着未闭合的仓门移动。**「仓门一直开着」这一格
无法无人化**，它是硬件能力边界，不是软件缺陷；软件能做到的极限是把人的介入从「管理员登录 HMI
走恢复握手」降为「把仓门带上」。

## 决策

1. **WIRE_TO_GATE 路径实现 ADR-cross-0040 的目标态闭环。** 光幕稳定读到与预期相反的状态时，
   自动重新输出开锁脉冲并提示操作员，不判失败、不进恢复、不设次数上限。仓位各自闭环，已达预期
   并安全锁闭的仓位不因其它仓位未完成而重开。

   *2026-09-18 改写（按 [program#55](https://github.com/trytoreachpeak0/8005-agv-program/issues/55)
   2026-09-13 的定论）：扫了子批号、核验通过、开了门之后，关门默认是意外关上。**期限前后一样**，读到
   相反态就重新弹开并提示，不设次数上限，**也不以本站期限为上限**。放弃这次装货只有一个出口：持工号的
   操作员按取消。在途装货的取消入口与 `recoveryResumeEnabled` 解绑，是站点操作员的普通一步；补偿、纠错、
   恢复入口仍受该开关挡。期限过后提示改为「请放入货物并关闭 N 号仓门；不装了请按取消」，并显示已过期多久。
   2026-09-12 那次回写（期限过后再宽限一轮、仍是相反态就按第 5 条结算）作废。见文末 Verification。*

2. **只有 UNKNOWN 进人工恢复。** SlotOccupancyState 为 UNKNOWN、锁闭反馈无效或开锁输出无法确认
   复位，才暂停并进入恢复。人未放料、未取料、未关门都不是 UNKNOWN。

3. **车载端 `OperationTimeout` 不再是判死依据。** 它退化为提示与告警的节拍，不产生业务终态。
   站点能停多久由服务端按 ADR-cross-0055 掌握，车载端只显示服务端截止时间。

4. **站点期限到期而仓门未闭时，不结束本站。** 这是基线未覆盖的一格。StopClosureCommit 要求车辆
   随后能够离站，而未闭合的仓门使离站不可能，因此期限到期只把该站转入告警升级状态并持续等待仓门
   闭合，闭合后立即按当时的真实 IO 读数结算。**告警升级的对象、通道与节奏由项目现场规程规定，
   不在本 ADR 内。**

   *2026-09-13 回写：规程已定，见
   [`docs/site-procedures/station-door-not-closed-escalation.md`](../../site-procedures/station-door-not-closed-escalation.md)
   （[program#55](https://github.com/trytoreachpeak0/8005-agv-program/issues/55)）。*

5. **仓门已闭合的超时按确定失败结算，不进恢复。** 期限到期时若仓门已闭、开锁输出已复位、
   SlotOccupancyState 明确，车载端报 `overallOutcome: FAILED` 与真实的三个物理字段；服务端据此
   走确定失败路径而非 `RecoveryRequired`。装货依 ADR-cross-0015 与 ADR-cross-0046 经
   LoadTaskCancellation 终结，**卸货不适用本条**——UnloadCompletionRequired 无取消分支，仍按
   第 1 条持续闭环直到取空。

   *2026-09-18 改写（按 program#55）：**车载端在装货侧不产出期限后的确定失败**（`FAILED`／
   `OPERATOR_TIMEOUT`）。按第 1 条的改写，期限过后空关照样重开，「门已闭、货没动、开锁输出已复位」这一态
   只在两次开锁之间或安全保持期间短暂出现，没有任何代码把它结算成结果；生产者核查见文末 Verification。
   装货的这一格由操作员按取消收口：服务端授权后车载端先中止原执行器，再按 ADR-cross-0046 清空。
   服务端**保留**确定失败结算作为防御性处理——协议照样注册了 `FAILED` 与 `OPERATOR_TIMEOUT`，别的车载端
   版本可能发来，收到了就以 `CANCELLED_BY_STATION_TIMEOUT` 终结需求并照常收尾，不当成故障。
   2026-09-12 那次回写（车载端产出确定失败、服务端据此终结）只剩服务端这一半。「卸货不适用本条」不变。*

6. **未开始的仓位不因其它仓位失败而被判失败。** 现行实现把 `command.Slots` 中所有未完成仓位
   一并写成 `NOT_STARTED` + `UNKNOWN`，使 2 号仓在从未开启的情况下进入恢复范围。未开启的仓位
   没有任何物理不确定性，应保持 `NOT_STARTED` 且不触发恢复。

7. **未录入 SUBLOT 超时后该订单不再重派。** 本地已实现、**尚未部署**的那套行为——
   `SublotWaitTimeout` 到期后 `CancelDemandBeforeLoadAsync` 记 `CANCELLED_BY_STATION_TIMEOUT`，
   并由 `TransportDemandSuppressions` 按 TransportDemandKey 写入永久禁令，候选评分以
   `TRANSPORT_DEMAND_SUPPRESSED` 挡下——**即为期望行为**，设计上无需改动。车辆释放去接后续需求，
   该订单由 MES 侧另行处理。Zhengyu Shao 于 2026-09-08 确认。

   **但它在线上不存在**（见上文版本一节），所以这一条不是"维持现状"，而是**一项待交付工作**：
   在这套代码部署之前，不录入 SUBLOT 就是无限期占站，与第 3、4 条要消除的卡死同类。它排在
   ADR-cross-0055 的 StationDepartureWaiting 之前，因为它已经写好了，只差一次发布。

   *2026-09-12 回写：已随 2026-09-09 的 RC 上线，2026-09-12 在真车上验收。见文末 Verification。*

**Status**: accepted（2026-09-12 由 proposed 转，依据见文末 Verification）

**Considered Options**:
- 维持现状，靠 `recoveryResumeEnabled` 打开 HMI 恢复入口（拒绝：把每一次操作员迟疑都升级为需要
  `MAINTENANCE_ADMINISTRATOR` 凭据的恢复会话，与 ADR-cross-0040「不得把人没放料当成故障」相悖）
- 超时后一律按确定失败结算并放行车辆（拒绝：仓门未闭时车辆不得移动，且卸货按 ADR-cross-0015
  必须完成，不存在「失败了结」的出口）
- 超时后自动关门再结算（拒绝：IO 模块无关门输出，物理上不可能）
- 延长车载端 `OperationTimeout` 到足够长（拒绝：治标；期限归属错误的问题不因数值变大而消失，
  且与 ADR-cross-0055 的站点期限重复计时）
- 恢复 ADR-cross-0040 的目标态闭环，期限归服务端，仅 UNKNOWN 进恢复（采纳）

**Consequences**:
- **不需要协议变更。** `overallOutcome` 与 SlotResult `outcome` 的 `FAILED`、三个物理状态字段的
  `UNKNOWN` 取值均已在 `protocol-v0.1.1` 中定义，两端 G1/G2/G3 证据不因本条作废。表达「操作员
  超时」的精确 ErrorCode 目前没有，`LOCK_NOT_CLOSED` 可覆盖仓门未闭一路；是否新增
  `OPERATOR_TIMEOUT` 留待下一次协议批次一并决定，不为此单独发布补丁。
- 车载端改动落在 `WireToGateSlotOperationExecutor`，属 `8005-agv-onboard-hmi`，按 `w2g/*` 分支加
  PR 的路径交付，需 Kun Wang 同意。`OnboardController` 中既有的重开循环是同一意图的既有实现，
  可作参考但不可直接复用——它由操作员按钮驱动且带 `MaxReopenAttempts` 上限，而 ADR-cross-0040
  要求自动触发且不设上限。
- 服务端改动落在 `WireToGateStore.ApplyOperationResultAsync` 的 `completedSafely` 分支与
  `JourneyRuntimeEngine` 的 `AwaitingLoadResult`，需要在 `StationOperationStatus` 上增加确定失败
  终态；`AwaitingUnloadResult` 不增加该分支。
- ADR-cross-0055 的 StationDepartureWaiting 至今未实现，本条第 3、4 条依赖它。两者应作为同一批
  工作推进，否则车载端撤掉判死依据后将没有任何期限收口。
- 第 4 条引入一个可能长期占用站点的状态。这是有意的：占站可被看见、可被告警、可被人解决，而
  带着未闭合仓门发车不可逆。
- 本条与 ADR-cross-0057 的持货超时是三个独立期限：0055 管「这次停靠还等不等人」，0057 管「这趟
  车还收不收货」，本条管「这个仓位的目标态达成没有」。前两者到期结束调度阶段，本条不设上限。
- L2 场景层需新增操作员不作为的场景：仓门已闭超时、仓门未闭超时、卸货未取空反复闭环三条，
  现有 `sublot-wait-timeout` 覆盖的是第 7 条那一路，不重叠。
- 验收必须在真实 IO 模块上进行。模拟器可以证明软件闭环，不能证明光幕极性、锁反馈时序与机械
  弹开行为——本条的每一条判据都建立在这三者之上。

## Verification（2026-09-12）

**本节是后加的。**上面「本文档比对的是哪个版本」与「实现差距」两节记的是 2026-09-08 线上 `75ea9f6`
的状态，原样保留，那是本条的出发点；它们描述的差距今天已全部关闭，现在成立的以本节为准。本条据此由
`proposed` 转 `accepted`。执行过程在 8005-agv-program#11 那张地图上，下文的 `#NN` 都是该仓库的 issue。

### 核对的是哪个版本

线上服务端 `3b379bb`（release run 34687146146，包 SHA-256 `78f5c665…`），车载端 `6b8a0b0`，
`protocol-v0.3.0`（`345c53c`，manifest `b6c81ca9…`）。下文引用的每个实现 commit 都核过是这两个线上
commit 的祖先。

### 七条决策各自落在哪

| 决策 | 实现 | 与原文不同的地方 |
| --- | --- | --- |
| 1 目标态闭环 | 车载端 `DriveSlotToTargetStateAsync`：并发等「达成态」与「相反态」，读到相反态就重打开锁脉冲并提示（`4bbe36f`，#16）；受本站期限约束（`3d8206f`，#24） | 「不设次数上限」收窄为「不设次数上限，但受本站期限约束」。上限不是次数，是服务端给的时刻：期限过后车辆在相反态上再宽限一轮，第二次读到相反态才停止重开、按第 5 条结算（#24）。**这一收窄已由 2026-09-18 的改写撤销**，v2 线不收窄，见下文「v2 线」一节 |
| 2 只有 UNKNOWN 进恢复 | 执行器里 `UNKNOWN` 只剩锁闭反馈无效、开锁输出无法确认复位那个 `catch`（#26）；客户端在开锁等操作员时退出，重启后按实时 IO 补交结果，开过的仓全到最终态报 `COMPLETED`、否则 `UNKNOWN`（`0f2cf9d`，#40）。恢复握手走得完：补偿对账后会话回到 `Ready`（`369919f`，#46），多需求旅程补偿一条后继续走（`8be28b1`，#47），被拒过一次的 attempt 仍能再开恢复会话（`6b8a0b0`，#49），恢复动作可经自动化面发起（`bb58b21`，#41） | 无 |
| 3 OperationTimeout 不判死 | `OperationTimeout` 退化为提示节拍，到期只再提示一次、不重复脉冲（`4bbe36f`，#16）；服务端随作业清单下发 `stationDepartureDeadlineAt`（`0f6b424`，#12），车载端显示倒计时（`f47092b`，#15） | 车载端不只**显示**截止时间，还**执行**它——第 1 条那一轮宽限就是按它判的（#24）。期限仍由服务端算、服务端发。倒计时归零文案是「已到期，等待本站结束」，理由见 ADR-cross-0055。v2 线车载端只读期限、不据它结算，见下文「v2 线」一节 |
| 4 期限到期而仓门未闭时不结束本站 | `AwaitingSublot` 那一处判定在 `80d7c65`；`AwaitingLoadResult` 这一格挂 `STATION_TIMEOUT_DOOR_NOT_CLOSED` 并持续等待（`ReconcileStationTimeoutDoorNotClosedAsync`，`d36f11b`，#24）；就绪豁免按 agvId 收窄（`770447f`，#25） | 告警码只在 `AwaitingLoadResult` 可达——操作员扫了码、开了门、走开，正是本条 Consequences 点名的那一格。`AwaitingSublot` 时本站一条仓位命令都没发过，开着的门没有我方命令能解释，会话按离站安全转 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`，旅程挂 `ONBOARD_SESSION_NOT_READY`，原因读 `SessionRecoveries`（#25）。那不是操作员迟疑，是正确行为。「本站不结束」两格都成立 |
| 5 仓门已闭的超时按确定失败结算 | 服务端 `StationOperationStatus.Failed` 与确定失败判定（`5f8f5a7`）；车载端产出 `FAILED` + 三个明确物理字段 + `OPERATOR_TIMEOUT`（`3d8206f`，#24，此前服务端那段判定没有生产者）；服务端收到后自己终结需求（`CancelDemandAfterDeterminateLoadFailureAsync`，`de3960e`，#39），经「本批以终态结束」的收尾分支离站（`946d460`，#28） | 装货不再经 LoadTaskCancellation 终结。原文让旅程停在 `AwaitingLoadResult` 等这条取消，L2 实测没有任何一方会发它：车载端对结果已记录的 attempt 不给「取消装货」，`CancelDemandBeforeLoadAsync` 拒绝有过仓位操作的需求，站点期限与持货超时都不在这一格检查。现在服务端以 `CANCELLED_BY_STATION_TIMEOUT` 终结需求、永久抑制、结算悬空的装货命令，然后照常决定再装一轮、去下一站还是去关卡。服务端有权关站，是因为车辆只在期限过后再宽限一轮才报 `FAILED`，它到达时关站条件已经成立。「卸货不适用本条」不变。**车载端这一半已由 2026-09-18 的改写撤销**：v2 线车载端不产出确定失败，服务端那一半保留为防御性处理，见下文「v2 线」一节 |
| 6 未开始的仓位不因其它仓位失败被判失败 | 车载端按真实 IO 读数填 `NOT_STARTED`、`reasonCodes` 留空，并修掉失败仓位被后续循环改写成 `NOT_STARTED` 的覆盖（`4bbe36f`，#16） | 无 |
| 7 未录入 SUBLOT 超时后不再重派 | `SublotWaitTimeout` → `CancelDemandBeforeLoadAsync` → `TransportDemandSuppressions`（`80f6b93`），随 2026-09-09 的 RC 上线（#18） | 原文写「尚未部署」，已部署 |

### 真机验收

条件是 2026-09-11 改定的：`agv01` 真车走真实线路，IO 接车上的 slots-simulator（`127.0.0.1:1502`），
扫码、开关仓门、放料取空、按 HMI 与恢复全部由 `8005-agv-control-server` 的
`scripts/field/FieldOperator.psm1` 经两端自动化面冒充，现场无人；人只做每次派车的授权。证据都在
`8005-agv-control-server` 的 `evidence/field/` 下，车载端全程是 `6b8a0b0`。

| 窗口 | 时间 | 服务端 | 证据 | 结论 |
| --- | --- | --- | --- | --- |
| 窗口一 FW-SC1（#45） | 2026-09-11 21:28–22:13 | `403f306` | `20260911-FW-SC1-unattended`（`123c5f9`） | finalize **FAIL 18/20**，两条红都归因到驱动与判据，以本窗口结案 |
| 窗口二 FW-FL2 第一次（#20） | 2026-09-12 13:30–14:02 | `403f306` | `20260912-FW-FL2-unattended`（`d20bc6c`） | 中止、未 finalize：T、X 成立后撞上 #52 |
| 窗口二续跑 | 2026-09-12 15:02–16:30 | `e0d6df7` | `20260912-FW-FL2-resumed`（`a0f8940`） | 未 finalize，对照原始输出人工判：S52、NE、R1/R2、两趟完整闭环成立，CH 撞上 #53 |
| 窗口二充电短窗口 | 2026-09-12 18:22–18:55 | `3b379bb` | `20260912-FW-FL2-charging`（`f8d355e`） | finalize **PASS/14**：CH、完整闭环、R1 |

按决策看：

- **决策 1**：SC1-A-01..04 PASS。停靠 1 的 1 号仓空关两轮，车自己重开两次（`UNLOCKING` 1→2→3），
  第三次放料照常提交，没有 `FAILED`、没有 `RecoveryRequired`。卸货一侧是续跑窗口的 NE：关卡上 5 号仓
  带货关门两轮，车每轮自己重开，取空后提交（人工判）。
- **决策 2**：反面由 SC1-A-04、SC1-B-03、SC1-B-05 给出——开门不放料与确定失败都没有进恢复，会话保持
  `Ready`。正面在真车上只发生过一次，不在验收窗口里：#19 那次人工窗口留下的真 `UNKNOWN`（客户端在开锁
  等操作员时退出），修复上线后经自动化面补偿清空，5 秒对账 `Reconciled / ALL_EMPTY`，会话同一世代回到
  `Ready`（#44，2026-09-11 20:16）。
- **决策 3**：SC1-C-06 PASS。门一直开着，晾过 `OperationTimeout` 之后提示还在走，脉冲只打过一次。
- **决策 4**：SC1-C-01..05 PASS。停靠 2 的 3 号仓开着走开，21:42:09 期限到期，21:42:11 挂上
  `STATION_TIMEOUT_DOOR_NOT_CLOSED`，stage 停在 `AwaitingLoadResult` 而不是 `Blocked`，过期 20 分钟后
  仍然如此；关门后按真实 IO 结算，告警消失。
- **决策 5**：SC1-B-01..06 PASS。同一格关门不放料，决策 1 先重开一轮，第二次空关后 22:03:03 结算
  `Failed`，服务端自己把需求判 `Cancelled` 并按 `CANCELLED_BY_STATION_TIMEOUT` 永久抑制，旅程不经任何人
  按任何按钮离站。**这条「空关判取消」的路径已随 2026-09-18 的改写作废**：它验的是车载端期限过后产出
  确定失败，而 program#55 定的规程是空关照样重开、只有操作员按取消才放弃。SC1-B-01..06 的证据原样保留，
  但不再是本条任何决策的验收依据；服务端那一半的防御性结算另由 v2 线的 L1 与合成场景覆盖。
- **决策 6**：**现场没有专门的判据。**只由车载端单元测试覆盖（`WireToGateSlotOperationExecutorTests`
  里四处断言未开始的仓位是 `NOT_STARTED`），真车上没有单独观测过。
- **决策 7**：窗口二第一次的场景 T。停靠 1 车要 SUBLOT 没人扫，13:40:02 期限到，2 秒后需求
  `Cancelled / CANCELLED_BY_STATION_TIMEOUT` 并永久抑制，旅程自己去停靠 2（`02-t-settled` 帧，人工判）。
  更早的人工窗口 #19 在停靠 1 也照此结算过一条。

窗口二里另有几样不属于本条七条决策、但在同一个验收终点里：扫码前取消订单（X）、两趟之间自动充电
（CH：49% 触发，RIoT 单展开为 `move 212 → move 211 → act 78(1,0)`，接上电，62% 释放后接着受理）、一趟
五条需求的完整闭环、车静止时服务重启后几秒回到 `Ready`。

### 没有证明的

1. **SC1-A-05「操作员迟疑时 HMI 不出现恢复入口」在现场没有观测。**驱动脚本读过车载端快照，但写现场
   记录前抛错，这一项找不回来，如实判红（驱动缺陷已修，`33093ea`）。它只由 L2 真装置整窗彩排
   `real-onboard-field-window-rehearsal-010`、`-012` 覆盖。
2. **SC1-W-03 在窗口一的原判据下是红的。**`b-settled` 那一帧取在车驶离之后，拍到的是发车即降级的
   `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`，不是把开着的仓门当成会话故障。判据已改为行驶中的帧
   不判（`f2aceec`），对该窗口五帧空跑为 PASS；证据目录里的原判不改。
3. **光幕极性、锁反馈时序与机械弹开。**上面 Consequences 最后一句要求验收在真实 IO 模块上进行，理由
   正是模拟器证明不了这三样。2026-09-11 改定验收全部无人值守之后，本条不再证明它们；它们仍是本条每一条
   判据的物理前提，第一次接真实模块时要单独验。
4. **窗口二四次运行里只有充电短窗口完整 finalize**，第一次与续跑的结论是对照原始输出人工判的（各自的
   `ABORTED.md`）。
5. **决策 1/4/5 的现场证据跑在 `403f306` 上。**之后上线的 `e0d6df7`（#52：结束本站之后本轮就判出车前
   安全检查、回答过期换 id 重问）与 `3b379bb`（#53：自动充电）都改过旅程运行时。它们不碰这三条的判定
   本身，但确定失败之后「旅程自己离站」那段路径被 #52 改过。改过之后的覆盖是 `CONTROL_SERVER_G2` 的
   `W2G-IS-02`/`-03`/`-04`/`-07`（在 `889cbcb` 上，产品代码与 `e0d6df7` 相同）和续跑窗口里真车上的离站；
   FW-SC1 整窗彩排最后一次跑在 `9e7db45`，没有在线上身份上重跑。
6. **另外两台车。**
7. **决策 4 的告警升级规程**（对象、通道、节奏）按原文不在本条内。2026-09-13 已定
   （[program#55](https://github.com/trytoreachpeak0/8005-agv-program/issues/55)），见
   [`docs/site-procedures/station-door-not-closed-escalation.md`](../../site-procedures/station-door-not-closed-escalation.md)。
   它依赖的两件事尚未合入：看板投影（[control-server#42](https://github.com/trytoreachpeak0/8005-agv-control-server/issues/42)），
   以及期限到期后空关仍弹开、在途装货可取消（[onboard-hmi#48](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/48)）——
   后者改写了本条决策 1 与决策 5 的 2026-09-12 回写，改写文字 2026-09-18 已落在本文（v2 线由
   onboard-hmi#78 先行实现，#48 在 MVP 跟进线落地时引用同一份文字）。

### Consequences 里今天已不成立的几句

原文不改，逐条记在这里：

- 「不需要协议变更……均已在 `protocol-v0.1.1` 中定义……是否新增 `OPERATOR_TIMEOUT` 留待下一次协议
  批次」：本条没有为自己单独改协议，但两端现在 pin 的是 `protocol-v0.3.0`。那一批加了
  `OPERATOR_TIMEOUT`（`8005-agv-protocol` 的 `docs/candidate-limitations.md` 写明是为本条加的），车载端在
  确定失败的仓位上报的就是它（MVP 线；v2 线车载端不再产出它，见下文「v2 线」一节）；同批新增的 `stationDepartureDeadlineAt` 与 `slotOperationAttemptId` 两端
  都已补上发送方（#12、#15、#22）。
- 「按 `w2g/*` 分支加 PR 的路径交付，需 Kun Wang 同意」：2026-09-09 起同意与合并都归我方，本条的车载端
  PR 都由我方合并。
- 「ADR-cross-0055 的 StationDepartureWaiting 至今未实现，本条第 3、4 条依赖它」：不补那套状态机，站点
  期限由 `SublotWaitTimeout` 承担，映射见 ADR-cross-0055 的实现映射一节（#14）。
- 「L2 场景层需新增三条」：已补（#17），其中「仓门未闭超时」一条后来改钉 `AwaitingLoadResult`（#25）。
- 「验收必须在真实 IO 模块上进行」：见上一节第 3 条。

### 与 ADR-cross-0057 组合起来的约束

Consequences 说三个期限相互独立，这没有错；但放进同一趟旅程，它们会约束验收剧本怎么排。窗口一照「停靠 1
演 A、停靠 2 演 C 接 B」排：A 在停靠 1 装上货，持货时钟开始走（30 分钟，全旅程一次）；C 要晾「站点期限
5 分钟 + 20 分钟」，到停靠 3 时持货必然超时，停靠 3–5 的三条需求被 `CANCELLED_BY_STOP_COMPLETE` 结掉。
两条 ADR 各自的行为都对。换成 C/B 在停靠 1、A 在停靠 2 就排得开，因为 B 的确定失败不起算持货（#45，驱动
默认编排已改，`f2aceec`）。**任何要在装货站上久晾的现场动作，排在第一条装载提交之后都要先算这笔账。**

### 收尾时的现场配置

- `wireToGate.recoveryResumeEnabled` 出厂是 `false`，没有改。验收期间经工作区
  `remote-ops/onboard-hmi/scripts/14-set-recovery-window.ps1` 临时开过，每次都 `-Revert` 关回；2026-09-12
  在 agv01 上实读为 `false`，`CONTROL_SERVER_RECOVERY_PROOF` 不存在，自动化面关着。
- agv01 的 IO 仍指向模拟器 `127.0.0.1:1502`。重新部署车载端会把它渲染回真实模块。

## v2 线：按 program#55 改写决策 1 与决策 5（2026-09-18）

**本节是后加的。**上面各节记的是 MVP 线（`ControlServer_MVP`／`OnboardHmi_MVP`，`protocol-v0.3.0`）。
program#55 在 2026-09-13 定了现场规程，与决策 1、5 的 2026-09-12 回写相反；全产品 v2 线
（`fp/v2-impl`／`w2g/fp-v2-impl`，`protocol-v2.0.0`）还没有那段期限结算代码，于是直接按新定论实现，决策 1、5
的回写同日改写（见两条决策下的斜体说明）。MVP 线的同一改动在
[onboard-hmi#48](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/48) 跟进，引用本节同一份文字。

### 实现映射

| 改写后的决策 | v2 线实现 |
| --- | --- |
| 1 期限前后一样重开，放弃只有操作员按取消 | 车载端 [onboard-hmi#78](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/78)（[PR #103](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/pull/103)）：执行器本来就不读期限（批次5-20，onboard-hmi#72），期限过后空关照样重开；期限后提示与倒计时「已过期 mm:ss」；在途装货取消入口与 `recoveryResumeEnabled` 解绑；授权后先中止原执行器（`AbortOperationAsync`，重做 MVP `75d02de` 的中止通道），取消执行器接手开着的仓门、不再打脉冲，按 ADR-cross-0046 清空；中止后服务端重发的同一条 `SlotOperationCommand` 不再执行（重做 `1086c4a`）；取消应答未到时重启，中断结算不交 `UNKNOWN`，按首发内容重发取消请求（重做 `1acb018`） |
| 4 期限到期而仓门未闭，本站不结束、转告警 | 服务端 [control-server#81](https://github.com/trytoreachpeak0/8005-agv-control-server/issues/81)（合并提交 `72496a85`）：`STATION_TIMEOUT_DOOR_NOT_CLOSED`；看板在 control-server#80 |
| 5 车载端不产出确定失败，服务端保留防御性结算 | 服务端 control-server#81（`72496a85`）：`DeterminateLoadFailure.Judge` 只在收到至少一个仓位 `FAILED` 且期限已过时结算，否则按 `LOAD_FAILED_BEFORE_STATION_DEADLINE` 等进恢复；车载端 onboard-hmi#78 见下面的生产者核查 |

onboard-hmi#78 的合并提交在它合入 `w2g/fp-v2-impl` 之后补记到 program#61。

### 装货侧确定失败的生产者核查（onboard-hmi#78）

结论：**v2 车载端在装货侧没有任何路径产出期限后的确定失败，也不发 `OPERATOR_TIMEOUT`。**「门已闭、货没动、
开锁输出已复位」这一态仍然可达，但只是瞬时态，没有代码把它结算成结果。逐条核过的路径（`w2g/fp-v2-impl` 加
PR #103）：

1. `WireToGateSlotOperationExecutor.DriveSlotToTargetStateAsync`：读到相反态一律重开；车辆安全事实不许开锁时
   在 `HoldReopenUntilPermittedAsync` 里等，照样不结算；门开着只按 `OperationTimeout` 重复提示。整个执行器不读
   站点期限。上面那一态只出现在两次开锁之间或安全保持期间。
2. `ExecuteRemainingSlotsAsync` 的失败分支：只接 `IOException`／`TimeoutException`／`InvalidDataException`，
   即决策 2 的三种传感器不可信，结果是 `UNKNOWN`。
3. `CreateRejectedResult`：`overallOutcome` 是 `FAILED`，但只在开锁之前的预检失败时产出，每个仓位都是
   `NOT_STARTED`、没有仓位级 `FAILED`；服务端的判据要求至少一个仓位 `FAILED`，所以不会被当成确定失败。
   它唯一能在开过门之后被触发的路子是中止后重发的同一条命令（MVP `1086c4a` 实测过），onboard-hmi#78 已堵上。
4. `SettleInterruptedAsync`（中断结算）：只有 `COMPLETED` 与 `UNKNOWN`；有待答装货取消时不结算。
5. `ResumeAsync`（恢复后续作）：与 1、2 同一条闭环。
6. 仓位级结果：执行器里构造仓位结果只用 `COMPLETED`、`NOT_STARTED`、`UNKNOWN` 三种 outcome。
7. `WireToGateRecoveryVectorExecutor` 会给出 `FAILED`，但那是 `LoadCancellationResult`／`LoadCompensationResult`
   的结论，不是装货的 `OperationResult`。
8. `OPERATOR_TIMEOUT`：全仓只出现在 `WireToGateSessionClient` 的协议错误码登记表里，没有发送方。

卸货侧不受本节影响：`UnloadCompletionRequired` 无取消分支，照旧按决策 1 闭环到取空。

### 仍未证明的

- 真装置 L2：`real-onboard-load-door-closed-empty-reopens` 与 `real-onboard-cancellation-authorization-lost`
  由 control-server#86、#88 在 v2 线补跑，本节写成时还没有跑。
- 真车现场：v2 线还没有上车，SC1-B 那一格的替代验收（期限过后空关重开、操作员按取消收口）要等备用车窗口。