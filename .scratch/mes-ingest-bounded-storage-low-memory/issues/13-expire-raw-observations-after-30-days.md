# 13 — 实施 30 天历史保留计时

**What to build:** 在一个保留状态模型中同时实现 DemandRawObservation 的 30 天过期和 RetentionEligibleDemandSeries 的第二个 30 天计时，使原始证据、活跃历史图和可清理 Series 各自拥有准确边界。

**Blocked by:** 12 — 快速验证冻结读取并发一致性.

**Status:** ready-for-agent

- [ ] RawObservationAvailabilityWindow 使用 Host UTC 的 PollTrace CompletedAt，不使用 MES DATES、自然月、本地午夜或 Watch 缓存时间。
- [ ] 边界前一 tick 仍完整可读，边界时刻及之后进入过期，不留下残缺原始集合。
- [ ] 已知过期的 PollTrace、snapshot 或历史对象返回 410 MES_INGEST_HISTORY_EXPIRED，并返回 earliest available Host UTC。
- [ ] 从未存在的身份继续使用既有未找到语义，不用 404 或 200 空集合表示已知过期。
- [ ] 当前物化状态与活跃 Series 结构化图不因 RawObservation 到期而被删除或改变。
- [ ] 只有已归档、当前 Demand 不为 VISIBLE 或 LONG_GONE_BUT_VISIBLE、且没有活动 CurrentCondition 或 ErrorPeriod 的 Series 才成为 RetentionEligibleDemandSeries。
- [ ] 首次满足资格时记录 Host UTC EligibilityAt 并计算精确 30×24 小时；新观测、条件、错误期间或事件原子取消资格。
- [ ] 再次满足资格时建立新的 EligibilityAt，不沿用 MES DATES、归档时间、创建时间或自然月。
- [ ] 复用现有 TimeProvider、PollTrace、Series 生命周期与 schema 夹具，以最小 Series/Observation 图跨越 30 天边界；不得真实等待、生成多天数据或建立第二套保留调度框架。
- [ ] 开发期只运行聚焦保留/410/资格测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。
- [ ] 只有最小图无法证明外键清理边界、并发投影出现竞态或实际 SQL 计划退化时，才扩大数据或运行额外并发矩阵。
