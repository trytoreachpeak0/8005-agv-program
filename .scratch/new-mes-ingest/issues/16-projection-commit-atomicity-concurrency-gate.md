# 16 — ProjectionCommit 原子性与并发可靠性门禁

**What to build:** 建立真实 SQL Server 上的发布门禁，证明每个成功 `MesTaskUnionRound` 以一个 `ProjectionCommit` 原子提交 PollTrace、Series、Demand、事件、当前条件、错误期间、资格、当前关注和目录修订，并在失败、重试、并发轮询与并发读取下保持唯一、单调且不撕裂。该门禁从正式 Host/API 观察提交结果，使内存或 LocalDB 测试不能替代生产存储可靠性证据。

**Blocked by:** 02 — 固化轮次证据、幂等冲突与非成功隔离；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible；07 — 实现按 WorkType 隔离的 TaskTypeProtection；09 — ExternallyReadableDemandCatalog 与 reference consumer；13 — CurrentIngestAttention 当前关注读取

**Status:** ready-for-human

- [x] 在成功提交的多个阶段注入 SQL 失败后，从正式 API 与重启后的持久化状态均观察不到半提交的 PollTrace 幂等记录、Series、Demand、事件、当前条件、错误期间、资格、CurrentIngestAttention、目录正文或 `CatalogRevision`。
- [x] 对失败后的同一完整轮次重试只产生一个 ProjectionCommit；相同 PollTraceId/相同规范化内容幂等无副作用，相同 id/不同内容明确冲突且不改变任何已提交业务事实。
- [x] 并发触发轮询时只有一个成功投影写入序列，不能为同一 TransportDemandKey 创建相互竞争的当前世代，也不能绕过 RestartBarrier 或目标 WorkType 的 TaskTypeProtection 缺席权威。
- [x] 并发与重启场景中 `SeriesSequence`、ProjectionCommit 身份和 `CatalogRevision` 保持单调且不重复、不倒退；同一轮多个目录变化只产生一个修订，无目录变化不产生新修订。
- [x] 在提交边界并发读取 DemandSeries、目录和 CurrentIngestAttention 时，每个响应完整属于一个已提交快照，不会组合新旧 Series、资格、关注项或目录字段。
- [x] FAILURE、INCOMPLETE、取消和存储异常均不会推进业务投影、结束错误期间或发布新目录修订，但其允许保留的技术失败证据与业务投影有明确隔离。
- [x] 真实 SQL Server seam 覆盖唯一行、重复键、多 WorkType、GONE、归档、LongGoneButVisible、TaskTypeProtection、活动错误与当前关注的联合轮次，并在 Host 重启后得到与重启前相同的历史和当前读取结果。
- [x] 门禁报告记录实际数据库产品与版本、故障注入点、并发规模、重试结果及可观察断言；仅在内存 store 或 LocalDB 通过时必须明确判为发布证据不足。

## Comments

- 2026-08-14：实现完成。成功轮次继续由一个 `SERIALIZABLE` SQL 事务提交，新增六个事务内故障注入点；正式读取在选择 DemandSeries、目录与 CurrentIngestAttention fence 后暴露测试观察边界，生产注册均为 no-op。
- 目录边界红测在真实 SQL Server 上复现了读写反向加锁死锁；修复为目录读在表锁前取得 commit-order application lock 的共享侧，响应因此完整位于写提交之前或之后。
- 严格发布门禁通过：SQL Server `16.0.1190.2`、engine edition 3、compatibility level 160；Ticket 16 测试 5/5、0 skipped，覆盖六个故障点、8 路并发写、2 路并发读以及 retry/replay/conflict。JSON、Markdown 与 TRX 报告由 `Invoke-Ticket16SqlServerGate.ps1` 生成到忽略的 `.artifacts/ticket16-tests/`。
- 依赖真实 SQL 回归 57/57；Release solution build 0 warning / 0 error。完整套件另暴露两个与本票 diff 无关的问题：日期敏感的 latency retention 测试失败，以及 mouse-drag UI automation 首次失败（单独重试通过）；未把它们宣称为 Ticket 16 通过证据。
- 独立 Standards/Spec review 的六项发现均已修复：测试 AREA 使用显式合法值；门禁只接受规范 marker；并发直接验证 RestartBarrier/TaskTypeProtection；重启核对 SeriesSequence 与 commit 身份；故障/重启冻结比较活动错误期间；票据与验证记录已完成交接。
