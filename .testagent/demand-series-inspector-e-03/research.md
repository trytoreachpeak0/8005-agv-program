# Demand Series Inspector E / Ticket 03 test research

## Scope and authority

This run is bounded to
`.scratch/demand-series-inspector-e/issues/03-render-reappearance-and-mes-boundaries.md`.
The public seams agreed by the specification are:

- `WatchDemandSeriesInspectorPresentation.Project(DemandSeriesDetailSnapshot, focusedDemandId)`
  for reason, formation-fact, MES-boundary, and ordering behavior.
- `WatchDemandSeriesInspectorWindow.Update(WatchDemandSeriesInspectorPresentation)`
  plus public WPF selection/click behavior for visible text, UI Automation,
  virtualization, scrolling, and selected/current-generation state.

No private-method tests, new Host/session seams, or tests of prototype UI belong
to this ticket. The production snapshot is authoritative. The requested
`find-untested-sources` helper is not installed or present in the workspace; one
bounded manual pairing pass was therefore used and must not be repeated.

The mandatory UI references were read: `docs/agents/fluent-ui.md` and
`docs/agents/golden-renderer.md`. Tier 2/3 work requires separate user approval
under `AGENTS.md`; it is not part of the local red-green loop.

## Bounded target inventory

| Target | Responsibility | Representative tests |
| --- | --- | --- |
| `MesIngest.Watch/WatchDemandSeriesInspectorPresentation.cs` | Projects production reason codes, ordered formation facts, raw observations, scalar diff eligibility, and immutable events | `MesIngest.Tests/WatchDemandSeriesInspectorPresentationTests.cs` |
| `MesIngest.Watch/WatchDemandSeriesInspectorWindow.xaml.cs` | Atomically renders one focused generation, switches scalar/raw evidence, filters events, scrolls the selected generation | `MesIngest.Tests/WatchDemandSeriesInspectorCoordinatorTests.cs` |
| `MesIngest.Watch/WatchDemandSeriesInspectorWindow.xaml` | Visible fact/evidence content, AutomationProperties, diff states, virtualized generation list, raw grid | `MesIngest.Tests/WatchDemandSeriesInspectorCoordinatorTests.cs`; golden journey below |
| `MesIngest.Watch.UiTests/WatchWorkspaceProductionJourneyTests.cs` | Existing real-process Inspector preview and UIA path | fixture test and `03-demand-series-detail` / `03b-demand-series-first-observation` steps |

`MesIngest.Tests` uses xUnit v2, STA WPF tests via `StaTestRunner`, direct public
window interaction, `FindName`, and stable AutomationId/Name assertions. The
Watch project exposes internals to this test assembly. Existing fixtures already
use real `DemandSeriesDetailSnapshot`, production event names, PollTrace IDs,
projection commits, and `MesObservationAssignment`.

## Current behavior and verified gaps

### Formation reasons and facts

- Existing projection tests already prove the prescribed Chinese labels,
  production `LONG_GONE_BUT_VISIBLE`, archive selection when present, neutral
  future/malformed fallback, and the normal pre-archive fact order.
- `ProjectFormationFacts` conditionally omits predecessor-last, GONE, and archive
  facts. A known reappearance with missing evidence therefore has no explicit
  unavailable entry. If the predecessor snapshot itself cannot be resolved it
  returns only the successor creation fact. This contradicts the ticket's
  requirement that missing facts be explicit and invites the UI to imply a
  complete lifecycle from an incomplete collection.
- `WatchDemandFormationFactPresentation` has non-null time/PollTrace/commit
  fields and no availability state, so the model cannot truthfully represent
  an expected but unavailable fact without inventing placeholder evidence.
- Normal fact tests assert nonblank PollTrace/commit in the presentation, but
  no public window test proves those values are visible or exposed to UIA.
  The current XAML fact card displays only label, value, occurrence time, and
  optional sequence. PollTrace and projection commit are silently absent.

### MES boundaries

- Existing tests cover the seven required fields, `MesSourceDate`, changed-field
  flags, cause disclaimer, one zero-row side, one duplicate assigned side, and
  suppression of scalar fields.
- `ProjectBoundarySide` first sorts matching raw rows by ordinal, then groups by
  assignment. `Update` flattens those assignment groups. With interleaved
  assigned/unassigned ordinals (for example 2/1/3), rendered order becomes
  assignment order rather than global ordinal order. The existing duplicate
  test uses assigned ordinals 1/2 followed by unassigned ordinal 3 and cannot
  detect this mutation.
- The presentation preserves assignment groups, as required by the E spec, but
  lacks a separate globally ordinal raw-row view for rendering. A correct fix
  must retain the real grouping metadata while exposing every row once in
  ordinal order; it must not select a canonical row in a conflict.
- Boundary state text currently contains only label and state. In unique scalar
  mode the entire raw-evidence panel is collapsed, so the boundary PollTrace and
  projection commit are not visible or reachable through UIA even though they
  are present in the presentation.
- Absence does not fabricate an all-null row today, which is correct, but there
  is no window test pinning the visible absence fact, its PollTrace/commit
  anchor, zero grid rows, and scalar-panel suppression as one intersection.
- Conflict correctly suppresses scalar projection, but there is no window test
  for a visible/UIA conflict state and an ordinal-complete raw grid. The raw
  grid's current AutomationId is after-side-specific even though it concatenates
  both sides, and its columns omit assignment and raw row identity fields that
  distinguish preserved evidence.
- The disclaimer correctly says field changes are observation evidence and not
  a DemandId cause. It should remain visible in every boundary state and should
  say `TransportDemand/DemandId` explicitly to match the ticket.

### Navigation, scrolling, and accessibility

- The ListBox enables recycling virtualization, content scrolling, and a
  vertical scrollbar. `Update` selects and calls `ScrollIntoView` on the focused
  generation. Existing tests inspect virtualization and two-generation focus,
  but not an off-screen selection in a many-generation list.
- `IsCurrent` and `SelectedItem` are distinct data/state paths. Current coverage
  only checks their labels with two items; it does not prove that focusing an
  off-screen historical generation leaves a different current generation
  marked current.
- Stable IDs already exist for formation facts, scalar comparison, before state,
  and raw grid, but the after state has no AutomationId and dynamic absence/
  conflict names are not set. Fact-item trace/commit evidence also lacks a
  content-derived automation name/help text.

## Ticket acceptance checklist and existing coverage

| ID | Ticket requirement (verbatim) | Existing evidence / gap |
| --- | --- | --- |
| R1 | `PREARCHIVE_REAPPEARANCE` 以“归档前消失后再现”呈现，并在证据存在时显示 predecessor、最后匹配观测、权威 absence/GONE 和 successor 首次匹配观测。 | Normal-path projection test exists. Missing expected facts and visible evidence are untested and currently wrong. |
| R2 | `POSTARCHIVE_REAPPEARANCE` 以“归档后再次出现”呈现，保留生产 `LONG_GONE_BUT_VISIBLE` 语义，并在证据存在时额外显示 archive fact。 | Normal-path projection test exists. Missing archive must become an explicit unavailable fact; window rendering is untested. |
| R3 | 未知或畸形原因使用中性中文说明和次要原始码，布局不崩溃，也不合成不受证据支持的生命周期解释。 | Projection theory exists. Raw code is currently collapsed; window-visible secondary metadata/layout behavior is missing. |
| R4 | 每项形成事实暴露真实 PollTrace 和 projection evidence，缺失事实明确缺失，不用占位值冒充已提交事实。 | Presentation normal facts contain evidence. Explicit unavailable state and visible/UIA evidence are missing. |
| R5 | 唯一可信边界行时，对齐显示 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES（MesSourceDate）和 PACKAGE，并区分“已变化”与“保持不变”。 | Projection field/flags test exists. Window test of seven rendered rows and both state labels is missing. |
| R6 | 画面明确说明 MES 字段差异是观察证据，不是 TransportDemand/DemandId 形成原因。 | Presentation asserts a shorter DemandId disclaimer. Window-visible exact wording is untested. |
| R7 | 任一边界为零行时显示明确 absence fact，不渲染全空字段行。 | Projection state/empty groups covered. Public window intersection is missing. |
| R8 | 任一边界为多行时显示冲突状态和全部原始行，保持 ordinal 顺序，不生成标量 diff 或 canonical row。 | Scalar suppression and grouped rows covered only for non-interleaved ordinals. Global ordering and public raw-grid completeness are missing/currently wrong. |
| R9 | 许多世代时导航继续虚拟化、滚动并保留当前/选中世代的独立标记。 | Virtualization flags and two-item selection covered. Many-item off-screen scroll and distinct current/selected state are missing. |
| R10 | 公开 presentation 和窗口交互测试覆盖归档前、归档后、未知原因、唯一 diff、零行、多行冲突及多世代滚动。 | Projection covers most states; public window coverage is limited to first observation and a two-item update. |
| R11 | 自动化名称覆盖形成事实、MES 对比、absence、conflict 和完整原始行网格。 | Some static IDs exist; dynamic state names, after-state ID, per-fact evidence UIA, and complete raw-grid assertions are missing. |
| R12 | 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。 | Not run during research; implementation exit gate. SQL skips must be counted by name, not inferred from `Failed: 0`. |
| R13 | Read `docs/agents/golden-renderer.md`. | Completed during research; implementation must follow it. |
| R14 | Ran the required golden-machine suites through an interactive task. | Deferred; requires user authorization for Tier 2 and the narrowest covering suite. |
| R15 | User approved the final real-window preview (visual changes only). | External approval gate after final preview. |
| R16 | Recorded the unique evidence directory and all named skips. | Deferred to approved golden run. |
| R17 | Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI. | Deferred to approved golden run cleanup. |

## Bug-revealing intersections to retain

- Known pre-archive reason + missing predecessor-last and GONE evidence + real
  successor creation: expected fact slots remain ordered, missing slots contain
  no invented time/PollTrace/commit, successor retains exact committed evidence.
- Known post-archive reason + missing archive event: archive is explicitly
  unavailable without losing `LONG_GONE_BUT_VISIBLE` or successor evidence.
- Conflict poll with ordinal 1 unassigned, ordinals 2 and 3 assigned: every row
  remains separate and renders as 1/2/3 while scalar projection stays off.
- Unique before/after rows with both changed and unchanged fields: seven aligned
  fields, visible trace/commit anchors, both state labels, and cause disclaimer.
- Zero assigned rows with a real authoritative boundary PollTrace/commit: visible
  absence, no synthetic blank row, and no scalar/canonical value.
- Many generations with historical focused item and a different current item:
  focused item is selected/scrolled into view; current marker remains on current.
