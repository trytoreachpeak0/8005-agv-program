# Tickets 13–14 test research — current attention and atomic Watch overview

## Scope and confirmed seams

Primary ticket: `.scratch/new-mes-ingest/issues/14-consistent-watch-overview-snapshot.md`.
Ticket 14 has a hard dependency on ticket 13, whose production read seam is absent,
so this change also supplies `.scratch/new-mes-ingest/issues/13-current-ingest-attention-read.md`.

The specification already confirms the end-to-end seam:

1. Scripted `MesTaskUnionRound` -> production `RoundIngestor` -> real SQL Server.
2. `GET /api/v2/current-ingest-attention` for the bounded current union.
3. `GET /api/v2/watch-overview?area=...` for one atomic Host snapshot.

Tests use the public Host routes and `IMesIngestProjection.CommitRoundAsync`; they do
not invoke private SQL/read helpers. `AdjustableTimeProvider` controls the 7-day and
24-hour boundaries. `[Ticket01SqlServerFact]` supplies the existing disposable real
SQL Server gate. Neither ticket changes Watch/XAML, so golden WPF validation does not apply.

## Snapshot and transition policy

- Every overview selects one immutable ProjectionCommit fence and one append-only
  attention-event high-water in a single read transaction.
- Projection-derived facts are reconstructed at the selected ProjectionSequence;
  failed/incomplete polls are fenced by the attention high-water because they do not
  create ProjectionCommits.
- A production no-op/read-observer boundary is replaceable in integration tests so a
  reader can pause immediately after selecting fence A, commit B normally, then prove
  the first response is wholly A and the refresh wholly B.
- Current Series attention directly uses `SeriesId + ErrorCode + Target + SubjectKind`.
  No issue/fingerprint/revision/occurrence lifecycle is introduced.
- Poll, task-protection, and unassigned transitions are append-only and replay-safe;
  unchanged observations do not manufacture overview activity.
- AREA is trimmed, ordinal, case-sensitive, de-duplicated input and scopes only Series
  and Readability. Errors and current attention remain global.
- Dynamics use the half-open `[snapshotAsOf - 24h, snapshotAsOf)` window, take five,
  and order by `OccurredAt DESC, EventId ASC`.
- V2 routes remain excluded from legacy V1 OpenAPI until ticket 17 freezes that contract.

## Framework and commands

- .NET SDK 10.0.302, xUnit 2.4.2, VSTest.
- Focused syntax: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~CurrentIngestAttentionTests|FullyQualifiedName~WatchOverviewSnapshotTests"`.
- Release evidence requires `MES_INGEST_TICKET01_SQLSERVER`, SQL Server product major 16,
  and compatibility level 160.
