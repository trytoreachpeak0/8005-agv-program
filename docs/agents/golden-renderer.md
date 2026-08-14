# Golden WPF renderer

This runbook is the repository-wide validation contract for tickets that change
`MesIngest.Watch` UI, XAML, Wpf.Ui controls, visual layout, UI Automation, DPI
behavior, or screenshot/XAML baselines.

## Machine contract

| Item | Required value |
| --- | --- |
| Hyper-V VM | `gpt_win11` |
| Guest host | `GPT-WIN11` |
| Interactive user | `GPT-WIN11\gpt` |
| Desktop | 1920x1080, 100% / 96 DPI |
| Locale / timezone | `zh-CN` / `China Standard Time` |
| Theme | Windows apps light theme |
| Fonts | Microsoft YaHei UI and Consolas |
| WPF rendering | `SoftwareOnly` |
| PowerShell | 7.x |
| .NET SDK | 8.0.423 |
| Offline NuGet cache | `C:\MesIngest\Ticket11\NuGetPackages` |

The host-side PowerShell Direct credential is stored outside the repository:

```text
%LOCALAPPDATA%\MesIngestWatch\gpt_win11.credential.xml
```

Do not put the guest password, an exported credential, or any other secret in
the repository, ticket comments, logs, or validation artifacts.

## Connection rules

- Use Hyper-V Basic Session only when a human must inspect the real desktop:
  `vmconnect.exe localhost gpt_win11`.
- Do not use RDP or Hyper-V Enhanced Session. They can change desktop session,
  resolution, scaling, font rasterization, and screenshot output.
- Use PowerShell Direct to copy files, register/monitor tasks, and retrieve
  evidence. A PowerShell Direct process is not the interactive desktop and must
  not capture WPF screenshots or drive FlaUI.
- Keep one `PSSession` for a validation run instead of reconnecting repeatedly.
- Never run two desktop suites in parallel.

## Standard entry points

Run from `mes\ingest\csharp` inside the interactive guest session:

```powershell
.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite watch-vm-tests
.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite watch-xaml-visual
.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite watch-ui-journeys
.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite watch-production-preview
.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite watch-window-visual
.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite all
```

`watch-production-preview` runs `watch-vm-tests` followed by the production
`watch-ui-journeys` inside one payload deployment and desktop-mutex lease. It is
the implementation-train preview entry point: it does not run either baseline
comparison suite and does not create, promote, or approve a baseline.

The 19-scenario Verify.Xaml stability gate is:

```powershell
.\Test-WatchXamlBaselineStability.ps1 -Configuration Release -Runs 10
```

For normal host-side orchestration, use the repository wrapper:

```powershell
.\Invoke-GoldenRendererValidation.ps1 `
    -Ticket 12 `
    -Suite watch-ui-journeys
```

The wrapper creates an isolated guest run directory, excludes local build/test
outputs from the payload, registers an `Interactive` scheduled task, waits for
completion, retrieves results, unregisters the task, and cleans residual test
processes. It never changes an approved baseline.

## Required environment gate

The interactive task must run `Test-GoldenRendererEnvironment.ps1` before the
suite. Formal 100% visual runs require all of the following:

- Explorer and an input desktop in the same interactive session;
- 1920x1080 desktop and 96 DPI;
- light apps theme;
- `zh-CN` culture and UI culture;
- `China Standard Time`;
- Microsoft YaHei UI and Consolas;
- `MesIngestWatch__RenderingMode=SoftwareOnly`.

If any condition differs, stop before producing `received` files or new
baselines. Retain the environment report as red evidence.

## Approval and baseline order

For visual changes, the order is mandatory:

1. Run code/non-pixel regressions.
2. Generate real golden-machine previews for all affected pages/states.
3. Show the final preview images to the user and obtain explicit approval.
4. Generate a fresh candidate matrix; do not bulk-promote historical candidates.
5. Run the candidate matrix 10 consecutive times and require byte-identical PNG
   and XML output.
6. Produce per-scenario before/after/diff evidence.
7. Promote only the explicitly approved candidate.
8. Run the same 10-run command against the promoted baselines and require
   `0 received`.

A later UI change invalidates an earlier visual approval. Test-only
normalization may reuse approval only when all approved PNG SHA-256 hashes remain
identical; record that comparison in evidence.

Never hide a red run with a successful rerun. Keep the first failure, explain
the cause, add a regression test when possible, and restart the required
consecutive-run count from one.

## DPI validation

Do not change the calibrated `gpt_win11` desktop away from 100% for Ticket-level
DPI work. Export/import a disposable clone with a new VM ID, disconnect its
network adapter before boot, and change DPI only inside the clone.

- 125% means 120 DPI.
- 150% means 144 DPI.
- The interactive environment report must prove the effective DPI; registry
  values observed through PowerShell Direct are not sufficient.
- Run `watch-ui-journeys` at each required scale.
- Retrieve evidence, remove scheduled tasks and residual processes, stop and
  delete the clone, then remove the exact export/import directories.
- Recheck the original VM is 1920x1080, 96 DPI, Explorer is in Session 1, and no
  Ticket test task/process remains.

## Evidence contract

Use a unique directory per attempt; never overwrite earlier evidence:

```text
C:\MesIngest\<Ticket-or-purpose>\run-YYYYMMDD-HHmmss\
<repo>\.artifacts\golden-renderer\ticket-<NN>\run-YYYYMMDD-HHmmss\
```

Record at least:

- source commit and dirty-diff identity;
- environment JSON;
- scheduled-task result and native exit code;
- restore/build/test logs;
- screenshots, UIA trees, Verify XML, and received/diff files when applicable;
- pass/fail/skip counts, with every skip named and assigned to a release gate;
- user approval message for visual candidates;
- cleanup and original-VM restoration result.

Expected offline `NU1801`/`NU1603` warnings remain in logs. They are not failures
when restore/build/test exits successfully, and they must not be suppressed.

## Ticket checklist

Every affected ticket should contain:

```md
- [ ] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
```
