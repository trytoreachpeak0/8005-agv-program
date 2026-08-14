# Ticket 21 test research

## Confirmed production seam

The specification confirms `ScriptedFakeHost -> MesIngestV2ApiClient ->
WatchV2WorkspaceSession -> production WatchWorkspaceWindow -> UI Automation`
as the Watch acceptance seam. Unit tests are limited to profile parsing/storage,
query construction, and presentation rules that are more precise below that
boundary. There is no page-only Host bypass.

## Existing authority and reusable code

- Ticket 10 owns the Host `ReadabilityAuditSnapshot` contract, filters, exact
  totals/facets, bounded paging, stable order, details, blockers, checks, raw
  observations, PollTrace, ProjectionCommit, and CatalogRevision.
- Ticket 18 owns Host/query/request/selection generations, late-response
  rejection, stale retention, and selection relocation/clearing.
- Ticket 19 owns the one production Fluent shell, settings, overview and local
  AREA display context.
- Ticket 20 owns frozen DemandSeries paging, source-snapshot comparison,
  explicit all-AREA confirmation, and the strong
  `WatchDemandSeriesNavigationContext.FromReadabilityAudit` drill seam.
- Production Readability Audit and AREA pages remain placeholders. No TXT
  profile parser/store exists.
- Readability auto-refresh currently replays a frozen page query and therefore
  cannot discover a later projection. AREA application updates three queries
  but immediately refreshes only Overview and an active DemandSeries page.

## Local TXT decisions

- Per-user directory: `%LocalAppData%/MesIngest.Watch/area-filters`; tests inject
  an isolated directory.
- UTF-8, one MesArea per effective line. Blank lines and whole-line `#`
  comments are ignored, matching the selected prototype's editor help.
- A draft with no effective MesArea is invalid. Duplicate effective values,
  non-canonical MesArea values, or more than the Host limit of 100 are invalid.
- Selecting a file changes only the editor. Save writes the selected valid TXT;
  Apply persists it as the active profile and changes the three scoped queries.
  Saving a currently applied file does not silently replace the persisted
  applied AREA snapshot; the operator must apply again. All-AREA is a built-in
  context, not an empty named TXT file.

## Existing test conventions

- SDK 10.0.302 with no `global.json` test runner setting: both xUnit v2 and
  xUnit v3 projects use VSTest through `Microsoft.NET.Test.Sdk` and adapters.
- Filter with `--filter "FullyQualifiedName~..."`.
- WPF tests use an STA dispatcher, deterministic gates/TaskCompletionSource,
  `FindName`, UI Automation properties, and no sleeps or screen coordinates.
- The shared tickets 19-22 golden-machine train owns real-window preview,
  pixel baselines, high contrast, and 125%/150% DPI evidence.

## Acceptance checklist

1. Audit rows cover every Demand generation and keep READABLE/NOT_READABLE
   separate from VISIBLE/GONE/archived lifecycle; rows use Host lead blocker
   while detail keeps every blocker and qualification check.
2. State, WorkType, blocker, DemandId and SUBLOT filters; Host facets, exact
   deduplicated totals, fixed order, 100/200 sizes and direct pages remain bound
   to one visible frozen audit snapshot.
3. Overlapping blocker facets never become the NOT_READABLE total; only a
   successful zero-result query renders an empty result, never loading/failure
   or a zero NOT_READABLE count as health.
4. Detail exposes trusted fields or raw conflicts, owning Series, PollTrace,
   ProjectionCommit, CatalogRevision, all checks/blockers and the same snapshot
   identity as the list.
5. Variant A keeps the named profile list visible beside selected TXT content,
   validation, save and apply state. Invalid drafts cannot be saved/applied.
6. Applying/switching an AREA profile restarts Overview, DemandSeries and Audit
   on page one with no frozen cursor, and does not query ErrorSearch or Current
   Attention or mutate Host business state.
7. Host receives only canonical trusted MesArea values and applies them before
   paging/counting; untrusted AREA remains visible only through All Areas.
8. Audit-to-Series drill carries SeriesId, DemandId and source snapshot facts;
   out-of-range navigation reuses Ticket 20's explicit All Areas confirmation.
9. Refresh failure retains the old committed query/snapshot; successful refresh
   reselects by DemandId or clears detail with an observable notice.
10. Both pages expose stable UIA names/ids, keyboard focus, non-color status and
    reachable key actions at the 720 epx minimum without local pixel approval.

## Risks to mutate explicitly

- Reusing a frozen audit query as a latest refresh.
- Showing facets calculated from current-page rows or summing blocker facets.
- Relabeling retained results with a newly failed filter/profile.
- Applying normalized profile values before reporting duplicate/empty errors.
- Treating editor selection as application or changing global business facts.
- Fetching audit detail from a different snapshot reference.
- Silently navigating outside the active AREA scope.
