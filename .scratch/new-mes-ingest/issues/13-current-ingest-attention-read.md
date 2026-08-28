# 13 — CurrentIngestAttention 当前关注读取

**What to build:** 让运维工程师从一个只读入口看到此刻需要处置的 `CurrentIngestAttention`，统一呈现活动 Series 错误、PollRunFailure、TaskTypeProtection 与无法归属 Series 的运维问题。Series 项直接引用领域中的稳定错误身份，非 Series 项保留可追到轮次或 WorkType 的结构化证据；已经结束的事实从当前入口消失但历史仍保留，系统不再复制旧 IngestAlert fingerprint/incident 生命周期。

**Blocked by:** 02 — 固化轮次证据、幂等冲突与非成功隔离；03 — 投影实时字段、字段异常与错误期间；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible；07 — 实现按 WorkType 隔离的 TaskTypeProtection

**Status:** ready-for-human

- [x] 当前读取能同时表达活动 Series 错误、最近仍未恢复的 PollRunFailure、处于保护或恢复进度中的 TaskTypeProtection，以及需关注的 UnassignedMesObservation，并以稳定种类、严重度、发生时间和证据引用区分来源。
- [x] Series 项直接携带 `SeriesId + SeriesErrorCode + Target + SubjectKind` 对应的稳定错误身份与下钻条件，不创建新的 IssueId、fingerprint、Revision、OccurrenceCount 或独立恢复时间线。
- [x] 字段异常、重复键、多 WorkType 和 LongGoneButVisible 的条件持续不变时不会每轮新增关注项；证据变化更新可观察诊断内容，但不改变错误身份。
- [x] 完整成功轮次以明确反证结束 Series 错误后，该项从当前读取消失且永久错误期间与证据不被删除；FAILURE、INCOMPLETE、Host 断联或 Watch 刷新失败不能冒充恢复。
- [x] PollRunFailure 只由后续完整成功轮次明确解除；TaskTypeProtection 的进入、恢复进度与解除均可追溯，并且解除后的当前视图不会残留旧 incident。
- [x] 缺少 SUBLOT 或 TASK_TYPE 的原始行以不可归属的轮次证据出现，不会被随机挂到 DemandSeries，也不会使其它可识别行从当前业务投影消失。
- [x] 当前读取有稳定排序、精确总数和有界响应；相同 PollTrace 幂等重放不改变项数或顺序，内容冲突与非成功轮次不会留下半更新的关注视图。
- [x] 端到端场景证明当前关注项可从正式 Host 读取，结束后的 Series 错误仍保留为历史事实，而读取本身不修改 TransportDemand、错误期间、Poll 状态或任何业务投影。

## Implementation evidence

- Contract/schema: `2026.08.new-mes-ingest.tracer.14` / schema `14`.
- Runtime route: `GET /api/v2/current-ingest-attention`, with exact kind/severity filters, bounded paging and stable structured navigation intents.
- Durable evidence: commit-scoped unassigned facts and transition events; poll ordering is serialized transactionally so `PollTraceHighWater` is a valid recovery fence.
- Real SQL Server 16 / compatibility 160 gate is shared with Ticket 14: exactly 6 passed, 0 skipped; `mes/ingest/csharp/.artifacts/ticket14-tests/ticket14-current-attention-overview-sqlserver.trx`.
