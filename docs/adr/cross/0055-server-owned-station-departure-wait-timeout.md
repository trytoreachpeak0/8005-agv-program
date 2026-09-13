# 服务端掌握装货站离站等待超时并原子结束本站

为了避免多仓位 AGV 在装货站因无人继续操作或无人点击“本站装货完成”而无限停留，服务端在车辆进入 StationDepartureWaiting 时启动 StationDepartureWaitTimeout。第一版项目默认 5 分钟，允许站点覆盖；车载端只显示服务端截止时间。每个 LoadBatch 或 LoadCorrection 安全闭环、放弃尚未产生物理动作的操作，以及新增待装 DemandId 的新版作业清单被车载确认后，都从完整时长重新计时。操作员不能暂停或延长期限；只有服务端先接受装货开始或纠错请求才退出等待。截止后服务端以 StopClosureCommit 原子终结本站并将全部尚未开始的待装 DemandId 记为 `CANCELLED_BY_STATION_TIMEOUT`；已核验操作员主动结束本站时使用同一流程并记为 `CANCELLED_BY_STOP_COMPLETE`。提交后关闭 OperationSession、清除 OnboardOperatorContext，待车载采用最新 CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot 并通过 PreDepartureSafetyCheck 后，才向 RIoT 请求移动。

StationDepartureWaiting 只适用于服务端裁定可继续装货的站点。纯卸货站卸完直接结束；装卸混合站须先完成全部卸货。部分 LoadBatch、LoadCorrectionPending、活动仓位操作、状态未知或断联均阻断倒计时离站；部分装货无进展达到同一时长时只告警。倒计时期间断联使本轮截止时间失效，恢复握手和投影对账完成后重新计满。装货开始、纠错开始与超时提交在服务端原子互斥，以先成功持久化者生效。

**Status**: accepted

**Considered Options**:
- 车载端独立倒计时并直接发车（拒绝：车载端不拥有任务、调度和取消事实）
- 提供“继续等待”让操作员延长（拒绝：可被反复使用而使车辆继续无限占站）
- 服务端掌握期限、原子结束本站并在投影同步和实时安全核验后发车（采纳）

**Consequences**:
- StationDepartureWaitPolicy 的项目默认值已实现，第一版 5 分钟；**可选的站点覆盖没有实现**，全线共用一个值（详见下方实现映射）。
- 手动结束与自动超时共享 StopClosureCommit，但使用不同的取消终态和审计主体。
- 发车失败不复活已取消任务，而是进入“本站已结束，等待发车重试”。
- 无下一 PlannedStop 且空载时进入停车点流程；载有已提交 Sublot 却无下一站时原地保持并报警。
- 车载界面在服务端给出截止时间时全程显示剩余时间，最后 60 秒转黄、最后 10 秒转红并逐秒闪烁，不依赖声音设备。期限缺席与期限耗尽这两种状态界面必须能分别表达：`stationDepartureDeadlineAt` 为空时（纯卸货站、关卡站、超时被配置为禁用）显示“无倒计时”而不是 00:00；剩余时间归零后不显示负数，改显示“已到期，等待本站结束”——ADR-cross-0058 决策 4 使期限到期不必然结束本站，仓门未闭时车辆会带着一个已耗尽的倒计时继续等下去；而仓门已闭时，按期限结算的是车辆自己（见文末 2026-09-12 核对），所以文案不说是谁在结算。2026-09-09 版这里写的是“等待服务端结算”。

## 实现映射（2026-09-09）

本 ADR 的三个名字——StationDepartureWaiting、StationDepartureWaitTimeout、StopClosureCommit——在
`8005-agv-control-server` 的 `src/` 里全部 0 命中。决策没有变，落成的形状与命名与本文不同：它搭在
ADR-cross-0058 决策 4 一并实现的 `SublotWaitTimeout` 上（`80d7c65`），而不是另起一套按原名命名的状态机。
之所以不补：服务端已有三个独立期限——`SublotWaitTimeout` 管“这次停靠还等不等人”、`HoldingTimeout` 管
“这趟车还收不收货”（ADR-cross-0057）、ADR-cross-0058 的仓位目标态不设上限——再加第四个只会让“车到底在
等什么”更难说清。

| 本文的名字 | 承载它的实现 |
| --- | --- |
| StationDepartureWaiting 状态 | `JourneyRuntimeStage.AwaitingSublot`（`ControlServer.Domain/WireToGateModels.cs:210`）。不是新状态——服务端本来就有一个“到站后等操作员录 SUBLOT”的 stage，期限挂在它上面 |
| StationDepartureWaitTimeout 选项 | `JourneyRuntimeOptions.SublotWaitTimeout`，默认 5 分钟；`TimeSpan.Zero` 表示禁用，非零时校验要求至少 5 秒（`JourneyRuntimeOptions.cs:60`、`:110`） |
| 计时起点 | `JourneyStopRow.SublotWaitStartedAt`，**每个停靠一份**。三处种下：发作业清单前（`JourneyRuntimeEngine.cs:988`，必须早于清单发出，否则车辆第一份快照里的倒计时是空的）、`SetStage` 进入该 stage 时（`:2219`）、断联后重填（`:547`） |
| “每个 LoadBatch 闭环后从完整时长重新计时” | `TryContinueLoadingAtStopAsync` 里的硬重置 `stop.SublotWaitStartedAt = now`（`:2418`），随下一轮作业清单一起发出 |
| “断联使本轮截止失效，恢复握手与对账后重新计满” | 会话失效时 `WireToGateStore` 把当前停靠的 `SublotWaitStartedAt` 置 null（`WireToGateStore.cs:90`），`AwaitingSublot` 分支在 readiness gate 之后重填——落在 gate 之后即是“握手与投影对账完成之后” |
| 到期判定 | `TryTimeOutSublotWaitAsync`（`JourneyRuntimeEngine.cs:2110` 起），只在 `AwaitingSublot` 且本轮找不到匹配 SUBLOT 时调用 |
| “只有服务端先接受装货开始或纠错请求才退出等待” | `FindMatchingSublotAsync` 返回非空即离开等待，转入重校验与发命令 |
| “活动仓位操作阻断倒计时离站” | 由 stage 机天然承担：有活动仓位操作时旅程在 `AwaitingLoadResult`/`AwaitingUnloadResult`，到期判定根本不会被调用（`:637` 的注释就是为此写的） |
| “部分装货无进展达到同一时长时只告警” | ADR-cross-0058 决策 4 落成 `STATION_TIMEOUT_DOOR_NOT_CLOSED`：仓门未闭时把 `runtime.BlockReasonCode` 设成该码并持续等待，stage 仍留在 `AwaitingSublot` 而**不转 Blocked**（`:2122` 起） |
| “车载端只显示服务端截止时间” | `StationDepartureDeadline(stop)`（`:2013`）由 `SublotWaitStartedAt + SublotWaitTimeout` 得出，随 `CurrentStopWorklistSnapshot` 的 `stationDepartureDeadlineAt` 下发（protocol-v0.3.0，服务端侧 `0f6b424`）。关卡站与超时禁用两种情况都发 `null` |
| `CANCELLED_BY_STATION_TIMEOUT` | 到期且仓门已闭时，对本停靠全部待装需求调 `CancelDemandBeforeLoadAsync`，并由 `TransportDemandSuppressions` 按 TransportDemandKey 写永久禁令（ADR-cross-0058 决策 7） |
| `CANCELLED_BY_STOP_COMPLETE` | 终态已注册（`WireToGateStore.cs:1205`）并在用，但**写它的不是操作员按钮**：`grep StopComplete` 在服务端零命中，实际由 `ConcludeLoadingStopAsync` 的 `HoldingExpired` 分支写入。**“已核验操作员主动结束本站”这个入口尚未实现** |
| StationDepartureWaitPolicy 的站点覆盖 | **未实现**，只有全局选项。当前没有需要不同时长的站点；真要加，落点是这个选项按 StationId 取值，判定点 `TryTimeOutSublotWaitAsync` 与下发点 `StationDepartureDeadline` 从同一处读，两边不会分叉 |

### 为什么没有一个叫 StopClosureCommit 的动作

“原子结束本站”被实现成一段共同尾部，而不是一个具名动作。到期结算的两步——逐条终结未开始的待装需求，
然后交给 `ConcludeLoadingStopAsync` 决定去下一个取货站还是关卡站并发出 `PreDepartureSafetyCheck`——写在
`TryTimeOutSublotWaitAsync` 里，落在同一次 `SaveChangesAsync` 中。

这么做是因为“结束本站”有三个入口：本站已装满或没有更多可装、持货超时（ADR-cross-0057）、本条的站点期限
到期。三者的差别只在“谁被取消、记什么理由”，尾部完全相同，而那个尾部就是 `ConcludeLoadingStopAsync`。
再包一层具名动作只会多一层间接；本文要求的原子性由 EF Core 的工作单元承担，不需要一个函数来命名它。

一处读代码时容易看反的地方：到期结算遍历的是 `PendingAt`（本停靠全部 `Planned` 需求），不是
`UncommandedAt`（其中还没发出装货命令的那些）。而 `CancelDemandBeforeLoadAsync` 碰到已记录 station
operation 的需求会抛 `BusinessIdentityConflictException`，不是跳过。两者不冲突，靠的是状态机不变式：装货
命令一发出旅程立刻转 `AwaitingLoadResult`，所以处在 `AwaitingSublot` 时不存在“已命令但未结算”的需求。这个
安全性来自 stage，不来自那个筛选条件本身。

## 实现映射核对（2026-09-12）

上表写于 2026-09-09。ADR-cross-0058 转 accepted 时（8005-agv-program#21）按线上服务端 `3b379bb` 与车载端
`6b8a0b0` 核了一遍：表里的名字全部还在，**行号已漂移，按名字查**；决策没有变。有三处与上表或上一节不再一致：

1. **到期判定多了一个执行点，在车上。**上表“到期判定”只列了 `TryTimeOutSublotWaitAsync`，它只在
   `AwaitingSublot` 跑。扫了 SUBLOT、仓位操作在途的 `AwaitingLoadResult` 那一格服务端不判——有在途操作时
   它既发不走车，也没有中止通道——由车载端按下发的 `stationDepartureDeadlineAt` 执行：仓门已闭而货没动时，
   期限过后再宽限一轮，第二次读到仍是相反态就报 `FAILED` / `OPERATOR_TIMEOUT`（车载端 `3d8206f`，
   8005-agv-program#24）。期限仍由服务端算、服务端发；本文“车载端只显示服务端截止时间”在这一格收窄为
   “车载端按服务端截止时间执行”。
2. **“部分装货无进展只告警”那一行的告警码有两个产地，现场可达的是另一个。**`STATION_TIMEOUT_DOOR_NOT_CLOSED`
   在 `AwaitingLoadResult` 由 `ReconcileStationTimeoutDoorNotClosedAsync` 挂上（`d36f11b`），2026-09-11 在
   真车上观测到（ADR-cross-0058 Verification，SC1-C-01）。表里写的 `AwaitingSublot` 那一处代码还在，但那一格
   一条仓位命令都没发过，开着的门没有我方命令能解释，会话先转 `RecoveryRequired`，旅程在就绪门挂的是
   `ONBOARD_SESSION_NOT_READY`，原因读 `SessionRecoveries`（8005-agv-program#25）。
3. **“结束本站”现在有四个入口，不是三个。**上一节列的三个——本站已装满或没有更多可装、持货超时、站点期限
   到期——之外，多了“本批以另一种终态结束”：操作员取消、补偿清空、故障货物交接（8005-agv-program#28），以及
   装载确定失败（8005-agv-program#39，`de3960e`：服务端以 `CANCELLED_BY_STATION_TIMEOUT` 终结需求后进这一支）。
   它的尾部仍是 `TryContinueLoadingAtStopAsync` 不成立时的 `ConcludeLoadingStopAsync`，所以“一段共同尾部而非
   具名动作”的判断不变。确定失败这个入口之所以归本文管，是因为车辆只在本站期限过后再宽限一轮才报 `FAILED`，
   它到达时关站条件已经成立。

“已核验操作员主动结束本站”入口仍不存在（服务端 `StopComplete` 仍零命中），站点覆盖仍未实现。
