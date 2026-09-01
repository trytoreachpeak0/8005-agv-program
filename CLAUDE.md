# 8005---AGV

Instructions for this repository. Historical tickets under `.scratch/` refer to
a root `AGENTS.md`; its content lives here now, and `.claude/rules/` holds the
parts that load only when Claude reads the files they govern.

## Repository write authority

The workspace root `CLAUDE.md` is the authority. In short: this repository is
writable; `8005-agv-onboard-hmi` and `slots-simulator` are read-only for
agents; `8005-agv-protocol` needs approval from both Zhengyu Shao and Kun Wang
before any write. If that file is not loaded — a clone of this repository on its
own, outside the workspace — treat those three as read-only and ask.

## Agent skills

### Fast mode

Matt Pocock's skills ship as the `mattpocock-skills` plugin and are
explicit-only. Use one only when the user names it directly (for example,
`/mattpocock-skills:diagnosing-bugs`, `/mattpocock-skills:implement`, or "use
the prototype skill"). Ordinary requests should be handled directly.

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

### Triage labels

Default five-role vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: root `CONTEXT.md` + categorized `docs/adr/{cross,sdk,mes}/`. See `docs/agents/domain.md`.

## Cross-repository problem routing

When Wayfinder discovers a defect or required change owned by another project,
first apply the protected-repository policy above. If writes are allowed, the
owning project's repository is the source of truth: put the issue, primary
evidence, fix, tests, and project-specific handoff there, then commit and push
them to that repository. If the owning repository is read-only or lacks the
required approvals, do not write there and do not fall back to storing the full
problem in `8005---AGV`; give the user a concise owner notification and request
an explicitly writable tracking destination. This repository may retain only a
minimal routing/blocker pointer. If ownership is ambiguous, or an artifact
genuinely spans projects, stop and get an explicit destination repository
before writing it.

## Test tiers

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
- Tier 1 skips the SQL Server tests unless three environment variables are set:
  `MES_INGEST_TICKET01_SQLSERVER` (a real instance — LocalDB is rejected on
  purpose), `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`, and
  `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL`. Without them the run still
  reports `Failed: 0` while silently skipping 88 tests, so a change to any SQL
  in `SqlServerMesIngestProjection.*.cs` is not covered — check the skip count,
  not just the failure count. That is acceptable in tier 1 only; tier 3 evidence
  must still name every skip.

## Claude Code

- Matt Pocock's engineering skills are installed as the `mattpocock-skills` plugin (user-level, from the `claude-plugins-official` marketplace). Invoke them namespaced: `/mattpocock-skills:<name>`.
- The ponytail skills live in `.claude/skills/` and are model-invocable — unlike the Matt skills, they can fire without being named.
- `code-review` collides with Claude Code's bundled `/code-review`. Use `/mattpocock-skills:code-review` for Matt's Standards+Spec review; bare `/code-review` (and `/code-review ultra`) stays the bundled one.
- Subagents are pre-authorised when a skill dispatches them as its own process — `/mattpocock-skills:code-review` fans Standards and Spec out in parallel. Exploration and search stay inline with Grep/Glob/Read, however broad the task sounds.
