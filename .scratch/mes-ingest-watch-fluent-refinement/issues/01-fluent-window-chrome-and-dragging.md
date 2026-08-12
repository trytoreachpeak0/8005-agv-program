# 使用 WPF-UI 完成 Win11 Fluent 窗口框架

Type: task
Status: wontfix
Blocked by: 无

## Question

如何在继续使用 WPF-UI 4.3.0 的条件下，让正式主窗口具备清晰的 Win11 Fluent 标题栏、最小化、最大化/还原、关闭、标题栏拖动、双击最大化和窗口边缘缩放，并保持现有页面状态、UI Automation 与窗口偏好不回归？

验收必须覆盖普通、最大化和还原状态，确认标题栏可拖动且右上角系统按钮可由鼠标、键盘和 UIA 到达。不得使用会破坏 Win11 圆角、DPI 或系统命中的自制透明窗口方案。

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-11 implementation and validation

- `MainWindow` now uses the WPF-UI `FluentWindow` extended-content title bar with a 48 px `TitleBar`, rounded Win11 corners, native resizable chrome, and visible minimize/maximize-or-restore/close commands. WPF-UI continues to own hit testing, dragging, double-click maximize, and edge resizing; no custom transparent-window hit-test implementation was introduced.
- The three system buttons are keyboard focusable and expose stable UIA names. Maximize/restore updates its UIA name with `WindowState`; existing page state and persisted window geometry remain in place.
- Added structural, in-process UIA, and real-window journey coverage for keyboard/UIA invocation, mouse double-click, dragging, minimizing, maximizing, restoring, and three-state screenshots.
- Local focused tests: 11 passed, 0 failed. Local `watch-vm-tests`: 83 passed, 0 failed, 1 skipped because the developer desktop was 192 DPI / `en-US`; owner: this ticket, discharged by the calibrated golden run below before approval.
- Full `MesIngest.Tests`: 500 passed, 19 SQL-environment tests skipped, and one unrelated existing failure, `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age`. Owner: final gate ticket 05; deadline: before ticket 05 is resolved in an environment with the required SQL dependency.
- Calibrated golden `watch-vm-tests`: 83 passed, 0 failed, 0 skipped. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-fluent-refinement-01/run-20260811-100635-watch-vm-tests`.
- Final calibrated golden real-window journeys: 6 passed, 0 failed, 0 skipped at 1920x1080, 96 DPI, `zh-CN`. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-fluent-refinement-01/run-20260811-101609-watch-ui-journeys`.
- Expected red visual evidence was preserved without baseline promotion: XAML preview/diff `run-20260811-101847-watch-xaml-visual` (19 baseline mismatches, 1 environment probe passed) and real-window compare `run-20260811-102545-watch-window-visual` (5 baseline mismatches). The diffs record the new 48 px Fluent title bar and resulting vertical layout shift.
- Earlier passing journey captures `run-20260811-100903-watch-ui-journeys` and `run-20260811-101256-watch-ui-journeys` are retained but superseded: their screenshots respectively captured desktop pixels around negative maximized bounds and an intermediate restore frame. They were not used as the approval preview.
- Every golden run removed its scheduled task and process tree. Final post-cleanup probes reported no residual task/process and restored the original VM to 96 DPI.
- Awaiting user approval of the final normal, maximized, and restored real-window preview. The ticket remains `claimed`; no visual baseline has been approved or overwritten.

### 2026-08-11 Fluent hierarchy revision after user review

- The user rejected the first preview because the 64 px `GlobalHeader` created a second full-width identity/command bar below the title bar and made the shell feel non-Fluent. That preview and its approval request are superseded.
- Removed `GlobalHeader` and the entire 64 px root row. The shell now has exactly one application-identity layer: the WPF-UI title bar contains the MI mark, dynamic `MesIngest Watch — Host` title, compact connection state, drag region, and caption buttons.
- Moved overview, TransportDemand, and IngestAlert auto-refresh/refresh/cancel controls into the right side of their respective page headers. Error and warning messages now use an inline content-area notice row that consumes no space while collapsed.
- Added mandatory repository guidance at `docs/agents/fluent-ui.md`, grounded in Microsoft Windows 11 Fluent and WPF-UI primary documentation. `AGENTS.md` now requires every `MesIngest.Watch` UI change to read both the Fluent rules and golden-renderer rules.
- Local focused shell/UIA tests: 11 passed, 0 failed, 0 skipped. Local `watch-vm-tests`: 83 passed, 0 failed, 1 environment-only skip because the developer desktop is 192 DPI / `en-US`; the calibrated run below discharges that skip.
- Calibrated golden `watch-vm-tests`: 83 passed, 0 failed, 0 skipped. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-fluent-refinement-01/run-20260811-104946-watch-vm-tests`.
- Final calibrated golden real-window journeys for the revised hierarchy: 6 passed, 0 failed, 0 skipped. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-fluent-refinement-01/run-20260811-110041-watch-ui-journeys`. Cleanup reports no scheduled task, no residual process, and a successful 96 DPI post-cleanup probe.
- The earlier passing revised-layout journey `run-20260811-105640-watch-ui-journeys` is retained but superseded because visual inspection found that WPF-UI's custom `Header` hid the bound title text. A regression assertion and the final run above verify the visible app/Host title.
- Infrastructure evidence retained: `run-20260811-105207-watch-ui-journeys` was terminated by Task Scheduler with `0x8007042B` before tests began; the controlled retry passed. `run-20260811-110533-watch-xaml-visual` was stopped by the host command window, and `run-20260811-111119-watch-xaml-visual` was terminated with `0x8007042B`; neither produced received/diff files. `run-20260811-111755-watch-window-visual` and `run-20260811-111846-watch-window-visual` exited before creating guest `Results`. Every failed orchestration cleaned the task/process tree and restored the calibrated environment.
- No baseline was approved, overwritten, or promoted. The final baseline comparison/promotion remains the responsibility of ticket 05 after user approval and after the golden task-start instability is resolved.
- Awaiting user approval of the revised final normal, maximized, and restored preview. The ticket remains `claimed`.

### 2026-08-11 connection-state placement revision

- The user explicitly did not approve the title-bar connection chip and requested that `连接正常` move to the bottom status bar. The `run-20260811-110041-watch-ui-journeys` approval preview is superseded.
- Removed `TitleBar.TrailingContent`. The title bar now contains only application identity, Host context, drag space, and caption buttons. The connection dot/text is a compact, text-accessible status item in the persistent bottom status bar beside the keyboard hints.
- Updated `docs/agents/fluent-ui.md` so MesIngest.Watch connection state is required to live in the bottom status bar and must not consume title-bar drag space.
- Local focused shell/UIA run initially passed 10/11 with one mouse double-click timing failure; the isolated `Fluent_title_bar_supports_uia_keyboard_double_click_and_mouse_drag` rerun passed. This first red remains recorded. Local `watch-vm-tests`: 83 passed, 0 failed, with the expected local-only 192 DPI / `en-US` environment skip.
- The final combined focused shell/UIA rerun passed 11/11 with 0 skips; `git diff --check` passed.
- The golden VM was found powered off and was started without RDP or Enhanced Session. Immediately after boot, elevated interactive tasks remained queued while Windows Update Orchestrator was active. A same-principal scheduler probe confirmed `Queued`; after the update worker exited, the probe completed with result 0 and was unregistered. No update service or registry setting was changed.
- Final calibrated golden `watch-vm-tests`: 83 passed, 0 failed, 0 skipped. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-fluent-refinement-01/run-20260811-113649-watch-vm-tests`.
- Final calibrated real-window journeys: 6 passed, 0 failed, 0 skipped. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-fluent-refinement-01/run-20260811-113932-watch-ui-journeys`. Cleanup reports no scheduled task, no residual process, and a successful 96 DPI post-cleanup probe.
- No visual baseline was approved, overwritten, or promoted. Awaiting user approval of the new normal, maximized, and restored previews; the ticket remains `claimed`.
