# Ticket 02 test status

## Requirement evidence

| Requirement | Test/evidence |
| --- | --- |
| Deterministic 0/7/30 distributions | `Packaged_scale_gate_declares_every_ticket_02_evidence_surface`; final real 0-day smoke manifest; 7/30 counts are deterministic profile calculations. |
| Explicit isolated target and owned cleanup | `Scale_gate_rejects_a_system_database_before_opening_sql`; final smoke left zero `MesIngest_Scale_*` databases and zero owned XEL files. |
| Seven query surfaces with plans/IO/time/grants/spill/latency | `Packaged_scale_gate_declares_every_ticket_02_evidence_surface`; final smoke has per-surface statement/plan counts and metrics. |
| Sparse actual-plan runtime counters remain collectable | `ShowPlan_validator_treats_missing_runtime_counter_attributes_as_zero_without_sql`; absent optional counters become zero while present logical reads remain intact. |
| Physical/logical storage breakdown | `Packaged_scale_gate_declares_every_ticket_02_evidence_surface`; final smoke has 2 physical files and 35 allocations. |
| Replay/build/contract/SQL identity | `Packaged_scale_gate_declares_every_ticket_02_evidence_surface`; final smoke records Host SHA-256, source dirty state, configuration, max memory, compatibility and recovery. |
| Missing plan, empty data or skipped SQL cannot pass | `Evidence_validator_rejects_a_missing_query_surface_plan_without_sql`; shared `Get-EvidenceGateFailures` is used by both fixture and production runs. |

## Gap and assertion review

- Baseline focused run: 3 passed / 0 failed / 0 skipped.
- Pseudo-mutation 1 changed the unsafe-database OR guard to AND. `Scale_gate_rejects_a_system_database_before_opening_sql` failed; mutation killed and reverted.
- Pseudo-mutation 2 disabled the incomplete-query-surface branch. It initially survived, so `Evidence_validator_rejects_a_missing_query_surface_plan_without_sql` was added. Reapplying the same mutation then failed that test; mutation killed and reverted.
- Final focused run after every revert: 3 passed / 0 failed / 0 skipped.
- Assertion review: the safety test observes exit code, pre-connect diagnostic, credential non-disclosure and absence of output; the fixture test observes exit code, exact missing-surface identity and proof that SQL configuration was not read. The static packaging test remains intentionally broad because package inclusion and evidence vocabulary are deployment contracts; behavior-critical guards have separate process tests.
- No remaining verified high-risk survivor. `assertion-quality` was unavailable; assertions were re-read manually against the script and final real-SQL report.
- Post-review focused run: 7 passed / 0 failed / 0 skipped. Tail percentiles now use nearest-rank; Tier 1 schema 2 binds the TRX and current Host build.
- Final smoke feedback exposed a real ShowPlan operator without `ActualScans`. The new sparse-counter regression was red on the missing fixture seam, then green after optional XML attributes were parsed safely; the full scale-gate class finished 5 passed / 0 failed / 0 skipped.

## Real SQL smoke

- Run: `mes/ingest/csharp/.artifacts/ticket02-scale-smoke/scale-20260823T080914Z-94ad296e/`.
- Gate: passed; 600 raw observations / 600 Series.
- Query evidence: 7 surfaces, 37 measured statements, 419 actual plans, zero spills.
- Storage: 2 physical files, 35 allocations (19 clustered, 16 nonclustered).
- SQL configuration: max server memory 1536 MB, compatibility 160, SIMPLE recovery.
- Tier 1 attestation consumed: Failed 0 / Passed 725 / Skipped 0 / Total 725.
- Cleanup: zero owned XEL files, zero `MesIngest_Scale_*` databases.
- Final current-source real SQL Tier 1: `mes/ingest/csharp/.artifacts/ticket02-tier1/run-20260823T081251Z/`, Failed 0 / Passed 728 / Skipped 0 / Total 728 (7m38s).
