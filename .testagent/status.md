# Ticket 19 test status

## Current

- Ticket 19's non-pixel implementation is frozen. Production `App` now owns the
  V2 composition/window and the tested seam is `ScriptedFakeHost -> production
  MesIngestV2ApiClient -> WatchV2WorkspaceSession -> production WPF window`.
- Standards review has no remaining documented-rule violation. Spec review
  passes the non-pixel implementation with no remaining P0-P3 finding.
- No golden baseline, candidate, promoted artifact, DPI clone, VM deployment,
  or user-approval checkbox was changed. Those remain intentionally deferred to
  the one shared tickets 19-22 preview.

## Red-green evidence

- Missing LongGone summary and failed-to-retry status first failed 2/8
  `WatchOverviewPresentationTests`, then passed 8/8 after implementation.
- Production Host/window tests first exposed stale UIA, incomplete summary, and
  stale Host preference overwrite (3 failures), then passed 4/4 after the
  generation gate, complete projections, state icons, and dynamic UIA names.
- A second UIA mutation showed fixed snapshot/InfoBar names hiding dynamic facts
  (2 failures); dynamic accessible names then passed 4/4.
- Auto-refresh notification tests cover Started/Completed ordering, observer
  isolation, and disposal suppression; preference tests cover schema fallback,
  all supported intervals, atomic replacement, geometry bounds, and no secret.

## Focused validation

- `dotnet build .\MesIngest.sln -c Release --no-restore --no-incremental`:
  succeeded, 0 warnings / 0 errors.
- General Ticket 19/V2 filter: 62 passed / 0 failed / 0 skipped.
- Production Host/session filter: 27 passed / 0 failed / 0 skipped.

## Pseudo-mutation audit

- Removing the production App's V2 composition ownership made the shell root test
  fail (expected V2, observed legacy composition).
- Removing auto-refresh notification subscription left the visible overview at
  `1` instead of the completed value `2`.
- Relabeling the retained Host snapshot with the new local AREA made the real
  Host failure test show local `B1-1` instead of committed `A1-1`.
- All three mutations were reverted before final validation.

## Final solution run

- Ran exactly once after focused validation:
  - `MesIngest.Watch.UiTests`: 109 passed / 0 failed / 27 named visual/interactive
    environment skips.
  - `MesIngest.Tests`: 695 passed / 3 failed / 99 named SQL-environment skips.
- The three failures are outside the Ticket 19 diff: an existing INSTALL.md
  `openapi/v1.json` assertion, latency telemetry retention using filesystem time,
  and a legacy `MainWindow` caption-drag timing assertion. Focused re-run passed
  the caption-drag test; the two deterministic pre-existing failures remained.
