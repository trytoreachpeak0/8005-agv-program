# Ticket 09 test-generation status

## Current state

- Implementation and executable evidence are complete from fixed review point `30864c8`.
- The production SQL/Host catalog, HTTP adapter, consumer-owned durable store, and reference order-intent flow are wired into `MesIngest.sln`.
- The user approved the local test database and Git metadata writes; the formal real-SQL gate is green and the delivery blocker is cleared.

## Requirement evidence

| Requirement | Exact executable evidence |
| --- | --- |
| Centrally qualified formal catalog | `Central_policy_requires_visible_unique_valid_condition_free_unarchived_demand`; `Central_policy_rejects_missing_or_invalid_required_fields`; `Catalog_only_contains_centrally_eligible_demands_while_operations_detail_keeps_every_rejected_demand` |
| Complete stable full-range facts and no Dispatch filters | `Catalog_returns_complete_stable_items_in_demand_id_order_and_rejects_dispatch_scope_queries`; `Complete_200_maps_the_host_contract_and_weak_etag_without_query_parameters` |
| Business-only CatalogRevision | `Initial_empty_catalog_is_a_complete_stable_revision_zero_resource`; `Catalog_revision_changes_once_only_for_member_or_member_value_changes`; `Failure_incomplete_and_replay_leave_the_committed_catalog_unchanged` |
| Atomic conditional read | `Conditional_catalog_read_returns_bodyless_304_or_one_atomically_committed_full_revision`; `Conditional_read_sends_the_weak_etag_and_maps_304_without_reading_a_body` |
| Disposable consumer cache | `New_consumer_rebuilds_discarded_cache_from_a_complete_catalog_without_a_revision_cursor` |
| Final reread, immutable acceptance, reliable intent | `Commit_point_unconditionally_rereads_and_rejects_a_changed_revision_or_value`; `Commit_point_accepts_an_unchanged_candidate_when_only_the_global_catalog_revision_advances`; `Commit_point_rejects_a_candidate_that_left_the_readable_catalog`; `Commit_point_rejects_changed_catalog_value_provenance_even_when_revision_and_mes_fields_match`; `Accepted_snapshot_and_order_intent_are_atomically_frozen_and_ignore_later_catalog_refreshes`; `File_store_survives_restart_and_rejects_same_key_with_different_content`; both `Unknown_remote_result_*` tests |
| Lifecycle/error and consumer-boundary E2E | `Field_duplicate_and_multiple_work_type_recovery_reenter_catalog_in_one_revision`; `Gone_demand_exits_and_postarchive_visible_successor_never_enters_catalog`; `Production_host_catalog_updates_leave_consumer_cancellation_and_dispatch_canaries_untouched`; `Mes_ingest_production_assemblies_do_not_reference_consumer_owned_dispatch_state` |

## Verification log

- Release solution build: success, 0 errors; 4 `NU1900` warnings because the NuGet vulnerability endpoint is unavailable.
- Focused ticket09 run with the approved real SQL Server: 33 passed, 0 failed, 0 skipped.
- Current focused TRX: `.artifacts/ticket09-tests/ticket09-focused-current.trx`.
- Reference consumer and HTTP adapter focused run after durable-store tightening: 18 passed, 0 failed, 0 skipped.
- Full core project with the approved SQL connection: 586 passed, 19 pre-existing SQL-fixture skips, and 1 unrelated existing wall-clock retention failure (`LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age`).
- Pseudo-mutation audit: 3/3 substantive mutations were killed (conditional commit-point read, no UNKNOWN same-key retry, and removed durable key-conflict guard); every mutation was reverted and the focused suite returned green.
- Final dual-axis review against `30864c8`: Spec 0 findings; Standards 0 actionable findings. No WPF files changed.
- `git diff --check`: clean.
- Formal gate `Invoke-Ticket09SqlServerGate.ps1 -ExpectedProductMajor 16 -ExpectedCompatibilityLevel 160`: 15 passed, 0 failed, 0 skipped against SQL Server major 16 / compatibility 160. TRX: `.artifacts/ticket09-tests/ticket09-externally-readable-catalog-sqlserver.trx`.
- The temporary external audit index was deleted after the user authorized cleanup.
