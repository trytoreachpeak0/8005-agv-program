# 28 — DemandSeries 列表高度、列宽与分页条可读性

**What to build:** 让运维人员在生产 Watch 的 DemandSeries 页面一屏看到足够多的 Series 行、读到每列的完整内容、并按自己的需要分配列表与详情的高度；分页条上的每页数量、页码与翻页按钮全部完整显示且文字对齐正确。

**Blocked by:** 无（票 20 已完成，本票在其成果上修正布局缺陷）

**Status:** resolved

## 背景

用户在 2026-08-20 的真实窗口（1920×1080、96 DPI）上提出四条界面问题，截图证据显示
DemandSeries 主列表只能看到 2.5 行数据。逐条定位的根因如下，全部在
`mes/ingest/csharp/MesIngest.Watch/WatchWorkspaceWindow.xaml`：

| 现象 | 根因 | 位置 |
| --- | --- | --- |
| 主列表只显示 2.5 行 | `DemandSeriesMasterDetailGrid` 三行固定为 `0.9*` / `16` / `1.1*`，列表恒定只拿 45% 页高，且中间没有 `GridSplitter`；该 45% 内还要容纳卡片标题两行、38px 表头和 40px 分页条 | 第 642 行起 |
| 列内容被截断且无法调宽 | 所有列写死像素宽（`105`/`165`/`125`…），不是 `*` 或 `SizeToCells`，`SeriesId`、`GONE SINCE`、时间列必然截断 | 第 679 行起 |
| “每页”数字显示不全 | `DemandSeriesPageSizeFilter` 的 `Width="62"` 装不下 `100`／`200`，实际渲染成 `1(` | 第 734 行 |
| 翻页按钮文字不居中 | 分页条父行死高 `Height="40"`，`ui:Button` 未设 `VerticalContentAlignment`，在被拉伸的行内文字偏上；同一死高还会裁掉 `WrapPanel` 换行后的第二行 | 第 669 行 |

### 已否决的方案：详情独立窗口

用户最初提出把 Series 详情移到独立窗口。经评估**不采纳**，改为可折叠 + 可拖动方案：

- 详情窗口必须跟随主窗口 10 秒自动刷新的冻结快照。票 20 的验收要求“刷新成功按稳定
  标识重选，刷新失败、游标失效或对象移出范围时不会把旧详情挂到新快照”，跨窗口重做
  这套语义才是真正的工作量，而收益仅是高度。
- 新增窗口会带来新的 FlaUI 旅程与窗口级视觉基线，直接进入 tier 3 成本。
- `.scratch/mes-ingest-watch-v2/map.md` 的 Decisions-so-far 记有“不得另造新的信息
  架构”，票 20 验收记有“保持 master-detail 边界”。
- 保留结论：若后续确认双屏运维场景（列表与详情各占一块屏且都要全尺寸），独立窗口
  作为本票之后的增量提案重新评估，而不是本票的替代方案。

## 验收项

- [x] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)；沿用票 20 的 master-detail 信息架构，不新增窗口、不改变页面骨架与导航。
- [x] DemandSeries 详情面板可折叠：收起后主列表占据页面全部可用高度，在 1920×1080 / 96 DPI 下一屏至少完整显示 12 行数据；展开后恢复到与收起前一致的比例。
- [x] 主列表与详情面板之间提供 `GridSplitter`，用户可自由分配两者高度；拖动结果在同一会话内切换页面后保持，最小高度不允许把任一侧压到无法使用。
- [x] 顶部“来源快照比较”说明区可收起；收起状态不丢失其中的快照时点、投影提交、序列与事实变化结论，展开时内容与当前实现一致。
- [x] 主列表所有列可由用户拖动调整宽度。若 WPF UI 4.x 的 `DataGridColumnHeader` 主题模板导致 resize thumb 不可用，须在实机确认后修复模板或改用受支持的等价方式，不得以“默认为 true”结案。
- [x] 主列表列宽策略改为按内容与可用宽度分配，`SeriesId`、`WorkType`、`SUBLOT`、`当前 Demand`、时间列和 `GONE SINCE` / `ARCHIVED` 表头在 1920×1080 下不出现截断；窗口变窄时通过横向滚动或重排承载，不裁切文字。
- [x] 分页条上的“每页”下拉能完整显示 `25`／`50`／`100`／`200` 四个值；页码输入框能完整显示实际最大页数的位数。
- [x] 分页条容器不再使用固定行高：`WrapPanel` 换行后第二行完整可见；“上一页”“跳转”“下一页”与页码框的文字在按钮内水平和垂直居中。
- [x] 上述所有尺寸与间距通过命名资源表达，遵循 `docs/agents/watch-ui-system.md` 的 Space / Control height / Type token 约束，不引入未记录的字面量。
- [x] 折叠开关、splitter 和分页控件具备稳定 UI Automation 名称与键盘可达路径；splitter 可用键盘调整，折叠状态对屏幕阅读器有文字表达。
- [x] 票 20 的既有行为不回归：冻结快照分页、精确总数、AREA 范围确认、刷新重选与失败保留上一成功快照全部照旧通过。
- [x] 清理本票暴露出的死资源：`DemandSeriesMasterListHeight`、`DemandSeriesGenerationHeight`、`DemandSeriesEventHeight`、`DemandSeriesEvidenceMinHeight` 当前无任何引用点，随本票一并移除或恢复使用。
- [x] tier 1 全量通过：`dotnet test MesIngest.Tests`，命名每一处 skip。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-20 — 开票

- 四条问题来自用户在真实窗口上的直接观察，附截图；根因已逐条定位到 XAML 行号，
  不需要额外的诊断或原型阶段。
- 详情独立窗口方案已评估并否决，理由记录在上方“已否决的方案”一节。
- 本票只改 `MesIngest.Watch` 的布局与样式，不触及 Host 契约、查询状态机或投影。
- 视觉验收进入 tier 2 / tier 3 前须先向用户说明成本并取得同意。

### 2026-08-20 — 实现与 tier 1 证据

- 已实现详情折叠/恢复、会话内高度比例保留、键盘可达的行 `GridSplitter`、可折叠顶部说明区、按内容测量且可由用户调宽的主列表列，以及无固定行高且内容居中的分页条。
- focused 生产窗口回归：`WatchV2ProductionShellTests.Demand_series_page_keeps_filter_list_exact_paging_and_evidence_journeys_accessible_at_720_epx`，1 passed / 0 skipped / 0 failed。
- tier 1：从 `mes/ingest/csharp` 执行 `dotnet test MesIngest.Tests`，474 passed / 82 skipped / 0 failed / 556 total。
- 逐项 skip 名称与结果保存在 `mes/ingest/csharp/.artifacts/ticket-28/ticket-28-tier1.trx` 的 82 个 `UnitTestResult outcome="NotExecuted"` 节点中；每一项的唯一 skip 原因均为 `Real SQL Server unavailable for Ticket 01 tracer-spine gate`。这些是 AGENTS.md 允许在 tier 1 缺少 LocalDB 时跳过的 SQL Server 集成测试。
- 尚未运行 tier 2 / tier 3；因此 1920×1080 的 12 行可见性、WPF UI 主题下列头 resize thumb、换行分页条和最终视觉外观仍保留给交互式黄金机验证，未据本地静态检查提前结案。

### 2026-08-20 — 双轴代码审查修正

- Standards 初审指出 3 类问题：顶部说明使用了原生 `Expander`、splitter 的 8 epx 命中区小于 32 epx、部分新间距与折叠行高未完全 token 化；Spec 初审仅重复指出 token 项，没有发现 scope creep。
- 已改用 WPF UI `CardExpander`；splitter 使用 32 epx 命中区和居中的 4 epx 视觉线；所有新增间距以及 auto/master-only/collapsed/splitter 行高均改为命名资源。
- 审查修正后的 focused 测试和最终 tier 1 再次通过，结果仍为 474 passed / 82 skipped / 0 failed；skip 集合及原因未变化。

### 2026-08-20 — 黄金机预览

- 在干净 detached worktree 上以提交 `5fbf133407f74f8f98b4a7066f56a8607110cc52` 执行
  `Invoke-GoldenRendererValidation.ps1 -Ticket 28 -Suite watch-production-preview`，结果通过。
- 唯一最终证据目录：`mes/ingest/csharp/.artifacts/golden-renderer/ticket-28/run-20260820-142214-watch-production-preview`。
- 环境门通过：交互式桌面 `1920×1080`、`96 DPI`、`100%`、浅色、`zh-CN`、
  China Standard Time、Microsoft YaHei UI / Consolas 均存在、SoftwareOnly 渲染。
- `watch-vm-tests`：149 total / 144 passed / 5 skipped / 0 failed。5 项 skip 为
  `WatchWindowCandidateEquivalenceTests.Candidate_directories_are_visually_equivalent`（未设置
  candidate reference/actual，仅由 stability gate 驱动），以及
  `WatchWindowVisualEquivalenceGoldenFixtureTests` 的 4 个 fixture 测试（未设置
  `MESINGEST_WATCH_GOLDEN_FIXTURES`）；均不是票 28 行为跳过。
- `watch-ui-journeys`：1 passed / 0 skipped / 0 failed；生产窗口旅程通过真实鼠标拖动
  `SeriesId` 列头分隔线并确认列宽增加，通过 UIA 收起详情后生成
  `03a-demand-series-master-only.png`，再展开并继续生成 `03-demand-series-detail.png`。
- 未批准、未覆盖任何视觉基线。清理证据：scheduled task 不存在、残留进程 0，清理后环境复检返回 0。
- 用户已于 2026-08-20 审阅收起态与恢复详情态的最终预览并明确回复“批准”。未批准、未覆盖视觉基线。

## Answer

票 28 已完成：DemandSeries 详情和顶部来源说明可折叠，主从区域可拖动且会话内保持比例，
主列表列宽可在真实 WPF 主题下拖动，窄窗使用横向滚动，分页控件完整并居中。Tier 1、
黄金机 `watch-vm-tests` 与生产 UI 旅程均通过，用户已批准最终真实窗口预览。
