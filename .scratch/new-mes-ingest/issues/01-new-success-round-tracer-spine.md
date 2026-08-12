# 01 — 建立新版成功轮次端到端骨架

**What to build:** 作为现场运维工程师和正式 API 消费者，我希望一个脚本化的完整成功轮次能够从生产 Host 进入全新的持久化模型，并通过正式版本化 HTTP API 读回稳定的 DemandSeries、第一代 TransportDemand、当前 MES 事实和轮次证据，以便新版系统拥有一条可独立演示、可在重启后复核的最小端到端主干。

**Blocked by:** None — can start immediately

**Status:** done

- [x] 在空的新数据库中提交包含一条唯一且字段有效的完整 SUCCESS 后，正式 API 能读到一个由 SUBLOT + WorkType 唯一确定的 DemandSeries、一个 VISIBLE 的第一代 TransportDemand、稳定的 SeriesId/DemandId，以及该轮完整原始观测和当前 MES 字段。
- [x] 首次成功轮次产生可追溯的 PollTrace、ProjectionCommit 和按 SeriesSequence 排序的首次事实事件；API 返回的 Series、Demand、事件和轮次证据都指向同一次原子投影提交，不会呈现半轮状态。
- [x] 再提交内容等价但 PollTraceId 不同的完整 SUCCESS 时，SeriesId、DemandId、世代和当前字段保持不变，且不会因无意义的重复观测追加业务变化事件。
- [x] Host 重启后，从正式 API 读到的标识、当前状态、原始证据和事件顺序与重启前一致，新历史不会依赖内存状态重建。
- [x] 新主干只发布新版 schema 和版本化契约，不迁移或重新解释旧 TransportDemand、冻结字段、IngestAlert、DemandChangeFeed 或旧 DTO，也不提供新旧契约混跑的兼容路径。
- [x] 自动验收以脚本化 MesTaskUnionRound → 生产 Host/领域入口 → 现场兼容的真实 SQL Server → 正式版本化 HTTP API 为门禁；内存存储或 LocalDB 结果只能提供开发反馈，不能替代该证据。

## Comments

- 2026-08-12：完成独立 `mesingest` schema、Production Host/领域入口、V2 只读 API 与真实 SQL Server tracer。正式门禁在 SQL Server `16.0.1190.2`、product major `16`、compatibility level `160` 上得到 `3 passed / 0 skipped`；错误 major `15` 的反向门禁按预期失败且未创建遗留测试库。
- Production 配置 V2 后不注册或发布旧投影、旧 API、旧 OpenAPI；未配置 V2 时 Production fail closed。旧面只允许 Development 显式开启，且不属于新版契约。
- 验收测试：`First_success_round_is_read_back_with_atomic_series_demand_and_round_evidence`、`Equivalent_success_round_preserves_identity_and_does_not_append_business_events`、`Restarted_host_reads_the_same_persisted_projection`。事务故障注入、并发和后续生命周期语义仍分别由票 02–16 承担。
