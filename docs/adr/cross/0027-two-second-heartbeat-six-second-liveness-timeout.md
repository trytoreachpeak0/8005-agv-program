# 采用 2 秒心跳与 6 秒静默失联判定

同事初稿 §24 建议车载端每 5 秒发送一次 Heartbeat、服务端返回 HeartbeatAck，但没有规定正式失联阈值。为使行驶断链保护能够及时触发，车载上位机每 2 秒发送一次心跳；任一侧收到属于当前 VehicleConnectionSession 的合法协议消息时，都刷新本侧最后接收时间。TCP 明确断开时立即判定失联；连接未断但连续 6 秒没有收到合法消息时，判定连接失联。

心跳与失联阈值是项目级统一配置，不允许按车辆设置不同值。单次心跳丢失不构成失联。失联发生时，仓位操作按 ADR-cross-0003 进入断联仓位操作收敛，行驶状态按 ADR-cross-0026 触发 MovementConnectionLossHold。

**Status**: accepted

**Considered Options**:
- 沿用 5 秒心跳且不定义失联阈值（拒绝：无法形成一致状态机，也无法确定何时触发行驶保护）
- 5 秒心跳、连续三次丢失后判定（拒绝：最坏约 15 秒才介入，行驶场景过慢）
- 2 秒心跳、6 秒静默或 TCP 明确断开时判定失联（采纳）

**Consequences**:
- 心跳必须独立于仓位操作和结果补报持续运行，不能因业务处理繁忙而停止。
- HeartbeatAck 仍由服务端返回；业务消息可以证明连接活跃，但不能替代周期性心跳的发送责任。
- 存活计时使用本机单调时钟；对端消息携带的时间只用于诊断，不用于计算本侧超时。
- Heartbeat payload 只携带 ADR-cross-0022 的 capabilityVersion 与 ADR-cross-0034 的 safetyStateVersion；发送时间使用 ProtocolEnvelope.sentAt，不承载完整能力或安全状态快照。
- 后续接口确认稿应将 §24 的“建议值”改为上述已确认规则。
