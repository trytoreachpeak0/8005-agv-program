# Ticket 03 test implementation plan

## Interface decision

Keep the existing small `RoundIngestor.IngestAsync(MesTaskUnionRound)` interface and deepen its SQL adapter. The adapter owns exact live-value replacement, validation, event sequencing, current-condition/error-period projection and readability in the same serializable transaction. The existing series read returns one consistent snapshot; Host only maps that snapshot to immutable DTOs.

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `MesFieldValidationAndSeriesErrorCatalogTests` focused rules | Requirements 3 and 6: exact AREA grammar, missing semantics and complete stable catalog |
| 2 | `Five_live_field_changes_update_the_same_demand_and_emit_exactly_five_auditable_events` | Requirements 1 and 2 |
| 3 | `Bootstrapped_missing_fields_remain_visible_extend_the_same_periods_and_clear_on_complete_success` | Requirements 3–6 |
| 4 | `Invalid_area_uses_one_persistent_period_non_success_rounds_cannot_clear_and_contract_publishes_catalog` | Requirements 3–7 |
| 5 | `First_round_bootstraps_every_erroneous_series_and_exact_repeats_add_no_error_noise` | Requirements 2–4 and 6, including no-loss overlong evidence |

## Production changes

- Core: exact field validation; contract-owned five-code error catalog; immutable current-condition, period/evidence and readability snapshots.
- SQL adapter: meaningful per-field change detection and events; exact live replacement; open/extend/close error periods and current conditions; strict SeriesSequence; all within the existing round transaction.
- SQL schema: bump isolated new-contract/schema version; add durable current-condition, error-period and error-evidence tables plus exact manifest validation.
- Host V2 DTO/read mapping: publish catalog through contract discovery and return current conditions, permanent periods/evidence, blockers and READABLE/NOT_READABLE on series reads.
- Tests: add focused rule tests and real-SQL `LiveMesFieldsAndErrorPeriodsTests`, reusing the strictly-owned database fixture and production Host composition.

## Verification

- Red/green evidence captured for missing Core seams, unsupported live changes, readability/period state, and overlong-value rejection.
- Ticket 01/02 regressions and ticket 03 acceptance passed together on real SQL Server: 16 passed, 0 skipped.
- Focused gap review added recurrence, latest-evidence linkage, exact-repeat no-noise, multi-Series bootstrap, stable meanings and blocker assertions.
- Release solution build passed with 0 warnings/errors; final full regression excluding two unrelated environment tests passed 515 with 19 environment-gated skips.
