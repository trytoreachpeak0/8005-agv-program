# Production SQL WebApplicationFactory fixture remediation status

## Progress

- Research complete: parsed 85 failures / 23 classes from the supplied TRX and paired them to 22 fixture source files.
- Plan complete: shared builder seam, precise hosted-service removal test, two migration phases, special-case preservation, and narrow validation are mapped.
- Implementation complete: all 22 source fixtures use `UseProductionSqlApiTestHost`; the delegated `FrozenReadCommitConsistencyMatrixTests` path is covered by the migrated `ProjectionCommitAtomicityConcurrencyTests` factory.
- All positive environments now use `SnapshotSource=Oracle`, `ContinuousPollEnabled=true`, and `RunOneShotOnStartup=false`.
- The intentional non-Oracle startup-policy test remains `SnapshotSource=None` and still passes.
- No production, Watch, XAML, or UI file was changed.

## Validation

- `dotnet build MesIngest.Tests`: succeeded, 0 warnings, 0 errors.
- Generated seam test: 1 passed, 0 failed, 0 skipped.
- Final representative VSTest filter: 5 passed, 0 failed, 0 skipped in 17 seconds. It included the generated seam test, one former producer-missing SQL fixture, one former non-Oracle SQL fixture, the fake Oracle manual-runner fixture, and the intentional non-Oracle rejection test.
- SQL Server was real local SQL Server 16 / compatibility 160. No `MesIngest_Ticket01_%` database remained after the run.
- The complete real-SQL suite was not run in this subtask.
- Parent validation first ran all 30 SQL-attributed classes and found 8 date-dependent cleanup failures in two fixtures. `NewSuccessRoundTracerSpineTests` and `RoundEvidenceIdempotencyTests` now inject a 2026-08-12 fixture clock while preserving `HistoryCleanupHostedService`; the focused rerun passed 9/9.
- Final SQL-only gate: 193 passed, 0 failed, 0 skipped in 11m 34s.
- Final standard Tier 1: 876 passed, 0 failed, 137 SQL-gated skips in 4m 18s.
- Post-run SQL state: max server memory 1536 MB and zero `MesIngest_Ticket01_%` databases. Host service remained stopped and port 5088 remained released.

## Review

- `test-gap-analysis` pseudo-mutation 1 broadened removal to every `IHostedService`; the generated seam test failed because the two preserved descriptors disappeared. Mutation restored.
- `test-gap-analysis` pseudo-mutation 2 removed builder-level `ConfigureTestServices`; the fake Oracle integration test failed because the background poll consumed a scripted executor step. Mutation restored.
- Mutation result: 2 injected, 2 killed, 0 surviving verified gaps; final clean representative run passed.
- Assertion-quality review: the generated test asserts exact ordered remaining implementation types and explicit poll absence; the fake Oracle test asserts exact outcomes and exactly three executor requests, so it detects background polling rather than merely successful Host startup.
- `assertion-quality` is not available in the installed skill set; the equivalent assertion review was performed inline.
