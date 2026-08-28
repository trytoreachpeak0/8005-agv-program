# Ticket 04 test implementation plan

## Phase 1 — presentation contract

Extend `WatchDemandSeriesInspectorPresentationTests` at the existing public `Project` / `EventsForDemand` seam.

- Strengthen `Project_Events_remain_real_immutable_sequence_and_support_local_demand_filtering` to assert:
  - stable committed `SeriesSequence` order;
  - no prototype convenience events;
  - exact `EventId`, `SeriesId`, `EventType`, occurrence, subject kind/id, PollTrace, ProjectionCommit, PayloadVersion, and raw payload;
  - all-events returns the same collection;
  - related filtering returns the same event objects in stable order across repeated filters;
  - unknown DemandId produces an empty local view without changing the source collection.

## Phase 2 — public WPF interaction contract

Extend `WatchDemandSeriesInspectorCoordinatorTests` because it already owns the real-window STA interaction tests.

1. `Event_workspace_exposes_exact_filter_labels_complete_evidence_and_accessible_keyboard_contract`
   - peer first-level tabs;
   - exact filter labels `全部 Series 事件` and `当前 Demand 相关事件`;
   - stable AutomationId/name and focus/tab-stop semantics for tab, related action, filters, and event grid;
   - grid binding paths for the complete production event evidence.
2. `Related_event_action_and_filter_roundtrip_stay_local_preserve_order_and_emit_no_request`
   - related action atomically selects event tab and current-Demand filter;
   - related/all/related roundtrip preserves order and object identity;
   - context text identifies filter, DemandId, and counts;
   - no `GenerationFocusRequested` event is emitted by event controls.
3. `Related_filter_tracks_the_new_focused_generation_after_one_atomic_update`
   - with related mode active, a same-Series presentation update to a new focused generation updates the related rows and context consistently.
4. `Series_switch_clears_event_filter_and_returns_to_generation_analysis_without_request`
   - a different Series resets the selected tab to generation analysis, selects all-events, renders only the new Series event collection, clears the old Demand context, and emits no outward request.

## Verification

1. Build/execute only the two test classes using VSTest `--filter` syntax.
2. Fix test compilation or invalid test mechanics only; do not modify production code and do not weaken behavioral expectations.
3. Preserve the first red failure as red-before-green evidence in `status.md`.
4. Re-open every generated assertion and record gap/assertion-quality review in `status.md`.
