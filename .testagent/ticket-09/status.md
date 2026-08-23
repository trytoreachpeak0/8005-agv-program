# Ticket 09 test status

## First red batch

Command (from `mes/ingest/csharp`, VSTest + xUnit v2):

```text
dotnet test MesIngest.Tests --filter "FullyQualifiedName~ReadabilityAuditCutoverTests" -v minimal
```

The first environment-less run compiled but correctly skipped all three SQL facts because the three Ticket 01 SQL variables were absent. A second run used the local real `MSSQLSERVER` instance through Windows integrated authentication after a read-only check proved SQL Server major 16, compatibility 160, and sysadmin capability. Result:

```text
Failed: 3, Passed: 0, Skipped: 0, Total: 3
```

| Test | Red reason |
| --- | --- |
| `Current_audit_list_does_not_wait_for_raw_history` | The latest V2 audit page blocked on `DemandRawObservations WITH (TABLOCKX, HOLDLOCK)` and cancellation surfaced from `ReadAuditPageAsync`, proving the current path still reads raw history. |
| `Audit_snapshot_exposes_the_database_history_epoch` | The V2 snapshot has no `historyEpoch`; `JsonElement.GetProperty("historyEpoch")` failed. |
| `Audit_list_and_detail_are_wholly_old_or_new_at_a_concurrent_commit_fence` | `ProjectionReadSurface` has no `ReadabilityAudit` value, so the approved observer seam cannot yet gate the frozen list/detail boundary. The green expectation additionally requires commit B to finish before the gate is released, proving the frozen readers do not block projection writes. |

After correcting the concurrency expectation to the ADR-mes-0027 nonblocking behavior, a rerun was attempted. The shared working tree was then mid-implementation: `ReadabilityAuditSnapshotIdentity` had gained a `HistoryEpoch` constructor argument while the SQL projection and Watch DTO call sites had not yet been updated, so the build stopped in those production files. No production file was changed by this test task. The original three-test real-SQL red run above remains the pre-implementation baseline; the corrected nonblocking branch must be executed when the parent implementation compiles.

## Gap and assertion review

- Static pseudo-mutation review only: a green baseline is intentionally unavailable during the red phase, so no production mutations were applied.
- Removing all raw-history access from the current route is necessary but not sufficient: the first test also asserts exact total, readability conclusion, blockers, and trusted current fields at the selected commit.
- Returning a constant or unrelated epoch is caught because the expected value is read independently from `SchemaInfo`.
- Merely adding the enum is insufficient: the concurrency test requires two observer notifications with the exact commit, sequence, HistoryEpoch, and CatalogRevision; it also requires the writer to complete while both readers are gated and checks list/detail blockers after release.
- Known planned gaps remain explicit in `plan.md`: cross-epoch token/cursor negatives require the production identity to gain `HistoryEpoch`; 0/7/30 logic-read and fail-closed scale evidence belongs to the later scale slice.
- `assertion-quality` is not available in this session. Assertions were re-read manually against the public Host/real-SQL seam; no tautological expected values or private implementation assertions were added.

## Green implementation and empirical gap review

The completed implementation was exercised through the public Host against SQL Server 16 / compatibility 160. The focused ReadabilityAudit run completed with `Failed: 0, Passed: 19, Skipped: 0`; it includes the original audit suite, the new cut-over tests, and Watch query/presentation coverage.

Three high-risk pseudo-mutations were then applied one at a time and immediately reverted:

| Mutation | Covering test | Observed result |
| --- | --- | --- |
| Remove `HistoryEpoch` from cursor identity comparison. | `Audit_tokens_bind_snapshot_filters_area_order_contract_and_reject_tampering_or_reuse` | Killed: expected rejection became acceptance. |
| Disable the database `HistoryEpoch` mismatch guard for a signed snapshot. | `Audit_snapshot_exposes_the_database_history_epoch` | Killed: expected `400 SnapshotMismatch` became `410 SnapshotNotFound`. |
| Route the latest request through the historical query instead of the current read model. | `Current_audit_list_does_not_wait_for_raw_history` | Killed: the request blocked behind `DemandRawObservations (TABLOCKX, HOLDLOCK)` and was cancelled. |

Result for the scoped high-risk mutation set: **3 killed, 0 survived, 0 no-coverage, 0 equivalent**. A subsequent Release solution build completed with 0 warnings / 0 errors, confirming every mutation was reverted. Remaining full-suite and 0/7/30 scale evidence is recorded after the implementation commit so attestation hashes bind the exact Host assembly.
