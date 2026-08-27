# Production SQL WebApplicationFactory fixture remediation plan

## Phase 1: Freeze the test-only seam

1. Extend `TestServiceCollectionExtensions` with `UseProductionSqlApiTestHost(IWebHostBuilder)`.
2. The helper sets the WebApplicationFactory environment to Production and uses `ConfigureTestServices` to call the existing precise `RemoveMesTaskUnionPollHostedService` removal.
3. Add `TestServiceCollectionExtensionsTests.RemoveMesTaskUnionPollHostedService_removes_only_the_poll_loop_and_preserves_other_hosted_services`.
4. Assert the remaining descriptors include `NewMesIngestHostSessionService` and `HistoryCleanupHostedService`, while the poll descriptor alone is absent.

## Phase 2: Migrate the producer-missing fixtures

Apply the shared builder seam and add the valid Oracle/continuous producer settings to:

- `ArchivedDemandKeyTombstoneTests`
- `CurrentIngestAttentionTests`
- `DemandSeriesFrozenSnapshotTests`
- `ErrorSearchTests`
- `HistoryResetSqlServerTests`
- `HistoryRetentionStateTests`
- `PollTraceRawEvidenceCutoverTests`
- `ReadabilityAuditTests`
- `StoragePressureSqlServerTests`
- `WatchOverviewSnapshotTests`

Apply the same shared builder seam to `HistoryCleanupSqlServerTests` at each of its three inline factories. Its environment also changes from `None`/idle to Oracle/continuous.

## Phase 3: Migrate the non-Oracle fixtures

Replace only each valid `ConfigureProductionV2Environment` source/producer pair and apply the shared builder seam in:

- `DuplicateKeyAndMultipleWorkTypesTests`
- `LiveMesFieldsAndErrorPeriodsTests`
- `NewSuccessRoundTracerSpineTests`
- `ProjectionCommitAtomicityConcurrencyTests` (also covers `FrozenReadCommitConsistencyMatrixTests`)
- `ReadabilityAuditCutoverTests`
- `RestartBarrierGoneAndPrearchiveReappearanceTests`
- `RoundEvidenceIdempotencyTests`
- `TaskTypeProtectionTests`
- `Ticket15RoundEvidenceTests`
- `TwelveHourArchiveAndLongGoneVisibleTests`

Leave `NewSuccessRoundTracerSpineTests.Production_V2_rejects_a_non_Oracle_snapshot_source_before_starting_an_idle_host` configured with `SnapshotSource=None` and continuous producer enabled so it still tests the intended policy branch.

## Phase 4: Preserve the fake Oracle runner case

For `OracleMesTaskUnionProductionEntryTests`:

- set `ContinuousPollEnabled=true` so Production startup is valid;
- use the shared builder seam to prevent the hosted poll;
- retain the fake executor registration and manual `MesTaskUnionPollRunner.RunOnceAsync` calls;
- use its exact-three-request assertion as integration evidence that no background Oracle poll ran.

## Phase 5: Verification

1. Static audit all 22 fixture source files: no positive `SnapshotSource=None`, no positive `ContinuousPollEnabled=false`, and no direct Production builder call outside the intentional negative path.
2. Build `MesIngest.Tests`.
3. Run the helper unit test plus the narrow real-SQL representatives selected by the parent: one `None`-source migration, one producer-missing migration, and the fake Oracle manual-runner test. Do not run the complete real-SQL suite in this subtask.
4. Re-open the helper/test assertions and perform test-gap/assertion-quality review. Record results in `.testagent/status.md`.
5. Diff audit: only `MesIngest.Tests` and `.testagent` may change; no production/Watch/XAML files.

## Phase 6: Stabilize fixed historical evidence

1. Run every SQL-attributed class without unrelated collections competing for local memory.
2. If the retained cleanup service expires fixed fixture evidence, inject a fixture-aligned `TimeProvider` in only the affected factories.
3. Re-run the affected classes, then the complete SQL-only gate.
4. Run standard Tier 1 with the SQL gate disabled so the two green runs cover the complete suite without resource contention.

## Requirement mapping

| Requirement | Planned evidence |
| --- | --- |
| `修复完整真实 SQL 测试运行中 23 个 Production WebApplicationFactory 测试类的夹具` | TRX inventory plus migrated 22 fixture sources; delegated matrix class maps to `ProjectionCommitAtomicityConcurrencyTests`. |
| `使它们满足 ProductionHostStartupPolicy（SnapshotSource=Oracle 且有显式 producer）` | Static settings audit and clean representative Production factory startup tests. |
| `但测试中不得真实访问 Oracle` | Shared builder seam plus fake Oracle production-entry test's exact three manual executor requests. |
| `精准移除 MesTaskUnionPollHostedService` | `RemoveMesTaskUnionPollHostedService_removes_only_the_poll_loop_and_preserves_other_hosted_services`. |
| `保留 NewMesIngestHostSessionService、HistoryCleanupHostedService 等其他托管服务` | Same generated unit test asserts both exact descriptors remain. |
| `复用/完善现有 TestServiceCollectionExtensions` | `TestServiceCollectionExtensions.UseProductionSqlApiTestHost`. |
| `避免修改生产代码或弱化启动策略` | Final path diff audit; policy source untouched. |
| `不要运行完整真实 SQL 套件；可以运行构建或极窄的代表性测试` | Validation log in `.testagent/status.md`. |
| `不要提交` | Final `git status` shows uncommitted worktree changes. |
