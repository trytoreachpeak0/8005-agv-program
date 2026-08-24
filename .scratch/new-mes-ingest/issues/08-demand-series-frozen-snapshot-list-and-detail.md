# 08 — 提供 DemandSeries 冻结快照列表与详情

**What to build:** 作为运维工程师，我希望通过正式 API 在一个冻结投影时点浏览 DemandSeries 列表并下钻详情，查看其全部 Demand 世代、当前字段、原始冲突、生命周期节点、错误条件和事件证据，以便分页或后台新轮次到来时，我看到的总数、列表与详情仍能共同解释同一个事实快照。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible

**Status:** ready-for-human

- [x] 正式版本化 API 返回绑定 ProjectionCommit 的 DemandSeries 冻结快照；列表中的精确总数、生命周期分面、当前出现状态、最后序列和详情都来自同一快照身份。
- [x] 列表能明确浏览 Tracking、GONE、Archived 和归档后可见状态，并为每项显示稳定 SeriesId、SUBLOT、WorkType、开始时间、当前生命周期、当前 Demand/世代和最后 SeriesSequence。
- [x] 详情完整展示一个 Series 的全部 Demand 世代及 predecessor 关系、当前与历史 MES 字段、规范化原始观测、重复或跨 WorkType 冲突、当前条件、错误期间、生命周期节点和不可读结论。
- [x] 每个详情事实都能追溯到对应 DemandId、PollTrace、Host UTC 时间和 ProjectionCommit；事件按严格 SeriesSequence 返回，归档、恢复和错误历史不会因只展示当前 Demand 而丢失。
- [x] Host 在冻结快照内执行筛选、精确计数、稳定排序和有界分页；翻页或直接定位时不由客户端下载全表或用当前页估算总数，游标/定位凭据不能跨快照、筛选或契约版本复用。
- [x] 获取列表后再提交会改变生命周期或字段的新成功轮次，旧快照的列表与详情仍保持内部一致；客户端请求最新快照时才看到新提交，失效或不匹配的快照引用返回明确错误而非静默切到第一页。
- [x] 真实 SQL Server → 正式 API 验收构造实时字段异常、重复键、多 WorkType、GONE、归档前重现、归档和 LongGoneButVisible，验证重启前后列表、详情、精确计数、排序、分页及证据链一致。

## Implementation evidence

- 契约/存储升级为 `tracer.8` / schema 8：`ProjectionCommits` 使用持久单调 `ProjectionSequence`，`SchemaInfo` 保存快照凭据签名密钥；快照可跨 Host 重启解析并按 immutable event/raw/evidence 截止序列重建。
- `GET /api/v2/demand-series` 在同一冻结提交内完成筛选、精确 total/facets、`StartedAt DESC, SeriesId ASC` 排序和最大 200 条分页；cursor 使用排序锚点 keyset seek，直接页码使用有界 `OFFSET/FETCH`。
- 列表、详情与 by-key 读取都回传同一 snapshot/commit 元数据；HMAC 凭据绑定用途、契约版本、snapshot、规范化筛选、排序、page size 与位置，篡改/错配返回结构化错误。
- 详情按 snapshot 返回全部 Demand 世代、predecessor、可信/冲突 raw observations、conditions/error periods/evidence、lifecycle/events 与完整 PollTrace/Host UTC/ProjectionCommit provenance，且不会泄露快照之后的 period close 或状态变化。
- 真实 SQL Server 2022 / compatibility 160 门禁 `Invoke-Ticket08SqlServerGate.ps1`：10 passed、0 failed、0 skipped；覆盖同 CompletedAt 的 A/B 冻结、重启、分页/筛选/凭据、字段错误恢复、四种 lifecycle/presence 组合、duplicate、多 WorkType、归档前重现、archive 与 LongGoneButVisible。
- 前序 ticket01-07 SQL 回归 28/28 通过；Release 非增量 build 0 warning/error。两轴 code review 复核无剩余 actionable finding。
- 流程说明：ticket06 的技术验收及真实 SQL 证据已具备，但其 tracker 仍为 `ready-for-human`；本票未将其表述为已完成人工接受。
