# 11 — ErrorSearchAsOf 列表、窗口与分面

**What to build:** 让运维工程师从永久 `DemandSeriesEvent` 历史中按错误含义和对象检索曾发生过问题的 DemandSeries，并在首个请求冻结 `ErrorSearchAsOf`。结果列表、活动状态、精确总数、分面和后续分页必须构成同一 `ErrorSearchSnapshot`，支持可预测的 UTC 时间窗口与稳定筛选语义，使错误在查询期间继续发生或恢复时也不会改变已经打开的历史视图。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible

**Status:** ready-for-agent

- [ ] 首次查询由 Host 冻结 `ErrorSearchAsOf`；默认窗口是截至该时点最近精确 7×24 小时，并可选择最近 24 小时、30×24 小时和全部历史，不按本地午夜或自然日取整。
- [ ] 错误期间与查询窗口统一采用 UTC 半开区间 `[from, to)`；边界相接不算命中，未显式给出 `to` 时以 `ErrorSearchAsOf` 为排他上界，显式非法区间得到明确失败而非静默改写。
- [ ] 查询支持主分类、SeriesErrorCode、`ACTIVE`/`ENDED`、时间、SeriesId、DemandId 与 SUBLOT；不同维度取交集、同维度多值取并集，默认同时包含活动和已结束，矛盾的分类与错误码组合明确失败。
- [ ] SeriesId、DemandId 与错误码采用去首尾空白后的不区分大小写精确匹配，SUBLOT 采用不区分大小写包含匹配；DemandId 命中时返回所属 Series，但只汇总满足全部条件的期间与证据。
- [ ] 列表按 DemandSeries 去重，并依次按匹配范围内 ACTIVE 优先、最近匹配证据时间降序、SeriesId 升序稳定排列；默认每页 100、最多 200，返回精确 totalSeriesCount，第一版不提供任意列排序或导出。
- [ ] 分类与状态分面按排除自身维度后的去重 DemandSeries 精确计算；一个 Series 可命中多个主分类，因此系统不会把分类数量机械相加解释为总数。
- [ ] 游标绑定完整规范化筛选、固定顺序、`ErrorSearchAsOf` 与契约版本；篡改、跨筛选复用或不匹配时返回稳定的明确错误，不自动冒充第一页。
- [ ] 在可控时间下，查询后追加、改变或关闭错误期间不会改变既有快照的列表、状态、分面和页序；刷新后才可观察到新的 `ErrorSearchAsOf` 与对应结果。
- [ ] 只有查询成功且零命中时才返回“该条件下没有错误历史”的空结果；加载失败、取消或零个活动错误都不会被报告为系统健康，AreaFilterProfile 也不会静默过滤错误检索。
