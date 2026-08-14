# Ticket 16 TDD plan and requirement evidence

## Red-green vertical slices

1. Add a no-op production commit-boundary observer with stable checkpoint names;
   fail the first real-SQL test at early, middle and late checkpoints, then prove
   rollback through formal HTTP before and after Host restart.
2. Extend the failure slice with retry, equal replay, conflict and cancellation;
   assert exactly one observable commit and unchanged prior snapshot.
3. Run a bounded concurrent writer burst through one production Host and assert
   serialized ProjectionSequence, SeriesSequence, generation, catalog revision,
   RestartBarrier and TaskTypeProtection outcomes.
4. Add shared read-fence observation for DemandSeries, catalog and attention;
   pause each after fence selection, commit a new round, and prove old/new whole
   snapshots through HTTP.
5. Drive the combined unique/conflict/lifecycle/protection/attention scenario,
   restart the Host, and compare the public snapshots.
6. Add the strict Ticket 16 PowerShell gate and machine-readable/Markdown report;
   enforce server version/compatibility, checkpoint coverage, concurrency scale,
   retry assertions, exact pass count and zero skips.
7. Run focused tests, dependency regression, Release solution build, full suite,
   independent Standards/Spec review, then fix findings and re-run. Complete:
   both reviews closed and the final strict SQL gate passed 5/5 with zero skips.

## Requirement mapping

| Checklist | Planned public-seam evidence |
| --- | --- |
| 1, 2 | `Six_SQL_failpoints_roll_back_every_public_surface_then_retry_replay_and_conflict_are_atomic` |
| 3, 4 | `Concurrent_writers_form_one_monotonic_sequence_one_generation_and_one_catalog_revision_per_round` |
| 5 | `Demand_catalog_and_attention_reads_are_wholly_old_or_new_at_a_concurrent_commit_fence` |
| 6 | `Failure_incomplete_and_mid_transaction_cancellation_preserve_business_projection_and_open_error_periods` plus the SQL-failpoint test |
| 7 | `Combined_projection_covers_conflicts_lifecycle_protection_attention_and_is_identical_after_restart` |
| 8 | strict `Invoke-Ticket16SqlServerGate.ps1` plus generated gate report |
