# 07 — 切换目录、关注与概览当前读取

**What to build:** 一次完成 ExternallyReadableDemandCatalog、CurrentIngestAttention 和 WatchOverview 的当前读取切换，使三个高频读取面共享当前投影与提交身份，不再通过详细历史 Browse 计算。

**Blocked by:** 06 — 切换 DemandSeries 当前与冻结读取.

**Status:** ready-for-agent

- [ ] 实现前审计 Ticket 06 的最终 diff、测试和执行计划对 Tickets 07–12 的覆盖；已满足的验收项只补证据，不重复改代码。
- [ ] 目录成员、成员业务值、精确 count 和 CatalogRevision 只从当前投影与中央资格策略计算；条件读取继续原子返回未变化或完整修订。
- [ ] 目录读取绑定 HistoryEpoch，旧纪元条件身份不能在新纪元复用；GONE、已归档、LONG_GONE_BUT_VISIBLE、重复键和数据异常 Demand 继续被排除。
- [ ] CurrentIngestAttention 只读取活动 Series 条件、PollRunFailure、TaskTypeProtection、清理失败和其它当前关注投影；已结束错误只留在历史检索。
- [ ] WatchOverview 的 Series、资格、错误、关注和近期动态来自专用当前聚合或同一 ProjectionCommit 缓存。
- [ ] Overview、Current Attention 与 Catalog 响应内部绑定明确 HistoryEpoch 和 ProjectionCommit，并发提交不得混合旧计数、新详情或不同提交的动态。
- [ ] 三条当前路径复用 Ticket 06 的两个固定小样本和执行计划采集，不新建数据生成器；计划必须不访问或排名 DemandRawObservation 历史。
- [ ] 正常实现只扩展既有 current read context、投影和测试夹具，不引入新的通用查询框架、缓存层或第二套 snapshot codec。
- [ ] 开发期运行聚焦 Catalog/Attention/Overview/reference consumer 测试，关闭时只运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成，最终 Failed: 0、Skipped: 0。
- [ ] 只有实际计划访问历史、逻辑读随小样本增长、出现异常 grant/spill 或并发身份证据失败时，才升级更大样本或额外性能运行。
