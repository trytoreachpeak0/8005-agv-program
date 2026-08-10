# Ticket 13 — V2 package and full regression acceptance

## Current release decision

The implementation is ready for human release approval, but no final release-signoff package exists yet. Two explicit gates remain:

1. run the 19 SQL Server tests on an available SQL Server/LocalDB, or approve the exact named skip set below;
2. record manual acceptance of the packaged Watch startup, D/E visual contract, all V2 pages/settings, and proof that the executable came from the package rather than the source tree.

The gate rejects a non-empty free-form waiver. SQL approval must supply a JSON `tests` array that exactly equals the observed skipped test names; the manual approval JSON must contain all four required confirmation tokens. Even after those checks pass, the guest produces only a readiness marker. The host promotes `RELEASE-SIGNOFF.json` and the package ZIP only after removing the original task/processes and passing the second interactive 96-DPI environment recheck; cleanup evidence is embedded in the signoff.

## Rebuild lineage

| Generation | Authoritative evidence | Result used by Ticket 13 |
| --- | --- | --- |
| Ticket 11, 2026-08-09 rebuild | [`ticket11-regression-2026-08-09.md`](ticket11-regression-2026-08-09.md) | Ticket 01–10 regression; 19 approved XAML/PNG scenarios; candidate and promoted 10-run stability |
| Ticket 12, 2026-08-09 rebuild | [`ticket12-flaui-window-baselines-2026-08-10.md`](ticket12-flaui-window-baselines-2026-08-10.md) | 5 approved real-window baselines; candidate/promoted 10-run matrices; final complete gate 50/50 |
| Ticket 13, 2026-08-09 rebuild | This file | Self-contained package, clean-install smoke, full regression/approval gates, per-file hashes |

`pack/RELEASE-EVIDENCE.json` embeds this lineage in every package and sets `oldVisualEvidenceAccepted=false`. The package validator rejects a different rebuild decision or the wrong 19/5/50 evidence counts.

## Package and clean-install evidence

- Local clean-copy smoke: `mes/ingest/csharp/.artifacts/ticket13-release/local-smoke-3/release-smoke-result.json`.
- Golden-machine pre-review diagnostic: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-13-rebuild-20260810/run-20260810-131320-watch-package-release/`.
- The diagnostic ran in the required `gpt_win11` interactive session at 1920×1080, 96 DPI, light theme, `zh-CN`, China Standard Time, required fonts and `SoftwareOnly`; scheduled-task result was 0 and cleanup reported 0 residual processes.
- Packaged smoke used a real packaged Host with a temporary CSV/in-memory projection and the packaged Watch. It matched the complete runtime/offline OpenAPI document, projected one VISIBLE demand, loaded an isolated `%LocalAppData%` layout preference, wrote an isolated latency log, and exposed the five overview UIA conclusions within 10 seconds.
- The pre-review diagnostic package contained 905 hashed files; ZIP SHA-256 was `A46CC5260BBBC6E7C1530792E4435BB9E4EECE58A9FDA92E44D9EF0F4D9E458E`. It is not release eligible because `sourceDirty=true` and later review fixes changed the gate.
- Packaged Watch acceptance in that diagnostic: `watch-vm-tests` 83/83, `watch-xaml-visual` 20/20, `watch-ui-journeys` 5/5, `watch-window-visual` 5/5; all reported 0 failed and 0 skipped.

## Core, Host, HTTP, and SQL regression

Final local result: 518 total, 499 passed, 0 failed, 19 skipped. TRX: `mes/ingest/csharp/MesIngest.Tests/TestResults/ticket13-final-core-host-http-sql.trx`.

The formal no-approval gate audit is preserved at `mes/ingest/csharp/.artifacts/golden-renderer/ticket-13-final-gate-audit-2/`. On the calibrated VM it passed the clean-install package smoke and the full regression with 499 passed, 0 failed, and the same 19 named SQL skips, wrote `summary.json`, then stopped with `SQL_SERVER_SKIPS_REQUIRE_EXACT_USER_APPROVAL` before UI/manual signoff. `cleanup.json` records no scheduled task, zero residual processes, and a successful second interactive post-cleanup check; `environment-after-host-cleanup.json` confirms 1920×1080, 96 DPI, Session 1, Explorer/input desktop, light theme, `zh-CN`, China Standard Time, required fonts, and `SoftwareOnly`.

All skips have the same environmental cause: the machine has neither `MES_INGEST_SQLSERVER` nor LocalDB. They remain individually gated:

1. `MesIngest.Tests.SchemaUpgradeTests.EnsureSchema_never_drops_or_truncates_transport_demands`
2. `MesIngest.Tests.SchemaUpgradeTests.Mid_upgrade_failure_leaves_no_half_migration_and_recovers_on_rerun`
3. `MesIngest.Tests.SchemaUpgradeTests.Upgrading_phase1_schema_preserves_demands_pauses_alerts_and_poll_health`
4. `MesIngest.Tests.SqlServerReadApiPersistenceTests.Http_reads_projection_alerts_and_health_after_store_restart`
5. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Alert_query_pages_new_sort_columns_on_the_shared_contract`
6. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Change_feed_full_purge_keeps_monotonic_watermark_and_expires_stale_cursors`
7. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Change_feed_survives_host_store_restart_and_purges_expired_entries`
8. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Gone_history_lookup_uses_ordinal_transport_demand_key_equality`
9. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Persisted_alerts_and_poll_health_are_readable_after_new_store_instance`
10. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Persisted_demands_and_pauses_are_readable_after_new_store_instance`
11. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Query_page_desc_page_boundary_inside_tie_group_has_no_gap_or_dup`
12. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Query_page_desc_with_tied_primary_values_has_no_gap_or_dup`
13. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Query_page_new_visible_columns_cover_nulls_ties_and_both_directions`
14. `MesIngest.Tests.SqlServerTransportDemandStoreTests.Query_page_uses_read_path_indexes_and_keyset_pagination`
15. `MesIngest.Tests.SqlServerTransportDemandStoreTests.ReplaceState_appends_change_feed_in_same_transaction_for_created_and_gone`
16. `MesIngest.Tests.SqlServerTransportDemandStoreTests.ReplaceState_commits_projection_and_alerts_atomically`
17. `MesIngest.Tests.SqlServerTransportDemandStoreTests.ReplaceState_does_not_rewrite_unchanged_resolved_alert_history`
18. `MesIngest.Tests.SqlServerTransportDemandStoreTests.ReplaceState_is_atomic_across_demand_and_pause_writes`
19. `MesIngest.Tests.SqlServerTransportDemandStoreTests.ReplaceState_writes_only_changed_rows_and_leaves_gone_immutable`

## Required approval inputs

When the calibrated VM must execute the SQL regression against an external SQL Server, supply all three host-side parameters: `-SqlServerCredentialPath`, `-SqlServerDataSource`, and `-SqlServerDatabase`. The credential file must be a `PSCredential` exported with `Export-Clixml` by the current host user, so its password is DPAPI-protected at rest. PowerShell Direct builds a transient guest connection-string file outside the payload ZIP; the interactive runner reads and deletes it before starting tests, and host cleanup deletes it again on every exit path. The connection string and password are not written to manifests, logs, source, or release evidence.

`-SqlSkipApprovalPath` accepts JSON with `approvedBy`, ISO-8601 `approvedAt`, the user approval message, and a `tests` array containing exactly the 19 names above. If SQL Server is supplied and no tests skip, no SQL approval file is needed.

`-ManualAcceptancePath` accepts JSON with `approvedBy`, ISO-8601 `approvedAt`, the user message, and exactly these `confirmedChecks`:

- `startup-within-10-seconds`
- `demand-alert-visual-contract`
- `v2-pages-and-settings`
- `package-run-not-source`

Only after those gates pass may the issue mark full regression, manual acceptance, final cleanup/recheck, and the overall ticket done.
