# 21 — 资格审计与 AREA Variant A 生产页面

**What to build:** 让运维人员在生产 Watch 中用本机命名 AREA 配置缩小需求与资格视图，并在一个冻结 ReadabilityAuditSnapshot 中核对每个 Demand 世代的 READABLE 或 NOT_READABLE 结论、全部阻断原因、精确分面和证据；编辑本地 AREA 范围不会改变 Host 的外部资格或目录事实。

**Blocked by:** 10 — ReadabilityAuditSnapshot 查询与详情；18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览

**Status:** ready-for-agent

- [ ] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，资格审计和 AREA 编辑分别采用已确认的生产信息层级与 Variant A 主从布局。
- [ ] 资格列表覆盖全部 Demand 世代并明确区分 ExternalReadabilityState 与 VISIBLE/GONE 生命周期；NOT_READABLE 摘要显示 Host 选择的 LeadReadabilityBlocker，详情保留全部 ReadabilityBlocker 和每项资格检查。
- [ ] 资格、WorkType、阻断原因、DemandId 和 SUBLOT 条件，以及资格与原因分面、精确去重总数、稳定默认顺序、默认或最大页大小、直接页码跳转，都绑定同一审计快照并由 Host 计算。
- [ ] 一个 Demand 可计入多个原因分面，但 NOT_READABLE 总数按 Demand 去重；空结果只表示成功查询在当前条件下零命中，不把失败、加载中或零个不可读 Demand 宣称为系统健康。
- [ ] 详情展示可信字段或原始观测冲突、所属 Series、PollTrace、ProjectionCommit 和当时 CatalogRevision；列表、分面和详情不会在刷新期间混入不同提交。
- [ ] AREA 页左侧持续显示命名配置列表，右侧显示选中 TXT 配置的内容、MesArea 格式校验、重复项或空项校验、保存和应用状态；非法草稿不能应用，保存与当前应用状态的含义清楚。
- [ ] 应用或切换 AreaFilterProfile 后只重新查询需求系列、资格审计和概览相关摘要；不改变 WatchDemandProjection、ExternallyReadableDemandCatalog、CatalogRevision、Dispatch 范围、错误检索或接入告警。
- [ ] Host 在分页和计数前只按当前可信单值 MesArea 精确筛选；AREA 缺失、非法或观测冲突的 Demand 只在“全部 AREA”资格范围出现，不借历史 AREA 填补。
- [ ] 从资格项跳转需求系列时携带 SeriesId、DemandId 和来源审计快照摘要；范围外导航必须显式确认切换范围，刷新失败或对象不再命中时保留旧快照语义并清除不再有效的详情。
- [ ] 两页的筛选、配置编辑、校验、分页、分面、详情、保存、应用和跳转具备稳定 UI Automation 名称、键盘焦点、非颜色状态语义，并在规定窗口尺寸与 DPI 下不裁切关键操作。
- [ ] 本票与 19、20、22 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [ ] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
