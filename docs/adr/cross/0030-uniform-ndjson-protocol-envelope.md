# 所有车载通信消息使用统一 NDJSON 外壳

同事初稿 §9.1 已确定车载—服务端使用 UTF-8 编码、每行一个 JSON 对象的 NDJSON 长连接，但未定义消息公共元数据。所有消息统一使用 ProtocolEnvelope，顶层字段固定为：

- `protocolVersion`：本消息使用的协议版本。
- `messageType`：消息类型。
- `messageId`：本条语义消息的稳定唯一编号。
- `correlationId`：响应或 ACK 所对应请求的 messageId；无对应请求时为 null。
- `agvId`：消息所属车辆。
- `sessionGeneration`：服务端授予的当前 VehicleConnectionSession 代次。
- `sentAt`：发送方时间，仅用于审计和诊断。
- `payload`：具体消息的业务内容对象。

`SessionHello` 发出时尚未取得服务端授予的代次，因此它的 `sessionGeneration` 为 null；认证拒绝等发生在会话授予前的响应也可为空。从 `SessionAccepted` 开始，属于已接受会话的消息必须携带正确代次，否则服务端或车载端按旧会话消息拒绝处理。

MessageId 标识一条语义消息：网络重发或重连补发同一消息时沿用原编号，内容或语义发生变化时必须使用新编号。ACK 或响应通过 correlationId 指向原 MessageId。SlotOperationAttemptId 标识整次有序多仓物理操作尝试，字段名为 `slotOperationAttemptId`，位于相关 payload 中，不能代替 MessageId。

**Status**: accepted

**Considered Options**:
- 各类消息自行定义顶层字段（拒绝：日志、鉴权、会话隔离和 ACK 处理会重复且不一致）
- 只保留 messageType 和 payload（拒绝：无法可靠去重、关联响应或隔离旧连接消息）
- 使用固定 ProtocolEnvelope，业务数据统一放入 payload（采纳）

**Consequences**:
- 所有 §10 消息以及新增的恢复握手消息必须使用同一序列化外壳。
- correlationId 可空，但字段本身必须存在，避免“未提供”与“没有关联”混淆。
- sentAt 不参与消息排序、超时或安全判定；这些判断使用会话代次、业务编号和本机单调时钟。
- 接收端应先校验外壳，再反序列化对应 payload；外壳无效的消息不得进入业务处理。
- 需要进一步明确 protocolVersion 的兼容与拒绝规则。
