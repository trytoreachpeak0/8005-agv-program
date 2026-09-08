# 8005-agv-program

The programme's requirements, decisions and archive. **No code lives here** —
`mes/ingest/csharp/` and `rcs/riot-sdk/` were split out on 2026-09-02 into
`8005-mes-ingest` and `riot-sdk`, and this repository was renamed from
`8005---AGV` at the same time. What remains is the versioned requirements
baseline, the commercial agreements, the cross-subsystem ADRs, `CONTEXT.md`, and
the `.scratch/` decision archive. The `mes/` and `rcs/` directories still here
hold domain research material, not buildable projects.

Instructions for this repository. Historical tickets under `.scratch/` refer to
a root `AGENTS.md`; its content lives here now, and `.claude/rules/` holds the
parts that load only when Claude reads the files they govern.

## Repository write authority

The workspace root `CLAUDE.md` is the authority. In short: this repository,
`8005-agv-control-server`, `8005-mes-ingest` and `riot-sdk` are writable;
`8005-agv-onboard-hmi` and `slots-simulator` are read-only for agents;
`8005-agv-protocol` is writable but every pushed change must be announced to Kun
Wang in a `@SocialKKKK` issue. If that file is not loaded — a clone of this
repository on its own, outside the workspace — treat all three as read-only and
ask.

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
problem in this repository; give the user a concise owner notification and request
an explicitly writable tracking destination. This repository may retain only a
minimal routing/blocker pointer. If ownership is ambiguous, or an artifact
genuinely spans projects, stop and get an explicit destination repository
before writing it.

## Collaboration workflow

Two people drive this project. Kun Wang (GitHub `SocialKKKK`) owns
`8005-agv-onboard-hmi` and `slots-simulator`; Zhengyu Shao owns
`8005-agv-control-server`; `8005-agv-protocol` is jointly maintained. The full
account, written for humans and in Chinese, is
[`docs/collaboration-workflow.md`](docs/collaboration-workflow.md).

What an agent must follow:

- **The unit of collaboration is the integration slice.** Do not invent another
  one. `8005-agv-protocol/integration-slices/index.json` defines `W2G-IS-00`
  through `W2G-IS-07`, each with a `sequence` and `prerequisites`. Each slice's
  `gates` array *is* the division of labour: `G1` shared, `CONTROL_SERVER_G2`
  ours, `ONBOARD_HMI_G2` **ours too since 2026-09-04**, `G3` ours as well —
  **one person has run it since 2026-09-08**; all three runners are loopback and
  unattended, so "both people present" was governance, not a technical need, and
  nobody was left to satisfy it.
- **Cross-repository feedback takes one of three routes.** A contract ambiguity
  or error goes to an issue in `8005-agv-protocol` carrying the `vectorId` that
  triggered it. The other side failing the contract goes to an issue in *their*
  repository — **run G3 for evidence first** and attach the evidence directory.
  Work inside a repository stays in that repository's issues.
  **A cross-repository claim must carry reproducible gate evidence; "it does not
  work on my side" is not a report.**
- **`8005-agv-protocol` needs no advance approval** — Zhengyu Shao decides its
  content alone — **but every push must be announced in an issue that
  `@SocialKKKK`**, stating what changed, which `W2G-IS-*` slices it touches, and
  whether their `ONBOARD_HMI_G2` evidence is now void. **Announce in the same
  task as the push, not later.** Tagging a release still needs the two-owner
  attestation in `attestations/`; **AI and CI cannot approve.**
- **Batch protocol changes.** A patch release voids the affected G1/G2/G3
  evidence on both sides (`docs/release-governance.md`), so every small change
  costs the other side a full gate re-run.

## Language

Agent instruction files — this file, `.claude/rules/`, `docs/agents/` — are
written in **English**.

Everything a human reads is written in **Chinese**: README files, documentation
prose, issue and pull-request titles and bodies, and commit message bodies.

Stay English inside Chinese text: conventional commit prefixes (`feat:`, `fix:`,
`docs:`, `chore:`), identifiers, paths, commands, environment variables, error
codes, gate and slice names (`G1`, `W2G-IS-00`), and protocol message names,
schema fields and `vectorId` values — those are the contract itself. Quote an
error or a test result in its original English first, then explain it in
Chinese. Do not rewrite existing text to match; this governs new writing.

## Tests

There is nothing to build or test here. The test tiers and the golden WPF
renderer moved to `8005-mes-ingest` along with the code they govern; the
WIRE_TO_GATE gates (`G1`, `CONTROL_SERVER_G2`, `G3`, `RC`) live in
`8005-agv-control-server` and `8005-agv-protocol`.

If a task in this repository seems to need a build, it is probably in the wrong
repository — check the routing rules above.

## Claude Code

- Matt Pocock's engineering skills are installed as the `mattpocock-skills` plugin (user-level, from the `claude-plugins-official` marketplace). Invoke them namespaced: `/mattpocock-skills:<name>`.
- The ponytail skills live in `.claude/skills/` and are model-invocable — unlike the Matt skills, they can fire without being named.
- `code-review` collides with Claude Code's bundled `/code-review`. Use `/mattpocock-skills:code-review` for Matt's Standards+Spec review; bare `/code-review` (and `/code-review ultra`) stays the bundled one.
- Subagents are pre-authorised when a skill dispatches them as its own process — `/mattpocock-skills:code-review` fans Standards and Spec out in parallel. Exploration and search stay inline with Grep/Glob/Read, however broad the task sounds.
