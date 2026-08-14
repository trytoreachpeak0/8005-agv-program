# Ticket 16 test research — ProjectionCommit atomicity/concurrency gate

## Bounded target inventory

- Public write seam: `RoundIngestor.IngestAsync` ->
  `IMesIngestProjection.CommitRoundAsync` -> production
  `SqlServerMesIngestProjection`.
- Public read seam: production V2 HTTP routes for DemandSeries, catalog,
  CurrentIngestAttention, overview and PollTrace.
- Storage: one SQL Server `SERIALIZABLE` transaction and transaction-owned
  `sp_getapplock` already serialize each accepted round. Schema uniqueness covers
  PollTrace, ProjectionCommit sequence, TransportDemandKey, generation and
  SeriesSequence.
- Existing test infrastructure: `Ticket01SqlServerDatabase` rejects LocalDB,
  verifies product/compatibility, and creates only disposable
  `MesIngest_Ticket01_<guid>` databases. The local SQL Server 2022 probe passed.
- Existing consistency proof covers overview only; there is no production write
  checkpoint seam and no deterministic DemandSeries/catalog/attention read gate.

## Explicit acceptance checklist

1. Multiple write checkpoints fail inside the real SQL transaction without
   leaking PollTrace, commit, Series, Demand, events, conditions, error periods,
   protection, attention, catalog body or revision through HTTP or after restart.
2. Retry after failure creates one commit; equal replay is inert; conflicting
   replay is rejected without changing committed state.
3. Concurrent rounds serialize, do not compete for generations, and cannot
   bypass RestartBarrier or TaskTypeProtection.
4. ProjectionSequence, SeriesSequence and CatalogRevision stay unique and
   monotonic across concurrency/restart; one round advances the catalog at most
   once and unchanged rounds do not advance it.
5. DemandSeries, catalog and CurrentIngestAttention concurrent reads are each
   wholly old or wholly new at a committed fence.
6. FAILURE, INCOMPLETE, cancellation and SQL exceptions do not advance business
   projection, close conditions, or publish a catalog revision; allowed technical
   PollTrace evidence remains isolated.
7. A combined real-SQL round set covers unique, duplicate, multi-WorkType, GONE,
   archive, LongGoneButVisible, TaskTypeProtection, active errors and attention,
   with the same formal reads after Host restart.
8. The gate report records server product/version, compatibility, checkpoints,
   concurrency scale, retries and observable assertions; LocalDB/in-memory is
   explicitly insufficient.

## Conventions and execution

- .NET SDK 10.0.302, xUnit 2.4.2, VSTest.
- Tests use production `WebApplicationFactory<Program>`, `RoundIngestor`, and V2
  HTTP responses; direct SQL is limited to real-engine fault setup/metadata, not
  business-result assertions.
- Focused command: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj -c Release
  --filter FullyQualifiedName~ProjectionCommitAtomicityConcurrencyTests`.
- Formal gate requires explicit non-LocalDB SQL Server product major 16,
  compatibility 160, and exactly zero skipped tests.
