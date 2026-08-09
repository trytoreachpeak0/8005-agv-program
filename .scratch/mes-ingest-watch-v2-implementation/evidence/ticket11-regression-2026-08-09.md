# Ticket 11 regression evidence — 2026-08-09

Fixed point: `5dae21a`

Implementation: selected UI rebuild on `factory-validation`

## Ticket 01–10 mapping

| Ticket | Re-proved seams |
| --- | --- |
| 01 | `WatchV2ShellTests`, `WatchHostSessionTests`, connection/preferences tests and the unchanged four-page navigation/one-Host composition root |
| 02 | `ScriptedFakeHostTests`, `WatchCompositionRootTests` and the serial `watch-vm-tests` entry |
| 03 | overview state/session, banner and status projections plus deterministic healthy/degraded/offline visual scenarios |
| 04 | VISIBLE browse/session/API tests, server sorting/filtering/cursor tests and the selected Demand UI scenario |
| 05 | independent GONE session/tab/cursor tests and the selected GONE visual scenario |
| 06 | `WatchDemandDetailsTests`, clipboard/startup tests and the always-visible MES input/local projection/related-alert card |
| 07 | alert query/session/page/detail tests and active/resolved/empty/loading/failure visual scenarios |
| 08 | `AlertDemandNavigationTests`, `WatchAlertRelationshipTests`, exact Demand fetch tests and separate previous-GONE/current-reappearance cards |
| 09 | auto-refresh, admission, cancellation, banner, staleness and local-log isolation tests; refresh/cancel controls remain visible in the selected UI |
| 10 | layout/preferences/UIA tests plus new 1440×900 assertions for 194px navigation, 64px top context, 260px filters, 28px status bar, core copy/controls and relationship-card visibility |

## Commands and results

- `dotnet build MesIngest.sln`: 0 warnings, 0 errors.
- `dotnet test MesIngest.Tests/MesIngest.Tests.csproj`: 496 passed, 19 skipped, 0 failed.
- `Invoke-WatchUiTests.ps1 -Suite watch-vm-tests`: 73 passed, 1 environment-reporting test skipped, 0 failed.
- Final `dotnet test MesIngest.sln --no-restore --no-build`: core 496 passed / 19 SQL skipped; UI 73 passed / 26 environment-gated visual and real-window cases skipped; 0 failed.
- A detached clean worktree at the implementation commit built successfully; 13 changed core/API tests and 6 selected-UI anchor tests passed.
- The first full-solution run exposed a test-side race in `Slow_overview_refresh_exposes_busy_state_and_cancel`: visible cancellation completed before the fake Host appended its canceled timeline event. The assertion now waits for that public fake-Host event; the focused diagnostic then passed 20/20 consecutive process runs. The original failure was not counted as a pass or hidden by the reruns.
- `watch-xaml-visual` stopped in its authoritative preflight with exit code 2 before starting Verify.Xaml; `Baselines/SelectedUi` contained zero `*.received.*` files.
- `watch-ui-journeys` stopped in its authoritative preflight with exit code 2 before starting FlaUI.

## Explicit skipped and blocked items

All 19 SQL skips use the same documented reason: `SQL Server unavailable (set MES_INGEST_SQLSERVER or enable LocalDB)`. They remain an explicit Ticket 13 release-gate item and are not reported as passing:

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

`WatchVisualEnvironmentTests.Current_environment_supports_real_window_uia_journeys` (Ticket 10 DPI/UIA regression) was skipped because the current culture/UI culture is `en-US/en-US`, not `zh-CN/zh-CN`.

The 19 Verify.Xaml cases and five real-window journeys were not run after their preflights rejected the desktop. The current desktop is `2560×1440`, 144 DPI (150%), `en-US/en-US`; the required XAML baseline desktop is `1920×1080`, 96 DPI (100%), `zh-CN/zh-CN`. Per ticket 11, this mismatch must stop the visual suites and must not be bypassed by accepting screenshots.

## Baseline state

The rejected pre-reset approved files remain historical evidence in `Baselines/`. Verify.Xaml and the 10-run stability script now target the empty, versioned `Baselines/SelectedUi/` directory. No selected-UI baseline is approved until a calibrated real preview is explicitly accepted and all 19 XAML/PNG pairs are byte-identical for ten consecutive runs.
