# DemandSeries 单实例 Inspector：E 世代调查工作台

Status: ready-for-agent

## Problem Statement

DemandSeries 主列表和完整调查详情目前挤在同一页面中。内联详情、分隔条和折叠开关占用大量垂直空间，使主列表和调查证据都得不到足够画布；把世代演化、MES 原始值和永久事件同时铺在一个详情面板中，又会让不同调查任务互相争夺空间。

现有详情还容易把某一种换代路径表现成通用流程。例如固定的“上一代最后匹配 → GONE 边界 → 新一代首次匹配”只适用于部分再现情形，不能准确表达首次观察、归档前再现、归档后再现及未来可能增加的形成原因。英文原因码直接占据醒目位置也增加理解成本。

调查人员需要在很多 Demand 世代之间快速切换，理解每一代为什么形成，查看形成边界两侧的真实 MES 观测差异，同时仍能完整查看 DemandSeriesEvent。界面必须忠实保留 MesIngest 的领域语义：字段差异只是证据，不是创建新 DemandId 的原因；重复或缺失原始观测不能被客户端挑选或合并成一个看似可信的值。

## Solution

用一个单实例、非模态、普通顶层 Inspector 一次性替换 DemandSeries 页面中的内联详情。主页面只保留满高需求系列列表和明确的“打开／显示详情窗口”命令；Inspector 打开期间跟随主列表选择，并复用主页面的冻结快照和刷新状态，不建立独立查询生命周期。

Inspector 采用最终 E 信息架构：顶部只保留紧凑的 Series 与冻结快照上下文；主体用“世代分析”和“事件”两个一级 Tab 分开调查任务。“世代分析”左侧是唯一的 Demand 世代导航，右侧展示所选世代的紧凑身份、中文形成原因、按原因变化的形成事实，以及代际边界 MES 原生字段对比。“事件”Tab 全宽展示真实的不可变 DemandSeriesEvent，并可从“相关事件”入口带入当前 DemandId 过滤。

形成原因以匹配该 DemandId 的 `TRANSPORT_DEMAND_CREATED` 事件和生产模型为权威来源。已知原因显示中文：“首次观察到”“归档前消失后再现”“归档后再次出现”；原始原因码只作为悬浮提示或辅助技术信息。形成事实不是固定箭头流程，而是由实际原因和现有证据组成的可变事实集合。

MES 对比只说明边界两侧原始查询内容发生了什么变化，不声称 EQP、DATES、PACKAGE 等字段变化触发了换代。当任一边界轮次没有唯一可信原始行时，界面停止标量字段对比，明确显示缺失或多行冲突，并提供对应全部原始行；绝不任意挑选、合并或覆盖原始观测。

## User Stories

1. As an MES 调查人员, I want the DemandSeries list to use the full remaining page height, so that I can scan and page through more series without a permanently occupied detail pane.
2. As an MES 调查人员, I want a visible “打开详情窗口” command, so that the way to begin an investigation is discoverable without knowing a shortcut.
3. As an MES 调查人员, I want the command to become “显示详情窗口” when the Inspector already exists, so that I understand it will reuse the current single instance.
4. As a keyboard user, I want Enter on a selected series to open or show the Inspector, so that I can investigate without using the mouse.
5. As a mouse user, I want double-clicking a selected series to open or show the Inspector, so that the common list interaction works as an accelerator.
6. As a keyboard user, I want Space to change list selection only, so that selection does not unexpectedly create or activate another window.
7. As an MES 调查人员, I want the Inspector to be modeless, so that I can compare it with the main list or place the two windows on separate monitors.
8. As an MES 调查人员, I want the Inspector to appear in the taskbar and Alt+Tab, so that it behaves like an ordinary investigation window.
9. As an MES 调查人员, I want only one Inspector instance, so that multiple windows do not drift to different snapshots or series.
10. As an MES 调查人员, I want an explicit open/show action to activate the Inspector, so that the requested window is immediately visible.
11. As an MES 调查人员 working in another application, I want list selection changes to update but not activate, restore, or raise the Inspector, so that background refresh and navigation do not steal focus.
12. As an MES 调查人员, I want the Inspector to follow the selected Series while it is open, so that the list remains the single source of navigation.
13. As an MES 调查人员, I want selection changes to identify the new target immediately and clear the previous body, so that stale evidence is never shown under a new Series heading.
14. As an MES 调查人员, I want new details to commit atomically only when SeriesId, frozen snapshot reference, and focused generation still match, so that late responses cannot overwrite the current investigation.
15. As an MES 调查人员, I want closing the Inspector to cancel its pending detail request and stop invisible detail reads, so that closed UI does not consume work or retain obsolete state.
16. As an MES 调查人员, I want reopening the Inspector to load the currently selected series, so that I resume from the visible main-list context rather than a closed investigation.
17. As an MES 调查人员, I want the Inspector top area to contain only one compact Series and snapshot context, so that repeated DemandId and “调查工作台” title rows do not waste vertical space.
18. As an MES 调查人员, I want “世代分析”和“事件” to be separate first-level tabs, so that permanent events remain available without squeezing the generation evidence.
19. As an MES 调查人员, I want a scrollable generation list as the only generation navigator, so that a Series with many DemandIds remains usable and does not grow into an unbounded horizontal card chain.
20. As an MES 调查人员, I want each generation item to show generation number, DemandId, status, and current-generation marking, so that history, selection, and current state are distinguishable at a glance.
21. As an MES 调查人员, I want the selected generation and current generation to be represented independently, so that inspecting history never makes an old generation look current.
22. As an MES 调查人员, I want same-Series refresh to preserve my focused DemandId when it still exists, so that live refresh does not reset my investigation.
23. As an MES 调查人员, I want a Series switch to clear generation-specific state, so that filters, evidence, and focus from the previous Series are not carried across identities.
24. As an MES 调查人员, I want the selected generation header to fit on one compact line, so that DemandId, generation, status, and predecessor are available without another large title block.
25. As an MES 调查人员, I want the formation reason to be shown in Chinese, so that I can understand it without decoding an internal enum-like value.
26. As a support engineer, I want the raw formation reason code available as secondary technical information, so that I can correlate the UI with logs and payloads without exposing the code as the primary explanation.
27. As an MES 调查人员, I want generation 1 to say “首次观察到”, so that the UI does not invent a predecessor or a replacement transition.
28. As an MES 调查人员, I want a pre-archive reappearance to say “归档前消失后再现”, so that it reflects a new TransportDemand created in the same tracking Series after authoritative absence.
29. As an MES 调查人员, I want a post-archive reappearance to say “归档后再次出现”, so that it reflects the production `LONG_GONE_BUT_VISIBLE` semantics rather than a prototype-only status name.
30. As an MES 调查人员, I want unknown future formation reasons to use a neutral Chinese fallback plus the raw code, so that the layout remains truthful instead of forcing new behavior into an old legend.
31. As an MES 调查人员, I want formation evidence to be a variable set of labeled facts, so that first observation, pre-archive reappearance, post-archive reappearance, and future reasons can show different relevant evidence.
32. As an MES 调查人员, I want pre-archive reappearance evidence to identify the predecessor, its last matching observation, the authoritative absence/GONE fact, and the successor's first matching observation when those facts are present, so that I can reconstruct the boundary.
33. As an MES 调查人员, I want post-archive reappearance evidence to include the archive fact when present, so that the longer lifecycle boundary is not flattened into the pre-archive case.
34. As an MES 调查人员, I want every fact to retain its real PollTrace and projection evidence, so that the explanation can be traced back to committed production facts.
35. As an MES 调查人员, I want all seven MES native fields—TASK_TYPE, SUBLOT, AREA, EQP, STEP, DATES, and PACKAGE—aligned in the comparison, so that I can scan complete query content rather than a hand-picked subset.
36. As an MES 调查人员, I want DATES to remain explicitly identified as the MES source field MesSourceDate, so that it is not confused with lifecycle event time.
37. As an MES 调查人员, I want unchanged fields and changed fields to be visibly distinguishable, so that the useful differences stand out without hiding stable key fields.
38. As an MES 调查人员, I want the UI to state that field differences are observational evidence rather than formation causes, so that ordinary MES value changes are not mistaken for DemandId creation rules.
39. As an MES 调查人员, I want scalar MES diff only when each compared boundary poll has exactly one assigned raw observation for the DemandSeries key, so that every displayed value has a trustworthy source.
40. As an MES 调查人员, I want a zero-row boundary to be shown as an explicit absence fact rather than a row of blank values, so that “没有匹配” is not confused with fields that are present but null.
41. As an MES 调查人员, I want a multi-row boundary to be shown as an explicit conflict with the complete raw row set, so that duplicate-key evidence is preserved and no arbitrary row becomes canonical.
42. As an MES 调查人员, I want the first generation to use a one-sided first-observation view, so that a fake “before” row is never fabricated.
43. As an MES 调查人员, I want changing the selected generation to atomically update its header, reason, facts, MES evidence, and event filter context, so that mixed-generation content is never visible.
44. As an MES 调查人员, I want a “相关事件” action from generation analysis, so that I can move directly to events concerning the selected DemandId.
45. As an MES 调查人员, I want the event tab to offer “全部 Series 事件”和“当前 Demand 相关事件” filtering, so that I can switch between lifecycle context and focused evidence.
46. As an MES 调查人员, I want event filtering to be a local view operation over the same frozen event collection, so that filtering cannot mutate, refetch, or reorder domain facts.
47. As an MES 调查人员, I want the event tab to show real DemandSeriesEvent fields and payload evidence at full width, so that no permanent event is lost by adopting the generation workbench.
48. As an MES 调查人员, I want events to remain ordered by SeriesSequence, so that their committed lifecycle order is stable and auditable.
49. As an MES 调查人员, I want current-detail refresh failures to retain the last successful detail with a clear stale/error state, so that transient Host failure does not erase useful evidence.
50. As an MES 调查人员, I want a target-switch failure to show a failure state for the requested target without the previous Series body, so that identity and evidence cannot be mismatched.
51. As an MES 调查人员, I want an item that leaves the refreshed result set to clear rather than silently select another Series, so that scope changes are explicit.
52. As an MES 调查人员, I want leaving the DemandSeries page to pause its refresh while preserving the last successful Inspector snapshot, so that inactive work does not refresh behind the user's current task.
53. As an MES 调查人员, I want precise deep links from overview, qualification audit, error search, and current attention to locate the Series and show the Inspector, so that cross-workflow investigation remains intact.
54. As an MES 调查人员, I want a deep-linked FocusedDemandId to establish the initial generation selection, so that I land on the evidence that motivated the navigation.
55. As an MES 调查人员, I want the Inspector to preserve generation focus, selected error/evidence context, column widths, and scroll position during a same-Series refresh where possible, so that refresh is not disruptive.
56. As an MES 调查人员, I want closing and recreating the Inspector to restore only its window layout, so that a deliberately ended investigation does not silently resume internal context.
57. As a multi-monitor user, I want Inspector size, normal position, monitor, and maximized state restored to a currently visible work area, so that saved geometry never strands the window off-screen.
58. As a user, I want the existing “记住窗口尺寸” preference to become a backward-compatible “记住窗口布局” preference, so that main and Inspector window placement follow one understandable choice.
59. As a user, I want the main window and Inspector to minimize independently, so that the Inspector remains a normal top-level work surface.
60. As a user, I want Alt+F4 to close the Inspector while Escape does not close it, so that standard window semantics are preserved.
61. As a user, I want changing Host settings to close the Inspector and clear old-Host detail while retaining geometry, so that evidence from different Hosts cannot be mixed.
62. As a user, I want closing the main window to close the Inspector and terminate the application cleanly, so that no orphan window or request remains.
63. As a low-resolution user, I want the Inspector to reflow vertically below the responsive breakpoint and remain scrollable, so that content is not clipped at the 720×600 minimum.
64. As an accessibility user, I want generation navigation, tab selection, open/show actions, filters, states, and evidence grids to expose stable automation names and keyboard behavior, so that the workflow is operable and testable without pointer-only interaction.

## Implementation Decisions

- The accepted information architecture is E. Prototype variants A through D remain design evidence only and do not ship alongside E.
- The Inspector replaces the existing inline DemandSeries detail, splitter, and expand/collapse control in one cutover. There is no runtime feature flag or hidden second detail implementation.
- The main DemandSeries page retains its filters, paging, selection, snapshot/source explanations, and full-height list. It adds only a visible open/show command and the agreed double-click/Enter accelerators; it does not add detail-state columns.
- The Inspector is a single, unowned, non-Topmost, modeless Fluent top-level window with taskbar and Alt+Tab presence. It has no owner relationship to the main window and no independent navigation shell.
- A coordinator owns Inspector creation, explicit activation, non-activating content updates, request cancellation, application shutdown cleanup, and geometry persistence. The Inspector itself does not own a Host client, timer, session, or refresh loop.
- The DemandSeries detail view consumes an immutable presentation and exposes user intent upward. It does not query the Session or infer domain facts from rendered values.
- Stable list selection and detail loading are separate session operations. A closed Inspector does not cause selection-only navigation to fetch invisible detail.
- All detail content comes from the same frozen snapshot reference used by the selected DemandSeries list. A response is committable only when Host generation, target SeriesId, snapshot reference, and focused DemandId still match the active request.
- Ordinary DemandSeries navigation opens only the list. Precise navigation targets originating elsewhere locate the target Series, create or show the Inspector, and carry source-snapshot comparison plus optional FocusedDemandId.
- The top of the Inspector uses one compact Series context, including stable Series identity (`SUBLOT + WorkType`), lifecycle/current presence, frozen snapshot identity/time, and stale or source-comparison state. It does not repeat large “Series 调查工作台” and DemandId title rows.
- “世代分析”和“事件” are first-level sibling tabs sharing the same Series context. Generation evidence and events are never permanently split side by side.
- A vertical, virtualizable generation list is the sole generation navigator. Current-generation state and selected-generation state are distinct visual properties.
- Generation 1 defaults to `FIRST_OBSERVED` presentation because its production creation event has no predecessor reason. Later formation reasons come from the matching `TRANSPORT_DEMAND_CREATED` event payload, not from status transitions or MES field differences.
- Known reason translations are `FIRST_OBSERVED` → “首次观察到”, `PREARCHIVE_REAPPEARANCE` → “归档前消失后再现”, and `POSTARCHIVE_REAPPEARANCE` → “归档后再次出现”. The primary UI shows Chinese; the raw code remains secondary technical metadata.
- Unknown or malformed reason payloads produce a neutral, explicit fallback. They do not crash rendering, borrow another reason's legend, or synthesize a lifecycle explanation.
- Formation evidence is a variable ordered collection of labeled facts. It may include predecessor identity, predecessor last observation, authoritative GONE event, archive event, successor creation event, and first observation according to what the reason and frozen evidence actually support.
- Production status vocabulary remains authoritative, including `LONG_GONE_BUT_VISIBLE`. Prototype-only status names and event types are forbidden.
- The event tab renders only real immutable DemandSeriesEvent values from the frozen snapshot. It must not invent convenience events such as `DEMAND_REAPPEARED` or `SNAPSHOT_COMMITTED` when those are not production event types.
- Event filtering is local and non-destructive. “相关事件” selects the event tab and filters by the selected DemandId; the user can return to all Series events without another Host request.
- Boundary MES evidence comes from DemandRawObservationSnapshot grouped by its actual PollTrace/commit and assignment. Raw duplicates remain separate rows in ordinal order.
- Scalar before/after comparison is allowed only when each applicable side has exactly one assigned row. A missing side is absence, not an all-null record. A multiple-row side is a conflict, not a candidate-selection problem.
- The MES field table preserves the native field vocabulary TASK_TYPE, SUBLOT, AREA, EQP, STEP, DATES, and PACKAGE. DATES is labeled as MesSourceDate and remains distinct from event occurrence and projection commit times.
- MES field changes are described as “已变化／保持不变” evidence only. The UI explicitly avoids causal wording because TransportDemand creation is governed by lifecycle disappearance/reappearance rules, not ordinary field mutation.
- Same-Series refresh attempts to preserve focused DemandId and local view state if those identities remain valid. Switching Series resets generation-specific filters and evidence state.
- Current-target refresh failure retains the last successful presentation and marks it stale. Switching-target failure clears the old body and presents the requested target's failure state.
- Inspector close, Host change, and application shutdown cancel pending detail work. Host change discards old-Host detail but does not discard valid saved geometry.
- Window layout persistence extends the existing preference document compatibly. Invalid or unavailable saved monitor coordinates are clamped to a visible work area.
- Default Inspector size is 1200×800 effective pixels; minimum size is 720×600. Narrow layouts reflow and scroll instead of clipping controls or data.
- The existing Inspector ADR remains authoritative for window ownership, focus, lifecycle, refresh, navigation, and persistence. This spec supersedes only its earlier statement that the first production version would copy the old inline information architecture unchanged.
- Production UI work must follow the repository Fluent UI rules and golden-renderer workflow. A local screenshot or prototype image is design evidence, not production visual acceptance.

## Testing Decisions

- Tests assert externally observable behavior at the highest stable seams and avoid private methods, visual-tree implementation details, or one assertion per internal control.
- The primary domain/presentation seam is the DemandSeries presentation projection. Focused tests cover reason extraction and Chinese translation, generation-1 fallback, pre- and post-archive evidence selection, production status/event vocabulary, raw observation grouping, scalar-diff eligibility, absence, duplicate-row conflict, and event filtering inputs.
- Presentation tests use real production-shaped DemandSeries snapshots and real event names. Test fixtures must not perpetuate prototype-only events or statuses.
- The primary window-lifecycle seam is the Inspector coordinator's public behavior. Tests cover single-instance creation, explicit show/activation, non-activating selection updates, close/recreate, pending-request cancellation, Host-change cleanup, and main-window shutdown.
- Session behavior tests cover the separation between stable selection and detail loading, frozen snapshot propagation, stale response rejection, same-target stale-detail retention, target-switch clearing, and closed-Inspector no-fetch behavior.
- Production shell tests cover removal of the inline detail/splitter/toggle, the full-height list, open/show command availability, empty-state disabling, default first-row selection, double-click, Enter, and Space semantics through public window interaction.
- Inspector interaction tests cover independent top-level window state, taskbar/Alt+Tab eligibility, no Owner, `Topmost=false`, independent minimization, standard Alt+F4 behavior, and no focus stealing during selection-driven content updates.
- Accessibility tests cover stable AutomationProperties for the Inspector, tab tasks, generation navigation, reason explanation, related-events action, event filter, conflict/absence states, and evidence grids, plus keyboard tab order at 720×600.
- Preference tests cover backward-compatible loading, layout opt-out, normal bounds, maximized state, monitor identity, invalid coordinates, missing monitors, and visible-work-area clamping.
- Existing focused unit and WPF shell tests are the prior art. The implementation run closes with the repository Tier 1 suite.
- Because this feature changes WPF layout, controls, automation, DPI behavior, and visual expectations, formal visual verification must follow the ticket checklist in `docs/agents/golden-renderer.md`: use the calibrated interactive golden desktop, run the narrowest covering UI suite, preserve red evidence, and obtain user approval before any baseline promotion.
- Visual scenarios include empty list, initial selected row, first-generation one-sided evidence, pre-archive reappearance, post-archive `LONG_GONE_BUT_VISIBLE`, unknown reason fallback, duplicate raw rows, many-generation scrolling, related-event filtering, stale detail, target-switch failure, 1440×900, 1920×1080 at 100% DPI, and the 720×600 responsive minimum.

## Out of Scope

- Changing the DemandSeries, TransportDemand, TransportDemandKey, DemandSeriesEvent, or DemandRawObservation domain contracts.
- Changing the Host API or database schema solely to fit the E layout. If required evidence is genuinely absent from the current frozen contract, that gap must be specified separately rather than inferred by Watch.
- Treating MES field changes as TransportDemand formation rules.
- Selecting, merging, deduplicating, or repairing conflicting MES raw observations in the client.
- Independent Inspector refresh intervals, API clients, timers, caches, or snapshots.
- Multiple simultaneous Inspector windows, pinned Series, side-by-side compare between two Series, or restoring a closed investigation's internal state.
- Shipping prototype variants A, B, C, or D, or copying prototype fake data and convenience event types into production.
- Generation search for hundreds of generations in the first release. The list must virtualize and scroll correctly; a dedicated search affordance can be proposed later from measured need.
- Editing or approving golden visual baselines without the required interactive golden-machine preview and user review.

## Further Notes

- The accepted WPF prototype demonstrated the intended E task separation, compact header, eight-generation navigation, selected-generation evidence switching, event-tab handoff, ordinary top-level window behavior, and off-screen placement recovery. It remains throwaway design evidence and is not a production source dependency.
- MesIngest's stable Series identity is `TransportDemandKey = SUBLOT + WorkType`; DemandId identifies a local TransportDemand generation inside that lifecycle. Copy and labels should preserve this distinction throughout the Inspector.
- `PREARCHIVE_REAPPEARANCE` and `POSTARCHIVE_REAPPEARANCE` describe why a successor TransportDemand was created. EQP, DATES, PACKAGE, and other raw value changes only describe what differed between observations.
- A complete authoritative poll with no matching key is lifecycle evidence even though it has no matching DemandRawObservation row. The Inspector should represent that as a fact anchored by the corresponding event/PollTrace, not fabricate a raw row.
- This spec is ready for implementation-ticket decomposition. Any UI implementation ticket must link the Fluent UI guidance and include the golden-renderer ticket checklist before work begins.
