# Ticket 22 test plan

> Ticket 22 content below predates the DemandSeries Inspector E work. It is
> retained verbatim. Ticket 06 planning is appended in a separate section at
> the end of this file.

Work in vertical red-green slices at the specification-confirmed production
seam.

1. Add Error Search query-helper tests for default latest first page, all
   filters/windows/page sizes, frozen previous/next/direct page requests and
   explicit attention drill conditions; implement the minimum query helpers.
2. Add Error Search presenter tests for exact facets/totals/order, normalized
   condition/UTC window facts, successful-empty vs loading/failure retention,
   matched period boundaries, cross-generation evidence and bounded raw states;
   implement the minimum presenter.
3. Add Current Attention presenter/query tests for all four current kinds,
   stable Series identity/drill, structured global evidence, facets/paging and
   explicit non-incident semantics; implement the minimum helpers.
4. Add production ScriptedFakeHost tests for initial loads, filters/windows,
   frozen paging/direct jump, selection/detail, failure retention, raw evidence
   expansion/error isolation and attention-to-error drill-down.
5. Replace both placeholders with production Fluent pages and wire event
   handling through the existing client/session/auto-refresh interfaces. Do not
   add a page-only Host or test bypass.
6. Add tests proving AREA application never changes/refetches either Ticket 22
   query and that Overview explicit intents open both pages on page one.
7. Add semantic WPF tests for the Variant A equal-height three-column layout,
   responsive stack, stable UIA names/ids, keyboard reachability and non-color
   statuses. Pixel and real-window claims remain deferred until the shared run.
8. Re-open every generated assertion against the checklist, then perform
   `test-gap-analysis` with empirically verified pseudo-mutations and close any
   substantive survivors.
9. Run focused presenter/query/session/page suites and a non-incremental Release
   solution build, then the full solution test suite exactly once. Record every
   environment skip and unrelated pre-existing failure.
10. Run the required two-axis `/code-review`, fix findings, and repeat only the
    affected focused gates.
11. Freeze Ticket 22 with an implementation commit, then run the single shared
    tickets 19-22 interactive targeted-suite and real-window preview train.
    Pause for explicit user approval; do not generate candidates, promote
    baselines or create DPI clones because Ticket 23 owns those gates.
12. Record shared evidence/approval/cleanup in tickets 19-22, set Ticket 22's
    final tracker state, and commit the evidence closure.

## Requirement mapping

| Checklist | Planned evidence |
| --- | --- |
| 1, 2, 3, 4 | `WatchErrorSearchPresentationTests`, `WatchErrorSearchQueryTests`, and production integration |
| 5 | Error raw-evidence presenter tests and ScriptedFakeHost production interaction |
| 6, 7 | `WatchCurrentIngestAttentionPresentationTests` plus attention production integration |
| 8 | AREA-isolation request timeline and visible state assertions |
| 9 | Ticket 22 responsive/UIA semantic integration tests |
| 10 | Shared golden preview directory, targeted-suite results, explicit approval, named skips and cleanup logs |

---

# DemandSeries Inspector E — Ticket 06 test plan

Work test-first at the spec-confirmed coordinator/window, workspace, and
preferences seams. Production edits and green implementation belong to the
parent agent.

1. Extend real-window coordinator tests with a vertical slice proving that a
   background `Update` leaves a minimized Inspector minimized and unactivated,
   while explicit `OpenOrShow` restores and activates the same instance.
2. Add public WPF lifecycle tests for independent main/Inspector minimization,
   Escape no-close, and the standard system-close path (the observable Alt+F4
   contract), preserving existing owner/topmost/taskbar assertions.
3. Extend the production shell test harness with close/reopen-current-selection,
   Host-switch cancellation/cleanup, and main-window shutdown cancellation.
   Reuse the deterministic delayed detail client; do not introduce timers or
   external dependencies.
4. Add preference-store/window integration tests that start from the old
   version-2 JSON, persist distinct main and Inspector layouts, reload through
   `WatchV2PreferencesStore`, and assert normal bounds, monitor identity, and
   maximized restore bounds through real windows.
5. Add opt-out, invalid-coordinate, missing-monitor, and reduced-work-area
   cases. Mutate a document first emitted by production so tests constrain
   semantics without inventing a private persistence schema.
6. Add the Settings accessible-name assertion for the backward-compatible
   “记住窗口布局” wording.
7. Run the narrowest VSTest filter covering the new Ticket 06 classes/methods,
   preserve the expected first red result, and report compile failures or
   behavioral mismatches exactly. Do not run Tier 2/3.

## Requirement mapping

| Checklist | Planned test evidence |
| --- | --- |
| 1 | `Background_update_keeps_a_minimized_inspector_minimized_until_explicit_show_restores_it` plus existing `Selection_update_changes_open_content_without_showing_or_activating_the_window` |
| 2 | `Main_and_inspector_minimize_independently_and_escape_does_not_close_inspector`; `System_close_command_closes_the_inspector_and_reopen_creates_a_new_window`; existing `Fluent_window_exposes_normal_top_level_semantics_and_first_observation_evidence` |
| 3 | `Closing_and_reopening_loads_current_selection_and_resets_local_investigation_state`; existing `Closing_inspector_cancels_pending_detail_and_rejects_its_late_body` |
| 4 | `Host_change_closes_inspector_cancels_old_detail_and_preserves_saved_layout` |
| 5 | `Closing_main_window_closes_inspector_and_cancels_pending_detail` |
| 6 | `Version_2_remember_window_size_document_loads_as_the_shared_layout_preference`; `Settings_names_the_backward_compatible_choice_remember_window_layout` |
| 7 | `Layout_opt_out_does_not_persist_main_or_inspector_geometry`; `Remembered_layout_round_trips_main_and_inspector_normal_bounds_and_monitor_identity`; `Maximized_inspector_restores_safe_normal_bounds_then_maximized_state` |
| 8 | `Invalid_inspector_coordinates_restore_the_clamped_1200_by_800_default` |
| 9 | `Missing_monitor_falls_back_to_a_visible_work_area`; `Changed_work_area_clamps_the_complete_inspector_normal_bounds` |
| 10 | Focused red command in `.testagent/status.md`; Tier 1/Tier 2/Tier 3 left to the parent implementation flow |
