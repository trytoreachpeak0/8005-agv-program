# Shared workspace rules

A workspace of independent git repositories, not a monorepo. Each subdirectory
is its own clone with its own remote — stage, commit, and push one repository at
a time, and never assume a change in one is visible to another.

Each repository carries its own `CLAUDE.md` with the rules for working inside
it, and Claude Code loads those only once it reads a file in that directory.

This file is the authority on write access and applies from the start of every
session. Where a repository restates any of it, this file wins.

The content is moved unchanged from `8005-workspace@727b52a`. Where a rule here
conflicts with an override sentence in a workspace's own `CLAUDE.md`, that
override sentence wins for that workspace.

## Repository write authority

Identified by remote, not by directory name. These rules apply to each remote
below and to every local clone or worktree whose `origin` resolves to it,
wherever it sits on disk.

| Remote under `github.com/trytoreachpeak0/` | Authority |
| --- | --- |
| `8005-agv-program` | Writable — requirements, cross-subsystem ADRs, decision archive. No code |
| `8005-agv-control-server` | Writable — WIRE_TO_GATE server |
| `8005-mes-ingest` | Writable — MesIngest service and its Watch client |
| `riot-sdk` | Writable — RIoT SDK, C# and Python |
| `8005-agv-onboard-hmi` | Writable **on `w2g/*` branches only** — never `OnboardHmi_MVP` |
| `slots-simulator` | Writable **on `w2g/*` branches only** — never `main` |
| `8005-agv-protocol` | Writable — no announcement duty since 2026-09-08 |
| `8005-test-lab` | Writable — agent-first multi-machine test lab; decisions only until its `wayfinder:map` issue clears |

### Branch-scoped write

`8005-agv-onboard-hmi` and `slots-simulator` were read-only for agents until
2026-09-04. **The development work on both is now ours** — Kun Wang is no longer
expected to carry them. What replaced the old rule is narrower than "writable":

- **Work only on `w2g/*` branches.** Create them, commit to them, push them.
  The local worktree is now ours to edit, which it was not before.
- **Never push to their working branch** — `OnboardHmi_MVP` for the onboard HMI,
  `main` for the simulator. Never force-push anything there, never delete or
  rewrite a branch that is not ours, never tag or release.
- **Changes still arrive as a pull request** into that working branch, and
  **since 2026-09-09 both the agreement and the merge are ours.** The pull request
  is not ceremony: it is still where a change is reviewed, where its evidence is
  recorded, and what the slice board points at. What it is no longer is a gate
  somebody outside this workspace holds.

  This rule moved twice, and the second move is the one to remember. Until
  2026-09-08 a merged PR was "a decision, not a delivery" — Kun Wang clicked
  merge. That day the click moved to us while **his agreement was still
  required**. On 2026-09-09 the user removed that requirement too, on exactly the
  grounds that moved the release signature: he took over Kun Wang's project
  outright, so a rule demanding an approval nobody is there to give does not hold
  a line — it just stalls work, and gets worked around instead of followed.

  Everything else about those branches is unchanged: **never push to
  `OnboardHmi_MVP` or `main` directly** — a change still gets there by opening a
  PR and merging it, never by pushing — never force-push, never delete or rewrite
  a branch that is not ours, never tag or release.
- Issues, pull requests and comments stay allowed, as they have been since
  2026-09-03.

Two consequences worth knowing before they bite:

- **A dirty worktree in either repository aborts an L2 run.**
  `Get-L2PeerPublish` publishes both peers from a throwaway clone of the local
  repository and refuses a dirty source rather than testing uncommitted state
  behind your back. That check used to be free — nothing wrote there. Now it is
  a thing to remember: commit to your `w2g/*` branch before running L2.
- **Their `CLAUDE.md` and `docs/` are still their documents.** Changing how those
  repositories describe themselves is a different act from fixing their code;
  it belongs in a PR he actually asked for, not in passing.

**`ONBOARD_HMI_G2` moved to us on 2026-09-04.** It was deliberately left open when
development transferred — taking over the code does not by itself move a gate —
and the user then decided that it does move. We run that gate and fill in that
column now; the board no longer waits on Kun Wang for it.

**Release signing moved too, on 2026-09-08.** It had not: this paragraph used to
say that taking over both G2 gates was "not a path to signing alone", and that
Kun Wang remained the mandatory second signature. The user then took over his
project outright, which left the rule demanding a signature nobody could give —
and a rule like that does not hold the line, it just gets worked around. So the
rule changed rather than being bypassed: `docs/release-governance.md`, the
attestation JSON Schema and `tools/g1-validate.mjs` (`size===2` → `size===1`)
were all changed together, and `protocol-v0.2.0` was released under the new one.

**Releases carry exactly one approval — and since 2026-09-12 an AI agent may give
it.** The user decided that on 2026-09-12: requiring them to run every release by
hand added a step without adding a decision. An agent approves a release only when
the user has authorized that specific release in the conversation, and the
attestation says so — `approverKind: AI_AGENT` plus `authorizedBy` naming the user —
so it is never read as the user's own signature. **CI still cannot approve.**

### Notify-after-change

`8005-agv-protocol` is writable. Zhengyu Shao decides its content alone — Kun
Wang's approval is **not** required in advance (changed 2026-09-02; the earlier
dual-approval gate no longer applies).

**There is no notify-after-change duty any more, as of 2026-09-08.** Until then
every pushed change had to be announced to Kun Wang in an issue that
`@SocialKKKK`, because the protocol was the contract his side built against and a
release voided his gate evidence. The user took over his project outright, so
neither premise holds: no other side builds against this contract, and there is
no gate evidence of his left to void. Do not open announcement issues, and do not
`@SocialKKKK` anything.

What did not change is why that rule existed. **A protocol push still voids gate
evidence — ours.** Say which `W2G-IS-*` slices a change touches and which evidence
it invalidates, in the commit message and in the slice board. The audience moved;
the accounting did not.

Formal releases need an approval attestation before an immutable tag — **exactly
one approval**: the product owner, or since 2026-09-12 an AI agent the product owner
authorized for that release (two product owners before 2026-09-08). **CI still
cannot approve.** That governs tagging a `ProtocolRelease`, not ordinary commits.

### Scope

Routing a problem to a repository never grants write access to it. These
restrictions override Wayfinder routing, execution authorization in map Notes,
and general requests to fix, document, commit, or push. Only a later explicit
user instruction changing this standing policy may alter the list above.

`8005-workspace/w2g-rc-*/` are release-candidate artifact snapshots, not working trees. Read
them for reference; never develop in them.

## Scripting baseline

PowerShell 7 is the shell for every script written in this workspace. Do not
write Windows PowerShell 5.1 compatible code, do not add version probes,
compatibility shims, or 5.1 fallbacks, and do not invoke `powershell.exe` —
call `pwsh`. Every new `.ps1` opens with:

```powershell
#Requires -Version 7
```

Use PS7 features directly where they are the clearest expression: `&&`/`||`,
`??`, `?.`, the ternary operator, `ForEach-Object -Parallel`,
`ConvertFrom-Json -AsHashtable`, and UTF-8-without-BOM file defaults. Every
machine this workspace reaches runs pwsh 7.6.5 — the control host, the AGV
onboard HMI machines under `8005-workspace/remote-ops/onboard-hmi/`, and the factory
server under `8005-workspace/remote-ops/factory-server/` — so remote scripts follow the same rule.

There is no live exception. The earlier one covered the Windows Server 2016
factory host, on the grounds that it was offline and had only Windows
PowerShell 5.1. Both premises stopped being true: verified 2026-09-01, that
host has pwsh 7.6.5, a registered `PowerShell.7` remoting endpoint, and direct
internet access. New scripts targeting it are PowerShell 7 like everything
else.

What survives is narrower, and it is a freeze rather than an exception: the
already-released MES ingest scripts under
`8005-mes-ingest/.artifacts/releases/` keep their
`#Requires -Version 5.1` header. They were validated and shipped as 5.1
artifacts. Never retrofit a released script in either direction — not to PS7,
and not back to 5.1.

## 协作与语言

项目由两个人推进。**分工在 2026-09-04 变了**：`8005-agv-onboard-hmi` 与
`slots-simulator` 原本由 Kun Wang（GitHub `SocialKKKK`）负责，现在**开发工作在
Zhengyu Shao 这边**——我们在那两个仓开自己的 `w2g/*` 分支改，改完开 PR 进它们的工作分支，
**2026-09-09 起同意与合并都归我方**，不再等 Kun Wang（见上面 Branch-scoped write）。
`8005-agv-control-server` 一直是 Zhengyu Shao 的；`8005-agv-protocol` 共同维护。**权威文档是
本仓 `docs/collaboration-workflow.md`**，各仓 `CLAUDE.md` 里内联了
agent 必须遵守的部分。

注意 `8005-workspace` 这个仓库**只有 Zhengyu Shao 有访问权**，Kun Wang 看不到。任何需要
对方看到的东西不能只写在这里。

协作单位是 `8005-agv-protocol/integration-slices/index.json` 里的 integration slice
（`W2G-IS-00` 到 `W2G-IS-07`），每个切片的 `gates` 就是分工。跨仓库反馈必须带可复现的
门禁证据。protocol 由 Zhengyu Shao 单独决定内容，**推送后不再需要通知任何人**
（2026-09-08 起，此前每次推送都要开 issue @`SocialKKKK`，见上面 Notify-after-change）。
发布打 tag 同日起**改为单人签名**（此前双人）；**2026-09-12 起 AI 也可以批准**，
前提是用户在对话里授权了那一次发布，attestation 如实记 `approverKind: AI_AGENT` 与
`authorizedBy`；**CI 仍然不能批准**。协议改动仍然要攒批次——发布会作废受影响的 G1/G2/G3
证据，现在作废的是我方自己的。

**agent 指令文件用英文**（各仓 `CLAUDE.md`、`.claude/` 下的规则与 skill、
`docs/agents/`）；**人看的东西用中文**（README、文档正文、`docs/defects/`、证据
`SUMMARY.md`、issue 与 PR 的标题和正文、commit message 正文）。中文里保持英文：
commit 的 conventional 前缀、标识符、路径、命令、环境变量、错误码、门禁与切片名、
协议消息名与 schema 字段与 `vectorId`。引用报错和测试输出先贴英文原文再中文解释。
不回溯改旧的。

## CI：不用托管 runner，改用 factory-server 上的 self-hosted runner

**不要用 GitHub 托管 runner。**2026-09-02 试过五轮，riot-sdk 与 control-server
通过，但 `8005-mes-ingest` 有一整批测试对运行机器有硬假设，托管 runner 满足不
了——断言真实桌面工作区 >= 1280x760、要 Oracle 客户端 thick 模式、断言"取消在
3 秒内返回"这种挂钟行为（托管机上要 46-53 秒）。这不是配置问题，是这套测试的
固有属性：它本来就是为一台特定机器写的。这个判断没有变。

**改用 self-hosted runner**（同日晚些时候的决定，取代了当时"完全不用 CI"的结
论）：runner 跑在 factory-server 的 Hyper-V 客户机 `win11-01` 上（`ssh vm01`），
那台机器同时接替控制端的 `gpt_win11` 成为黄金渲染机。它满足全部机器假设，而且
砍掉了 `Invoke-GoldenRendererValidation.ps1` 那 823 行"因为测试机在别处"才需要
的编排——payload 部署、PowerShell Direct 会话、计划任务注册、证据回捞全部不再
需要。**已于 2026-09-02 落地**：该脚本删除，其中真正有价值的打包发布门禁独立成
`8005-mes-ingest/Invoke-PackagedReleaseGate.ps1`，视觉基线走
`.github/workflows/golden-renderer.yml`（`mode=verify` / `mode=candidates`，只能
手动触发）。

**已落地（2026-09-02）。**win11-01 上跑着**八个** runner，用标签分工。以下是
2026-09-03 从 `gh api repos/<仓>/actions/runners` 实读的结果，不是当初的计划——本表
一度只记了下面前三行，漏掉了 control-server 与 protocol 那两个，而它们一直在跑。
第六个 `win11-01-onboard-hmi` 于 2026-09-18 加上（`8005-agv-onboard-hmi#101`），只跑
`w2g/fp-v2-impl` 这条线；`OnboardHmi_MVP` 不加 CI，因为 MVP 预计几周后会被 v2 替换。
第七个 `win11-01-control-server-2` 于 2026-09-19 加上（`8005-agv-control-server#168`，
调研报告里的方案 d），**只跑服务端的 `test.yml`**：它只带 `cs-test`、不带 `headless`，
所以 `l2.yml` 与 `release.yml` 仍只落在原 runner 上，两个 l2 永远不会同时抢那 4 个
端口槽位，而同一张票的 test 与 l2 能并行。回退办法是把 `test.yml` 的 `runs-on` 改回
`[self-hosted, headless]`。同日 vm01 页面文件由 4 GB 调到 8 GB（已提交上限 16 GiB），
因为实测 test 单独 +4.0 GiB、与 l2 并行时整机峰值 9.42 GiB。
第八个 `win11-01-control-server-desktop` 于 2026-09-19 加上（用户当日批准，
`8005-workspace-v2/ci-research/real-rig-bottleneck.md` 方案 b），**交互式、只跑服务端的
真装置 L2**（`l2.yml` 的 `real-rig` 作业，手动 `-f rig=real`）：真装置要起车载端 WPF 与模拟器窗口，session 0 的服务 runner
起不了。它只带 `cs-desktop`，不带 `headless`／`cs-test`／`golden-renderer`，所以不会领
别的作业；装法是 `8005-workspace/remote-ops/factory-server/scripts/18-install-control-server-desktop-runner.ps1`
（`-Remove` 卸掉）。它与 mes-ingest 的桌面作业共用同一个桌面，靠下面第 2 条的互斥体排队：

**2026-10-20 起 CI 按仓从 vm01 迁到 vm-win-01**（用户本机 Hyper-V 上的客户机，`ssh vm-win-01`，
过程与对照见 `8005-workspace-v2/ci-research/migration-vm-win-01-build-log.md`）。每个仓切换时，
新 runner 加上正式功能标签，vm01 上对应 runner 经 API 摘掉功能标签（不卸载、不停服务，留作备用，
两周无事再卸）。「状态」一列以 `gh api repos/<仓>/actions/runners` 为准，切一个仓改一行。

| runner | 机器 | 模式 | 标签 | 归属仓 | 状态 |
| --- | --- | --- | --- | --- | --- |
| `win11-01-riot-sdk` | vm01 | 服务（session 0） | `dotnet8`（10-20 摘掉 `headless`） | riot-sdk | **备用**，不领作业 |
| `win11-01-mes-ingest` | vm01 | 服务（session 0） | `dotnet8`（10-20 摘掉 `headless`） | 8005-mes-ingest | **备用**，不领作业 |
| `win11-01-mes-ingest-desktop` | vm01 | 交互式（session 1） | `golden-renderer` | 8005-mes-ingest | 在用（不迁） |
| `win11-01-control-server` | vm01 | 服务（session 0） | `dotnet8`（10-20 摘掉 `headless`） | 8005-agv-control-server | **备用**，不领作业 |
| `win11-01-protocol` | vm01 | 服务（session 0） | `node24`（10-20 摘掉 `headless`） | 8005-agv-protocol | **备用**，不领作业 |
| `win11-01-onboard-hmi` | vm01 | 服务（session 0） | `dotnet8`（10-20 摘掉 `headless`） | 8005-agv-onboard-hmi | **备用**，不领作业 |
| `win11-01-control-server-2` | vm01 | 服务（session 0） | `dotnet8`（10-20 摘掉 `cs-test`） | 8005-agv-control-server（只跑 `test.yml`） | **备用**，不领作业 |
| `win11-01-control-server-desktop` | vm01 | 交互式（session 1） | `dotnet8`（10-20 摘掉 `cs-desktop`） | 8005-agv-control-server（只跑 `l2.yml` 的 `real-rig` 作业） | **备用**，不领作业 |
| `win11-01-simple` | vm01 | 服务（session 0） | `simple` | simple（2026-10-17 加，`trytoreachpeak0/simple#20`） | 在用（不在迁移范围） |
| `vmwin01-protocol` | vm-win-01 | 服务（session 0） | `node24` `headless` | 8005-agv-protocol | **在用**（10-20 切入） |
| `vmwin01-riot-sdk` | vm-win-01 | 服务（session 0） | `dotnet8` `headless` | riot-sdk | **在用**（10-20 切入） |
| `vmwin01-mes-ingest` | vm-win-01 | 服务（session 0） | `dotnet8` `headless` | 8005-mes-ingest（test、repo-scan、release） | **在用**（10-20 切入） |
| `vmwin01-control-server` | vm-win-01 | 服务（session 0） | `dotnet8` `headless` | 8005-agv-control-server（release、g3 的 register/gate/report、夜间 trigger、main 与 MVP 的推送；cs#820 合入前还有 l2 合成场景） | **在用**（10-20 切入） |
| `vmwin01-control-server-2` | vm-win-01 | 服务（session 0） | `dotnet8` `cs-test` | 8005-agv-control-server（只跑 `test.yml`） | **在用**（10-20 切入） |
| `vmwin01-control-server-3` | vm-win-01 | 服务（session 0） | `dotnet8` `cs-test` | 8005-agv-control-server（只跑 `test.yml`，与 `-2` 并行） | **在用**（10-21 01:19 切入，cs#820） |
| `vmwin01-control-server-l2` | vm-win-01 | 服务（session 0） | `dotnet8` `cs-l2` | 8005-agv-control-server（只跑 `l2.yml` 的 `scenarios`，8 路） | **已挂标签**（10-21 02:21，cs#820）；control-server#821 合入后接活 |
| `vmwin01-control-server-desktop` | vm-win-01 | 交互式（session 1，账户 `vm-win-01`） | `dotnet8` `cs-desktop` | 8005-agv-control-server（`l2.yml` 的 `real-rig`、g3 的 g3 作业） | **在用**（10-20 切入） |
| `vmwin01-onboard-hmi` | vm-win-01 | 服务（session 0） | `dotnet8` `headless` | 8005-agv-onboard-hmi | **在用**（10-20 切入） |

vm01 上的九个都带 `self-hosted` `Windows` `X64` `win11-01`；vm-win-01 上的只带 `self-hosted` `Windows` `X64`
加上表中的标签（临时标签 `vmwin01-*` 切换后保留，无害）。`win11-01-simple` 另外只带 `simple`，不带
`headless`／`cs-test`／`cs-desktop`／`golden-renderer`，所以不会领 v2 各仓的作业。注意两个交互式 runner 都**不带**
`headless`，`win11-01-mes-ingest-desktop` 是唯一带 `golden-renderer` 的，
`vmwin01-control-server-desktop`（10-20 前是 `win11-01-control-server-desktop`）是唯一带 `cs-desktop` 的——这一条正是标签分工能成立的原因。`vmwin01-control-server-l2` 是唯一带 `cs-l2` 的：两个 l2 合成作业不能同时跑，否则会在槽 1～8 的端口锁上逐场景排队，谁也不更快（cs#820 实测）；要加第二个 L2 runner，先给它分不重叠的槽段。

交互式 runner 由登录触发的计划任务（`GitHubRunner-<名字>`）在桌面会话里拉起，依赖客户机的 autologon（用
Sysinternals Autologon 配的，密码进 LSA secret 而不是明文注册表，`DefaultPassword`
键不存在）。vm-win-01 上的账户名与计算机名相同（都叫 `vm-win-01`），计划任务要写 `vm-win-01\vm-win-01`。**workflow 的 `runs-on` 一定要带 `headless`、`golden-renderer`、`cs-test` 或 `cs-desktop`**，
只写 `[self-hosted, win11-01]` 会被两种 runner 里任意一个领走，而其中一个画不了图。

**加了 runner 就回来改这张表。**它漏记了两个 runner 至少一天，而这张表是判断
「某个仓有没有 CI」的唯一依据——第一次挂 L2 到 CI 时，就是照着它得出「control-server
没有 runner」的错误结论，实际上有。

`8005-mes-ingest` 的测试按 `[Collection("WpfDesktop")]` 标记划成两半：`test.yml`
在 headless 上跑其余全部，`desktop-tests.yml` 在交互式 runner 上跑这些。划分由
`Get-WpfDesktopTestFilter.ps1` 扫源码推导，不是手写清单——手写过一次，下一轮就漏
了两个新类。合起来的结果与本地等价：

| | 本地 | CI |
| --- | --- | --- |
| 通过 | 962 | 961（798 + 163） |
| 跳过 | 138 | 138 |
| 失败 | 0 | 1（`8005-mes-ingest#1`，已知） |
| 总计 | 1100 | 1100 |

三条硬约束：

1. **哪些仓库是 public 由用户决定，2026-09-14 起八个组件仓库全部是 public**
   （Repository write authority 表里那八个）；`8005-workspace` 本身仍是 private。
   先改的是 `8005-agv-control-server` 与 `8005-mes-ingest`，同日用户要求其余六个
   一并公开。起因是 artifact 存储配额：私有仓库共用个人账户
   每月 500 MB·月的免费额度，按「大小 × 存放小时数」累计，发布包把它用满后所有
   上传都被拒（`Artifact storage quota has been hit`），删文件也扣不掉当月已累计的
   量；公开仓库的 artifact 不计额度。用户明确接受了代价，并说不用管：任何人都能看到
   代码、完整历史、证据目录里的厂区地址和凭据样值、Actions 日志和发布包；任何人提一个
   PR 就能在 win11-01 上执行代码，而它经跳板能碰到 factory-server 上的生产服务。
   公开前没有做敏感信息清理，也没有关 PR 或加 fork PR 审批。**不要自行把它们改回
   private，也不要自行加这些防护**——要改等用户开口。

   这条原本是「挂了 self-hosted runner 的仓库绝不能是 public」，`8005-agv-protocol`
   正是为此于 2026-09-02 从 public 转为 private。
2. **`trytoreachpeak0` 是个人账号不是组织，一个 runner 只能绑一个仓库。**要给
   多个仓做 CI，就必须在同一台机器上装多个 runner 实例（不同目录、不同服务名），
   而它们会各自并行领作业。所以**不要指望"一台机器一个 runner"去保证黄金渲染机
   契约的 "Never run two desktop suites in parallel"**——跨仓库的桌面独占
   GitHub 的 `concurrency` 表达不了（它只在单个仓库内生效）。

   **它现在由一个机器级命名互斥体承担：`Global\W2G-InteractiveDesktop`，唯一定义
   处是 `8005-mes-ingest/Invoke-WithDesktopLock.ps1`**（2026-09-03 落地）。任何仓库
   的任何脚本，只要在动那台机器的交互式桌面（起 WPF 窗口、抓像素、驱动 UI
   Automation），都必须先拿到同一个名字的互斥体。各仓是独立克隆、没有共享包，所以
   第二个仓要用就自己拷一份 helper——**名字才是契约，代码不是**。

   在那之前这句话只有一半是真的：`golden-renderer.yml` 用的名字是仓库作用域的
   `Global\MesIngestWatchUiTests`（只能把那个脚本与自己串起来），而
   `desktop-tests.yml` **一把锁都没有**，靠的是本仓共用的 `concurrency` 分组。

   **2026-09-19 起第二个仓加进来了，CI 排队、手动仍快速失败。**`8005-agv-control-server`
   的真装置 L2 在交互式 runner `win11-01-control-server-desktop` 上跑，每个场景拿一次锁
   （排队 1800 秒，`scripts/DesktopLock.psm1`）；`8005-mes-ingest` 的 `desktop-tests.yml`
   与 `golden-renderer.yml` 同日改为传 1800 秒超时排队（`8005-mes-ingest#8`，合入
   `b670166a`），作业超时相应加大。脚本默认值仍是 0（exit 3），给在客户机上手动跑的人用。
   CI 作业该排队，不该因为撞上另一个仓的调度就变红。

   只给需要金机的 runner 打 `golden-renderer` 标签，别的 runner 不要带。
3. **黄金渲染机的 Validation 阶段只能 `workflow_dispatch` 手动触发。**它会产生
   候选基线，那必须是用户点头之后的动作，见 `8005-mes-ingest/CLAUDE.md`。

那轮托管 CI 抓到过一个本地发现不了的真 bug（`.gitattributes` 的字节规则在拆分时
丢失，导致查询文件摘要对不上）。**教训是：改动会影响构建的文件后，用干净
checkout 验证一次**——例如临时克隆到别处再跑测试。

### 不要取消 self-hosted runner 上正在跑的 job

（原在 v1 `CLAUDE.md` 的「CD：WIRE_TO_GATE」一节，2026-11 随共用规则搬来。）

**绝不要取消 self-hosted runner 上正在跑的 job。**2026-09-03 实测：取消一个 job 会
把 runner 的 broker 长轮询连接一起取消，退避重试（日志里的
`Back off 9.921 seconds before next retry. 4 attempt left.`）耗尽之后会话就卡住，
不再领任何新作业。它没有自愈——直到 GitHub 主动推了一条 `RunnerRefreshConfigMessage`
触发会话重启才恢复，**中间空转了 4 小时 14 分**。这些仓库每个只有一个 runner，一个
会话卡死就是整个仓库的 CI 停摆。

那次的动机是「两个分支推同一个 commit，test 跑了两遍，取消一个省点机时」。省下的是
2 分钟，代价是 4 小时。宁可让重复作业跑完。

**这件事有一个自动版本，2026-09-03 已经堵上。**`cancel-in-progress: true` 会在同一分支
连推两次时自动取消正在跑的作业，与手动取消同一条路径。当时
`8005-agv-control-server` 与 `riot-sdk` 的 `test.yml`、`8005-agv-protocol` 的 `g1.yml`
三个 workflow 都是 `true`（`8005-mes-ingest` 的六个早就是 `false`），现已统一改为
`false`。**新写 workflow 时不要再设成 `true`。**注意改为 `false` 后仍会取消**排队中**的
作业——第三个到达时中间那个被顶掉——那不碰 runner 会话，是安全的。

**这条曾被误记为「控制端笔记本一睡，CI 就停摆到它醒」，那个归因是错的**，不要据此去
改 `NO_PROXY` 或电源设置。控制端设了永不睡眠（睡眠超时 AC/DC 都是 0），实测 7 天内
零 `Kernel-Power` 42/107 事件，win11-01 同样没睡过。runner 日志里那段时间的报错是
`TaskCanceledException` 与 `SocketException(995)`——本地取消，不是代理拒绝也不是断网。

## 全产品（v2）的完整测试与实车运行：用 agv02／agv03 隔离做，不干扰 MVP

**用户 2026-09-14 定，今后都照此执行。**生产跑的是 MVP 线（`ControlServer_MVP`／`OnboardHmi_MVP`，
`protocol-v0.3.0`）：factory01 上的 `8005 AGV ControlServer` 服务只管 `agv01`，正在服务客户。
全产品 v2 线（`fp/v2-impl`／`w2g/fp-v2-impl`，`protocol-v1.0.0`）的完整测试、实车运行与现场演练
（例如批次 2 票 19 的 W1 空载急停演练）**不等生产切到 v2**，在备用车上、用独立的 v2 服务端实例做。

**允许（不必再逐项问）：**

- 访问 `agv02`、`agv03`：SSH 上位机，在上面部署与启动 v2 车载端，修它们的时钟，填
  `8005-workspace/remote-ops/onboard-hmi/config/site-agv02.json`／`site-agv03.json` 的现场值。
- 在生产位置之外运行 v2 服务端实例，并让它经 RIoT 只为 `agv02`／`agv03` 建单、发订单命令与急停命令。

**四样共享资源必须隔离：**

| 资源 | 冲突 | 隔离做法 |
| --- | --- | --- |
| MES 需求 | 两版默认都从工厂服务器本机 `127.0.0.1:5088` 的生产 MesIngest 取需求，v2 会抢走真实需求 | v2 实例不接生产 MesIngest，用 `8005-agv-control-server` 的 `tools/ControlServer.FakeMesIngest` 注入测试需求。**这一条在并行期继续有效，用户 2026-09-20 明确定过**：约 10-08 起 v2 与 MVP 在 factory01 上并行时，v2 仍然只吃注入的测试需求；真实需求要到约 10-15 切换当天才转给 v2，**同时停掉 MVP**。理由是取走就是取走了——任何时刻只允许一个实例认领真实需求，「抢」这件事从根上不存在。要在并行期就吃一部分真实需求，唯一安全的做法是在 MesIngest 那一侧按站点或任务类型分流，那是一个要开发的机制，得单开票。**2026-10-09 用户放宽（客户要求 10-10 起用 v2 跑 STAGING_TO_WIRE）**：v2 可以读生产 MesIngest，**但只允许 `STAGING_TO_WIRE` 一种任务类型**，MVP 继续只做 `WIRE_TO_GATE`。依据是读代码得到的两条事实：MVP（含 agv01 现场线）在受理前写死只做 `WIRE_TO_GATE`；MesIngest 只读、没有认领语义，两边看到的是同一份目录——所以分流靠的是「两边任务类型不相交」，不是「认领后对方看不见」（上面那句理由按代码并不成立）。v2 的 `allowedWorkTypes` 一旦含 `WIRE_TO_GATE` 就会和 MVP 抢同一批料，部署脚本的「生产来源模式」负责拒绝这种配置（control-server 对应票）。整体割接（停 MVP、v2 接全部任务类型）仍按原计划，在 v3 发布、W2、program#61 之后 |
| 端口与数据库 | 两版默认都监听 `58005`／`58007`，库都在 `%ProgramData%/8005/ControlServer` | v2 实例换端口、换库目录，不用 `C:\Program Files\8005 AGV\ControlServer` 与 `D:\zhengyushao\ControlServer`。**「不在 factory01 上跑」这条已由用户 2026-09-20 解除**：约 10-08 起的并行期，v2 实例就跑在 factory01 上（那一天之前的日常开发测试仍然不要占 factory01，没必要）。**解除的只是这一条**，同表其余三条一字未改、仍然全部有效。绑定要绑具体网卡 IP，不要 `0.0.0.0`——后者会把服务连带暴露到 Hyper-V 的 `AGV-Internal`，而 CI runner 就住在那个网段上 |
| RIoT | 两版连同一个 RIoT（`172.19.206.222:8888`），RIoT 上有 25 台可调度车 | `JourneyRuntime.agvId`／`vehicleKey` 只能是 `agv02` 或 `agv03`（见 `8005-workspace/remote-ops/fleet.md`）；绝不对 `agv01` 或其他车建单、发订单命令或急停 |
| 地图与通道 | MVP 与 `agv01` 在 RIoT map 25（`老厂前线new`），v2 与备用车在 map 26（`老厂前线new_wk`）。2026-09-21 用户更正：09-19 那次「同在 map 26」是误记 | 选 `agv01` 不经过的路段、`agv01` 空闲的时段，避开演示与生产高峰 |

**不碰，要碰先问：**`agv01`；factory01 上 MVP 服务的进程、安装目录、配置与数据库；生产 MesIngest；
`ControlServer_MVP`、`OnboardHmi_MVP` 分支。

**仍然逐次授权：**任何会让车动、或会发出急停的运行，每一次都要用户在对话里单独授权，现场有人盯着、
物理急停可按；急停演练车必须空载。授权不跨次，上面「允许」那一栏不替代它。

**急停之后怎么释放，要事先写进演练方案。**在途单被报 FAILED 触发的急停目前没有自动解除路径
（`8005-agv-control-server/docs/emergency-stop-field-fallback.md`）；v2 实例仍在运行、故障仍在时去 RIoT
手动解锁，会被判为外部解除并立即重触发。

2026-09-14 18:28 从控制端探测：`agv02`、`agv03` 的 CPE 上 RIoT 用的 5001 端口通，上位机 SSH 的 22022
不通（上位机大概率没开机）；两台都还没部署车载端。

## .NET 工具链基线

四个可写 .NET 仓库统一到一套工具链，真相来源是
本仓 `docs/adr/cross/0056-dotnet-toolchain-baseline.md`：

| 项 | 锁定值 |
| --- | --- |
| SDK | 8.0.426，`rollForward: disable` |
| 运行时目标 | `net8.0`（`8005-mes-ingest` 的 WPF 侧另有 `net8.0-windows`，那是合理的） |
| 测试栈 | xunit.v3 3.2.2 + Microsoft.NET.Test.Sdk 18.8.1 + xunit.runner.visualstudio 3.1.5 |

**禁用 xunit v2、NUnit、MSTest 与 coverlet.collector。**基线不靠读文档维持，靠
四层机制：`global.json` 锁 SDK、`Directory.Packages.props` 集中版本（配
`CentralPackageVersionOverrideEnabled=false`，内联 `Version=` 触发 NU1008）、
`Directory.Build.props` 统一目标框架与 `LangVersion`、`Directory.Build.targets`
的禁用包守卫在构建期报错。

v1 工作区（`8005-workspace` 仓）根的 `check-toolchain.ps1` 扫全部七个仓报告偏离，可写仓有偏离则退出码 1。
`8005-agv-onboard-hmi` 与 `slots-simulator` 属于 Kun Wang，**只报告不修改**，也不
影响退出码。

**不要单独升某一个仓的版本。**改 ADR 和各仓的 props 文件，一起动。
