# 服务端掌握装货站离站等待超时并原子结束本站

为了避免多仓位 AGV 在装货站因无人继续操作或无人点击“本站装货完成”而无限停留，服务端在车辆进入 StationDepartureWaiting 时启动 StationDepartureWaitTimeout。第一版项目默认 5 分钟，允许站点覆盖；车载端只显示服务端截止时间。每个 LoadBatch 或 LoadCorrection 安全闭环、放弃尚未产生物理动作的操作，以及新增待装 DemandId 的新版作业清单被车载确认后，都从完整时长重新计时。操作员不能暂停或延长期限；只有服务端先接受装货开始或纠错请求才退出等待。截止后服务端以 StopClosureCommit 原子终结本站并将全部尚未开始的待装 DemandId 记为 `CANCELLED_BY_STATION_TIMEOUT`；已核验操作员主动结束本站时使用同一流程并记为 `CANCELLED_BY_STOP_COMPLETE`。提交后关闭 OperationSession、清除 OnboardOperatorContext，待车载采用最新 CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot 并通过 PreDepartureSafetyCheck 后，才向 RIoT 请求移动。

StationDepartureWaiting 只适用于服务端裁定可继续装货的站点。纯卸货站卸完直接结束；装卸混合站须先完成全部卸货。部分 LoadBatch、LoadCorrectionPending、活动仓位操作、状态未知或断联均阻断倒计时离站；部分装货无进展达到同一时长时只告警。倒计时期间断联使本轮截止时间失效，恢复握手和投影对账完成后重新计满。装货开始、纠错开始与超时提交在服务端原子互斥，以先成功持久化者生效。

**Status**: accepted

**Considered Options**:
- 车载端独立倒计时并直接发车（拒绝：车载端不拥有任务、调度和取消事实）
- 提供“继续等待”让操作员延长（拒绝：可被反复使用而使车辆继续无限占站）
- 服务端掌握期限、原子结束本站并在投影同步和实时安全核验后发车（采纳）

**Consequences**:
- StationDepartureWaitPolicy 使用项目默认值和可选站点覆盖，第一版默认 5 分钟。
- 手动结束与自动超时共享 StopClosureCommit，但使用不同的取消终态和审计主体。
- 发车失败不复活已取消任务，而是进入“本站已结束，等待发车重试”。
- 无下一 PlannedStop 且空载时进入停车点流程；载有已提交 Sublot 却无下一站时原地保持并报警。
- 车载界面全程显示剩余时间；最后 60 秒黄色，最后 10 秒红色逐秒闪烁，不依赖声音设备。
