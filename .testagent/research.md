# Ticket 20 test research

## Confirmed production seam

The specification fixes the client acceptance boundary as `ScriptedFakeHost ->
production MesIngest.Watch -> UI Automation / golden machine`. Local TDD uses
the real V2 HTTP client, exact contract discovery, `WatchV2WorkspaceSession`,
production `WatchWorkspaceWindow`, WPF controls, and dynamic automation names.
It does not add a page-only Host bypass.

## Existing authority and gap

- Ticket 08 already supplies frozen `DemandSeriesBrowseQuery`, exact totals and
  facets, bounded direct-page/cursor reads, and snapshot-bound full detail.
- Ticket 18 already owns Host/query/request/selection generations, stale
  retention, late-response rejection, and selection relocation/clearing.
- Ticket 19 supplies the one `FluentWindow`/`TitleBar`/`NavigationView` shell,
  settings, local AREA context, overview drill intents, and always-on refresh.
- Production `DemandSeriesPage` is still a placeholder. Navigation only arms a
  timer and does not perform the initial read.
- A frozen page-two-or-later query cannot itself discover a newer projection:
  the client must first acquire latest page one, then reopen the desired page
  with that new snapshot reference, committing only the final page.

## Test conventions

- .NET 8 WPF. `MesIngest.Tests` is xUnit v2/VSTest;
  `MesIngest.Watch.UiTests` is xUnit v3/VSTest and owns `ScriptedFakeHost` V2.
- WPF tests run on an STA dispatcher and avoid sleeps. Host timing uses gates or
  deterministic scripted sequences.
- Assert observable text, query timeline, frozen snapshot identity, control
  availability, automation names, and clipboard payloads—not private helpers.
- Formal packaged-process FlaUI journeys and all pixel/DPI work remain in the
  one tickets 19–22 shared integration train. Existing packaged journeys still
  target the legacy Host/window and cannot prove the V2 page locally.

## Acceptance checklist

1. Lists Tracking, GONE, Archived, and LongGoneButVisible without filtering out
   `NOT_READABLE` or malformed data.
2. Host resolves filters, exact AREA scope, stable order, exact totals,
   previous/next, and direct page within one frozen snapshot.
3. Detail distinguishes generations/predecessors, lifecycle timestamps,
   `LiveMesFieldSet`, `DemandRawObservation`, duplicate observations, current
   conditions, blockers, events, `PollTrace`, and `ProjectionCommit`.
4. `DATES` is visibly named `MesSourceDate`, separate from lifecycle time.
5. Overview/audit navigation carries SeriesId, focused DemandId, and source
   snapshot summary; the target compares that source to its own current read.
6. An out-of-AREA target requires explicit confirmation before all-AREA query.
7. Loading/failure retains the previous successful list/detail; new success
   reselects by stable id or clears with a reason.
8. Filters, paging, grids, detail, time copying, and evidence drill-down have
   stable automation names and keyboard focus without coordinate dependence.
9. Master/detail, pagination, and primary actions remain reachable at 720 epx;
   1440/2560 and DPI visual proof is deferred to the shared train.

## Risks to mutate explicitly

- Reusing a frozen page query as “refresh” and never seeing a new commit.
- Calling detail directly for a range-excluded SeriesId because the detail
  snapshot token itself is not AREA-bound.
- Relabeling retained old results with a newly drafted filter or AREA scope.
- Treating `MesSourceDate` as StartedAt/last-seen/GONE time.
- Clearing old detail while a refresh is pending, or retaining it after a new
  snapshot no longer contains the selected SeriesId.
- Using current-page length as total count or local sorting/filtering.
