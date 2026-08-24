# Ticket 23 — shared golden-machine UI integration acceptance, evidence index

Single non-overwriting index for the Ticket 19–22 integration train. Every run directory
below is unique and none was reused or overwritten. Earlier red evidence from the
root-cause investigation is preserved untouched under `.artifacts/ticket23-rootcause/`.

## Source identity

| Item | Value |
| --- | --- |
| Branch | `factory-validation` |
| Commit at capture | `5b32ace` — *feat(watch): bound golden-renderer equivalence and clear ticket 23 regressions* |
| Dirty at capture | `docs/agents/golden-renderer.md`, `WatchWindowVisualEquivalence.cs` (XML doc comments), `New-WatchWindowBaselineProposal.ps1` (new optional parameter) |
| Golden VM | `gpt_win11`, id `7d804f09-8e93-48f9-9bff-07e85f6adc45` |
| Environment | 1920x1080, 96 DPI / 100%, light theme, zh-CN, China Standard Time, SoftwareOnly, Explorer + input desktop in session 1 |

The three dirty files cannot affect rendering. That is not asserted — it is proven by
`candidate-identity-vs-approval.json`, which shows all 110 candidate PNGs byte-identical to
the approved preview captured before those edits.

## Runs

| Phase | Evidence directory | Result |
| --- | --- | --- |
| Preview (vm-tests + journeys) | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-23-acceptance-preview/run-20260819-001953-watch-production-preview` | PASSED — 227 tests 0 failed 5 skipped; journeys 1/0/0 |
| Candidate stability, 10 runs | `.../ticket-23-candidate-gate/run-20260819-010449-watch-window-stability` | PASSED — 110 PNGs byte-identical, 0 tolerated |
| Promoted stability, 10 runs | `.../ticket-23-promoted-gate/run-20260819-013127-watch-window-promoted-stability` | PASSED — `0 received`, 1 tolerated step reviewed |
| DPI 125% (120 DPI) | `.../ticket-23-dpi-120/run-20260819-083824-watch-ui-journeys` | PASSED |
| DPI 150% (144 DPI) | `.../ticket-23-dpi-144/run-20260819-084741-watch-ui-journeys` | PASSED |
| Final VM recheck at 96 DPI | `.../ticket-23-final-vm-recheck/run-20260819-085538-watch-vm-tests` | PASSED — 227 tests 0 failed 5 skipped |
| Verify.Xaml stability, 10 runs | `.../ticket-23-xaml-gate/run-20260819-090314-watch-xaml-stability` | **FAILED** — run 6 differs; diagnosed and fixed below |
| Verify.Xaml stability after fix, 3 runs | `.../ticket-23-xaml-gate-fixed-2/run-20260819-105020-watch-xaml-stability` | PASSED |
| 720 epx at 100% | `.../ticket-23-epx-720-baseline-96dpi-v2/run-20260819-113728-watch-ui-journeys` | PASSED — 720x600 epx |
| 720 epx at 125% | `.../ticket-23-epx-720-dpi-120/run-20260819-115708-watch-ui-journeys` | PASSED — 900x750 physical = 720x600 epx |
| 720 epx at 150% | `.../ticket-23-epx-720-dpi-144/run-20260819-115136-watch-ui-journeys` | PASSED — 1080x900 physical = 720x600 epx |
| Final VM recheck after the 720 epx phase | `.../ticket-23-final-vm-recheck-after-720epx` | PASSED — 228 tests 0 failed 5 skipped |

Every run records its own scheduled-task result, native exit code, restore/build/test logs,
environment JSON before and after, screenshots, UIA tree, and cleanup JSON.

## User approvals

| What | Where | Message |
| --- | --- | --- |
| Final real-window preview, 11 states | `ticket-23-acceptance-preview/run-20260819-001953-watch-production-preview/user-approval.json` | 批准，继续候选门禁与提升 |
| Tolerance-accepted step, human review | `ticket-23-promoted-gate/run-20260819-013127-watch-window-promoted-stability/tolerance-review.json` | 接受，这正是预期行为 |

The 2026-08-18 09:55 approval was **superseded**, not reused: it covered an aliased-text
experiment at commit `2280c62` that was reverted. The reasoning is recorded in the
approval file rather than left implicit.

## Baseline promotion

11 initial baselines promoted to `MesIngest.Watch.UiTests/WindowBaselines/`, one per state
of `WatchProductionBaselineMatrix`. Proposals with `before=(none)`, after, diff and the
environment manifest are under
`ticket-23-candidate-gate/run-20260819-010449-watch-window-stability/baseline-proposals/`.
No pre-existing baseline was overwritten; the promotion step refuses to.

`-Runs` was **10**, not the new default of 3. Reason, per the "Repetition count" section of
`docs/agents/golden-renderer.md`: a baseline was being promoted for eleven journeys that are
all new. The predicate classifies the known antialiasing flip rather than needing repetition
to find it, so this count is about the weight of a first promotion, not about detection.

## Tolerance accounting

| Gate | Runs | Steps accepted by tolerance | Pixels |
| --- | --- | --- | --- |
| Candidate | 10 | 0 | 0 |
| Promoted | 10 | 1 (`run-09`, `07-current-ingest-attention`) | 116 of 1536 allowed |

The single accepted step is the defect this ticket exists for: the `跳转` glyph of
`CurrentAttentionGoToPageButton`, 116 pixels in 8 regions inside x 326–353 / y 856–867,
achromatic, deltas of 1 and 2 only, ink support unchanged, button chrome byte-identical.
Under the previous byte-exact rule that run would have failed and blocked the promotion of
output the maintainer had already approved. Magnified 10x crops were shown before the
decision and are stored beside the record.

## Verify.Xaml stability gate — red, diagnosed, fixed, re-run green

Resolved. The red is preserved in full rather than rerun away; the fix and its regression
test are below, and the clean re-run is
`ticket-23-xaml-gate-fixed-2/run-20260819-105020-watch-xaml-stability` — PASSED, 3 runs.

`ticket-23-xaml-gate/run-20260819-090314-watch-xaml-stability` failed at run 6 of 10:

```
Visual artifacts are not deterministic: run 1 differs from run 6.
Files: overview-loaded-2560x1440.received.png
```

What it is, from the retained artifacts:

| Fact | Value |
| --- | --- |
| Scenario | `overview-loaded` at 2560x1440, `WatchVisualState.OverviewHealthy` |
| Surface | `MesIngest.Watch/MainWindow.xaml` — the legacy Watch window, **not** the Ticket 19–22 `WatchWorkspaceWindow` |
| Runs affected | 1 of 10 (run 6); the other 9 share one hash |
| Differing pixels | 695,918 of 3,686,400 — 18.88% of the frame |
| Max per-channel delta | 166 |
| Chromatic pixels | all 695,918 — dominant delta `(-65,-25,-2)` on 687,468 of them |
| Bounding area | x 1383–2547, y 799–1398 |
| Visual-tree XML | **byte-identical** between the two runs |

Visually: the `OverviewDemandsButton` card ("VISIBLE TransportDemand") renders with a blue
accent fill instead of its `Background="White"`. Crops are stored beside the run as
`xaml-diff-run01.png` and `xaml-diff-run06.png`.

This is **not** the antialiasing class the visual-equivalence predicate accepts, and the
predicate would reject it on rules 3, 4, 5 and 6. Nothing here argues for widening a bound.
It is the other thing repetition exists for, named in "Repetition count": genuinely
intermittent behaviour — an interaction state reaching the capture.

Leading cause: `WatchXamlVisualTests` performs no pointer or focus neutralisation before
capture. Grepping the suite and `WatchVisualCaptureConverter` finds no `SetCursorPos`, no
cursor handling and no focus reset, whereas the window path calls `MovePointerOffWindow()`,
settles 2000 ms, and requires three consecutive byte-identical `PrintWindow` frames
(`WatchWindowCaptureStability`). A Wpf.Ui button's hover or focus visual overrides a local
`Background` through its control template, and that state is rendered but not serialised —
which is exactly the observed signature: identical XML, large chromatic raster difference.

Impact on the promoted work: none. The 11 promoted baselines are `WatchWorkspaceWindow`
captures whose own gates were green at 10 runs each with `0 received`. This scenario belongs
to the legacy MainWindow surface and was not promoted, altered, or approved here.

Choosing `-Runs 10` is what surfaced it. At the default of 3 a 1-in-10 defect has about a
73% chance of going unseen.

### Fix

`WatchVisualScenario.CreateCaptureTarget` now clears mouse capture and focus and calls
`Mouse.Synchronize()` before the content leaves the window. Ordering is the whole fix: the
focus scope is the window, so clearing after reparenting leaves `IsFocused` set — the first
attempt did exactly that and the new test caught it.

Regression test:
`WatchXamlVisualTests.Capture_target_carries_no_hover_capture_or_focus_state` puts the card
into the focused state and asserts the capture surface carries no capture, focus or hover.

### Cost of the gate, measured

`ticket-23-xaml-gate-fixed-2`, three iterations on `gpt_win11`:

| Phase | Cost |
| --- | --- |
| restore | ~30 s on iteration 1, skipped after (`-ReuseBuild`) |
| `dotnet run` evaluation | 4.4 s, or 1.8 s with `--no-build`; the built exe starts in 0.7 s |
| xUnit reported test time | 38.6 s |
| **last capture written → process exit** | **5.6–6.0 min** |
| total per iteration | ~7.3 min |

The dead time at exit is ~80% of every iteration and is **unexplained**. Build, restore and
`dotnet run` evaluation were each measured and are seconds; the STA threads are
`IsBackground` with a 30 s cap, so they are not holding the process either. This wants its
own ticket, not a guess.

`-ReuseBuild` was added on the assumption that build dominated. That assumption was wrong —
it saves ~30 s per iteration, not minutes. The switch is kept because it is correct and
free, but the honest lever today is `-Runs`: 3 costs ~22 min where 10 cost ~77.

## Named skips and their release gates

| Skip | Count | Release gate |
| --- | --- | --- |
| `WatchWindowCandidateEquivalenceTests.Candidate_directories_are_visually_equivalent` | 1 | Driven by `Test-WatchWindowBaselineStability.ps1`; runs whenever two candidate runs are not byte-identical. Skips by design otherwise. |
| `WatchWindowVisualEquivalenceGoldenFixtureTests` | 4 | Real captures live outside the guest payload. Gate: host-side run with `MESINGEST_WATCH_GOLDEN_FIXTURES` set — 14 passed on 2026-08-19. |

`MesIngest.Tests` skips 99 of 919 host-side; those are the SQL Server suites, gated by the
per-ticket `Invoke-TicketNNSqlServerGate.ps1` scripts, unchanged by this ticket.

## Known failures carried, by maintainer decision

| Test | Owner | Why not fixed here |
| --- | --- | --- |
| `InstallPackageLayoutTests.Install_doc_describes_production_v2_release_smoke_without_claiming_v1_openapi_or_watch` | Ticket 24/25 | `pack/INSTALL.md` now mentions `/openapi/v1.json` precisely to require it return 404; the assertion is a blanket `DoesNotContain`. Packaging scope, not the UI train. |

## Non-pixel regressions fixed to clear the gate

- `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age` — aged its fixture with the wall clock while the telemetry ran on an injected 2026-07-31 clock, so it began failing on 2026-08-10 independent of any change.
- `WatchAreaFilterProfileTests.Every_profile_transaction_fails_busy_without_blocking_the_caller` — timed a 500 ms budget from `Task.Run`, measuring thread-pool scheduling latency; failed on whichever parameter queued behind the STA UI tests.
- `WatchV2ProductionShellTests.Demand_series_page_...at_720_epx` — still asserted the pre-`0024945` DemandSeries list. Aligned to the approved prototype hierarchy that shipped, per maintainer decision.

## DPI validation

See `.artifacts/ticket23-dpi/dpi-findings.json`. Disposable clone `gpt_win11_ticket23_dpi`,
new VM id `4e3e5252-b7be-412e-b557-3b0253dcc446`, network disconnected, disks isolated to
its own import root and asserted not shared with the source.

Effective DPI is proven by the interactive environment report at both scales, before and
after each suite — not by a registry read over PowerShell Direct, which the runbook says is
insufficient.

Scope honesty: the original 1440x900 runs proved reflow and scrolling at 125% and 150% but
did **not** exercise the 720 epx width floor — their narrowest client was 960x600 epx. That
gap was closed afterwards on a second clone (`gpt_win11_ticket23_dpi720`, new VM id
`83b0777b`) using `-JourneyClientEpx 720x600`, which pins the client in effective pixels so
the width under test no longer follows the machine's scaling. 720x600 epx passes at 100%,
125% and 150%, each with the effective DPI proven by the interactive environment report.

Deviation recorded: the host has 15.3 GB RAM and `gpt_win11` holds a static 4 GB, so the
clone could not boot alongside it. With maintainer approval the golden machine was shut down
gracefully for the DPI phase and restarted afterwards — a power cycle, not a calibration
change. Its Hyper-V automatic checkpoint merged into the parent VHDX on shutdown, which is
normal and preserves guest state.

## Cleanup

| Item | State |
| --- | --- |
| Scheduled tasks on `gpt_win11` | none — the 8 stale tasks left by tickets 1/10/12 were removed with maintainer approval |
| Residual Watch/test processes | none |
| DPI clone | removed |
| `F:\ticket23-dpi-export-20260819`, `F:\ticket23-dpi-import-20260819` | removed; ~167 GB reclaimed |
| Original VM | 1920x1080, 96 DPI / 100%, light, zh-CN, CST, SoftwareOnly, Explorer + input desktop in session 1 — proven by the final recheck |

VM `gpt_win11_ticket23_unstable_backup` was removed on maintainer instruction, together with
its two disks in `F:\virtual_hard_disks\` (`gpt_win11.vhdx` and its differencing
`...BD96E874....avhdx`), reclaiming about 65 GB. Before deleting, the live `gpt_win11` disk
chain was walked to its parent and checked against the deletion list, and every VM on the
host was enumerated to confirm nothing else referenced those two files — `rocky_9_minimal`
and `windows_server_2022_100` share that directory but use their own disks and were left
alone. After deletion the live VM remains Running on
`F:\ticket23-font-import-20260818\Virtual Hard Disks\`.

Guest payload directories are removed: 29 of them (`23`, `23-*`, `ticket-23-preview-v2`,
`Ticket23FontCalibration`), leaving zero ticket-23 directories under `C:\MesIngest` and
83 GB free on the guest system drive. The deletion was scoped by name to this ticket only —
other tickets' payloads and the offline `Ticket11\NuGetPackages` cache were verified intact
afterwards, along with zero scheduled tasks and zero residual processes.

An earlier attempt was refused by a repository safety hook and was not worked around; the
directories were left in place and recorded as outstanding until the maintainer asked for
them to be cleared.

A cleanup note worth carrying forward: the scheduled-task purge used a `*MesIngest*`
wildcard, which also matched the recheck task that was live at that moment. It happened to
be harmless — the wrapper had already unregistered its own task and the run had completed
successfully — but the wildcard was broader than it should have been. Scope such a purge to
names that cannot match a running wrapper task.

## Cross-links

Tickets 19, 20, 21 and 22 share this acceptance. They do not each repeat the candidate
stability, post-promotion stability, or DPI clone procedure; they reference this directory.

- Ticket 19 — production Fluent shell, settings and overview: states `01`, `01e`, `01f`, `02`, `02v`
- Ticket 20 — DemandSeries production page: state `03`
- Ticket 21 — readability audit and AREA Variant A: states `04`, `05`
- Ticket 22 — Error Search Variant A and ingest attention: states `06`, `07`, `08`
- Root-cause investigation for the antialiasing flip: `.artifacts/ticket23-rootcause/EVIDENCE-01-static-forensics.md`
- Predicate contract and repetition guidance: `docs/agents/golden-renderer.md`
- Gate policy: `mes/ingest/csharp/MesIngest.Watch.UiTests/UI-GATE-POLICY.md`

## Re-validation rule

Per the ticket: after this point, only a change that alters visual, XAML, UI Automation or
DPI output — or a scenario failure — re-triggers the affected scenarios and invalidates the
corresponding approval and consecutive count. Backend, documentation and packaging changes
that do not touch UI output must not trigger a full revalidation.
