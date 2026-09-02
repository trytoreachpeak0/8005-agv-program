# Ticket 13 test status

## Focused result

- `HistoryRetentionStateTests`: 4 passed, 0 failed, 0 skipped on SQL Server 16 / compatibility 160.
- Affected frozen/API matrix: 50 passed, 0 failed, 0 skipped.
- Token-stability regression matrix: 8 passed, 0 failed, 0 skipped.
- Frozen-read concurrency regression matrix: 5 passed, 0 failed, 0 skipped.
- Final Tier 1: 790 passed, 0 failed, 0 skipped in 9m48s.

## Requirement coverage

- `Retention_clocks_use_exact_thirty_day_boundaries` covers tick-before, exact, tick-after, and exact 30 x 24 hour arithmetic for both clocks.
- `Raw_observation_multiset_expires_atomically_at_the_Host_UTC_boundary` covers PollTrace CompletedAt authority, old/future MES DATES irrelevance, complete multiset deletion, earliest boundary, 410/404 distinction, and unchanged current/structural Series facts.
- `Empty_expired_PollTrace_is_410_when_the_cutoff_is_the_earliest_boundary` covers marker-based expiry when a zero-row PollTrace cannot be inferred from missing observations or a strict-earliest comparison.
- `Series_eligibility_is_created_cancelled_and_restarted_from_each_qualifying_Host_UTC` covers qualification predicate, first timestamp stability, active observation/condition/error/event cancellation, and later requalification.
- `EmptyDatabaseBootstrapTests.An_empty_database_bootstraps_the_whole_schema_once` covers both retention columns and the filtered eligibility index.

## Pseudo-mutation audit

Four high-risk mutations were injected one at a time against real SQL and reverted immediately. All four were killed:

1. Exact raw cutoff `<=` changed to `<`.
2. Explicit `RawObservationsExpiredAt` read check removed.
3. First `EligibilityAt` overwritten by every later eligible commit.
4. Ineligible transitions stopped clearing `EligibilityAt`.

The restored focused suite passed afterward. No verified survivor remains in the ticket13 policy/state paths.

## Review result

- Spec fixed-point review: no actionable findings.
- Standards/code-quality fixed-point review: no actionable findings.
- No Tier 2, Tier 3, Golden WPF, multi-day fixture, or soak run was required.
