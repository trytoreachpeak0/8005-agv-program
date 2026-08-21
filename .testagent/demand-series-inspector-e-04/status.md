# Ticket 04 test generation status

## State

- Research, plan, test implementation, compilation, and red-before-green run complete.
- Production files modified: none.
- Test files modified:
  - `MesIngest.Tests/WatchDemandSeriesInspectorPresentationTests.cs`
  - `MesIngest.Tests/WatchDemandSeriesInspectorCoordinatorTests.cs`
- Pipeline artifacts created in `.testagent/demand-series-inspector-e-04/`.

## Red-before-green evidence

Command from `mes/ingest/csharp`:

```powershell
dotnet test MesIngest.Tests --filter "FullyQualifiedName~WatchDemandSeriesInspectorPresentationTests|FullyQualifiedName~WatchDemandSeriesInspectorCoordinatorTests" -v:minimal
```

Detected platform: VSTest 17.11.1, xUnit 2.4.2, `net8.0-windows`.

Final result before production implementation:

```text
Failed: 5, Passed: 23, Skipped: 0, Total: 28
```

Expected red failures:

1. `Event_workspace_exposes_exact_filter_labels_and_accessible_keyboard_contract`
   - expected `全部 Series 事件`; actual `全部事件`.
2. `Event_workspace_exposes_complete_auditable_production_evidence`
   - expected bindings include `EventId`, `SeriesId`, and `PayloadVersion`; current grid omits them.
3. `Related_event_action_and_filter_roundtrip_stay_local_preserve_order_and_emit_no_request`
   - related context omits exact label `当前 Demand 相关事件`.
4. `Related_filter_tracks_the_new_focused_generation_after_one_atomic_update`
   - updated related context omits exact label `当前 Demand 相关事件`.
5. `Series_switch_clears_event_filter_and_returns_to_generation_analysis_without_request`
   - all-events context uses `全部事件`, not exact label `全部 Series 事件`.

The strengthened presentation test compiles and passes inside the same run. The interaction tests reach and pass their order/filter/state assertions up to the first intentionally missing label/evidence assertion.

## Test-gap review

`test-gap-analysis` was applied as a static pseudo-mutation review only. Empirical production mutations were not allowed because this subtask explicitly forbids production edits and the intended baseline is red.

| Hypothetical defect | Killing assertion |
| --- | --- |
| Project sorts events by occurrence instead of `SeriesSequence` | `Project_Events_remain_real_immutable_sequence_and_support_local_demand_filtering` asserts exact `[1,2,3,4,5]` sequence and event-type order. |
| Projection drops or substitutes any production evidence field | Same presentation test asserts every field on sequence 4, including non-default payload version 7. |
| Related filter synthesizes/clones rows | Presentation and WPF roundtrip tests use `Assert.Same` for each filtered event. |
| Related filter includes unrelated rows, drops a related row, or reorders rows | WPF roundtrip asserts `[1,3]`; all view asserts `[1,2,3]`; repeated related mode reasserts `[1,3]`. |
| Event controls emit generation intent | Roundtrip and Series-switch tests count `GenerationFocusRequested` and require zero. There is no separate Host/client surface on the Inspector window. |
| Focused-generation update keeps the old Demand filter | Generation-focus test requires only sequence 2 and new DemandId context after the atomic update. |
| Series switch carries the old filter/tab/context | Series-switch test asserts generation tab, all filter, new row identity, new DemandId, and absence of old DemandId. |
| Evidence grid hides one production field | Grid test asserts the complete ordered binding path list, then exact row evidence. |

No additional substantive Ticket 04 gap was found at the two agreed public seams. Actual keyboard event synthesis is intentionally not duplicated: WPF-native `TabControl`, `Button`, `RadioButton`, and read-only `DataGrid` behavior is represented by concrete control types plus focus/tab-stop and AutomationId/name assertions; end-to-end keyboard navigation remains Tier 2 evidence.

## Assertion-quality review

- Strong secondary observables: tab selection, radio state, context, row sequence, row reference identity, and outward-request count are asserted together.
- Non-degenerate fixtures: roundtrip uses three rows with two non-adjacent related events; payload version uses 7 rather than the default.
- Mutation resistance: exact sequences, exact binding paths, exact field values, and negative old-Demand/prototype-event assertions replace weak non-null/count-only checks.
- No sleeps, external services, filesystem dependencies, skipped tests, or production-only helpers were introduced.
- The tests close windows in every STA path under green behavior. On assertion failure, `StaTestRunner` isolates the failing thread; no persistent external process is created.

## Remaining validation

- Tier 2 golden-machine execution, preview approval, evidence directory, named
  skips, and cleanup remain user-authorized validation work.

## Green implementation and empirical pseudo-mutations

The production event workspace now uses the two exact filter labels, exposes all
eleven immutable event fields, keeps the active DemandId/count in visible and
UIA context, and marks the evidence grid with the same frozen-view semantics.
The E-authoritative event-count badge is in the event Tab header, and native
keyboard tests exercise Tab selection, related-action invocation, both filter
modes, and DataGrid row navigation. The final focused command passed 29/29 with
zero failures or skips.

Six production mutations were injected one at a time. Each was killed by the
narrow public-seam tests, reverted immediately, and followed by a final clean
29/29 run:

| Injected mutation | Killing evidence |
| --- | --- |
| Reverse projection order from ascending to descending `SeriesSequence` | Presentation test failed with actual `[5,4,3,2,1]` versus expected `[1,2,3,4,5]`. |
| Return all events for every Demand filter | Presentation and WPF tests rejected unrelated rows and wrong related counts. |
| Disable cross-Series target-change detection | `Series_switch_clears_event_filter_and_returns_to_generation_analysis_without_request` rejected the retained event Tab/filter. |
| Invert all-versus-related view selection | Roundtrip and focused-generation tests rejected the swapped row sets. |
| Remove the `PayloadVersion` grid binding | Complete production-evidence test rejected the missing binding path. |
| Emit generation intent from the related-event action | No-extra-request assertions rejected the outward event count of one. |

No substantive survivor or no-coverage zone remains at the two Ticket 04 public
seams. Assertion quality was rechecked inline: all tests use independent literal
labels/field paths, non-adjacent related rows, exact order, reference identity,
negative old-Series context, and outward-request counts. The optional
`assertion-quality` skill is not installed in this session.

## Final Tier 1 and two-axis review

From `mes/ingest/csharp`, final `dotnet test MesIngest.Tests` completed in 1m03s:

- Passed: 611
- Failed: 0
- Skipped: 82
- Total: 693

All 82 skips are the named `Ticket01SqlServerFact` environment gate. The three
required variables were absent:
`MES_INGEST_TICKET01_SQLSERVER`,
`MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`, and
`MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL`. Ticket 04 changes no SQL.

The final Standards review has no hard finding. Its two initial hard findings
(ad-hoc badge typography and a count-less UIA name) were fixed with the theme
`CaptionText` style and a bound `冻结事件总数 {0}` name. A low-priority
`Divergent Change` judgment remains because Inspector window tests historically
share the coordinator test file; moving the existing suite is outside this
ticket. The final Spec review reports no missing, partial, wrong, or scope-creep
finding. `MesIngest.Watch.UiTests` builds with zero warnings/errors, and its
production journey now captures `03c-demand-series-related-events` for the
authorized golden-machine preview.

## First golden-machine preview — visual rejection

- Authorized suite: `watch-ui-journeys`, Release, clean source `f855ccf4`.
- Evidence:
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-04/run-20260821-203205-watch-ui-journeys`.
- Runner: 1 total, 0 errors, 0 failed, 0 skipped, 0 not run, 121.108 seconds.
- Environment and cleanup: interactive Session 1, Explorer/input desktop,
  1920×1080, 96 DPI, light theme, zh-CN, China Standard Time, software
  rendering; scheduled task absent, residual processes 0, post-cleanup gate 0.
- Visual verdict: rejected. Four long technical headers were clipped in
  `03c-demand-series-related-events.png`, preventing direct field
  identification. This passing automation run remains red visual evidence.
- Fix: widen all event evidence columns and apply `DataGridTextCell` so headers
  remain legible and values use the repository's ellipsis/foreground rules.
  Post-fix focused tests pass 29/29; UI test project builds 0 warnings/errors.

## Second golden-machine preview — visual rejection

- Clean source `fefafd52`; runner 1 total, 0 errors, 0 failed, 0 skipped,
  0 not run, 119.177 seconds.
- Evidence:
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-04/run-20260821-204023-watch-ui-journeys`.
- Environment/cleanup again passed at 1920×1080 / 96 DPI with task absent and
  residual processes 0.
- Visual verdict: rejected. The cell style corrected value spacing but the
  runtime DataGrid still compressed long header identities.
- Fix: every event column now has an explicit `MinWidth` equal to its intended
  width, forcing horizontal scrolling instead of header compression. The
  public real-window test asserts both `ActualWidth` and `MinWidth` for all
  eleven columns. Focused tests pass 29/29; UI tests build cleanly.
