# Ticket 22 test status

> Ticket 22 content below predates the DemandSeries Inspector E work. It is
> retained verbatim. Ticket 06 status is appended in a separate section at the
> end of this file.

## Current

- Ticket 22 Error Search Variant A and Current ingest attention production pages
  are implemented through the production V2 HTTP/DTO/session/window path.
- The final Spec review passed with no actionable findings. The final Standards
  review finding (cross-period raw-evidence selection) was reproduced red,
  fixed, and independently rechecked.
- The shared Ticket 19-22 golden-machine preview suite has completed its code
  and infrastructure gates, but the first green runner exposed an internally
  inconsistent final drill preview. That run is preserved and excluded from
  approval. Ticket 22 remains open until a corrected unique golden run,
  explicit user approval, evidence backfill, and cleanup recheck are complete.

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
- Error-detail identity follow-up after the first runner-green preview:
  34 core presenter/API-client tests passed; 39 session/Error/responsive/journey
  tests passed with the one real-window journey locally skipped by its explicit
  environment gate. New red-green facts reject route, Series, snapshot,
  filter, window, and order mismatches without replacing a successful list.
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
  - `run-20260814-235546-watch-production-preview` proved that isolation fix:
    AREA loaded/applied `Factory-East` and produced its preview. Its next red
    evidence showed the Error Search page visibly loaded and the Host request
    completed, while the journey waited on the page's WPF `Grid` root, which is
    not present in the UIA Control view after the responsive layout refactor.
  - The journey now waits on the exposed normalized-filter status text and
    selects a real matched period before waiting for that period's evidence.
    The exact local check passed 6 Error Search UI facts with the real-window
    journey remaining the one expected environment-gated skip.
- `run-20260815-000454-watch-production-preview` passed both formal suites and
  all environment/orchestration/cleanup gates: `watch-vm-tests` reported 139
  passed plus the one named nonbaseline chrome skip; the production journey
  reported 1 passed. The commit and guest payload hashes matched and no task or
  product/test process remained.
- That runner-green evidence is intentionally not an approval candidate. Its
  final Current Attention drill showed the normalized filter and row for
  `SERIES-ATTENTION-22` while the detail status still named
  `SERIES-ERROR-22`, with empty period/evidence grids. The fake detail callback
  ignored its request and the journey captured after only the filter changed.
- The follow-up now makes the fake detail query/request-aware and waits for the
  selected Series identity, periods, and evidence before capture. Production
  also fails closed at the HTTP and session boundaries and no longer reports a
  rejected detail as successfully read. A new unique golden run is required;
  the inconsistent run remains preserved.
- `run-20260815-005125-watch-production-preview` used clean commit `dd905a8`.
  Its calibrated environment and `watch-vm-tests` passed (150 passed, one named
  nonbaseline chrome skip), but the production journey stopped at DemandSeries:
  the DataGrid root does not expose UIA `ScrollItem`, while the journey requested
  that unsupported pattern directly. Cleanup and post-cleanup environment gates
  passed with no residual task or process.
- The exact real-process journey was reproduced locally in 7 seconds with the
  same `PatternNotSupportedException`, then passed 1/1 in 18 seconds after the
  evidence grid received keyboard focus and let WPF scroll its ancestor through
  the accessible focus path. The unsupported pattern is no longer requested;
  another unique formal golden run is required.
- Pending: inspect all retrieved runner/environment/cleanup artifacts and PNG/UIA
  evidence, show the final preview to the user, receive explicit approval, then
  backfill Tickets 19-22. Ticket 23-only baseline promotion/stability/DPI-clone
  work remains intentionally excluded.

---

# DemandSeries Inspector E — Ticket 06 test status

## Red-before-green evidence

The first compilable slice was run from `mes/ingest/csharp` with:

```powershell
dotnet test MesIngest.Tests --filter "FullyQualifiedName~WatchDemandSeriesWindowLifecycleTests|FullyQualifiedName~WatchV2PreferencesTests.Layout_opt_out|FullyQualifiedName~WatchV2PreferencesTests.Version_2_remember"
```

Result: `Total 5 / Passed 3 / Failed 2 / Skipped 0`.

- `Background_update_keeps_a_minimized_inspector_minimized_until_explicit_show_restores_it`
  failed because explicit `OpenOrShow` left the real Inspector in
  `WindowState.Minimized`. The preceding assertion proved a background
  `Update` correctly left it minimized.
- `Layout_opt_out_does_not_persist_main_or_inspector_geometry` failed because
  the opt-out JSON still wrote the supplied `1777x1111` geometry.
- The version-2 migration and the two ordinary top-level lifecycle facts in
  the same slice passed.

The layout-focused red command was:

```powershell
dotnet test MesIngest.Tests --no-restore --filter "FullyQualifiedName~WatchWindowLayoutPersistenceTests"
```

Result: `Total 6 / Passed 0 / Failed 6 / Skipped 0`.

- Normal round-trip, invalid-coordinate, missing-monitor, and work-area-clamp
  tests all failed because the production-emitted preference document had no
  Inspector `920x680` layout object/monitor identity to restore or mutate.
- Maximized round-trip failed because the reopened Inspector was `Normal`
  rather than `Maximized`.
- The Settings accessibility assertion failed because the label remained
  `记住窗口尺寸` rather than `记住窗口布局`.

A combined lifecycle/preferences run compiled and reached 24 tests before the
shutdown slice exposed an additional red and aborted the WPF testhost:

- `Closing_main_window_closes_inspector_and_cancels_pending_detail` caused
  `WatchV2WorkspaceSession.Dispose()` to cancel an already disposed detail CTS,
  throwing `ObjectDisposedException` from `CancelAndDispose` line 1637. This is
  direct evidence that main-window shutdown is not yet idempotently clean.

The abort is preserved as red evidence, not a claimed clean run. Tier 1 was not
run by this delegated test-first slice, and Tier 2/3 were intentionally not
entered.

## Requirement-to-evidence mapping

| Ticket requirement (verbatim) | Concrete test evidence |
| --- | --- |
| `只有显式打开/显示动作激活或恢复 Inspector；列表选择和刷新只更新内容，不恢复、置顶、激活或抢焦点。` | New `Background_update_keeps_a_minimized_inspector_minimized_until_explicit_show_restores_it`; existing `Selection_update_changes_open_content_without_showing_or_activating_the_window` and `Space_never_opens_or_activates_and_selection_updates_open_content_without_focus_stealing`. |
| `主窗口和 Inspector 可独立最小化；Inspector 无 Owner、Topmost=false，Alt+F4 正常关闭，Escape 不关闭窗口。` | New `Main_and_inspector_minimize_independently_and_escape_does_not_close_inspector` and `System_close_command_closes_the_inspector_and_reopen_creates_a_new_window`; existing `Fluent_window_exposes_normal_top_level_semantics_and_first_observation_evidence`. `SystemCommands.CloseWindow` exercises the standard WPF system-close route used by Alt+F4 without synthesizing fragile native keystrokes. |
| `关闭 Inspector 结束内部调查上下文并取消 pending detail；重开时加载当前列表选择，只恢复窗口布局。` | New `Closing_and_reopening_loads_current_selection_and_resets_local_investigation_state`; existing `Closing_inspector_cancels_pending_detail_and_rejects_its_late_body`. |
| `Host 设置变更关闭 Inspector、清除旧 Host detail 并取消请求，但保留有效布局偏好。` | New `Host_change_closes_inspector_cancels_old_detail_and_preserves_saved_layout`, with concrete cancellation count, cleared detail, closed coordinator/window, and persisted display assertions. |
| `主窗口关闭时协调器主动关闭 Inspector、取消工作并确保应用无孤儿窗口或请求地干净退出。` | New `Closing_main_window_closes_inspector_and_cancels_pending_detail`; its first run found the non-idempotent CTS-disposal red described above. |
| `“记住窗口尺寸”向后兼容升级为“记住窗口布局”，同一偏好统一控制主窗口和 Inspector 布局，旧偏好文档仍可加载。` | New `Version_2_remember_window_size_document_loads_as_the_shared_layout_preference`, `Settings_names_the_backward_compatible_choice_remember_window_layout`, and the two-window round-trip test. |
| `保存并恢复 Inspector 的正常尺寸、正常位置、显示器身份和最大化状态；关闭记忆偏好时不持久化这些值。` | New `Remembered_layout_round_trips_main_and_inspector_normal_bounds_and_monitor_identity`, `Maximized_inspector_restores_safe_normal_bounds_then_maximized_state`, and `Layout_opt_out_does_not_persist_main_or_inspector_geometry`. |
| `无效坐标、显示器缺失或工作区变化时，将默认 1200×800、最小 720×600 的 Inspector 约束到当前可见工作区，不落在屏幕外。` | New `Invalid_inspector_coordinates_restore_the_clamped_1200_by_800_default`, `Missing_monitor_falls_back_to_a_visible_work_area`, and `Changed_work_area_clamps_the_complete_inspector_normal_bounds`; all assert the complete normal rectangle is within the visible work area. |
| `公开协调器/窗口测试覆盖显式激活、非激活更新、独立最小化、Alt+F4、Escape、关闭重开、Host 切换和应用退出。` | The exact lifecycle tests cited in the first five rows form the public coordinator/window coverage set. |
| `偏好测试覆盖旧格式、opt-out、normal bounds、maximized、monitor identity、无效坐标、缺失显示器和 visible-work-area clamp。` | The exact preference/layout tests cited in the last three rows cover every named case. |

## Test-gap and assertion review

- Static pseudo-mutation review (the production baseline is intentionally red,
  so empirical mutation injection was not appropriate) found each substantive
  Ticket 06 branch mapped to a concrete assertion: update-vs-explicit restore,
  opt-in-vs-opt-out, normal-vs-maximized, valid-vs-invalid coordinates,
  present-vs-missing monitor, Host close, Inspector close, and application
  close.
- Assertions use independent literals or OS-reported work-area bounds, not
  values recomputed with the production algorithm. Geometry tests also assert
  secondary observables (monitor identity, state, full-rectangle containment,
  or coordinator instance identity).
- No sleeps, network calls, skipped tests, private-method calls, or production
  source inspection were added. Temporary files are isolated and cleaned.
- Remaining real-desktop Alt+F4/input focus and multi-monitor OS integration are
  Tier 2 concerns under the repository golden-renderer policy; the unit seam
  deliberately uses standard WPF system close and a production-emitted monitor
  identity rather than native input automation.

## Green implementation and empirical pseudo-mutation closure

- The combined lifecycle, layout, shell, and preference gate passed 45/45 with
  zero failures and zero skips after implementation.
- The main-window shutdown red was fixed by making convergent request-source
  cancellation idempotent; its exact regression now passes 1/1.
- Six high-risk pseudo-mutations were injected one at a time, run through the
  narrowest covering test, and immediately reverted. All six were killed:
  1. explicit show no longer restored a minimized Inspector;
  2. background `Update` incorrectly restored a minimized Inspector;
  3. invalid coordinates reused the stale saved size instead of 1200x800;
  4. the horizontal visible-work-area clamp was removed;
  5. opt-out persisted the supplied live geometry;
  6. maximized restore was forced to normal.
- The pre-implementation shutdown run independently killed the seventh
  high-risk mutation: non-idempotent duplicate cancellation. No substantive
  survived mutation or uncovered ticket branch remains in the focused scope.
- Every temporary mutation was reverted before the final green run.
