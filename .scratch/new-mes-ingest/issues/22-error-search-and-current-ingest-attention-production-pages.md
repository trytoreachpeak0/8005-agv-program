# 22 — Error Search Variant A 与接入告警生产页面

**What to build:** 让运维人员在生产 Watch 中通过 Error Search Variant A 从错误分类定位曾经受影响的 DemandSeries 和真正命中的证据，同时在接入告警页只处理当前仍需关注的 Series 与全局接入问题；已恢复历史、当前风险和 AREA 显示范围不会再被混为一谈。

**Blocked by:** 11 — ErrorSearchAsOf 列表、窗口与分面；12 — 错误详情与受限原始证据；13 — CurrentIngestAttention 当前关注读取；18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览

**Status:** ready-for-agent

- [ ] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，错误检索采用已确认的 Variant A“分类导航 + Series 结果 + 证据详情”三列布局，三列共享上下边界并填满可用内容高度。
- [ ] 错误检索支持分类、错误码、ACTIVE/ENDED、24 小时、7 天、30 天或全部历史、SeriesId、DemandId 和 SUBLOT 条件，并明确显示冻结 ErrorSearchAsOf、UTC 半开窗口和当前规范化条件。
- [ ] 结果按 DemandSeries 去重，显示稳定排序、精确总数、分面和服务端分页；详情只展示当前条件真正命中的期间与证据，并标明跨出窗口的期间边界和跨 Demand 世代关系。
- [ ] 成功零命中只说明当前条件下没有历史；加载、取消、游标错误和刷新失败不会显示为空结果，刷新失败保留上一成功快照及其 AsOf 和条件。
- [ ] 默认诊断证据可解释字段、观测值、规则、DemandId 或 WorkType、证据时间和 PollTrace；完整原始观测只能按需、有大小上限且受敏感字段白名单约束。
- [ ] 接入告警只显示 CurrentIngestAttention，覆盖活动 Series 错误、PollRunFailure、TaskTypeProtection 和 UnassignedMesObservation；已结束 Series 错误从当前页消失但仍能在错误检索中找到。
- [ ] Series 当前关注项引用稳定错误身份并能带显式条件下钻错误检索，不创建或展示另一套 fingerprint incident、人工确认或人工恢复语义。
- [ ] Error Search 和接入告警不受 AreaFilterProfile 静默过滤；页面明确区分历史错误、当前关注、Host 连接失败和 Watch 刷新失败。
- [ ] 分类、筛选、时间范围、分页、Series 选择、证据详情、关注项和下钻均具备稳定 UI Automation 名称、键盘焦点和非颜色状态表达，并在规定窗口尺寸和 DPI 下保持三列关系或可理解的响应式重排。
- [ ] 本票与 19–21 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [ ] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
