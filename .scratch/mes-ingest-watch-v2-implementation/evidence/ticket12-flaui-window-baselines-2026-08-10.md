# Ticket 12 — FlaUI journeys, real-window baselines, and gate evidence

## Evidence generations

| Generation | Authority | Evidence | Eligible for promotion |
| --- | --- | --- | --- |
| 2026-08-09 frozen Ticket 12 attempt | Historical diagnostic only; the issue comments record that its single `received` candidates predated the Ticket 11 reset | [`../issues/12-flaui-journeys-window-baselines-and-evidence.md`](../issues/12-flaui-journeys-window-baselines-and-evidence.md) | No |
| Ticket 11 selected-UI XAML matrix | User-approved D/E production UI, 19 PNG/XML scenarios, final v26 10/10 and 0 received | [`ticket11-regression-2026-08-09.md`](ticket11-regression-2026-08-09.md) | XAML baselines only |
| Ticket 12 pre-approval candidate diagnostic | Five terminal states were 10/10 byte-identical, but this matrix preceded the user's explicit preview approval | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12/run-20260810-085355-watch-window-stability/` | No; procedural history only |
| Ticket 12 pre-correction promotion diagnostic | Five matching bytes were copied and a single comparison passed, before review caught the ordering error | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12/run-20260810-090408-watch-window-visual/` | No; must be re-established in the required order |
| Ticket 12 invalid partial 50-run attempt | Four suites per run; stopped after review found the approval-order defect | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12/run-20260810-090549-watch-ui-stability/` | No runs count toward the release gate |
| Ticket 12 post-approval candidate matrix | Fresh candidate matrix after the user's approval and review fixes; 10/10 byte-identical | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12/run-20260810-093218-watch-window-stability/` | Approved and promoted |
| Ticket 12 promoted-baseline matrix | 10/10 comparisons against the promoted five-file matrix, 0 received | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12/run-20260810-094032-watch-window-promoted-stability/` | Active |
| Ticket 12 final 50-run gate | Fresh complete-gate count after all review fixes; 50/50 passed | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12/run-20260810-095809-watch-ui-stability/` | Release-gate eligible |

The frozen generation was not copied, renamed, hashed into, or otherwise used to create the active Ticket 12 matrix.

## Golden environment and source identity

All new Ticket 12 formal runs used the `gpt_win11` interactive scheduled-task path required by [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md): Session 1, Explorer and input desktop present, `1920x1080`, 96 DPI, light apps theme, `zh-CN`, `China Standard Time`, Microsoft YaHei UI and Consolas, and WPF `SoftwareOnly`. The run manifests pin source commit `0b56d3d68a57885aa1614250cb483e42ae9deff2`, the dirty source list, payload SHA-256, environment JSON, scheduled-task result, and cleanup result.

Ticket 11 reran the same current Wpf.Ui five-journey harness at 125% on the disposable offline clone; see the DPI section of [`ticket11-regression-2026-08-09.md`](ticket11-regression-2026-08-09.md). Ticket 12 independently rebuilt the 150% evidence on the disposable, network-disconnected `gpt_win11_ticket12_dpi150` clone. Its interactive probe proved `1920x1080`, 144 DPI, `zh-CN`, light theme, `China Standard Time`, required fonts, and `SoftwareOnly`; all five journeys passed. Evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12-dpi150/run-20260810-095140-watch-ui-journeys/`.

The 150% clone initially retained the source VM's saved runtime state and host-user ISO attachment, so its first cold start failed with an access-denied restore error. That red creation log is retained under `.artifacts/ticket12-dpi/`. The disposable clone alone was corrected by detaching the ISO and discarding its saved state, then cold-booted with the network still disconnected. After evidence retrieval, the clone, its scheduled tasks/processes, and the exact export/import directories were removed. The original `gpt_win11` then passed a fresh 1920x1080/96-DPI environment probe and `watch-vm-tests`; evidence: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-12-original-recheck/run-20260810-095536-watch-vm-tests/`.

## Journey and baseline results

The formal journey run at `run-20260810-084957-watch-ui-journeys` passed all five production-executable FlaUI.UIA3 journeys:

1. cold-start overview;
2. independent VISIBLE/GONE paging and demand details;
3. IngestAlert to exact TransportDemand navigation;
4. slow-request cancellation with the last successful result retained;
5. offline failure followed by a successful reconnect.

The host wrapper's outer wait expired after the guest task had already completed successfully. The scheduled task reported native result `0`; its Results and UI evidence were retrieved, and the task and residual process counts were both verified as zero. This was orchestration recovery, not a test retry, and it did not replace a failed gate.

The pre-approval diagnostic candidate run produced five byte-identical manifests for 10 consecutive runs. These hashes identify the reviewed previews, but the run is not used to satisfy the mandatory post-approval candidate gate:

| Baseline | SHA-256 |
| --- | --- |
| `alert-to-demand-1440x900.verified.png` | `7282C5B229B50D1089E849DBEB098C79F0829E1722880E61FC071E42C0FD1707` |
| `cold-start-overview-1440x900.verified.png` | `31DDEC2CB169DB91C1A692BA91DA7DC05B1CD453FB58FBEE77984E0FA4BAAE40` |
| `offline-reconnect-1440x900.verified.png` | `31DDEC2CB169DB91C1A692BA91DA7DC05B1CD453FB58FBEE77984E0FA4BAAE40` |
| `slow-request-cancel-1440x900.verified.png` | `4159E39B10E3FDD978652CB68ACD13B00BD212B58E8E813ED3B92A4BC04198FA` |
| `visible-gone-paging-details-1440x900.verified.png` | `BBED42D4867D864BC94B395FA3839189FCE403128F426BC39678E87749447AE8` |

The user reviewed the five final previews and replied `批准` on 2026-08-10. Review then identified that the first 10-run matrix occurred before that approval, while the mandatory order requires approval before a fresh candidate matrix. The initial promotion, its single comparison, and the subsequently started partial 50-run attempt are therefore retained but superseded. The scheduled task was stopped, unregistered, and left zero residual Watch/test processes.

After the review fixes, the post-approval matrix at `run-20260810-093218-watch-window-stability` produced the same five user-reviewed SHA-256 values for 10 consecutive runs. Fresh before/after/diff proposals record that equality and the user's review. Promotion re-established the same bytes, and `run-20260810-094032-watch-window-promoted-stability` passed 10 consecutive five-baseline comparisons with zero received files. The final 50-run complete gate starts from zero after those results.

## Failure and redaction contract

The entry point holds the global `MesIngestWatchUiTests` mutex and runs `watch-vm-tests`, `watch-xaml-visual`, `watch-ui-journeys`, and `watch-window-visual` serially. It exits on the first non-zero suite result and retains that result without automatic retry. Journey evidence contains fixed fake values only and redacts configured identifiers, authorization values, and sensitive query values from text artifacts. A failure bundle includes expected/actual/diff where applicable, received XAML from the XAML suite, step/failure screenshots, UIA tree, Watch logs, separate stdout/stderr, fake Host timeline and summary, failed step/exception/timeout, runner logs, and environment/manifests.

## Final gate

`run-20260810-095809-watch-ui-stability` completed all 50 consecutive runs at 2026-08-10 12:39:41 +08:00. Every run executed `watch-vm-tests`, `watch-xaml-visual`, `watch-ui-journeys`, and `watch-window-visual` in that order under the desktop mutex. Result: `status=PASSED`, `consecutivePasses=50`, `releaseGateEligible=True`, 50 run directories, zero received files, and zero non-zero-skip summaries. The wrapper unregistered the interactive task and reported zero residual Watch/test processes.

The separate full local solution run also passed. `MesIngest.Tests` ran 515 tests: 496 passed and the 19 named SQL Server environment tests skipped because no SQL Server/LocalDB was configured; those remain the explicit Ticket 13 release-environment gate already recorded by Ticket 11. `MesIngest.Watch.UiTests` ran 108 tests locally: 82 passed and 26 environment/guarded-runner checks skipped on the non-golden `en-US`, 150% host desktop. The corresponding XAML, environment, five-journey, and five-window checks all ran without skips inside each golden-machine complete-gate iteration.
