# 21 — 资格审计与 AREA Variant A 生产页面

**What to build:** 让运维人员在生产 Watch 中用本机命名 AREA 配置缩小需求与资格视图，并在一个冻结 ReadabilityAuditSnapshot 中核对每个 Demand 世代的 READABLE 或 NOT_READABLE 结论、全部阻断原因、精确分面和证据；编辑本地 AREA 范围不会改变 Host 的外部资格或目录事实。

**Blocked by:** 10 — ReadabilityAuditSnapshot 查询与详情；18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览

**Status:** ready-for-human

- [x] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，资格审计和 AREA 编辑分别采用已确认的生产信息层级与 Variant A 主从布局。
- [x] 资格列表覆盖全部 Demand 世代并明确区分 ExternalReadabilityState 与 VISIBLE/GONE 生命周期；NOT_READABLE 摘要显示 Host 选择的 LeadReadabilityBlocker，详情保留全部 ReadabilityBlocker 和每项资格检查。
- [x] 资格、WorkType、阻断原因、DemandId 和 SUBLOT 条件，以及资格与原因分面、精确去重总数、稳定默认顺序、默认或最大页大小、直接页码跳转，都绑定同一审计快照并由 Host 计算。
- [x] 一个 Demand 可计入多个原因分面，但 NOT_READABLE 总数按 Demand 去重；空结果只表示成功查询在当前条件下零命中，不把失败、加载中或零个不可读 Demand 宣称为系统健康。
- [x] 详情展示可信字段或原始观测冲突、所属 Series、PollTrace、ProjectionCommit 和当时 CatalogRevision；列表、分面和详情不会在刷新期间混入不同提交。
- [x] AREA 页左侧持续显示命名配置列表，右侧显示选中 TXT 配置的内容、MesArea 格式校验、重复项或空项校验、保存和应用状态；非法草稿不能应用，保存与当前应用状态的含义清楚。
- [x] 应用或切换 AreaFilterProfile 后只重新查询需求系列、资格审计和概览相关摘要；不改变 WatchDemandProjection、ExternallyReadableDemandCatalog、CatalogRevision、Dispatch 范围、错误检索或接入告警。
- [x] Host 在分页和计数前只按当前可信单值 MesArea 精确筛选；AREA 缺失、非法或观测冲突的 Demand 只在“全部 AREA”资格范围出现，不借历史 AREA 填补。
- [x] 从资格项跳转需求系列时携带 SeriesId、DemandId 和来源审计快照摘要；范围外导航必须显式确认切换范围，刷新失败或对象不再命中时保留旧快照语义并清除不再有效的详情。
- [ ] 两页的筛选、配置编辑、校验、分页、分面、详情、保存、应用和跳转具备稳定 UI Automation 名称、键盘焦点、非颜色状态语义，并在规定窗口尺寸与 DPI 下不裁切关键操作。
- [ ] 本票与 19、20、22 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [x] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

### 2026-08-14 — 非像素实现冻结，等待共享视觉列车

- 生产资格审计页已接入 Host 冻结快照、精确分面/总数、同维 OR 与跨维 AND 条件、100/200 页大小、冻结直接页码、刷新保留/重选、全部检查/阻断/原始观测/Series/PollTrace/ProjectionCommit/CatalogRevision 详情，以及携带来源摘要的 DemandSeries 下钻。
- AREA Variant A 已实现本机 UTF-8 TXT 配置列表与编辑器、逐行格式/重复/空集合/100 项边界校验、原子保存、选择/保存/应用分离和独立 applied marker；损坏 marker 会明确警告后回退，应用只重查 Overview、DemandSeries、ReadabilityAudit，不触碰错误检索、接入告警或 Host 业务投影。
- 页面使用 WPF UI Card、命名尺寸资源、稳定 AutomationId/Name、显式键盘焦点与非颜色状态；720 epx 会把详情堆叠到 master 下方。正式真实窗口旅程、高对比度、1440×900/2560×1440 与 125%/150% DPI 仍按共享列车保留为未勾选。
- 聚焦复核：profile/presenter/auto-refresh 52/52；session 与 Audit/AREA/DemandSeries 生产 WPF 31/31；另有 ProductionHost 4/4、CompositionRoot 16/16、ProductionShell/导航 7/7。四个高风险伪变异（多值 OR、AREA 100 项边界、CatalogRevision 身份、启动恢复 applied profile）均先存活、再由新增断言杀死，工作树不留变异。
- 非增量 Release 构建为 0 warning / 0 error。全量只运行一次：UiTests 124 passed / 27 named environment/golden skips；MesIngest.Tests 748 passed / 2 failed / 99 named SQL skips。两个失败均不在本票 diff：既有 INSTALL.md V1 OpenAPI 字样断言与文件保留时间戳测试；本票聚焦回归全部通过。
- 初始 Spec/Standards 审查分别发现并修复刷新换页选择、显式 All AREA 状态、损坏 marker、Card/token、清除条件、中文诊断和失败呈现等问题；最终两轴只读复审均为 no findings。未生成/提升 golden candidate，未改视觉基线，未创建 VM 任务或 DPI clone；等待 19–22 四票冻结后的一次共享黄金机预览。
