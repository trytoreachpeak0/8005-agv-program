# Ticket 12 test research — frozen error detail and bounded raw evidence

## Scope and confirmed seams

Ticket: `.scratch/new-mes-ingest/issues/12-error-detail-bounded-raw-evidence.md`.

The accepted production seams are:

1. Scripted `MesTaskUnionRound` -> production `RoundIngestor` -> real SQL Server.
2. `GET /api/v2/error-search/{seriesId}?snapshot=...` for frozen matched detail.
3. `GET /api/v2/error-search/{seriesId}/evidence/{evidenceId}/raw-observations?...` for explicitly authorized, bounded raw expansion.

Tests do not call private projection helpers, SQL, or token codecs directly. Time is controlled with `AdjustableTimeProvider`. Real-SQL tests use `[Ticket01SqlServerFact]` and reject LocalDB as release evidence.

Ticket 12 does not change Watch/XAML/UI Automation/DPI/visual baselines, so the golden WPF renderer rules do not apply.

## Frozen public policy

- Detail and raw reads accept only Ticket 11's signed error-search snapshot; callers do not resubmit filters or windows.
- Raw expansion requires the configured `MesIngest:SharedSecret` as `Authorization: Bearer ...`, including localhost.
- Allowed raw fields: `workType,sublot,area,eqp,step,mesSourceDate,package`.
- Raw limits: at most 20 items, 2,048 UTF-8 bytes per item, 65,536 UTF-8 bytes total.
- Default diagnostic detail summarizes `RAW_OBSERVATION_SET` as count plus digest and never returns the canonical raw JSON.
- Object misses share `ERROR_SEARCH_OBJECT_NOT_IN_SNAPSHOT`; authorization is checked first to avoid an existence oracle.
- V2 routes remain excluded from legacy v1 OpenAPI until ticket 17.

## Storage and semantic risks

- Mutable period closing columns must be reconstructed through the closed event's projection commit fence.
- Detail must use the exact Ticket 11 scope: period window overlap; evidence-level DemandId; category/code period filters; state as a series-level aggregate gate.
- Evidence is not clipped to the query window, so causal opening evidence for a crossing period remains visible.
- `RAW_OBSERVATION_SET` currently stores the complete seven-field observation multiset in `ObservedValue`; exposing it directly would bypass raw authorization.
- Raw rows must be located only after snapshot membership is proven, by evidence `(PollTraceId, ProjectionCommitId, DemandId)`.
- Existing tables and indexes are sufficient; no schema table or index is required.
- Ticket 08 explicitly owns the existing DemandSeries/PollTrace raw-detail payloads. Ticket 12 applies the stricter authorization and bounded expansion policy to Error Search; changing the legacy endpoints here would be a breaking scope expansion.

## Framework and commands

- .NET SDK 10.0.302, xUnit 2.4.2, VSTest runner.
- Focused syntax: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~ErrorSearchDetailTests"`.
- Real SQL gate requires `MES_INGEST_TICKET01_SQLSERVER` and SQL Server product major 16 / compatibility 160.
