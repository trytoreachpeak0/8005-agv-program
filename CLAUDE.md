# 8005---AGV

Instructions for this repository. Historical tickets under `.scratch/` refer to
a root `AGENTS.md`; its content lives here now, and `.claude/rules/` holds the
parts that load only when Claude reads the files they govern.

## Repository write authority

The workspace root `CLAUDE.md` is the authority. In short: this repository is
writable; `8005-agv-onboard-hmi` and `slots-simulator` are read-only for
agents; `8005-agv-protocol` is writable but every pushed change must be
announced to Kun Wang in a `@SocialKKKK` issue. If that file is not loaded — a
clone of this repository on its own, outside the workspace — treat all three as
read-only and ask.

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

## 协作工作流

项目由两个人推进：Kun Wang（GitHub `SocialKKKK`）负责 `8005-agv-onboard-hmi` 与
`slots-simulator`；Zhengyu Shao 负责 `8005-agv-control-server`；`8005-agv-protocol`
共同维护。完整说明见 [`docs/collaboration-workflow.md`](docs/collaboration-workflow.md)。

Agent 必须遵守的部分：

- **协作单位是 integration slice**，不要自己发明推进单位。
  `8005-agv-protocol/integration-slices/index.json` 定义了 `W2G-IS-00` 到 `W2G-IS-07`，
  每个带 `sequence` 与 `prerequisites`。每个切片的 `gates` 就是分工：`G1` 双方共用、
  `CONTROL_SERVER_G2` 我方、`ONBOARD_HMI_G2` 对方、`G3` 两人一起。
- **跨仓库反馈分三条路**：协议契约的歧义或错误 → `8005-agv-protocol` 的 issue，附
  触发它的 `vectorId`；对方实现不符合契约 → **对方仓库**的 issue，**必须先跑 G3 拿
  证据**并附上 evidence 目录；自己仓库的活 → 自己仓库的 issue。
  **跨仓库指控必须带可复现的门禁证据，不能只是"我这边跑不通"。**
- **改 protocol 由 Zhengyu Shao 单独决定，不需要事先批准**，但**每次推送都要在
  `8005-agv-protocol` 开 issue @`SocialKKKK` 通知**，写清改了什么、影响哪些
  `W2G-IS-*` 切片、他的 `ONBOARD_HMI_G2` 证据是否作废。**通知要和推送在同一个任务里
  完成，不能拖到以后。**发布（打 tag）仍需双人签名走 `attestations/` 那套机制，
  **AI 和 CI 不能批准**。
- **协议改动要攒批次。** 补丁发布会作废两边受影响的 G1/G2/G3 证据
  （`docs/release-governance.md`），每一次小改都在让对方重跑整套门禁。

## 语言约定

写进 GitHub 的东西用中文：README、文档正文、issue 标题与正文、PR 标题与正文、
commit message 正文。

保持英文：commit 的 conventional 前缀（`feat:` `fix:` `docs:` `chore:`）、标识符、
路径、命令、环境变量、错误码、门禁与切片名（`G1`、`W2G-IS-00`）、协议消息名与
schema 字段与 `vectorId`（它们是契约的一部分，改不得）。引用报错和测试输出时先贴
英文原文，再用中文解释。不回溯改旧的。

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
| 3 — validation gate | `.\Invoke-GoldenRendererValidation.ps1`, `Test-*Stability.ps1 -Runs 3` | tens of minutes | **only when cutting a release candidate, or when the user explicitly asks to promote a visual baseline** |
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
- Tier 3 is deliberately narrow: it runs when cutting a release candidate or on
  an explicit request to promote a baseline, never on an ordinary ticket. Its one
  irreplaceable job is catching intermittent defects — the Ticket 23 antialiasing
  flip appeared in ~12% of runs, which 3 runs miss about a third of the time — and
  that job does not arise in day-to-day work. A ticket that changes Watch UI stops
  at tier 2 plus the user's preview approval.
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
