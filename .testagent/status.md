# Ticket 4 test completion status

## Pseudo-mutation verification

The Ticket 4 production changes were mutated one at a time, exercised with the
narrowest xUnit/VSTest filter, and restored immediately.

| Injected mutation | Killing evidence |
| --- | --- |
| Do not clear the rejected conditional cache | `Second_old_epoch_signal_is_not_retried_and_the_next_refresh_stays_unconditional` observed the stale identity on the next refresh. |
| Parse only the first raw-evidence `fields` query value | `Raw_evidence_fields_parse_comma_repeated_and_mixed_query_forms_identically` lost `package`. |
| Map `HistoryEpochMismatchException` to 400 instead of 409 | `Catalog_old_epoch_exception_is_a_typed_http_409_response` observed BadRequest. |
| Accept repeated by-key values instead of rejecting them | `Demand_series_by_key_missing_empty_and_repeated_keys_use_the_stable_typed_error` escaped into SQL rather than returning the typed 400. |
| Let Watch synthesize a missing scheduler DTO | `Current_attention_rejects_the_pre_v2_4_shape_without_poll_scheduler` stopped throwing the required decode failure. |
| Recompute/corrupt scheduler `backoffLevel` in Host | `Host_singleton_snapshot_is_exposed_as_a_minimal_serializable_attention_field` observed 0 instead of the coordinator's 2. |

Observed injected mutations: 6; killed: 6; surviving verified gaps: 0.
No mutation remains in the worktree.

## Assertion review

- Host HTTP tests assert status, stable code, and both current/supplied epoch UUIDs.
- Consumer tests assert the exact conditional identity sequence, single
  unconditional retry, cache clearing after retry failure, and replacement by
  the new complete epoch.
- Query tests cover missing, empty, repeated, comma, repeated-key, and mixed
  forms with exact typed error or normalized field assertions.
- OpenAPI tests assert 503 reasons, enum values, scheduler required/nullability
  and bounds, typed 409 schema, parameter serialization, and canonical/live
  equality.
- Watch tests require the v2.4 scheduler field and preserve its five values in
  non-UI consumption logic.

The three real-SQL focused scenarios are correctly skipped when the documented
Ticket01 SQL Server environment variables are absent; Tier 1 must report that
skip count explicitly.

## Final validation

- Focused affected classes: 109 passed, 0 failed, 36 skipped (SQL-gated).
- Tier 1 `dotnet test MesIngest.Tests`: 872 passed, 0 failed, 137 skipped,
  1009 total in 9m 59s.
- All three `MES_INGEST_TICKET01_*` variables were absent. No Tier 2 or Tier 3
  command was run.
