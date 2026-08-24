# 02 — 切换为单实例 Inspector 并贯通首次观察

**What to build:** 用单实例、非模态的普通顶层 Inspector 一次性替换 DemandSeries 内联详情，并贯通一个可独立演示的首次观察调查路径：从满高列表显式打开窗口，选择世代，看到紧凑 Series/快照上下文、中文形成原因和单侧首次观察证据。

**Blocked by:** 01 — 同步 E 架构决策并建立可信 Presentation。

**Status:** done

**UI authority:** [Fluent UI guidance](../../../docs/agents/fluent-ui.md) · [Golden Renderer workflow](../../../docs/agents/golden-renderer.md)

- [x] DemandSeries 页面移除内联详情、splitter 和展开/折叠控件，保留过滤、分页、选择和来源说明，列表占满剩余高度。
- [x] 页面提供随窗口状态切换的“打开详情窗口”/“显示详情窗口”命令；空结果或无稳定选择时不可执行。
- [x] Enter 和双击等价于显式打开/显示；Space 只改变列表选择，不创建、显示或激活 Inspector。
- [x] Inspector 是单实例、无 Owner、非 Topmost、显示在任务栏与 Alt+Tab 中的 modeless Fluent 顶层窗口；显式打开/显示会激活已有实例。
- [x] Inspector 不拥有 Host client、timer、refresh loop 或独立 snapshot，只消费主页面冻结快照对应的不可变 presentation 并向上报告用户意图。
- [x] 顶部只呈现一个紧凑 Series 与冻结快照上下文；主体建立“世代分析”和“事件”两个一级任务入口，不复制旧内联布局。
- [x] 可滚动、可虚拟化的纵向世代列表是唯一世代导航，并独立表达当前世代与选中世代。
- [x] 第一代路径完整显示紧凑身份行、“首次观察到”、真实形成事实和单侧 MES 观察，不制造 predecessor 或 before 行。
- [x] 切换选中世代时，其标题、原因、事实、MES 证据和事件过滤上下文作为同一状态更新，不出现混代内容。
- [x] Shell/协调器公开行为测试覆盖单实例、显式激活、非激活内容更新、Enter、双击、Space、默认首行选择和空状态。
- [x] 自动化名称覆盖窗口、打开/显示命令、一级 Tab、世代导航、形成原因和首次观察证据。
- [x] 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-22 — implementation and acceptance evidence reconciled

- Commits `33a7a38a` and `e557b570` replaced the inline detail with the
  selected-prototype E single modeless Inspector and aligned its production
  hierarchy and interactions. At the validated source identity `7111f77c`,
  shell/coordinator public behavior tests cover the full-height list, disabled
  empty state, one-window reuse, explicit activation, non-activating content
  updates, Enter, double-click, Space, default first-row selection, normal
  top-level window semantics, first-observation one-sided evidence, atomic
  generation updates, virtualized generation navigation, and stable UI
  Automation names.
- The final integrated Tier 1 run passed 641, failed 0, skipped 82, total 723.
  The 82 named skips are the existing SQL Server environment gate documented
  in Ticket 01; this ticket changed no SQL.
- Earlier Ticket 02 renderer directories are retained only as historical design
  evidence: their latest manifest was dirty and contained no manual acceptance.
  Final acceptance therefore uses the later clean, superset production
  validation from Ticket 07, which explicitly exercised and displayed the
  current-generation and first-observation one-sided path required here.
- After explicit authorization, `watch-ui-journeys` ran from clean detached
  commit `7111f77c` on the calibrated interactive `gpt_win11` desktop. The
  720x600 run passed 1/1 with zero skips at
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-07/run-20260822-031219-watch-ui-journeys-720x600`;
  the 1440x900 run passed 1/1 with zero skips at
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-07/run-20260822-031653-watch-ui-journeys-1440x900`.
- Both runs passed pre/post environment checks at 1920x1080 and 96 DPI with an
  interactive Explorer session, and cleanup found no scheduled task or residual
  process. The user reviewed the final production previews, including the
  first-observation one-sided evidence, and explicitly replied “批准” on
  2026-08-22. No Tier 3 suite or baseline promotion ran. Ticket 02 is complete.
