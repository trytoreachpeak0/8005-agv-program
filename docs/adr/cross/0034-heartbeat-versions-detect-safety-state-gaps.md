# 心跳通过版本号发现能力与安全状态缺口

同事初稿 §24 的 Heartbeat/HeartbeatAck 只用于连接存活，无法发现可靠状态消息因重启、存储故障或实现缺陷造成的漏报。Heartbeat payload 固定只携带 `capabilityVersion` 和 `safetyStateVersion`；发送时间由 ProtocolEnvelope.sentAt 提供，不在 payload 中重复，也不携带仓位列表、原始 IO 或具体安全状态。

服务端将心跳版本与已确认的 OnboardCapabilitySnapshot 和 SafetyStateProjection 比较。发现 safetyStateVersion 未知、回退、跳号或与当前投影不一致时，立即进入 SafetyStateUnknown，阻断新的仓位操作和移动，并请求完整 SafetyStateSnapshot。若车辆当时正在执行移动，按 ADR-cross-0011 的任务来源分级规则暂停、取消或升级急停。

完整快照能够与当前 VehicleConnectionSession、车载能力及服务端业务事实自动对账时，服务端自动解除 SafetyStateUnknown；仍存在无法解释的矛盾时才进入 VehicleRecoveryRequired，避免普通版本补同步都要求人工处理。

**Status**: accepted

**Considered Options**:
- 心跳只证明连接在线（拒绝：状态事件缺口可能长期不被发现）
- 心跳携带完整能力与安全状态（拒绝：重复数据量大，并模糊可靠状态同步与存活探测）
- 心跳只携带两个版本，差异时按状态未知阻断并拉取完整快照（采纳）

**Consequences**:
- capabilityVersion 或 safetyStateVersion 不匹配都不能只显示告警后继续工作。
- SafetyStateSnapshot 只包含抽象安全事实，不改变 ADR-cross-0004 的车载 IO 权限边界。
- 版本差异首先触发可自动完成的重新同步，不直接等同于人工恢复。
- HeartbeatAck 可回传服务端当前已确认的两个版本，帮助车载端发现服务端投影落后，但不承担可靠 ACK。
- 后续接口确认稿应在 §24 明确 Heartbeat payload，并在 §10 新增 SafetyStateSnapshot 的请求与响应。
