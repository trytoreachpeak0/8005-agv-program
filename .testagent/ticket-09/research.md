# Ticket 09 test research

## Scope and confirmed seams

- Ticket: `.scratch/mes-ingest-bounded-storage-low-memory/issues/09-cut-over-readability-audit-reads.md`.
- Confirmed production seam: scripted `MesTaskUnionRound` -> production `RoundIngestor` / Host -> real SQL Server -> `/api/v2/readability-audit` list and detail.
- Confirmed concurrency seam: the production `IProjectionReadBoundaryObserver` introduced by Tickets 06/07. Ticket 09 must extend that existing boundary to ReadabilityAudit; no private method, SQL-text, or test-only production seam is introduced.
- Current and frozen reads are different physical paths under ADR-mes-0026. Frozen list, facets, count, paging, and detail share `HistoryEpoch` plus `ProjectionCommit` under ADR-mes-0016/0027.
- UI/XAML and Tier 2/3 are out of scope.
- The working tree is dirty and user-owned. In particular, the two pre-existing `Serializable` -> `ReadCommitted` edits in `SqlServerMesIngestProjection.ReadabilityAudit.cs` are preserved and production code is not edited by this test task.

## Platform and conventions

- SDK: .NET 8.0.424 (`global.json` requests 8.0.423 with latest-patch roll-forward).
- Platform: VSTest; neither `global.json` nor project/Directory props enable Microsoft.Testing.Platform.
- Framework: xUnit v2 (`xunit` 2.4.2 and `Microsoft.NET.Test.Sdk` 17.6.0).
- SQL integration convention: `[Ticket01SqlServerFact]` plus collection `Ticket01SqlServer`; every SQL assertion also proves non-LocalDB product and compatibility metadata.
- Narrow command shape: `dotnet test MesIngest.Tests --filter "FullyQualifiedName~<Ticket09Class>"` from `mes/ingest/csharp`.
- The code-testing-agent package does not contain an executable `find-untested-sources`; target pairing was therefore performed once from the requested test inventory and `rg` symbol references.

## Existing coverage and proven seams

- `ReadabilityAuditTests` already covers blocker completeness, filter normalization, stable order and bounded paging, facets, exact count, detail payload, old snapshot replay, and token tampering. Its old-snapshot test commits the writer before replaying the snapshot, so it does not prove a read at a live commit boundary.
- `ProjectionCommitAtomicityConcurrencyTests` proves DemandSeries, Catalog, and CurrentIngestAttention are wholly old-or-new by gating the existing `IProjectionReadBoundaryObserver`. `ProjectionReadSurface` currently has no ReadabilityAudit value and the ReadabilityAudit reader does not notify the observer.
- `ScaleAndQueryEvidenceGateTests` enumerates ReadabilityAudit as a query surface, but its fail-closed no-history-growth/resource regression theory currently covers only DemandSeries and Ticket 07 surfaces.
- Ticket 06 established `HistoryEpoch`-bound snapshot/cursor identities and a current read that remains available while `DemandRawObservations` is locked.
- Ticket 07 established the commit-round shared read fence followed by `IProjectionReadBoundaryObserver` notification for current production surfaces.

## Production gaps observed before writing tests

- `ReadabilityAuditSnapshotIdentity` has `ProjectionCommitId`, sequence, commit time, PollTrace, and CatalogRevision, but no `HistoryEpoch`; the Host DTO therefore cannot expose it and tokens cannot bind it.
- `ListReadabilityAuditAsync` and `GetReadabilityAuditDetailAsync` use the user-owned `ReadCommitted` edits but do not notify `IProjectionReadBoundaryObserver` or establish another observable commit-consistent frozen-read mechanism. Unlike Ticket 07 current reads, Ticket 09 frozen reads must not hold the writer behind the observer gate.
- The list SQL reconstructs latest fields and blockers from `DemandRawObservations`, `DemandSeriesEvents`, and other historical tables, so a current list request blocks behind an exclusive raw-history table lock.
- The list/detail transaction is multi-statement `ReadCommitted`, which is not a commit-consistent frozen view under ADR-mes-0027.

## Acceptance checklist

1. "当前资格结论从当前 Demand、Series、条件和资格投影读取，不通过完整历史重算。"
2. "冻结列表、精确总数、原因分面、稳定分页与详情绑定同一 HistoryEpoch 和 ProjectionCommit。"
3. "详情保持完整 ReadabilityBlocker 集合、可信字段或冲突证据、Series、PollTrace 与 CatalogRevision。"
4. "snapshot/cursor 跨纪元、提交、筛选、AREA、顺序或页大小复用时被明确拒绝。"
5. "并发投影不能让列表结论与详情理由来自不同提交。"
6. "0、7、30 天真实 SQL Server 门禁证明当前逻辑读有界，全部 SQL 测试实际运行。"

## First red-slice inventory

- `Current_audit_list_does_not_wait_for_raw_history`: lock `DemandRawObservations` with `TABLOCKX, HOLDLOCK`, then request the latest production V2 audit page and assert the current conclusion still returns. Current code is expected to time out because it reads raw history.
- `Audit_snapshot_exposes_the_database_history_epoch`: ingest through the production Host and assert the V2 snapshot exposes the exact `SchemaInfo.HistoryEpoch`. Current DTO is expected to omit the field.
- `Audit_list_and_detail_are_wholly_old_or_new_at_a_concurrent_commit_fence`: gate the already-approved read-boundary observer, let a commit that changes the blocker without changing catalog revision finish before releasing the frozen readers, then assert the in-flight list and detail remain at the old commit. Current code is expected to fail because ReadabilityAudit has no observer surface/notification; an implementation that blocks the writer will also fail.
