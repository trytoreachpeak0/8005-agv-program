# Demand Series Inspector E / Ticket 03 TDD plan

Implement vertical slices at the two public seams. Add the named red tests first,
make only the minimum production change for that slice, and keep production-shaped
snapshot/event names. Do not run Tier 2/3 without user approval.

## Slice 1 — truthful formation facts

Extend `WatchDemandSeriesInspectorPresentationTests`:

1. Keep/refine
   `Project_Production_creation_events_translate_reasons_and_select_reason_specific_facts`
   to assert the full normal pre-archive order and exact PollTrace/commit/sequence
   for every available fact.
2. Keep/refine
   `Project_Postarchive_reappearance_keeps_production_status_and_archive_evidence`
   to assert `LONG_GONE_BUT_VISIBLE`, full post-archive order, and exact archive
   evidence.
3. Add
   `Project_Known_reappearance_marks_missing_expected_facts_unavailable_without_placeholder_evidence`
   with pre-archive missing predecessor-last/GONE and post-archive missing archive
   cases. Assert ordered expected fact slots, an explicit availability state,
   null/absent time/sequence/PollTrace/commit for unavailable facts, and exact
   successor evidence.
4. Keep the unknown/malformed theory and add a no-creation-event case if needed;
   assert neutral label/raw metadata and no predecessor/GONE/archive narrative.

Minimum production shape: represent fact availability explicitly (nullable
committed-evidence fields for unavailable slots), produce reason-specific ordered
slots, and never use display placeholders as committed evidence.

## Slice 2 — boundary truth, all seven fields, and ordinal-complete rows

Extend `WatchDemandSeriesInspectorPresentationTests`:

1. Strengthen
   `Project_Unique_assigned_boundary_rows_enable_all_seven_scalar_mes_fields`
   to assert exact order, changed and unchanged labels/flags, `MesSourceDate`,
   before/after PollTrace+commit, and the exact TransportDemand/DemandId disclaimer.
2. Split the broad missing/duplicate test into:
   - `Project_Zero_assigned_boundary_is_explicit_absence_without_a_synthetic_row`
   - `Project_Multiple_assigned_rows_disable_scalar_projection_and_preserve_every_raw_row_in_global_ordinal_order`
3. Use an interleaved fixture: ordinal 1 `Unassigned`, ordinals 2/3 `Assigned`.
   Assert assignment groups are retained, the flattened render view is exactly
   1/2/3, all rows retain PollTrace/commit/assignment/identity/native values, and
   no scalar/canonical row is exposed.

Minimum production shape: preserve assignment grouping and add/use a per-boundary
ordinal-sorted raw-row view. Do not obtain UI order by flattening assignment
groups. Keep absence as state/evidence anchored by PollTrace/commit, never an
all-null `DemandRawObservationSnapshot`.

## Slice 3 — public window evidence and UI Automation

Add STA tests in `WatchDemandSeriesInspectorCoordinatorTests` (the existing file
already exercises the real public `Update` seam):

1. `Update_Reappearance_facts_expose_visible_and_automation_trace_commit_or_explicit_unavailable_state`
   covers normal pre/post facts plus an unavailable expected fact. Assert visible
   label/value/evidence text and content-derived UIA name/help text; unavailable
   cards must say missing without a fake trace, commit, time, or sequence.
2. `Update_Unique_boundaries_show_trace_commit_all_seven_fields_change_states_and_noncausal_explanation`
   asserts both boundary summaries remain visible in scalar mode, contain their
   real PollTrace/commit, render seven rows, include both “已变化” and “保持不变”,
   and show the TransportDemand/DemandId disclaimer.
3. `Update_Zero_row_boundary_exposes_named_absence_and_no_blank_raw_row`
   asserts dynamic visible/UIA absence text, scalar panel hidden, raw panel shown,
   and zero rows for that side.
4. `Update_Conflict_boundary_exposes_named_conflict_and_complete_global_ordinal_raw_grid`
   asserts conflict UIA/text, scalar panel hidden, raw grid rows 1/2/3, no
   canonical value, and columns/row values sufficient to distinguish assignment,
   SeriesId, DemandId, seven native fields, PollTrace, and projection commit.
5. `Update_Unknown_reason_keeps_neutral_primary_text_and_secondary_raw_code_visible`
   asserts both technical metadata and layout remain present without borrowed
   lifecycle copy.

Give stable AutomationIds to both boundary status elements and the full raw grid.
Dynamic AutomationProperties must carry absence/conflict and committed evidence;
color alone is never evidence. Keep the existing formation-facts and MES-compare
IDs stable where possible.

## Slice 4 — many-generation public interaction

Add
`Update_Many_generations_virtualizes_scrolls_focused_history_and_preserves_distinct_current_marker`:

- construct enough generations to exceed the viewport;
- make an off-screen historical generation focused and the last generation current;
- call public `Update`, show/layout the window, and assert recycling virtualization,
  content scrolling, selected item/container brought into view, current marker on
  the different current generation, and generation-selection intent still reports
  the selected DemandId;
- avoid private methods, sleeps, pixel coordinates, and a single-item fixture.

## Slice 5 — production journey and visual handoff

After the public seams are green, update the real-process production journey
fixture to include pre-archive, post-archive `LONG_GONE_BUT_VISIBLE`, unknown,
absence, conflict/interleaved raw rows, and many generations as the narrowest
useful scenario matrix. UIA checks should find the named formation facts,
MES comparison, absence/conflict status, and complete raw grid before captures.

Run non-pixel gates first. Then stop and ask for permission before Tier 2, stating
that the interactive golden suite costs minutes and must run serially on
`gpt_win11`. If authorized, use the narrowest affected suite/class/method through
the repository wrapper, preserve every red attempt, show the final real-window
preview for explicit user approval, and do not promote a baseline unless separately
authorized by the golden workflow.

## Requirement-to-evidence map

| ID | Requirement (verbatim) | Planned evidence |
| --- | --- | --- |
| R1 | `PREARCHIVE_REAPPEARANCE` 以“归档前消失后再现”呈现，并在证据存在时显示 predecessor、最后匹配观测、权威 absence/GONE 和 successor 首次匹配观测。 | Normal pre-archive projection test + `Update_Reappearance_facts_expose_visible_and_automation_trace_commit_or_explicit_unavailable_state` |
| R2 | `POSTARCHIVE_REAPPEARANCE` 以“归档后再次出现”呈现，保留生产 `LONG_GONE_BUT_VISIBLE` 语义，并在证据存在时额外显示 archive fact。 | Post-archive projection test + same public window test |
| R3 | 未知或畸形原因使用中性中文说明和次要原始码，布局不崩溃，也不合成不受证据支持的生命周期解释。 | Existing projection theory + `Update_Unknown_reason_keeps_neutral_primary_text_and_secondary_raw_code_visible` |
| R4 | 每项形成事实暴露真实 PollTrace 和 projection evidence，缺失事实明确缺失，不用占位值冒充已提交事实。 | `Project_Known_reappearance_marks_missing_expected_facts_unavailable_without_placeholder_evidence` + fact window/UIA test |
| R5 | 唯一可信边界行时，对齐显示 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES（MesSourceDate）和 PACKAGE，并区分“已变化”与“保持不变”。 | Strengthened unique projection test + unique-boundary window test |
| R6 | 画面明确说明 MES 字段差异是观察证据，不是 TransportDemand/DemandId 形成原因。 | Unique projection exact-copy assertion + unique-boundary window test |
| R7 | 任一边界为零行时显示明确 absence fact，不渲染全空字段行。 | Zero-boundary projection test + `Update_Zero_row_boundary_exposes_named_absence_and_no_blank_raw_row` |
| R8 | 任一边界为多行时显示冲突状态和全部原始行，保持 ordinal 顺序，不生成标量 diff 或 canonical row。 | Interleaved-ordinal projection test + conflict window/raw-grid test |
| R9 | 许多世代时导航继续虚拟化、滚动并保留当前/选中世代的独立标记。 | `Update_Many_generations_virtualizes_scrolls_focused_history_and_preserves_distinct_current_marker` |
| R10 | 公开 presentation 和窗口交互测试覆盖归档前、归档后、未知原因、唯一 diff、零行、多行冲突及多世代滚动。 | Exact presentation/window test set in slices 1–4 |
| R11 | 自动化名称覆盖形成事实、MES 对比、absence、conflict 和完整原始行网格。 | Window/UIA tests in slice 3 plus production-journey UIA probes |
| R12 | 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。 | Final clean command and complete pass/fail/skip transcript; name every skip, especially the SQL-server skips described by `AGENTS.md` |
| R13 | Read `docs/agents/golden-renderer.md`. | Recorded in research; re-check workflow before authorized run |
| R14 | Ran the required golden-machine suites through an interactive task. | User-authorized unique golden evidence directory and runner log |
| R15 | User approved the final real-window preview (visual changes only). | Explicit approval message tied to final preview hashes |
| R16 | Recorded the unique evidence directory and all named skips. | Evidence manifest and named skip list |
| R17 | Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI. | Cleanup/original-VM environment report |

## Verification sequence

1. Red-green each slice with the narrowest `MesIngest.Tests` class filter.
2. Re-open every test and map concrete assertions to R1–R11; empty-function and
   interleaved-order pseudo-mutations must fail.
3. Run the mandated test-gap and assertion-quality reviews and record fixes in
   `.testagent/demand-series-inspector-e-03/status.md`.
4. From `mes/ingest/csharp`, run exactly `dotnet test MesIngest.Tests` for Tier 1
   and record Passed/Failed/Skipped plus every named skip.
5. Run the implementation skill's required two-axis code review and repair any
   Standards or Spec findings.
6. Only after explicit user authorization, perform the narrow interactive golden
   preview/evidence/approval/cleanup sequence described above.
