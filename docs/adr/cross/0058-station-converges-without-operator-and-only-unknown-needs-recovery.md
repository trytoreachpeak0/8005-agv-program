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
| 站点期限 | 无 StationDepartureWaiting；只有 `JourneyRuntimeOptions.SublotWaitTimeout`（默认 5 分钟）覆盖「未录入 SUBLOT」 | ADR-0055 的 StopClosureCommit 未实现 |
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

2. **只有 UNKNOWN 进人工恢复。** SlotOccupancyState 为 UNKNOWN、锁闭反馈无效或开锁输出无法确认
   复位，才暂停并进入恢复。人未放料、未取料、未关门都不是 UNKNOWN。

3. **车载端 `OperationTimeout` 不再是判死依据。** 它退化为提示与告警的节拍，不产生业务终态。
   站点能停多久由服务端按 ADR-cross-0055 掌握，车载端只显示服务端截止时间。

4. **站点期限到期而仓门未闭时，不结束本站。** 这是基线未覆盖的一格。StopClosureCommit 要求车辆
   随后能够离站，而未闭合的仓门使离站不可能，因此期限到期只把该站转入告警升级状态并持续等待仓门
   闭合，闭合后立即按当时的真实 IO 读数结算。**告警升级的对象、通道与节奏由项目现场规程规定，
   不在本 ADR 内。**

5. **仓门已闭合的超时按确定失败结算，不进恢复。** 期限到期时若仓门已闭、开锁输出已复位、
   SlotOccupancyState 明确，车载端报 `overallOutcome: FAILED` 与真实的三个物理字段；服务端据此
   走确定失败路径而非 `RecoveryRequired`。装货依 ADR-cross-0015 与 ADR-cross-0046 经
   LoadTaskCancellation 终结，**卸货不适用本条**——UnloadCompletionRequired 无取消分支，仍按
   第 1 条持续闭环直到取空。

6. **未开始的仓位不因其它仓位失败而被判失败。** 现行实现把 `command.Slots` 中所有未完成仓位
   一并写成 `NOT_STARTED` + `UNKNOWN`，使 2 号仓在从未开启的情况下进入恢复范围。未开启的仓位
   没有任何物理不确定性，应保持 `NOT_STARTED` 且不触发恢复。

7. **未录入 SUBLOT 超时后该订单不再重派。** 现行行为——`SublotWaitTimeout` 到期后
   `CancelDemandBeforeLoadAsync` 记 `CANCELLED_BY_STATION_TIMEOUT`，并由
   `TransportDemandSuppressions` 按 TransportDemandKey 写入永久禁令，候选评分以
   `TRANSPORT_DEMAND_SUPPRESSED` 挡下——**即为期望行为**，无需改动。车辆释放去接后续需求，该订单
   由 MES 侧另行处理。Zhengyu Shao 于 2026-09-08 确认。

**Status**: proposed

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
