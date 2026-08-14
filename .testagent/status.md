# Ticket 22 test status

## Current

- Ticket 22 Error Search Variant A and Current ingest attention production pages
  are implemented through the production V2 HTTP/DTO/session/window path.
- The final Spec review passed with no actionable findings. The final Standards
  review finding (cross-period raw-evidence selection) was reproduced red,
  fixed, and independently rechecked.
- The shared Ticket 19-22 golden-machine preview suite is implemented but has
  not yet been run. Ticket 22 must remain open until the golden run, explicit
  user approval, evidence backfill, and cleanup recheck are complete.

## Red-green evidence

- Error Search query construction started red before its production helper was
  added, then passed after normalization and opaque-cursor navigation were
  implemented.
- Current attention query/presentation tests were written before the matching
  production helpers and passed after the four active-only kinds, stable
  identity, Host-authoritative paging/facets, and structured drill were added.
- Production UI tests drove the Error Search, Current Attention, raw-evidence,
  cancellation/failure retention, keyboard/UIA, and responsive implementations.
- Final Standards regression:
  `Raw_evidence_grid_tracks_the_selected_period_across_real_selection_and_button_render_cycles`
  failed before the fix because two periods' evidence were mixed in the grid;
  it passed after the grid was constrained to the selected period and stale
  period/evidence/raw state was cleared.

## Verified test-gap closure

Ten pseudo-mutations were injected one at a time and reverted. All ten are now
killed by focused tests:

1. Host exact total replaced by loaded row count.
2. Failed retained zero misreported as a successful empty result.
3. Raw failure discarded the last successful bounded payload.
4. Current-attention rolling window used the wrong navigation window.
5. Series-error drill omitted the required ACTIVE activity state.
6. Direct Error Search page navigation fabricated/skipped a Host cursor.
7. Direct page navigation walked one cursor beyond the requested page.
8. Raw-evidence allowlist trusted Host-reported included fields.
9. The exact 20-item raw-evidence boundary was rejected.
10. Current-attention drill trusted stale navigation SeriesId instead of the
    authoritative item identity.

## Focused validation

- Ticket 22 core query/presentation tests: 31 passed, 0 failed.
- Ticket 22 UI integration/responsive tests before the final Standards fix:
  9 passed, 0 failed.
- Final Error Search UI class after the cross-period fix: 6 passed, 0 failed.
- Raw presenter/API-client safety tests: 30 passed, 0 failed.
- Session/Error WPF state tests: 26 passed, 0 failed.
- Shared production-journey evidence tests: 3 passed, 0 failed.
- Process file-location isolation tests added after the first real-window run:
  5 passed, 0 failed. They prove production defaults remain unchanged and UI
  test mode fails closed unless `LOCALAPPDATA` is an absolute isolated root.
- Adjacent Watch core regression set: 332 passed, 4 named integration tests
  skipped by their existing environment gate.
- Adjacent nonvisual Watch UI regression set: 57 passed, 0 failed.
- Release solution builds used by the final focused checks completed with
  0 warnings and 0 errors.
- Golden scripts parse successfully; trait discovery isolates the new V2
  production journey, the five approved legacy baseline scenarios, and the
  nonbaseline Fluent chrome fact. No baseline was created or approved.

## Full solution and golden train

- The single frozen-tree full Release run was executed once:
  `dotnet test mes/ingest/csharp/MesIngest.sln --no-restore --configuration Release --verbosity minimal`.
- `MesIngest.Watch.UiTests`: 138 passed, 28 skipped, 0 failed.
- `MesIngest.Tests`: 781 passed, 99 skipped, 2 failed.
- Both failures reproduce under an exact two-test filter and are pre-existing
  baseline failures in files unchanged from fixed point `3eb6224`:
  - `InstallPackageLayoutTests.Install_doc_describes_production_v2_release_smoke_without_claiming_v1_openapi_or_watch`
    conflicts with the unchanged install document's explicit statement that
    `/openapi/v1.json` must return 404.
  - `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age`
    fails the unchanged age-retention implementation/test at line 275.
- The full solution was not rerun. These unrelated failures are recorded rather
  than silently changing non-Ticket-22 production/docs behavior.
- Pending formal command (from `mes/ingest/csharp`):
  `./Invoke-GoldenRendererValidation.ps1 -Ticket '19-22-shared-preview' -Suite watch-production-preview -Configuration Release -ExpectedDpi 96 -ExpectedDesktopWidth 1920 -ExpectedDesktopHeight 1080 -TimeoutSeconds 7200`.
- Preserved golden-machine red evidence:
  - `run-20260814-232704-watch-production-preview` stopped before any suite
    because the VM offline cache lacked `System.Data.Odbc 8.0.0`.
  - `run-20260814-233317-watch-production-preview` stopped before any suite on
    the transitive `System.Text.Encoding.CodePages 8.0.0` dependency.
  - Both exact trusted packages were copied into the required offline cache and
    verified by nupkg SHA-256; all 93 package id/version pairs in the current UI
    test assets file then reported present.
  - `run-20260814-233601-watch-production-preview` passed the calibrated
    environment and `watch-vm-tests` (139 passed, 1 named skip), then preserved
    a real-window failure at AREA because Windows Known Folder resolution
    ignored the child `LOCALAPPDATA` environment override.
  - The harness fix now explicitly maps the existing UI-test-mode isolated root
    into the existing internal composition file-location seams. Spec and
    Standards rechecks passed with no public/page bypass and no production-mode
    behavior change.
- Pending: inspect all retrieved runner/environment/cleanup artifacts and PNG/UIA
  evidence, show the final preview to the user, receive explicit approval, then
  backfill Tickets 19-22. Ticket 23-only baseline promotion/stability/DPI-clone
  work remains intentionally excluded.
