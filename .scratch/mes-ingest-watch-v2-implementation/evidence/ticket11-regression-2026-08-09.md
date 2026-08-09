# Ticket 11 regression evidence — 2026-08-10

Fixed point: `de20ea90545811110560608473d00ffa2f76b706`

Implementation: Wpf.Ui 4.3.0 selected-UI rebuild on `factory-validation`

## Ticket 01–10 mapping

| Ticket | Re-proved seams |
| --- | --- |
| 01 | Four-page navigation, one Host composition root, connection/preferences, and read-only shell behavior. |
| 02 | Scripted fake Host, composition-root contracts, serial UI entry, and copied-run baseline-directory override. |
| 03 | Overview healthy/degraded/offline states, banners, status projections, and deterministic completed offline refresh. |
| 04 | VISIBLE query/session/API sorting, filtering, paging, and five-column selected task workspace. |
| 05 | Independent GONE state/session/cursor and selected GONE visual scenario. |
| 06 | MES inputs, local projection, detail/copy seams, and always-visible related-alert cards. |
| 07 | Alert query/session/page/detail, active/resolved/empty/loading/failure states, and five-column alert workspace. |
| 08 | Exact DemandId navigation, business-key/task/global scopes, and separate previous-GONE/current-reappearance cards. |
| 09 | Refresh admission, cancellation, retained results, staleness, auto-refresh, and shared top/status projections. |
| 10 | 64/194/260/28 layout anchors, AutomationIds/names, keyboard seams, 100% real-window journeys, plus the retained Ticket 10 125%/150% DPI journey evidence and current narrow-DIP layout assertions. |

## Implementation and local regression

- Production `MainWindow` is a `Wpf.Ui.Controls.FluentWindow`; Light theme resources, primary buttons, and page auto-refresh switches use locked `WPF-UI` 4.3.0 controls.
- D/E anchors are enforced by deterministic structure tests: 64px global header, 194px navigation, 260px filters, 28px status bar, five core columns, and visible relationship cards.
- `dotnet test MesIngest.Tests/MesIngest.Tests.csproj -c Release --no-restore`: 496 passed, 19 SQL-environment skips, 0 failed (515 total).
- `Invoke-WatchUiTests.ps1 -Configuration Release -Suite watch-vm-tests`: 80 passed, 2 skips, 0 failed (82 total).
- Focused copied-run baseline-directory tests: 2 passed; deterministic completed-offline-state regression: 1 passed.
- `git diff --check` on Ticket 11 source/test files: clean (line-ending notices only).

The two local UI skips are explicit and are not counted as passes:

1. `WatchVisualEnvironmentTests.Current_environment_supports_real_window_uia_journeys` — local desktop culture/UI culture is `en-US/en-US`, not the required `zh-CN/zh-CN`; the same probe passed on `GPT-WIN11`.
2. `WatchWindowJourneyTests.Operator_can_review_all_four_production_pages_on_the_golden_desktop` — deliberately requires the guarded interactive runner; it passed there as part of the five real-window journeys.

## Golden-machine evidence

Golden environment: `GPT-WIN11`, interactive Session 1, 1920x1080, 96 DPI, Windows light theme, `zh-CN`, `China Standard Time`, Microsoft YaHei UI/Consolas, and `SoftwareOnly`.

- Four real-window previews (Overview, Demand, Alert, Settings) were generated under `.artifacts/ticket11-golden/final-wpf-ui-previews/`. The user reviewed the final images and answered `这版符合` on 2026-08-10.
- Five FlaUI journeys passed, 0 skipped, 0 failed under `.artifacts/ticket11-golden/final-wpf-ui-journeys/20260810-002103-984/`.
- Candidate v17: all 19 PNG + 19 XML received files were byte-identical for 10 consecutive runs (`WATCH_XAML_CANDIDATE_STABLE`). Evidence: `.artifacts/ticket11-golden/final-xaml-stability/candidate-v17/`.
- Nineteen individual before/after/diff proposals, XML pairs, SHA-256 hashes, pixel-change ratios, contact sheets, and scenario decisions are under `.artifacts/ticket11-golden/final-xaml-stability/proposals-v17/`. No tolerance or mask was used; the legacy files one directory above `SelectedUi` were not overwritten.
- The first approved run (v18) correctly exposed a run-7 race in `overview-offline-stale`: capture occurred after the first of three failures while refresh was still busy. The red result and received pair are retained under `.artifacts/ticket11-golden/final-xaml-stability/approved-v18-flake-run7/`; later green repetitions were not used to hide it.
- A rejected diagnostic v19 candidate demonstrated why converting offline into one-resource partial failure was semantically wrong; it remains evidence only and was not promoted.
- Final v20 after deterministic three-gate fake-Host sequencing: 10/10 complete matrix runs passed, 0 failures, 0 received, `WATCH_XAML_STABLE`. Result: `.artifacts/ticket11-golden/final-xaml-stability/approved-v20-final/xaml-stability-result.json`.
- All Ticket 11 scheduled tasks and residual `MesIngest.Watch`/`testhost`/`vstest.console` processes were removed after evidence collection.

The golden desktop was deliberately kept at its user-mandated 100% DPI throughout Ticket 11. Ticket 10's already-retained real 125% and 150% runs remain at `mes/ingest/csharp/TestResults/ticket10-dpi-smoke-20260809/` (each 5 journeys passed); Ticket 11 did not mutate the calibrated desktop DPI.

## Explicit SQL Server skips / Ticket 13 gate

All 19 use the documented reason `SQL Server unavailable (set MES_INGEST_SQLSERVER or enable LocalDB)` and remain a Ticket 13 release gate:

1. `SchemaUpgradeTests.EnsureSchema_never_drops_or_truncates_transport_demands`
2. `SchemaUpgradeTests.Mid_upgrade_failure_leaves_no_half_migration_and_recovers_on_rerun`
3. `SchemaUpgradeTests.Upgrading_phase1_schema_preserves_demands_pauses_alerts_and_poll_health`
4. `SqlServerReadApiPersistenceTests.Http_reads_projection_alerts_and_health_after_store_restart`
5. `SqlServerTransportDemandStoreTests.Persisted_demands_and_pauses_are_readable_after_new_store_instance`
6. `SqlServerTransportDemandStoreTests.Change_feed_full_purge_keeps_monotonic_watermark_and_expires_stale_cursors`
7. `SqlServerTransportDemandStoreTests.Query_page_desc_with_tied_primary_values_has_no_gap_or_dup`
8. `SqlServerTransportDemandStoreTests.Persisted_alerts_and_poll_health_are_readable_after_new_store_instance`
9. `SqlServerTransportDemandStoreTests.ReplaceState_commits_projection_and_alerts_atomically`
10. `SqlServerTransportDemandStoreTests.ReplaceState_does_not_rewrite_unchanged_resolved_alert_history`
11. `SqlServerTransportDemandStoreTests.Query_page_desc_page_boundary_inside_tie_group_has_no_gap_or_dup`
12. `SqlServerTransportDemandStoreTests.ReplaceState_writes_only_changed_rows_and_leaves_gone_immutable`
13. `SqlServerTransportDemandStoreTests.Query_page_uses_read_path_indexes_and_keyset_pagination`
14. `SqlServerTransportDemandStoreTests.Alert_query_pages_new_sort_columns_on_the_shared_contract`
15. `SqlServerTransportDemandStoreTests.ReplaceState_is_atomic_across_demand_and_pause_writes`
16. `SqlServerTransportDemandStoreTests.Gone_history_lookup_uses_ordinal_transport_demand_key_equality`
17. `SqlServerTransportDemandStoreTests.Query_page_new_visible_columns_cover_nulls_ties_and_both_directions`
18. `SqlServerTransportDemandStoreTests.Change_feed_survives_host_store_restart_and_purges_expired_entries`
19. `SqlServerTransportDemandStoreTests.ReplaceState_appends_change_feed_in_same_transaction_for_created_and_gone`

## Baseline state

`MesIngest.Watch.UiTests/Baselines/SelectedUi` now contains the reviewed active matrix: 19 `*.verified.png` and 19 `*.verified.xml`. The rejected pre-reset baselines remain versioned historical evidence in the parent directory. Ticket 12/13 are not implicitly approved by this Ticket 11 result.
