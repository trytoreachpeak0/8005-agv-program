# 协议消息采用明确的交付类别

同事初稿 §15、§16、§18、§24 分别规定了指令接受 ACK、无 ACK 的 OperationProgress、必须 ACK 的 OperationResult 和 HeartbeatAck，但没有统一交付语义。协议清单中的每个 messageType 必须固定归入一种 MessageDeliveryClass，发送方不能在调用时临时选择是否等待 ACK。

采用以下类别：

1. **可靠业务或安全消息**：接收方达到 DurableAcceptance 后返回显式 ACK；超时表示结果未知，发送方使用原 MessageId 和原内容重发。仓位操作指令、LoadCorrectionCommand、LoadCompensationCommand、OperationResult、LoadCorrectionResult、LoadCancellationResult、LoadCompensationResult、车载能力变化、DepartureSafetyRevoked 和业务就绪授权属于此类。ACK 只表示可靠接收，不表示动作完成。
2. **请求—响应消息**：响应的 correlationId 指向请求 MessageId；请求超时后使用原 MessageId 重试，接收方对重复请求返回原有或等价结果。SessionHello、SublotSubmitted、LoadCancellationStartRequested、恢复对账请求和 PreDepartureSafetyCheck 属于此类。
3. **非可靠遥测消息**：不 ACK、不补发，允许丢失；OperationProgress 属于此类，不能用于服务端业务入账。
4. **连接存活消息**：Heartbeat 对应 HeartbeatAck，只更新 ConnectionLivenessPolicy 的存活判断，不构成 DurableAcceptance，也不代表任何业务数据已经保存。
5. **可替换状态快照**：使用单调 revision 表达完整当前状态；发送方保留并重发最新版本直到 ACK，接收方原子应用后 ACK。旧版本可以丢弃且不需要逐事件补齐；CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot 属于此类。

**Status**: accepted

**Considered Options**:
- 所有消息都统一 ACK（拒绝：产生无意义 ACK 流量，并模糊遥测与业务事实的差别）
- 各功能自行决定 ACK 和重试方式（拒绝：相同故障会出现不同语义，难以统一恢复）
- 每种 messageType 在协议中固定声明交付类别（采纳）

**Consequences**:
- 接口确认稿的消息表必须增加“交付类别”和“去重键/关联方式”列。
- DurableAcceptance 必须落入可恢复存储；仅进入内存队列不能返回可靠 ACK。
- 对可靠消息或请求重试时不得改 MessageId、SlotOperationAttemptId 或内容；需要更改内容时必须创建新的语义消息，并遵守对应业务状态机。
- ACK 超时统一解释为“未知”，不能解释为“对方未执行”。
- OperationResult 的业务动作完成状态仍由其 payload 表达，不能从 OperationResultAck 推断。
- 可替换状态快照的 ACK 表示该 revision 已被采用；车载端重启后不依赖本地持久化列表，RecoveryHandshake 必须重新取得最新快照。
