# 车辆已连接不等于业务就绪

同事初稿 §9.1 定义车载端主动建立 TCP 长连接，§18、§20、§21 分别定义最终结果确认、重复操作对账和重连补报，但没有定义连接恢复后何时可以重新承接业务。VehicleConnectionSession 建立并通过 TLS 与 VehicleCredential 认证，只表示通信可用，不表示车辆已经达到 VehicleBusinessReadiness。

服务端必须在全量车载能力同步、未结 SlotOperationAttemptId 与 OnboardExecutionJournal 状态对账、积压 OperationResult 补报、SlotPhysicalState 与 SlotBusinessState 核对均通过后，明确授予 VehicleBusinessReadiness。在此之前只允许心跳、能力同步、恢复对账、结果补报、诊断和必要的安全处置消息，不允许开始扫码、下发新的仓位操作或执行 OrderContinue。

若存在无法自动解释的状态差异，连接保持在线并进入 VehicleRecoveryRequired，由人工处置；不得为了恢复产线而默认信任任一侧状态。若原因是锁 DI 等硬件故障，信号重新有效后仍须取得 HardwareRecoveryConfirmation，服务端才可重新授予业务就绪或授权原操作继续。

**Status**: accepted

**Considered Options**:
- TLS/TCP 连接成功后立即允许业务（拒绝：未结操作和积压结果尚未对账，可能重复开仓或覆盖业务事实）
- 发现差异时自动以车载物理状态或服务端业务状态覆盖另一侧（拒绝：违反“物理事实归车载端、业务事实归服务端”）
- 连接后先恢复对账，由服务端明确授予业务就绪；无法对账则转人工恢复（采纳）

**Consequences**:
- 服务端必须维护独立于连接在线状态的车辆业务就绪状态。
- 车载界面应分别展示“已连接”和“业务就绪/待恢复”，不能只显示一个在线指示灯。
- Heartbeat 和 HeartbeatAck 在未就绪或待恢复状态仍持续工作。
- 行驶中断链后的 OrderContinue 也受此状态约束，并且仍须新的 PreDepartureSafetyCheck。
- 后续接口确认稿应补充就绪授权与待恢复结果，不能仅依靠连接建立事件隐式放行业务。
