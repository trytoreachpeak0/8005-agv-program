# 15 — 原子清理 Series 并永久保留墓碑

**What to build:** 让一个到期 RetentionEligibleDemandSeries 能够整体删除详细历史，同时永久保留最小 ArchivedDemandKeyTombstone，保证旧业务键永不重新外读。

**Blocked by:** 13 — 实施 15 天历史保留计时.

**Status:** ready-for-human

- [x] ArchivedDemandKeyTombstone 只保存 TransportDemandKey、原 Series 身份、归档结论及安全判断所需的最小版本化事实。
- [x] 单个 Series 清理在同一事务内先幂等写墓碑，再删除完整世代、事件、错误、条件与关联详细历史图。
- [x] 在墓碑写入后、各删除阶段和提交前注入失败时整笔事务回滚，不出现遗忘归档身份的安全空窗。
- [x] 重试只产生一个墓碑并恰好完成一次详细图清理，不因部分批次重复或丢失事实。
- [x] 墓碑对应业务键后来重现仍归入原 Series 的 LONG_GONE_BUT_VISIBLE，Watch 可见但永不进入 ExternallyReadableDemandCatalog。
- [x] 故障注入只使用一个包含最小完整关系图的 Series；每个事务断点用同一夹具重置，不生成规模历史或重复运行等价失败矩阵。
- [x] 复用既有投影 failpoint、事务和目录测试基础设施，不为本票建设通用故障注入框架。
- [x] 开发期运行聚焦墓碑/回滚/重现测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。

## Comments

- Schema v24 新增永久 `ArchivedDemandKeyTombstones`，并以既有 commit-order applock、Serializable 事务和投影 checkpoint observer 实现一次一个 Series 的原子清理。
- 清理顺序固定为幂等墓碑、当前读模型、条件/错误图、事件、Demand 世代和 Series 根；每个事务断点均由同一最小完整图夹具验证回滚，成功重试后墓碑与清理均恰好一次。
- 墓碑键重现沿用原 SeriesId，保持 `ARCHIVED / LONG_GONE_BUT_VISIBLE` 且不进入外读目录；原始起点历史已过期时 `StartedAt` 明确为 `null`，重现以 `ARCHIVED_DEMAND_KEY_REAPPEARED` 记录真实新事实，不伪造归档事件。
- 聚焦 SQL Server 测试：`ArchivedDemandKeyTombstoneTests` 2/2 通过，0 跳过；受影响 API/冻结快照/审计/Watch/OpenAPI 回归 59/59 通过，0 跳过。
- 最终 Tier 1：`dotnet test MesIngest.Tests --no-build`，真实 SQL Server ProductMajor 16 / compatibility 160；794 通过，0 失败，0 跳过，10 分 22 秒。未运行 Tier 2/3（本票不修改 WPF UI，且未请求基线验证）。
- 最终双轴复核：规格/范围与代码/标准均为 no findings；先前关于伪造历史时间/归档事件及版本常量散落的发现均已关闭。
