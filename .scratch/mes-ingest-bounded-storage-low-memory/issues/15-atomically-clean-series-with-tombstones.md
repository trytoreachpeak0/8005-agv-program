# 15 — 原子清理 Series 并永久保留墓碑

**What to build:** 让一个到期 RetentionEligibleDemandSeries 能够整体删除详细历史，同时永久保留最小 ArchivedDemandKeyTombstone，保证旧业务键永不重新外读。

**Blocked by:** 13 — 实施 30 天历史保留计时.

**Status:** ready-for-agent

- [ ] ArchivedDemandKeyTombstone 只保存 TransportDemandKey、原 Series 身份、归档结论及安全判断所需的最小版本化事实。
- [ ] 单个 Series 清理在同一事务内先幂等写墓碑，再删除完整世代、事件、错误、条件与关联详细历史图。
- [ ] 在墓碑写入后、各删除阶段和提交前注入失败时整笔事务回滚，不出现遗忘归档身份的安全空窗。
- [ ] 重试只产生一个墓碑并恰好完成一次详细图清理，不因部分批次重复或丢失事实。
- [ ] 墓碑对应业务键后来重现仍归入原 Series 的 LONG_GONE_BUT_VISIBLE，Watch 可见但永不进入 ExternallyReadableDemandCatalog。
- [ ] 故障注入只使用一个包含最小完整关系图的 Series；每个事务断点用同一夹具重置，不生成规模历史或重复运行等价失败矩阵。
- [ ] 复用既有投影 failpoint、事务和目录测试基础设施，不为本票建设通用故障注入框架。
- [ ] 开发期运行聚焦墓碑/回滚/重现测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。
