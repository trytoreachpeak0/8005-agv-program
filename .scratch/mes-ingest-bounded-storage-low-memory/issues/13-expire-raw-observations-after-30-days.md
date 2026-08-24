# 13 — 实施 30 天历史保留计时

**What to build:** 在一个保留状态模型中同时实现 DemandRawObservation 的 30 天过期和 RetentionEligibleDemandSeries 的第二个 30 天计时，使原始证据、活跃历史图和可清理 Series 各自拥有准确边界。

**Blocked by:** 12 — 快速验证冻结读取并发一致性.

**Status:** ready-for-human

- [x] RawObservationAvailabilityWindow 使用 Host UTC 的 PollTrace CompletedAt，不使用 MES DATES、自然月、本地午夜或 Watch 缓存时间。
- [x] 边界前一 tick 仍完整可读，边界时刻及之后进入过期，不留下残缺原始集合。
- [x] 已知过期的 PollTrace、snapshot 或历史对象返回 410 MES_INGEST_HISTORY_EXPIRED，并返回 earliest available Host UTC。
- [x] 从未存在的身份继续使用既有未找到语义，不用 404 或 200 空集合表示已知过期。
- [x] 当前物化状态与活跃 Series 结构化图不因 RawObservation 到期而被删除或改变。
- [x] 只有已归档、当前 Demand 不为 VISIBLE 或 LONG_GONE_BUT_VISIBLE、且没有活动 CurrentCondition 或 ErrorPeriod 的 Series 才成为 RetentionEligibleDemandSeries。
- [x] 首次满足资格时记录 Host UTC EligibilityAt 并计算精确 30×24 小时；新观测、条件、错误期间或事件原子取消资格。
- [x] 再次满足资格时建立新的 EligibilityAt，不沿用 MES DATES、归档时间、创建时间或自然月。
- [x] 复用现有 TimeProvider、PollTrace、Series 生命周期与 schema 夹具，以最小 Series/Observation 图跨越 30 天边界；不得真实等待、生成多天数据或建立第二套保留调度框架。
- [x] 开发期只运行聚焦保留/410/资格测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。
- [x] 只有最小图无法证明外键清理边界、并发投影出现竞态或实际 SQL 计划退化时，才扩大数据或运行额外并发矩阵。

## Comments

- 2026-08-24：schema 22 新增 `PollTraces.RawObservationsExpiredAt` 与 `DemandSeries.RetentionEligibilityAt`，保留推进在既有提交顺序锁和单个事务内按 PollTrace 整体删除原始多重集、写入过期标记并推进最早 Host UTC 边界；没有引入第二套调度器，小时预算调度仍归 Ticket 16。
- 30×24 小时边界统一由 `TimeProvider` 和 PollTrace `CompletedAt` 决定。聚焦真实 SQL 覆盖边界前一 tick、边界时刻、边界后、零行 PollTrace、410/404 区分、MES DATES 无关性、完整集合删除、当前物化/结构化图保持，以及已归档 Series 的资格建立、取消和重新计时。
- DemandSeries、ReadabilityAudit 与 ErrorSearch 的不透明 snapshot token 使用签名的 `RawAvailabilityCutoff`/`ErrorSearchAsOf` 基线：历史可用集合未变化时 token 稳定；跨越边界的旧 snapshot 统一 410；边界后新 snapshot 以当时可用原始历史为基线。最新当前模型采用无锁乐观前后序列校验，发生并发提交时丢弃并回退历史路径，不阻塞投影。
- 统一 Host 中间件把 `MesIngestHistoryExpiredException` 映射为 410 `MES_INGEST_HISTORY_EXPIRED`，携带 `HistoryEpoch` 与 `earliestAvailableHostUtc`；OpenAPI 明确声明历史过期响应，精确 raw-evidence 继续按其 PollTrace 独立判断，已在签发时不可用的结构化错误证据保留 `rawEvidenceAvailable=false`。
- 聚焦真实 SQL `HistoryRetentionStateTests`：4 passed、0 failed、0 skipped；受影响契约/冻结/审计/错误/证据矩阵：50 passed、0 failed、0 skipped；token 稳定性回归矩阵：8 passed、0 failed、0 skipped；冻结读取并发回归矩阵：5 passed、0 failed、0 skipped。
- 最终 Tier 1 `dotnet test MesIngest.Tests --no-restore --logger "console;verbosity=minimal"`：790 passed、0 failed、0 skipped，耗时 9m48s，真实 SQL Server ProductMajor 16 / compatibility 160，低于 45 分钟预算。
- 未运行 Tier 2、Tier 3 或 Golden WPF；本票未改 `MesIngest.Watch` UI。`$code-review` Spec 与 Standards 双轴复核达到 fixed point，均无剩余 finding；Ticket 15 的墓碑/整图删除与 Ticket 16 的小时预算调度未进入本票。
