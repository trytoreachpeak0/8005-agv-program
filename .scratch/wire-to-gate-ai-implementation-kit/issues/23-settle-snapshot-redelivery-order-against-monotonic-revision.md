# 快照重发顺序对上车载端的单调 revision 规则

Type: task
Mode: AFK
Status: resolved
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

## Answer

**不可达，归属不成立，未改产品代码。**

假设漏掉的一环是：**重发本身就是修复**。车载端
`OnboardHmi_MVP@304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6` 的 `WireToGateSessionClient` 里，采用、
落 journal、回 ACK 是三条顺序语句，中间**没有提前返回**：

```
(long revision, string snapshotKind) = ApplyJourneyProjection(envelope, payloadContentSha256, ct);
await _journal.SaveAppliedJourneySnapshotAsync(..., ct);
await SendSnapshotAppliedAckAsync(..., ct);
```

`ApplyJourneyRevision` 对「等于已持有 revision」的重复确实提前 return，但那个 return 在一个 `void`
辅助方法内部——journal 与 ACK 照发。所以**重复快照会被再次 ACK**。而服务端每个 runtime 迭代开头都会
重发全部未确认行（`JourneyRuntimeEngine.AdvanceAsync` → `ReplayPendingForSessionAsync`），于是丢掉
一次 ACK 会在下一个迭代被补上，远早于关卡分配更高的 revision。

（以上为只读读取：`git fetch` 后 `git show origin/OnboardHmi_MVP:<path>`，未 checkout、未写入该仓。）

### 可证伪观测（`ControlServer_MVP@d243abf`，13 条全 PASS）

`AdoptingPeer` 复刻车载端判据（按 MessageType 记账、永不遗忘、更低 revision 拒绝且不 ACK、重复
再 ACK），并把 ACK 按迭代缓冲，以便精确丢掉「连接断开那一刻对端还在飞的那一批」。

1. **单迭代丢包一律干净**：9 个窗口（含关卡那一迭代本身）无一出现低于对端已持有 revision 的快照。
2. **绿不是空的**：每次运行都断言对端确实进入了危险状态——三条流各自采用过两个不同 revision。
3. **检测器会响**：对端 ACK 永不到达时，三条流全部复现假设的形态：对端持有 2，却被投递 1。
4. **边界是连续五个迭代**：丢 3～7 变红；丢 4～7 或 3～6 皆绿。该区间内任意一次成功送达即收口。

### 为什么那个边界在真实链路上不成立

需要被丢掉的那五个迭代，恰好是旅程消费 `SublotSubmitted` 与 `PreDepartureSafetyCheckResult` 的
区间。这两条消息与 ACK **同向、同一条连接**。一个「ACK 连续五个迭代全丢、业务应答却照常到达」的
对端在该传输上不存在。第 3 条之所以能走到关卡，是因为 fixture 直接写 inbox 绕过了传输——这正是
票 22 里看到 `1, 2, 1, 2` 交错重发的成因：那是永不 ACK 的 fixture 对端，不是可达序列。

### 具名残留风险（不修，归属已指定）

服务端此处的正确性**依赖一条协议并未要求的对端行为**：重复快照必须被再次 ACK。`protocol-v0.1.1`
不强制对端应答重复。一个合规但对重复保持沉默的对端会让取货行永久 pending，关卡 revision 一到，
它的重发就成为 `SNAPSHOT_REVISION_REGRESSION`——可达，且是自维持的重连死循环（对端 journal 永不
遗忘，outbox 行永不被 fence）。

服务端侧的闸门形态已经存在于恢复流：`OnboardRecoveryCoordinator.QueueSessionSnapshotAsync` 在排入
新快照前 fence 掉被取代的 pending 行。把它推广到三种旅程快照（排入更高 revision 时，fence 掉同
MessageType 同车辆的更低 revision pending 行）即可收口，**无需迁移**。本票**未实施**：对本次发布
绑定的对端不可达，而这是发布候选。

风险归属：改动对端「重复快照是否再 ACK」行为的人，或把本服务端绑到另一个车载端实现的人。二者任一
发生，上述闸门在该绑定投用前即成为必需。

### 路由指针

Owning repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`
Owner issue/artifact: `evidence/g2/20260830-issue23-snapshot-redelivery/SUMMARY.md`
Published branch/commit: `ControlServer_MVP@d243abf`（**尚未推送**）
Impact on this ticket: 已收口；**不阻断票 12**。

### 收尾门禁

Release 0 warning / 0 error，`dotnet format --verify-no-changes` 干净，tier 1
**243 passed / 0 skipped**（较票 22 的 230 增加的 13 条即本票新增）。未触产品代码、未动车、未建单、
未触 RIoT、未写入只读仓。
