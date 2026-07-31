# 车载端可靠发布抽象安全状态变化

同事初稿 §2.3 将 IO 控制和机构安全裁决归车载端，§16 的 OperationProgress 不可靠，§17 只在最终结果中携带一次 departureSafe，§17.4 与 §27 又明确服务端负责移动决策。若车辆空闲期间发生仓门开启、光幕异常或 IO 离线，服务端不能继续依赖旧的安全快照。

车载端在抽象安全状态发生变化时可靠发送 `SafetyStateChanged`。payload 至少包含：

- `departureSafe`
- `safetyStateVersion`
- 受影响的物理仓位号；整车级变化时允许为空
- 稳定的抽象原因码
- `observedAt`

消息不得包含原始 DI/DO 值、IO 通道映射或 IO 配置。服务端达到 DurableAcceptance 后返回 ACK，并据此更新 SafetyStateProjection。该投影用于阻断业务、触发处置、界面显示和诊断，但 SlotPhysicalState 的权威仍在车载端；收到恢复安全事件也不能替代下一次 PreDepartureSafetyCheck。

车辆已经处于服务端授权的移动阶段时，`SafetyStateChanged` 中从安全到不安全的转换同时构成 DepartureSafetyRevoked，服务端按 ADR-cross-0010 和 ADR-cross-0011 自动介入，不要求车载端再发送一条内容重复的线协议消息。

**Status**: accepted

**Considered Options**:
- 服务端周期读取原始 IO（拒绝：违反 ADR-cross-0004 的车载独占 IO 权限）
- 只在 OperationResult 和发车检查时取得安全状态（拒绝：两次检查之间的安全变化无法及时触发服务端动作）
- 车载端可靠推送抽象安全变化，服务端只保存非权威投影（采纳）

**Consequences**:
- `SafetyStateChanged` 属于 ADR-cross-0032 的可靠安全消息，必须持久化、ACK 和使用原 MessageId 补发。
- 服务端不能根据 SafetyStateProjection 的 true 直接发车，只能将 false 用作立即阻断条件。
- RecoveryHandshake 必须取得当前完整抽象安全状态及版本，才能授予 VehicleBusinessReadiness。
- 需要利用 safetyStateVersion 发现事件缺口，并在发现缺口时重新取得完整安全状态。
- 后续接口确认稿应在 §10 增加该消息，并修订 §17.4，说明 departureSafe 不再只存在于最终结果快照。
