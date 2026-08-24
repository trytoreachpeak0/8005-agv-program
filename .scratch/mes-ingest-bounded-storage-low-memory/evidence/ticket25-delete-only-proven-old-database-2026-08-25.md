# Ticket 25 — exact old database deletion evidence

Date: 2026-08-25

Scope: `.scratch/mes-ingest-bounded-storage-low-memory/issues/25-delete-only-proven-old-database.md` only. Ticket 24 remains `wontfix`; ticket 26 and later tickets were not implemented.

## Implementation boundary

- The automatic deletion capability is reachable only from `pack/cutover/Invoke-MesIngestCutoverRun.ps1` for one validated `CutoverRunId`.
- Host, Watch, reference consumer, install, and uninstall contain neither the deletion helper call nor `DROP DATABASE`.
- The run writes immutable `<RunId>.pre-delete.json/.md` and a complete Windows Application event before elevation.
- The destructive helper independently revalidates the raw same-run gate set, stopped old Host, old/new identity, exact schema/contract, HistoryEpoch, resolved data directory, tombstone count/hash/algorithms, new-database exclusion, and global old-database session state both before and after elevation.
- The run-scoped SQL login is disabled and denied `CONNECT SQL` before it receives `VIEW SERVER STATE`, `VIEW SERVER PERFORMANCE STATE`, and `CONTROL` on only the exact old database. Its impersonated session is closed and the exact login/user is removed and verified absent in every handled exit path. Cleanup has three synchronous attempts; deletion itself is never retried.
- The Ticket 25 drop command checks sessions and executes exact `DROP DATABASE` without `SINGLE_USER` or `ROLLBACK IMMEDIATE`, so a racing business connection causes failure and preservation.
- Evidence states `IsDatabaseBackup=false` and `HasRollbackPath=false`.

## Real SQL Server deletion paths

Server gate: local default SQL Server product major 16, database compatibility 160, not LocalDB.

1. Success path, `One_time_permission_deletes_only_the_revalidated_isolated_old_database_and_is_revoked`:
   - deleted old database: `MesIngest_Ticket01_fc5b7b2e07764dc7aeaaaaba3bb29532`
   - preserved new database: `MesIngest_Ticket01_585d20da22b848149cbba6c4bcd52ff3`
   - permission result: `REVOKED_AND_PRINCIPAL_DROPPED`, `VerifiedAbsent=true`
2. Deliberate drop-failure path, `Failed_drop_preserves_both_isolated_databases_and_revokes_the_one_time_permission`:
   - preserved old database: `MesIngest_Ticket01_9bbd49ab71b04886b0587819fff4ff42`
   - preserved new database: `MesIngest_Ticket01_77cbaa464bd14b92b757b26a7a9de04d`
   - failure mechanism: server DDL trigger matched only the exact old database and raised `MESINGEST_TICKET25_EXPECTED_DROP_FAILURE`
   - permission result: `REVOKED_AND_PRINCIPAL_DROPPED`, `VerifiedAbsent=true`, no revocation failure

No production database was connected to or deleted. All four names were created by `Ticket01SqlServerDatabase` on the explicit local test instance and disposed after assertion.

## Windows event evidence

`Write-CutoverWindowsEvent` was written and read back from the Windows Application log with:

- source: `Application`
- event id: `2300`
- validation RunId: `25252525-2525-4525-8525-252525252525`
- status: `TICKET25_VALIDATION_ONLY`
- database deletion: `VALIDATION_ONLY_NO_DATABASE_OPERATION`
- permission status: `NOT_GRANTED`
- generated at: `2026-08-25T03:19:49+08:00`

This validation event exercised the complete event schema without connecting to or deleting a database. Production cutover success/failure events are emitted by the same function with the actual server, old/new identities, HistoryEpoch, contract/schema, projection, interface gates, execution identity, timestamps, deletion result, and permission result.

## Test results

- Focused cutover and packaged-release validation: 15 passed / 0 failed / 0 skipped.
- Final Tier 1: `dotnet test MesIngest.Tests`
  - Passed: 878
  - Failed: 0
  - Skipped: 0
  - Duration: 10m58s
  - Environment: SQL Server 16 / compatibility 160 / non-LocalDB
- Tier 2/3: not run because Ticket 25 does not modify Watch UI, XAML, layout, UI Automation, DPI behavior, or visual baselines.

## Review

- Standards axis: Pass after deterministic ambiguous-creation cleanup, raw destructive revalidation, and release-package boundary fixes.
- Spec axis: Pass after post-elevation full identity/proof/session revalidation, non-forcing session-safe drop, disabled run login, complete event fields/order, and expanded dry-run rejection matrix.

## Human follow-up

- Review and approve this irreversible cutover mechanism before using it at the factory.
- A real factory cutover was intentionally not run. The operator must supply the explicit production old/new database names, resolved SQL data directory, stopped service, expected versions/HistoryEpoch, one-time privileged broker connection, and a new CutoverRunId during the approved maintenance window.
- There is no backup or rollback path after a successful production deletion; subsequent fixes are forward-only on the new database and contract.
