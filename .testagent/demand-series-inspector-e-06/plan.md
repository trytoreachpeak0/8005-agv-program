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
