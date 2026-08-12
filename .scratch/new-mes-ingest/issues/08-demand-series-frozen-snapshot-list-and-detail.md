# 08 — 提供 DemandSeries 冻结快照列表与详情

**What to build:** 作为运维工程师，我希望通过正式 API 在一个冻结投影时点浏览 DemandSeries 列表并下钻详情，查看其全部 Demand 世代、当前字段、原始冲突、生命周期节点、错误条件和事件证据，以便分页或后台新轮次到来时，我看到的总数、列表与详情仍能共同解释同一个事实快照。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible

**Status:** ready-for-agent

- [ ] 正式版本化 API 返回绑定 ProjectionCommit 的 DemandSeries 冻结快照；列表中的精确总数、生命周期分面、当前出现状态、最后序列和详情都来自同一快照身份。
- [ ] 列表能明确浏览 Tracking、GONE、Archived 和归档后可见状态，并为每项显示稳定 SeriesId、SUBLOT、WorkType、开始时间、当前生命周期、当前 Demand/世代和最后 SeriesSequence。
- [ ] 详情完整展示一个 Series 的全部 Demand 世代及 predecessor 关系、当前与历史 MES 字段、规范化原始观测、重复或跨 WorkType 冲突、当前条件、错误期间、生命周期节点和不可读结论。
- [ ] 每个详情事实都能追溯到对应 DemandId、PollTrace、Host UTC 时间和 ProjectionCommit；事件按严格 SeriesSequence 返回，归档、恢复和错误历史不会因只展示当前 Demand 而丢失。
- [ ] Host 在冻结快照内执行筛选、精确计数、稳定排序和有界分页；翻页或直接定位时不由客户端下载全表或用当前页估算总数，游标/定位凭据不能跨快照、筛选或契约版本复用。
- [ ] 获取列表后再提交会改变生命周期或字段的新成功轮次，旧快照的列表与详情仍保持内部一致；客户端请求最新快照时才看到新提交，失效或不匹配的快照引用返回明确错误而非静默切到第一页。
- [ ] 真实 SQL Server → 正式 API 验收构造实时字段异常、重复键、多 WorkType、GONE、归档前重现、归档和 LongGoneButVisible，验证重启前后列表、详情、精确计数、排序、分页及证据链一致。
