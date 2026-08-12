## Agent skills

### Issue tracker

Issues and specs live as markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-role vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: root `CONTEXT.md` + categorized `docs/adr/{cross,sdk,mes}/`. See `docs/agents/domain.md`.

### Golden WPF renderer

Any ticket that changes `MesIngest.Watch` UI, XAML, Wpf.Ui controls, layout,
UI Automation, DPI behavior, or visual baselines must read
`docs/agents/fluent-ui.md` and `docs/agents/golden-renderer.md` before
implementation and validation. The Fluent rules are mandatory acceptance
criteria, not optional visual guidance.

- Formal WPF visual validation runs on Hyper-V VM `gpt_win11` through an
  interactive scheduled task. PowerShell Direct is only for deployment,
  monitoring, and artifact retrieval.
- Keep the calibrated VM at 1920x1080 and 100% / 96 DPI. Do not use RDP or
  Hyper-V Enhanced Session. Use a disposable offline clone for 125%/150% DPI.
- Never approve or overwrite visual baselines before the user reviews the final
  golden-machine preview. Preserve red evidence and clean test tasks/processes.
