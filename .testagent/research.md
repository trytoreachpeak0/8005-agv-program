# Production SQL WebApplicationFactory fixture remediation research

## Scope and authority

- Isolated worktree: `C:\Users\szy\.codex\worktrees\mesingest-sql-fixture-remediation` at detached commit `31e853fd918d50984ef8335451655e2e1fb1277e`.
- Failure evidence: `C:\Users\szy\AppData\Local\Temp\mesingest-full-real-sql-20260828.trx`.
- The full real-SQL run had 1016 tests, 931 passed, 85 failed, 0 skipped. The 85 failures are startup-policy failures in 23 test classes: 47 missing an explicit producer and 38 using a non-Oracle snapshot source.
- This task changes test fixtures and test-only support only. It must not change production code, weaken `ProductionHostStartupPolicy`, touch Watch/XAML, start a real Oracle poll, or modify the user's main checkout.
- `find-untested-sources` is not available in the installed tool/skill set. One bounded TRX-to-source inventory and `rg` pairing pass was used instead.

## Existing conventions

- `MesIngest.Tests` uses xUnit 2.4.2 through VSTest on `net8.0-windows`.
- Real SQL tests use `[Collection("Ticket01SqlServer")]`, `[Ticket01SqlServerFact]`, disposable `Ticket01SqlServerDatabase`, and process-scoped configuration.
- Production HTTP tests use `WebApplicationFactory<Program>` and `WithWebHostBuilder`; service replacement is performed with `ConfigureServices` or `ConfigureTestServices`.
- Test names are descriptive snake-case and assertions use direct xUnit APIs.
- `TestServiceCollectionExtensions.RemoveMesTaskUnionPollHostedService` already removes only the `IHostedService` descriptor whose implementation is `MesTaskUnionPollHostedService`.

## Bounded target inventory

| Source fixture | TRX failures | Required migration |
| --- | ---: | --- |
| `ArchivedDemandKeyTombstoneTests` | 2 | Production SQL test host + Oracle/continuous producer config. |
| `CurrentIngestAttentionTests` | 2 | Same; preserve test `TimeProvider`. |
| `DemandSeriesFrozenSnapshotTests` | 9 | Same. |
| `DuplicateKeyAndMultipleWorkTypesTests` | 4 | Replace `None` source and idle producer. |
| `ErrorSearchTests` | 5 | Production SQL test host + Oracle/continuous producer config. |
| `FrozenReadCommitConsistencyMatrixTests` | 1 | No independent fixture; delegates to `ProjectionCommitAtomicityConcurrencyTests`. |
| `HistoryCleanupSqlServerTests` | 3 | Apply seam to three inline factories; preserve cleanup hosted service and test clocks/operations. |
| `HistoryResetSqlServerTests` | 1 | Apply seam to inline factory. |
| `HistoryRetentionStateTests` | 4 | Apply seam; preserve clocks and read/commit observers. |
| `LiveMesFieldsAndErrorPeriodsTests` | 4 | Replace `None` source and idle producer. |
| `NewSuccessRoundTracerSpineTests` | 3 | Migrate only valid SQL environment; retain intentional non-Oracle rejection test. |
| `OracleMesTaskUnionProductionEntryTests` | 1 | Advertise continuous producer, suppress only hosted poll, retain fake executor and manual runner calls. |
| `PollTraceRawEvidenceCutoverTests` | 2 | Production SQL test host + Oracle/continuous producer config. |
| `ProjectionCommitAtomicityConcurrencyTests` | 5 | Replace `None` source and idle producer; also repairs delegated matrix test. |
| `ReadabilityAuditCutoverTests` | 3 | Replace `None` source and idle producer. |
| `ReadabilityAuditTests` | 4 | Production SQL test host + Oracle/continuous producer config. |
| `RestartBarrierGoneAndPrearchiveReappearanceTests` | 6 | Replace `None` source and idle producer. |
| `RoundEvidenceIdempotencyTests` | 5 | Replace `None` source and idle producer. |
| `StoragePressureSqlServerTests` | 1 | Apply seam to inline factory. |
| `TaskTypeProtectionTests` | 6 | Replace `None` source and idle producer. |
| `Ticket15RoundEvidenceTests` | 2 | Replace `None` source and idle producer. |
| `TwelveHourArchiveAndLongGoneVisibleTests` | 5 | Replace `None` source and idle producer. |
| `WatchOverviewSnapshotTests` | 7 | Production SQL test host + Oracle/continuous producer config; no Watch UI changes. |

## Constraints and hazards

- Production startup must see `SnapshotSource=Oracle` and an explicit producer. The fixtures will use `ContinuousPollEnabled=true` and keep `RunOneShotOnStartup=false`.
- A valid producer config would normally register and start `MesTaskUnionPollHostedService`; the test seam must remove exactly this one hosted service after application registration.
- Do not use `RemoveAll<IHostedService>()`: `NewMesIngestHostSessionService`, `HistoryCleanupHostedService`, and any other hosted services remain part of the integration contract.
- `NewSuccessRoundTracerSpineTests.Production_V2_rejects_a_non_Oracle_snapshot_source_before_starting_an_idle_host` intentionally supplies `SnapshotSource=None`; its invalid configuration must remain unchanged.
- `OracleMesTaskUnionProductionEntryTests.Canonical_Oracle_result_flows_through_Production_V2_runner_to_poll_trace_and_non_success_never_mutates_business_state` must retain its fake `IOracleStatementExecutor` and exactly three manual runner requests; a background poll would corrupt this assertion.
- Environment settings are process-global. Existing `Ticket01SqlServer` collection serialization and process environment scopes must remain in place.
- `NewSuccessRoundTracerSpineTests` and `RoundEvidenceIdempotencyTests` use fixed 2026-08-12 evidence but previously inherited wall-clock time. Once the real cleanup hosted service could start, those fixtures became date-dependent and expired their own evidence. Their factories require a fixture-aligned `TimeProvider` while retaining the cleanup service.

## Acceptance checklist

- [x] All positive Production SQL WebApplicationFactory fixtures use one shared builder seam.
- [x] Positive environments publish `SnapshotSource=Oracle`, `ContinuousPollEnabled=true`, and `RunOneShotOnStartup=false`.
- [x] The seam removes only `MesTaskUnionPollHostedService`.
- [x] `NewMesIngestHostSessionService` and `HistoryCleanupHostedService` descriptors are preserved.
- [x] The intentional non-Oracle startup-policy test remains invalid and unchanged in purpose.
- [x] The fake-Oracle production-entry test remains manual and cannot receive a background poll.
- [x] No production or Watch/UI file changes.
- [x] Test project builds and a narrow, clean representative run passes.
- [x] The complete SQL-only gate passes without competing non-SQL collections, and standard Tier 1 remains green.
