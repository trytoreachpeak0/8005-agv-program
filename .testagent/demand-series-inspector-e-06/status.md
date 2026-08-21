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

## Review closure and final Tier 1

- The two-axis review found one same-Series close/reopen focus leak. The
  strengthened `Closing_and_reopening_loads_current_selection_and_resets_local_investigation_state`
  failed while the historical DemandId survived close, then passed after the
  shell cleared `_focusedDemandId` with the closed Inspector context.
- Standards findings were closed by centralizing named layout tokens and
  constraints, consolidating explicit show/restore/activate, and using
  `RememberWindowLayout` internally while retaining `rememberWindowSize` only
  at the version-2 JSON boundary.
- Focused lifecycle/layout/shell/preferences gate after review: 45 passed,
  0 failed, 0 skipped.
- `MesIngest.Watch.UiTests` build: 0 warnings, 0 errors.
- Final Tier 1 `dotnet test MesIngest.Tests`: 637 passed, 0 failed, 82 skipped,
  719 total in 1m56s. The 82 skips are the existing SQL Server environment gate;
  its three required `MES_INGEST_TICKET01_*` variables were absent.
- Tier 2/3 was not run without explicit user authorization.
