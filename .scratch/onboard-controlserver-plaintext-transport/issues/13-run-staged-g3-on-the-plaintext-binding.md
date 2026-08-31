# 在明文绑定上实跑 staged G3

Type: task
Mode: AFK（不装服务、不需管理员；但 `run-staged-g3.ps1` 会在交互桌面起 WPF 车载端并占住前台，
开跑前与用户约定时间窗）
Status: open
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
