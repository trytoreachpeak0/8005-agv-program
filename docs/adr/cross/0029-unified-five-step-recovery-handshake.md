# 首次连接与重连采用统一五步恢复握手

同事初稿 §10 的消息清单没有连接后的业务恢复握手；§18、§20、§21 分散描述了最终结果确认、重复 SlotOperationAttemptId 对账和重连补报。为避免首次启动与重连产生两套状态机，二者统一执行 RecoveryHandshake：

1. 车载端发送 `SessionHello`，服务端验证身份和协议后返回 `SessionAccepted`，并建立 ADR-cross-0023 规定的带代次 VehicleConnectionSession。
2. 车载端发送完整 `CapabilitySnapshot`。
3. 车载端发送 `RecoveryStateReport`，明确报告未结 SlotOperationAttemptId、OnboardExecutionJournal 的 ProvenRecoveryCheckpoint，以及待确认 OperationResult；没有未结状态也必须显式报告为空。
4. 车载端沿用原 SlotOperationAttemptId 补报 OperationResult，服务端按既定规则逐条确认，直到双方对待确认结果达成一致。
5. 服务端发送 `SessionReadiness`，结果只能为 `READY` 或 `RECOVERY_REQUIRED`，并携带可诊断的原因码。

只有 `SessionReadiness=READY` 才授予 VehicleBusinessReadiness。握手期间仅允许心跳、能力同步、恢复对账、结果补报、诊断和必要的安全处置消息。服务端是业务就绪的唯一授予方，车载端不能依据自身检查结果自行进入就绪。

**Status**: accepted

**Considered Options**:
- 首次连接直接就绪，仅重连执行恢复（拒绝：服务端无法证明首次启动的车载存储和 IO 确实没有遗留状态）
- 各类同步消息无固定顺序，到齐后自动就绪（拒绝：实现容易出现竞态，也难以诊断卡在哪个恢复阶段）
- 首次连接和重连共用五步握手，服务端最后明确裁决（采纳）

**Consequences**:
- 初稿 §10 需要新增 `SessionHello`、`SessionAccepted`、`CapabilitySnapshot`、`RecoveryStateReport` 和 `SessionReadiness`。
- Heartbeat/HeartbeatAck 从会话接受后持续运行，不受后续恢复阶段阻塞。
- 如果握手完成前再次断线，新连接必须取得新代次并从第一步重新执行；旧会话后到消息按 ADR-cross-0023 丢弃。
- `RECOVERY_REQUIRED` 必须包含稳定原因码，界面文案不能作为协议判断依据。
- 第四步的结果补报继续遵守 ADR-cross-0014 的同一 SlotOperationAttemptId 对账和初稿 §18 的可靠 ACK 规则。
