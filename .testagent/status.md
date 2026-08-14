# Ticket 21 test status

## Current

- Audit query/session/auto-refresh, presentation, production WPF page and
  Audit-to-DemandSeries drill wiring are implemented.
- TXT-backed AREA profiles, selected/saved/applied separation, persisted
  applied snapshot, production Variant A page and three-view refresh isolation
  are implemented.
- Stable UIA landmarks/tab stops and 720 epx stacked layouts are frozen by
  semantic tests.
- Golden candidates, baselines, VM deployment and DPI clones remain untouched;
  they belong to the tickets 19-22 shared integration train.

## Red-green evidence

- `WatchAreaFilterProfileTests`: initial `CS0103` for missing parser/store;
  final 24 tests green, including a visible corrupt-marker fallback diagnostic.
- `WatchReadabilityAuditQueryTests`: initial `CS0103` for missing query helper;
  final 3 tests green.
- `WatchReadabilityAuditPresentationTests`: initial `CS0103` for missing
  presenter; final 6 tests green.
- `WatchReadabilityAuditProductionIntegrationTests`: initial missing
  `ReadabilityAuditNavigationTask` and selection entry point; final tests also
  cover multi-value OR filters, page size 200 and direct frozen page 3.
- `WatchTicket21AreaAndResponsiveIntegrationTests`: unchanged test first caught
  missing page/card AutomationId/Name and then missing explicit tab stops;
  final 2 tests green.

## Verified test-gap closure

Four high-risk pseudo-mutations were empirically confirmed as survivors,
reverted, covered, and then re-injected to prove the new assertion kills them:

1. Truncating comma-separated audit OR values to one item initially passed;
   production integration now asserts two states, WorkTypes and blockers.
2. Rejecting exactly 100 AREA values (`>` changed to `>=`) initially passed;
   a boundary test now fails that mutation.
3. Omitting CatalogRevision from list/detail snapshot identity initially passed;
   the presenter test now rejects a detail differing only in CatalogRevision.
4. Ignoring the persisted applied AREA profile at startup initially passed;
   production integration now proves the initial Overview request uses the
   persisted scope and that Save alone does not replace it.

No mutation remains in the working tree.

## Focused validation

- Review-fix unit/session/presenter/profile filter: 52 passed, 0 failed.
- Review-fix audit/AREA/DemandSeries/session WPF filter: 31 passed, 0 failed.
- `WatchV2ProductionHostTests`: 4 passed, 0 failed.
- `WatchCompositionRootTests`: 16 passed, 0 failed.
- `WatchV2ProductionShellTests` plus navigation context: 7 passed, 0 failed.
- `MesIngest.Watch` Release build: succeeded with 0 warnings and 0 errors.
- Initial two-axis review found three spec and six documented UI-standard
  issues. Fixes now preserve off-page selections through same-snapshot detail,
  distinguish corrupt AREA markers, retain explicit All AREA applied state,
  use Fluent Cards/tokens/platform type, and expose truthful draft/failure
  states. Final Spec and Standards read-only re-reviews both report no findings.

## Final solution run

- Non-incremental Release solution build: succeeded, 0 warnings, 0 errors.
- Full solution test pass (run once): `MesIngest.Watch.UiTests` 124 passed,
  0 failed, 27 named environment/golden skips; `MesIngest.Tests` 748 passed,
  2 failed, 99 named SQL skips.
- Both failures are outside the Ticket 21 diff: the known INSTALL.md V1 OpenAPI
  wording assertion and the file-retention timestamp test. All Ticket 21
  focused filters remain green.
- No golden candidate/baseline, VM task, preview artifact, or DPI clone was
  generated or changed; those gates remain pending for the shared 19-22 train.
