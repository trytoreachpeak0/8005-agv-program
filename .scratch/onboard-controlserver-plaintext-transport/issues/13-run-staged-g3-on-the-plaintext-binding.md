# 在明文绑定上实跑 staged G3

Type: task
Mode: AFK（不装服务、不需管理员；但 `run-staged-g3.ps1` 会在交互桌面起 WPF 车载端并占住前台，
开跑前与用户约定时间窗）
Status: resolved
Blocked by: 08

## Question

三个 G3 runner 的**实际可运行性至今零证据**：票 02 只证服务端单侧，票 03 只证安装链，票 12 只做了
静态对齐与静态取证，没有任何一次改后的 staged G3 真跑过。用户 2026-08-31 就票 12 第 3 节的三个选项
选定 **A：推到票 08 之后**——理由是同机 loopback 证不了 Destination 要的异机明文形态（那是票 07），
而票 08 之前跑要先做一次注定作废的绑定更新。本票执行那次运行。

### 先决动作：把 `ControlServerCommit` 移到候选身份

票 12 发现并留下的实跑前置：

> `scripts/run-staged-g3.ps1:11` 的 `$ControlServerCommit` 仍锁 `3d8b00c7558ae700358f1f995a5ac75d12a3250c`，
> 那是 TLS 期服务端（`fix: publish each stop's worklist under its own revision`），既不含票 02 的
> `ae4a17d` 也不含票 03 的 `c7874f0`。不动它就跑，等于「TLS 期服务端 ＋ 明文车载端」，必然握不上手。

本票开跑前把它移到**票 08 冻结的候选服务端提交**，并确认 `$OnboardCommit` 仍等于票 08 采用的车载端
提交（票 12 锁的是 `238b46eb2c9ae90584e4288a782176f66b7de942`；若票 08 期间王昆又推了新提交，两处必须
同时更新，否则 `New-ExactClone -RemoteRef 'origin/OnboardHmi_MVP'` 会以 remote ref mismatch 硬失败——
那是设计意图，不是回归）。

票 08 已给出目标值（2026-09-01）：`$ControlServerCommit` 改为
`56d4b1cc2f26325ca853acc4e7278bbde8651874`；`$OnboardCommit` **不动**，王昆在票 08 期间未推新提交，
远端 `origin/OnboardHmi_MVP` 头仍是 `238b46eb2c9ae90584e4288a782176f66b7de942`（开跑前仍应自己再核
一次远端头，不要照抄本行）。注意票 08 之后本仓又多了证据提交 `eaaa5b1`，那**不是**候选身份，不要
把绑定设到它。

注意杠杆（票 12 已取证）：`run-staged-g3.ps1` 的 param block 是三个 runner 的**唯一**绑定源，
`run-staged-g3-restart.ps1` 的 `Get-SharedCommitBinding` 与 `run-demand-bearing-g3-vectors.ps1`
都是解析它，不各自持有副本。改一处三个都变，改错也一次打穿三个。

**staged G3 绑的是 commit，不是票 08 的候选包**——它从 exact clone 重新 publish。因此本票依赖票 08
只为拿到「已冻结的服务端身份」，不构成对候选产物本身的验收（那是票 09／10）。这一点须在证据里写明，
免得后续把本票误读成候选包验收。

## 跑哪几个 runner

- `run-staged-g3-restart.ps1`——**必跑**。最便宜、可无人值守，且它正是票 12 修掉那处失败的 runner，
  不跑它等于票 12 的修复始终只有静态证据。
- `run-staged-g3.ps1`——**必跑**。它是主 runner，且是唯一会起 WPF 车载端的一个，占交互桌面。
- `run-demand-bearing-g3-vectors.ps1`——**视条件**。它需要一份授权现场 run 的 `controlserver.db` 作
  `-FieldRunRoot`。若手上没有可用的现场 run，据实记为未跑并说明原因，不要拿伪造或隔离实例的库冒充
  现场库（该 runner 的证据里 `storeProvenance` 就是为这件事存在的）。

## 判据设计要求

- 三个（或两个）runner 各自的 PASS/FAIL 判定必须是脚本**自身发射**的机器可读结果，不是事后转写；
- 证据落仓内既有 G3 证据目录惯例，并**显式记录本轮与上一轮的形态差异**：无 TLS 代理、无临时信任根、
  无证书生成——证据字段 `tls = $false` / `temporaryTrustRootInstalled = $false` / `certificatesGenerated = $false`
  应据实为 false 并被读回，而不是只出现在硬编码字面量里；
- 绑定回读：证据里的 `commitBinding` 四个值必须等于本票设定的值，且 `sourceSha256` /
  `functionSourceSha256` 与当时的源文件实测哈希一致；
- 至少一条**红侧**：本轮新形态下要有一条能证明检测器会响的对照。最省事的是复用票 12 的那条——
  在无 `useTls` 的车载端配置上恢复无条件赋值必抛 `SetValueInvocationException`；若本票另设断言，
  同样要给出会红的证明；
- 若某个 runner 跑失败，**保留红证据**，据实记录，不要重跑到绿再只留绿的那次。

## 不在本票范围

- 异机明文联调——票 07；
- 候选包的干净安装验收——票 09；真车闭环——票 10；
- `StagedG3TlsHarness` 等 TLS 期命名残留的改名（地图 Out of scope，另起一轮）。

## Answer

**三个 runner 全跑了，全绿。** 不是两个——票正文写的「视条件」那个前置在开跑前核实成立
（见 §3）。五十九条断言零失败，全部由 runner 自身发射。

主证据：服务端仓 `evidence/g3/20260901-plaintext-binding-g3-runs/`（`SUMMARY.md` ＋ 三次运行的
原样 `run-result.json` / `configuration.json` / `logs/` ＋ `controls/`）。逐条数字在那里，本节不重复。
提交 `ControlServer_MVP@c0f1e84`（绑定，单行）与 `@b6524ca`（证据），均已推送。

### 1. 先决动作

`run-staged-g3.ps1:11` 的 `$ControlServerCommit`：`3d8b00c7…`（TLS 期）→
`56d4b1cc2f26325ca853acc4e7278bbde8651874`（票 08 冻结进候选 0.2.0 的服务端提交，**不是**其后的
证据提交 `eaaa5b1`）。改动一行。

`$OnboardCommit` 未动。开跑前实测 `git ls-remote origin OnboardHmi_MVP` 头仍是
`238b46eb2c9ae90584e4288a782176f66b7de942`，与票正文记的值一致，王昆在票 08 之后没有再推，
`New-ExactClone -RemoteRef` 的远端引用校验因此继续通过。**这一次是自己核的，不是照抄票正文。**

改后按三条**各自的**解析链回读：主 runner 自身 param block、restart runner 的
`Get-SharedCommitBinding`、vectors runner 的 `Get-ScriptFunction` 提取链。四个值一致，只有
`ControlServerCommit` 变。票 12 说的「唯一绑定源」在这里被证成了。

### 2. 三次运行

| runner | 运行 ID | 结果 | 断言 |
| --- | --- | --- | --- |
| `run-staged-g3.ps1` | `20260831T180238976Z` | `STAGED_G3_RECOVERY_REPLAY_PASS` | 19 / 19 |
| `run-staged-g3-restart.ps1` | `20260831T180034188Z` | `STAGED_G3_PROCESS_RESTART_PASS` | 20 / 20 |
| `run-demand-bearing-g3-vectors.ps1` | `20260831T180416352Z` | `DEMAND_BEARING_G3_VECTORS_PASS` | 20 / 20 |

三次 `failedAssertions` 与 `secretLeakFiles` 均为空数组。串行跑，三次共约四分钟，
端口 58205/58207、58105/58107、58305/58307 互不重叠，也与生产服务的 58005/58007 错开。
主 runner 的协议 G1 为 PASS（node 与 pnpm 走的是 codex 运行时那份捆绑副本，PATH 上没有）。

**这不是候选包验收，票正文要求写明的那点已落进证据**：三次 `classification` 都是
`formalSlicePass: false`、`fullG3: INCONCLUSIVE`、`releaseCandidate: INCONCLUSIVE`，四个正式切片
（`W2G-IS-00`／`04`／`05`／`06`）全部保持 `INCONCLUSIVE`。staged G3 从 exact clone 重新 publish，
绑的是 commit，全程没碰票 08 冻结的候选包。

### 3. 第三个 runner 为什么跑得成

票正文把 `run-demand-bearing-g3-vectors.ps1` 记为「视条件」，条件是一份授权现场 run 的
`controlserver.db`。上次 vectors 运行用的那份仍在：
`C:\Users\szy\w2g-stage\run\fullloop-20260829T131549Z\controlserver.db`，本次证据的
`storeProvenance.fieldDatabaseSha256` = `87220f7990990106…`。既然真库还在，就没有理由记「未跑」。

### 4. 绑定回读，以及比文件哈希更强的那条

restart 与 vectors 两份证据里的 `commitBinding` 四个值都等于本票设定的值；
`sourceSha256` = `62711a64a8eb…` 等于当时 `run-staged-g3.ps1` 的实测哈希，vectors 另有
`functionSourceSha256` = `90989268477eb…` 等于 `run-staged-g3-restart.ps1` 的实测哈希。

但**文件哈希只证明参数写了什么，不证明跑起来的是什么**。更强的一条是进程自报：restart runner 的
`sessionIdentity.serverBuildCommits` 跨三次重启各报一次 `56d4b1cc…`，`onboardBuildCommits` 各报一次
`238b46eb…`，对应断言 `runningControlServerReportsBoundBuildCommit` /
`runningOnboardReportsBoundBuildCommit` 为 PASS。真正在明文链路上握手的，确实是候选服务端与
王昆那版车载端。

### 5. 红侧（`controls/red-side-controls.json`，`RED_SIDE_CONTROLS_PASS`）

十三行，两个检测器**各自双向**。按 map Notes 那条「取证表里同时放正反两向的期望」办的。

**A. 票 12 修的 `useTls` 守卫**（`run-staged-g3-restart.ps1:515`）：
明文 `238b46e` 配置无 `useTls` 键、TLS 期 `31263b1` 配置有（两条前置各自实测）；无条件赋值在
明文配置上抛 `SetValueInvocationException`（RED）；守卫式赋值不抛且写回后仍无该键（GREEN）；
**守卫式赋值在 TLS 期配置上进得去分支并写 False（CONTROL）**。最后一行是关键——只有 RED＋GREEN
的话，一个恒不进分支的坏守卫看起来同样合理。

**B. `Get-SharedCommitBinding`**：对真文件读回四值全绿；三个变异体各自证红——带老 SHA 的副本
读回老 SHA（证明读的是文件而非内建常量），大写 SHA 与截断 SHA 各自被
`-cnotmatch '^[0-9a-f]{40}$'` 拒绝。

两份配置都是在 stage 的一次性 exact clone 里用 `git show` 取的，对只读仓写入为零。

### 6. 「无 TLS」不靠字面量（`controls/corroboration.json`，`CORROBORATION_PASS`）

票正文要求 `tls` / `temporaryTrustRootInstalled` / `certificatesGenerated` **被读回而不是只出现在
硬编码字面量里**。三个 runner 里这三个字段确实就是硬编码字面量，本身不构成证据，所以另做了
二十四行独立观测佐证：

- 四个证书存储跑前跑后的**指纹集合摘要**逐一相同（`CurrentUser\Root` 44 张、`CurrentUser\My` 1、
  `LocalMachine\Root` 42、`LocalMachine\My` 1）。比的是集合摘要，不只是数量；
- 三个 stage 根 ＋ 三个证据根递归扫七类密钥材料后缀与 `certs\` 目录，全 0；
- staged 与 restart 实际 publish 出来的车载端 `appsettings.json` 回读：`useTls` /
  `serverCertificateSha256` / `serverCertificatePath` 一个都不存在；
- 全部 runner 日志搜 `Schannel|SslStream|AuthenticationException|X509|https://127.0.0.1|certificate`
  命中 0。票 07 记过「错配时唯一点出真因的是服务端的 `AuthenticationException`」——这里一条没有；
- vectors runner 的 `publish\` 只有 `control-server`，它用的是从主 runner 提取的合成对端，从不
  克隆或发布车载端。这条按设计事实断言，将来真冒出一个车载端 peer 会翻红；
- 生产服务 `8005 AGV ControlServer` 全程 PID 8632、`Running`、进程启动时间早于本轮；
- 只读仓 `8005-agv-onboard-hmi` 工作树零改动，HEAD 仍 `bbfbc52f…`。

### 7. 据实记录：佐证脚本自己红过一次

`stage-vectors publishes no onboard peer` 那行第一版是红的，而 `expected` 与 `observed` 打印出来
**字面相同**（都是 `control-server`）。原因是 `@(Get-ChildItem -Directory).Name` 在单元素结果上
经成员枚举退化成一个**字符串**，于是 `[0]` 取到的是首字符 `c`，比 `'control-server'` 永远不等。

与 map Notes 里 `@($hash[$missingKey]).Count -eq 1` 是同一族：`@()` 包错了位置，PowerShell 的
标量／集合退化就会把判断悄悄改成另一件事。这次也同样是靠**正反两向并排打印**当场暴露的——
如果表里只写 pass 一列，会看成一条真发现去追。已修（`@()` 包投影而不是包源）并重跑，脚本连同
结果一起归档在 `controls/`。

### 8. 未做 / 边界

- 未安装、未卸载、未升级任何 Windows 服务；未创建 RIoT 订单、未发送移动命令、未使用现场凭据、
  未伪造停稳／驻车信号（三次 `noMovementOrExternalSideEffects` 均 PASS，MesIngest 与 RIoT 均指向
  死端口 `http://127.0.0.1:1`）；
- 未跑 tier 1：本票只改了一行 runner 脚本里的 commit 字面量，不触及产品源码、测试或构建输入；
- `StagedG3TlsHarness` 等 TLS 期命名残留原样保留，仍属地图 Out of scope。
