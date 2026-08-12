# 20 — DemandSeries 生产页面

**What to build:** 让运维人员在生产 Watch 中按当前 AREA 范围浏览 Tracking、GONE、Archived 和 LongGoneButVisible 的完整 DemandSeries，并在一个冻结快照里查看 Demand 世代关系、生命周期节点、实时 MES 事实、原始观测和永久事件，从列表结论一直追到轮次证据。

**Blocked by:** 08 — 提供 DemandSeries 冻结快照列表与详情；18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览

**Status:** ready-for-agent

- [ ] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，并以已确认的 DemandSeries 信息层级重写生产页面。
- [ ] 列表覆盖 Tracking、GONE、Archived 和归档后可见状态，显示稳定 SeriesId、SUBLOT、WorkType、开始时间、当前出现状态、最后序列及相关关注状态，不按 ExternallyReadableDemand 资格隐藏坏数据。
- [ ] 筛选、AREA 精确范围、稳定排序、精确总数、上一页、下一页和直接页码跳转都由 Host 在同一冻结快照内解析；Watch 不下载全表或用当前页推算总数。
- [ ] 选中 Series 后可查看全部 Demand 世代、generation、predecessor 关系、VISIBLE/GONE/归档节点、DemandLastSeenAt、GoneConfirmedAt、当前条件和不可变 DemandSeriesEvent 流。
- [ ] 详情能区分 LiveMesFieldSet、DemandRawObservation、重复观测、当前错误、资格阻断、PollTrace 和 ProjectionCommit，且 DATES 明确作为 MesSourceDate 展示，不冒充生命周期时间。
- [ ] 从概览或资格审计进入时携带 SeriesId、聚焦 DemandId 和来源快照摘要；目标页读取自身当前快照并说明事实是否已变化，范围外对象必须经用户确认切换到“全部 AREA”，不能静默绕过范围。
- [ ] 加载和刷新保留上一成功列表及详情；刷新成功按稳定标识重选，刷新失败、游标失效或对象移出范围时不会把旧详情挂到新快照。
- [ ] 生命周期、资格、错误和陈旧状态以文字或图标表达；筛选、分页、表格、详情、复制时间与下钻具备稳定 UI Automation 名称、键盘焦点和无需屏幕坐标的正式旅程。
- [ ] 页面在 1440×900、2560×1440、720 epx 最小宽度和规定 DPI 下保持 master-detail 边界、分页与关键操作可见，必要时重排或滚动而不裁切。
- [ ] 本票与 19、21、22 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [ ] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
