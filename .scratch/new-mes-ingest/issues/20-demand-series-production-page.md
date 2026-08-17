# 20 — DemandSeries 生产页面

**What to build:** 让运维人员在生产 Watch 中按当前 AREA 范围浏览 Tracking、GONE、Archived 和 LongGoneButVisible 的完整 DemandSeries，并在一个冻结快照里查看 Demand 世代关系、生命周期节点、实时 MES 事实、原始观测和永久事件，从列表结论一直追到轮次证据。

**Blocked by:** 08 — 提供 DemandSeries 冻结快照列表与详情；18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览

**Status:** done

- [x] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，并以已确认的 DemandSeries 信息层级重写生产页面。
- [x] 列表覆盖 Tracking、GONE、Archived 和归档后可见状态，显示稳定 SeriesId、SUBLOT、WorkType、开始时间、当前出现状态、最后序列及相关关注状态，不按 ExternallyReadableDemand 资格隐藏坏数据。
- [x] 筛选、AREA 精确范围、稳定排序、精确总数、上一页、下一页和直接页码跳转都由 Host 在同一冻结快照内解析；Watch 不下载全表或用当前页推算总数。
- [x] 选中 Series 后可查看全部 Demand 世代、generation、predecessor 关系、VISIBLE/GONE/归档节点、DemandLastSeenAt、GoneConfirmedAt、当前条件和不可变 DemandSeriesEvent 流。
- [x] 详情能区分 LiveMesFieldSet、DemandRawObservation、重复观测、当前错误、资格阻断、PollTrace 和 ProjectionCommit，且 DATES 明确作为 MesSourceDate 展示，不冒充生命周期时间。
- [x] 从概览或资格审计进入时携带 SeriesId、聚焦 DemandId 和来源快照摘要；目标页读取自身当前快照并说明事实是否已变化，范围外对象必须经用户确认切换到“全部 AREA”，不能静默绕过范围。
- [x] 加载和刷新保留上一成功列表及详情；刷新成功按稳定标识重选，刷新失败、游标失效或对象移出范围时不会把旧详情挂到新快照。
- [x] 生命周期、资格、错误和陈旧状态以文字或图标表达；筛选、分页、表格、详情、复制时间与下钻具备稳定 UI Automation 名称、键盘焦点和无需屏幕坐标的正式旅程。
- [x] 页面在 1440×900、2560×1440、720 epx 最小宽度和规定 DPI 下保持 master-detail 边界、分页与关键操作可见，必要时重排或滚动而不裁切。
- [x] 本票与 19、21、22 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

### 2026-08-14 — 非像素实现冻结，等待共享视觉列车

- 生产 DemandSeries 页面已接入 V2 Host 冻结快照：当前 AREA 列表、Host 精确总数与分页、最新当前页刷新、全证据详情、概览/资格审计来源比较，以及范围外对象的显式“全部 AREA”确认均已完成。
- 页面使用稳定 AutomationId、可聚焦筛选/分页/表格/详情和绝对时间/证据复制；空结果、旧快照保留、并发导航、关闭窗口与自动刷新仲裁均有非像素回归。正式真实窗口旅程、高对比度与规定 DPI 验证仍按共享列车保留为未勾选。
- 聚焦验证：Ticket 20 核心 43/43；生产 Host/session/window 29/29；旧页面剪贴板/选择回归 2/2。`watch-vm-tests` 为 118 passed / 1 named skip（当前会话 `en-US`，旅程契约要求 `zh-CN`），证据目录为 `C:\Users\szy\AppData\Local\Temp\ticket20-watch-vm-20260814-165832`。
- 非增量 Release 构建为 0 warning / 0 error。全量只运行一次：UiTests 118 passed / 27 named skips；MesIngest.Tests 711 passed / 5 failed / 99 named SQL skips。其后已修复并定向验证其中 2 个本票引入的共享剪贴板回归；剩余 3 个既有失败（INSTALL.md V1 字样断言、文件时间保留、旧 MainWindow caption 双击计时）定向复跑仍失败，均不在本票 diff。
- Standards、Spec 与 correctness 独立审查最终均为 no findings。未生成/提升 golden candidate，未改视觉基线，未做 DPI clone，也未勾选黄金机套件、用户批准、共享证据与清理项；等待 19–22 四票冻结后的一次共享黄金机预览。

### 2026-08-17 — 共享 Preview v8 批准并完成

- 冻结源码为 `7ec9bf073609eed7396aa36aae0f19e7b7a526f5`；共享
  `watch-production-preview` 在校准黄金机通过，VM tests 206 total / 205 passed /
  0 failed / 1 named desktop-entry skip，生产真实窗口 journey 1/1 passed。
- 用户于 2026-08-17 明确批准 Preview v8 全部页面。唯一 skip、用户批准、源码身份、
  环境与 cleanup 说明统一记录在票 19；本票引用同一不可覆盖证据目录：
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-19-22-prototype-alignment-preview-v8/run-20260815-205801-watch-production-preview`。
- 本票未生成或提升 baseline，也未运行 DPI clone；这些正式门禁仍由票 23 独占。
