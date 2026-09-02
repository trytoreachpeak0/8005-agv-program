# Ticket 07 test research

## Scope and confirmed seam

- Ticket: `.scratch/mes-ingest-bounded-storage-low-memory/issues/07-cut-over-external-catalog-reads.md`
- Confirmed production seam: scripted `MesTaskUnionRound` -> production projection/Host -> real SQL Server -> V2 HTTP -> reference consumer / Watch client.
- UI/XAML is out of scope; Tier 2 is not entered.
- Existing dirty changes are user-owned. Relevant pre-existing changes switch Catalog to `ReadCommitted` and rewrite one Current Attention evidence lookup; they must be integrated, not discarded.

## Existing coverage

- `ExternallyReadableDemandCatalogTests` covers central eligibility, exact revision changes, conditional reads, GONE/archived/long-gone exclusion, duplicates, field errors, and consumer canaries.
- `CurrentIngestAttentionTests` covers the four current sources, clearing semantics, exact facets/order, paging/filtering, and stable evidence.
- `WatchOverviewSnapshotTests` covers exact summaries, AREA scope, recent activity, and an old-or-new concurrent fence.
- `ProjectionCommitAtomicityConcurrencyTests` covers Catalog and Attention old-or-new reads at a commit boundary.
- `ScaleAndQueryEvidenceGateTests` and `Invoke-ScaleAndQueryEvidence.ps1` already enumerate Ticket 07 surfaces, but fail-closed raw-history/growth rules currently apply only to DemandSeries.

## Gaps mapped to Ticket 07

1. Catalog conditional identity is only `CatalogRevision`; an ETag from a different `HistoryEpoch` can incorrectly produce 304.
2. Catalog, Current Attention, and Overview production response identities do not all expose `HistoryEpoch`.
3. Current Attention still reconstructs active Series errors and TaskTypeProtection from history instead of maintained current rows.
4. Overview still invokes historical Browse/Readability/ErrorSearch readers for current summaries.
5. Attention and Overview select a fence under `ReadCommitted` without first acquiring the commit-round read fence lock.
6. The scale evidence gate has no Ticket 07-specific fail-closed no-growth/no-spill rules or representative-history baseline comparison.

## Platform and conventions

- SDK: .NET 8.0.424.
- Platform: VSTest (`Microsoft.NET.Test.Sdk` 17.6.0; no MTP signal).
- Framework: xUnit v2.
- Test project already references Core, Host, ReferenceConsumer, and Watch.
- SQL integration tests use `[Ticket01SqlServerFact]` and collection `Ticket01SqlServer`.

