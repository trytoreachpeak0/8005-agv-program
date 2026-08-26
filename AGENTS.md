## Agent skills

### Fast mode

Matt skills under `.agents/skills/` are explicit-only. Use one only when the
user names it directly (for example, `$diagnosing-bugs`, `/implement`, or
"use the prototype skill"). Ordinary requests should be handled directly.

When the user says "fast", "quick", "直接做", or "快速处理":

- Do not create issues, specs, ADRs, research notes, handoff documents, or
  other workflow artifacts unless the user asks for them.
- Do not start an interview, grilling flow, or optional sub-agent workflow.
- Inspect only the context needed for the request and run the narrowest useful
  validation.

Fast mode does not relax repository safety requirements, prototype-authority
rules, or the test-tier and Golden WPF renderer constraints below.

### Issue tracker

Issues and specs live as markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Wayfinder cross-repository routing

When Wayfinder discovers a defect or required change owned by another project,
the owning project's repository is the source of truth. Put the issue, primary
evidence, fix, tests, and project-specific handoff there, then commit and push
them to that repository. Do not keep those artifacts in `8005---AGV` merely
because its Wayfinder map exposed the problem. This repository may retain only
a concise map/ticket pointer to the owning repository's issue and pushed
branch/commit. If ownership is ambiguous, or an artifact genuinely spans
projects, stop and get an explicit destination repository before writing it.

### Triage labels

Default five-role vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: root `CONTEXT.md` + categorized `docs/adr/{cross,sdk,mes}/`. See `docs/agents/domain.md`.

### Prototype-authoritative implementation

When a ticket or user points to an existing prototype, selected variant, or
prototype-generated result, the selected prototype is the design authority for
layout and interaction unless the user explicitly asks to depart from it.

Before editing production UI:

1. Locate the actual final prototype source, not just its spec or screenshots.
   Search the working tree, all Git refs/history (`git log --all`,
   `git ls-tree`), registered worktrees, and saved evidence. Do not conclude
   that the source is absent merely because it is not on the current branch.
2. Run the selected prototype when possible and read its relevant XAML and
   code-behind. Identify the exact selected variant/commit before implementing.
3. Write a concrete prototype-to-production mapping for window hierarchy,
   grids, dimensions, spacing, controls, states, and interactions. Implement
   that structure with production data and terminology instead of designing a
   merely spec-compliant alternative.

`PROTOTYPE`, `throwaway`, “do not promote this XAML directly”, and “must not
be a production dependency” mean that prototype projects, fake data, and
prototype-only vocabulary must not ship. They do **not** mean that agents may
ignore or redesign an accepted prototype's XAML structure.

For visual approval, capture the production UI at the same meaningful state and
comparable viewport as the accepted prototype, then inspect them side by side.
A green test run or a successfully generated screenshot is not evidence of
visual parity. If the referenced prototype source or selected state still
cannot be found after the searches above, stop and ask the user before inventing
a replacement design.

### Test tiers

"Run the full test suite" means tier 1. It never means the golden renderer.
Skills that close a run with a full-suite pass (`/implement` and anything it
calls) stay in tier 1 unless the ticket asks for more.

Test authorization is scoped to the current task. A request to inspect, clean,
organize, commit, or push an already-dirty worktree does **not** authorize or
trigger tests merely because existing production-code or test-file changes are
present. Run tests only when the current task changes product code, tests, or
build inputs, or when the user explicitly asks for validation. Never infer test
authorization from `git status` alone.

| Tier | Command, from `mes/ingest/csharp` | Cost | Run it |
| --- | --- | --- | --- |
| 1 — handoff gate | `dotnet test MesIngest.Tests` | ~50 s of tests, ~2.5 min cold build, no VM | once before handing off a completed production-code change |
| 2 — UI preview | `.\Invoke-WatchUiTests.ps1 -Configuration Release -Suite <one suite>` | minutes, needs the interactive golden desktop | only when the change touches `MesIngest.Watch` UI |
| 3 — validation gate | `.\Invoke-GoldenRendererValidation.ps1`, `Test-*Stability.ps1 -Runs 3` | tens of minutes | only when the user asks to validate a ticket or promote a baseline |

- During implementation, run only the narrowest relevant test selection needed
  for feedback. Prefer a class or method filter when it covers the changed
  behavior.
- Before handing off a production-code change implemented in the current task,
  run tier 1 once. Do not repeat tier 1 unless production code, tests, or
  relevant inputs changed after that run.
- Documentation, agent configuration, and other non-product changes do not
  require tier 1 unless the user asks for it or the change can affect the build.
- Do not enter tier 2 or tier 3 on your own initiative. Ask first, and say what
  it costs.
- Pick the narrowest suite that covers the change. `-Suite all` is not a
  default, and `-Class`/`-Method` narrow one suite further; see
  `docs/agents/golden-renderer.md`.
- `-Runs 3` is step 5 of the approval order in `docs/agents/golden-renderer.md`.
  It belongs to baseline promotion, not to implementation.
- Tier 1 skips the SQL Server tests unless three environment variables are set:
  `MES_INGEST_TICKET01_SQLSERVER` (a real instance — LocalDB is rejected on
  purpose), `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`, and
  `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL`. Without them the run still
  reports `Failed: 0` while silently skipping 88 tests, so a change to any SQL
  in `SqlServerMesIngestProjection.*.cs` is not covered — check the skip count,
  not just the failure count. That is acceptable in tier 1 only; tier 3 evidence
  must still name every skip.

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
