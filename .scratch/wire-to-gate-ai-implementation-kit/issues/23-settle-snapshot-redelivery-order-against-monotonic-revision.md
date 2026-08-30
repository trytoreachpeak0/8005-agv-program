# 快照重发顺序对上车载端的单调 revision 规则

Type: task
Mode: AFK
Status: open
Blocked by: 22

## Question

票 22 在只读检查 `OnboardHmi_MVP@304e6ad` 时确认了车载端的采用判据：已采用快照按 **MessageType**
持久在 SQLite，**更低 revision 一律判 `SNAPSHOT_REVISION_REGRESSION`**，随后发 protocol problem 并
rethrow，连接被拆。

票 22 修的是 revision **分配**（跨趟不再回退）。但**重发顺序**是另一条路径，未处理：

服务端对未确认的 outbox 行按行内顺序重发。若某条快照的 `SnapshotAppliedAck` 丢失，而更高 revision
的下一条快照已被对端采用，则那条旧快照的重发会带着**更低的 revision** 到达——按上述判据，同样拆连接。

票 22 的测试 fixture 里 peer 从不 ACK，因此实际观测到过这个序列（三条流各自 `1, 2, 1, 2, …`
的重发交错），只是被按 messageId 去重的断言排除在外，因为它不属于 revision 分配。

**要回答的是：这在真实对端上可达吗？如果可达，归谁修？**

- 服务端在收到更高 revision 的 ACK 后，是否应把同类型的更低 revision outbox 行判为已被取代
  （superseded）而停止重发？
- 还是应由车载端按 ADR-cross-0048 原文「更低 revision 丢弃并返回当前已采用版本」处理？
  ——但那是车载端行为，仓对 agent 只读，不能在本项目内修。

### 完成判据

- 先用一次可证伪的观测确定它是否可达（合成对端可复用票 18／19 建立的注入能力，**不需要动车**）；
- 若可达且归服务端，修复须有一条「回退即变红」的回归测试，收尾按 AGENTS.md 的产品改动要求；
- 若归车载端，不写入该仓，按跨仓规则给用户一份 owner 通知并请求可写的跟踪目的地；
- 证据归 ControlServer 仓，本票只留路由指针。

### 注意

- 本票是否应挡住票 12（授权发布）由用户决定：它是假设，尚未证实可达。票 22 已收口，**不再**
  阻断票 12。
- 不动车、不建单、不使用现场凭据。
