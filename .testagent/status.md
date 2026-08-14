# Ticket 20 test status

## Current

- Ticket 20's non-pixel implementation is frozen. The production page uses the
  existing V2 DemandSeries list/detail contract and the tested integration seam
  is `ScriptedFakeHost -> MesIngestV2ApiClient -> WatchV2WorkspaceSession ->
  production WatchWorkspaceWindow`.
- Independent Standards, Spec, and correctness reviews have no remaining
  findings after fixes.
- No golden baseline, candidate, promoted artifact, DPI clone, VM deployment,
  or user-approval checkbox was changed. Those remain intentionally deferred to
  the shared tickets 19-22 preview.

## Red-green evidence

- Presenter tests first failed to compile without the source object facts, then
  proved complete lifecycle, LiveMesFieldSet/raw evidence, provenance, exact
  zero-page state, retained-failure state, and source snapshot comparison.
- The automatic-target race test first observed two requests for the old filter;
  after suspending the old target while a manual/AREA operation is pending, the
  new query commits and reactivates atomically.
- Production integration tests cover current-AREA-first navigation, explicit
  all-AREA confirmation, frozen paging, focused audit drill, stale-operation
  rejection, disposal, AREA changes, and manual-versus-automatic arbitration.
- The final solution run exposed two legacy-grid regressions caused by changing
  the shared clipboard selection unit. The behavior now preserves `FullRow`
  only when the DemandSeries page explicitly requests it; both legacy regression
  tests passed 2/2 after the fix.

## Focused validation

- Ticket 20 presentation/query/clipboard/auto-refresh/shell filter: 43 passed /
  0 failed / 0 skipped.
- Production Host/session/DemandSeries integration filter: 29 passed / 0 failed /
  0 skipped.
- Legacy clipboard/selection regression filter: 2 passed / 0 failed / 0 skipped.
- `Invoke-WatchUiTests.ps1 -Suite watch-vm-tests`: 118 passed / 0 failed / 1
  named skip (`zh-CN` required, current session `en-US`). Evidence:
  `C:\Users\szy\AppData\Local\Temp\ticket20-watch-vm-20260814-165832`.
- Final non-incremental Release build: 0 warnings / 0 errors.

## Final solution run

- Ran exactly once after the initial focused validation:
  - `MesIngest.Watch.UiTests`: 118 passed / 0 failed / 27 named
    visual/interactive-environment skips.
  - `MesIngest.Tests`: 711 passed / 5 failed / 99 named SQL-environment skips.
- Two failures were the shared clipboard regression described above and passed
  their 2/2 focused verification after the scoped fix. The three remaining
  failures are outside the Ticket 20 diff and failed again in a focused run: the
  existing INSTALL.md `openapi/v1.json` assertion, latency telemetry retention
  using filesystem time, and legacy `MainWindow` caption double-click timing.
