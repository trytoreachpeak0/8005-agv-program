# 车载通信采用整数版本并要求精确匹配

同事初稿 §9.1 确定了 NDJSON 长连接，但未规定协议升级与不兼容处理。第一版 ProtocolEnvelope 的 `protocolVersion` 固定为整数 `1`，不引入 major/minor 范围协商。

同一 ProtocolVersion 内只允许增加可选字段；接收方必须忽略不认识的可选字段。删除或新增必填字段、改变已有字段含义、改变消息处理语义，或者增加会影响既有状态机的强制步骤，都属于破坏性变更，必须提升 ProtocolVersion。

`SessionHello` 使用车载端支持的版本。服务端只在版本精确匹配时返回 `SessionAccepted`；版本不一致时返回 `SessionRejected`，原因码为 `UNSUPPORTED_PROTOCOL_VERSION`，不授予 sessionGeneration，也不允许车辆进入 VehicleBusinessReadiness。

**Status**: accepted

**Considered Options**:
- 不携带版本，部署时保证两端一致（拒绝：错配只能通过运行故障暴露）
- 使用 major/minor 范围协商（拒绝：当前项目不需要同时维护多套协商分支）
- 使用整数版本、可选字段保持向后兼容、破坏性变更升版并精确匹配（采纳）

**Consequences**:
- 两端升级涉及破坏性协议变化时必须协调部署；未升级车辆会明确保持未就绪。
- 增加可选字段时不得让其缺失改变旧接收端的安全或业务判断。
- 未知可选字段可以忽略，但未知 messageType 不属于可选字段兼容，必须按协议错误处理。
- 协议版本与服务端、车载软件自身版本分开记录，不能用安装包版本代替。
- 后续接口确认稿应在 §9.1 和所有消息示例中固定写出 `protocolVersion: 1`。
