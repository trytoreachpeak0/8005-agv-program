# Ticket 18 test research

## Confirmed seam

The confirmed client seam in `.scratch/new-mes-ingest/spec.md` is
`ScriptedFakeHost -> production MesIngest.Watch`. Ticket 18 is non-visual: no
XAML, UI Automation, DPI, or golden-baseline files are in scope.

## Target inventory

- `MesIngest.Watch/WatchHostSession.cs`: reusable Host generation,
  cancellation, settings validation, failure vocabulary.
- `MesIngest.Watch/MesIngestApiClient.cs`: reusable HTTP/Bearer/timeout,
  correlation, telemetry, and redaction mechanics, but currently legacy-only.
- `MesIngest.Watch/WatchDemandSession.cs` and `WatchAlertSession.cs`: reference
  algorithms for request generations, atomic success commits, retained failure
  windows, and stable-id selection relocation; their legacy DTOs and cursor
  recovery are not reusable.
- `MesIngest.Watch/WatchAutoRefresh.cs`: legacy optional refresh model; ticket
  18 needs a separate interval-only, always-on five-view schedule.
- `MesIngest.Watch.UiTests/ScriptedFakeHost.cs`: deterministic timing harness,
  currently an in-memory legacy adapter that must gain a production-HTTP path.
- Frozen V2 authority: `MesIngest.Core/SeriesProjection/NewMesIngestContract.cs`,
  Core query/snapshot contracts, `MesIngest.Host/NewMesIngestEndpoints.cs`, and
  `pack/openapi/v2.json`.

## Existing conventions

- C# / .NET 8, xUnit 2, VSTest; test names are behavior sentences with
  underscores.
- Integration-style Watch tests use production internal interfaces via
  `InternalsVisibleTo`; deterministic gates use `TaskCompletionSource` rather
  than wall-clock sleeps.
- External HTTP is replaced at the `HttpMessageHandler` boundary. Tests must
  exercise production URI construction, JSON DTOs, Bearer headers, structured
  status errors, cancellation, and session admission.
- Core query records provide `NormalizeAndValidate`; list-valued record equality
  is reference-based, so a canonical query key/URI is required.

## Acceptance checklist

1. ScriptedFakeHost drives every Watch V2 read through the production HTTP,
   DTO, bearer, strict-contract, paging, and session entry path.
2. Applying Host/credential/version cancels the prior generation and clears all
   prior Host snapshots, cursor/query state, selections, and details; failure
   never displays the old Host.
3. Authentication, exact-contract mismatch, network, and server-query failures
   are separately observable and credentials are redacted.
4. Auto-refresh is always enabled; settings can only change each data view's
   interval. Loading/failure retains the last successful snapshot with success,
   failure, and stale timestamps.
5. Only a response matching Host generation, canonical query, and request
   generation can atomically replace a snapshot; canceled/late work cannot.
6. Query changes and snapshot/cursor/page failures retain the old result under
   its old committed query and expose the attempted-query failure; no implicit
   first-page fallback.
7. Successful refresh relocates selections by SeriesId or DemandId; a missing
   object clears selection/detail with an observable reason.
8. Deterministic tests cover Host switching, slow work, cancellation, late
   completion, retained failure/staleness, mismatch, query changes, selection,
   AREA scope, and all V2 page/detail reads without visual files.
