# Ticket 04 test-generation status

## Current state

- Implementation and review complete on the confirmed production seam; no new incident model or physical schema shape was introduced.
- Focused Ticket 04 SQL Server/API gate is green: 4 passed, 0 failed, 0 skipped against SQL Server 16.0.1190.2 / compatibility 160. Ticket 01-04 key regressions are 16 passed, 0 failed, 0 skipped.
- Non-incremental Release solution build is green with 0 warnings and 0 errors.
- The complete test project was executed: 519 passed, 19 environment-gated skipped, and 2 unrelated failures. The WPF caption-drag failure passed when isolated; the telemetry retention failure is deterministic legacy test-clock drift (`utcNow` fixed at 2026-07-31 while the file timestamp uses the actual 2026-08-13 clock). A later parallel WPF package-stream race also passed when isolated.
- TDD caught and fixed two Ticket 04 regressions: a duplicate observation falsely cleared an existing field error, and closing an absent WorkType conflict made a stale `VISIBLE` Demand externally readable.
- Final two-axis review found 0 Spec issues and 0 documented-standard violations. Non-blocking follow-ups are to move pure conflict canonicalization/evaluation from the SQL adapter into Core and eventually share the repeated ticket gate harness.

## Requirement evidence

| Ticket acceptance | Automated evidence |
| --- | --- |
| duplicate one Series/Demand, complete multiset, no fabricated live set | `Duplicate_multiset_reorders_without_noise_changes_evidence_in_place_and_recovers_the_same_demand_after_restart`; `Exact_duplicate_observations_preserve_multiplicity_and_cannot_clear_a_field_error_without_unique_counterevidence` |
| duplicate error/readability and full API traceability | duplicate lifecycle tracer plus `Duplicate_key_and_multiple_work_type_conditions_coexist_with_complete_raw_assignments` |
| reorder no-noise; content/count evidence changes in same period | duplicate lifecycle tracer, including same-PollTrace canonical replay |
| unique recovery preserves identity/generation and ends period | duplicate lifecycle tracer and field-error counterevidence regression |
| independent per-WorkType Series/Demand and complete set evidence | `Multiple_work_types_create_independent_series_update_complete_membership_evidence_and_clear_the_still_visible_demand_after_restart` |
| recovery keeps keys and permanent histories while ending related conditions | multi-WorkType tracer closes the observed A condition; absent B/C remain blocked until Ticket 05 has authority to mark them `GONE` |
| real SQL/API plus Host restart | all four Ticket 04 tests run through production Host/API and real SQL; duplicate and multi-WorkType histories are compared across Host restart |
