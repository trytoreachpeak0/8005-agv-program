# 构建并验证可安装的 MVP 发布候选

Type: task
Mode: AFK
Status: resolved
Blocked by: 10

## Question

如何从精确绑定的两端构建和协议候选生成可安装、可启动的 MVP Release Candidate，包括程序二进制或安装包、版本 manifest、配置样例、数据库初始化/迁移、启动停止脚本、健康检查、日志路径、回滚说明和 SHA-256，并在干净环境验证构建、安装、首次启动、停止和重启？

发布候选必须包含两个真实产品程序和精确协议身份；仅有源码、README、Spec、Fake 演示或 ZIP 文档包不得通过。本票必须执行秘密扫描、依赖/许可证清单和发布物哈希，并列出仍阻断目标硬件或现场使用的外部条件。

还必须执行一次“无 Matt/无 Codex 上下文”安装检查：仅按远程仓库和发布物公开入口，证明另一台受控环境能够安装/启动两端、运行核心测试场景并定位证据；不能依赖原开发会话。

## Answer

发布候选可构建、可安装、可启动、可回滚，并已在与生产部署完全隔离的第二实例上验证通过。

### 跨仓路由

Owning repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`（用户于本轮明确
指定它为联合 RC 的集成／发布仓）
Owner issue/artifact: `docs/RELEASE-CANDIDATE.md`、`scripts/New-WireToGateReleaseCandidate.ps1`、
`evidence/rc/20260830-isolated-install-2eeb6f0/SUMMARY.md`
Published branch/commit: `ControlServer_MVP@ee54988`（已推送，回读一致）
Impact on this ticket: 已解决；车载端仓保持只读，未写入任何内容。

### 交付了什么

一条命令从两个精确 commit 组装出完整 RC：

```powershell
.\scripts\New-WireToGateReleaseCandidate.ps1 -OutputRoot <新目录> -OnboardCommit 304e6ad…
```

绑定身份：`ControlServer_MVP@2eeb6f0` + `OnboardHmi_MVP@304e6ad` + `protocol-v0.1.1`
（`1531489e`，`APPROVED_RELEASE`）。RC 内含两端 self-contained 二进制、逐文件 SHA-256 的联合
`release-manifest.json` 与 `SHA256SUMS.txt`（868 个文件）、安装／卸载／重建脚本、依赖与许可证
清单、秘密扫描报告，以及唯一的操作入口 `RELEASE-CANDIDATE.md`。

协议身份是**从产物读回**的（`controlserver/appsettings.json` 的 `ProtocolCandidate`），不是脚本
里重述的；`approvalStatus` 不是 `APPROVED_RELEASE` 就拒绝出包。车载端从**一次性克隆**构建，
从不写入只读的车载端工作副本。

### 验证结果

二十六条断言全 PASS（两端构建 0 警告、包哈希、EF 迁移建库、`/health/live`、`/health/ready` 返回
`503 RECOVERY_HANDSHAKE_REQUIRED`、停→起、强制重启、`/version`、持久日志且无秘密泄漏、车载端
起窗并写日志、两种卸载、收尾四项、生产服务全程 `Running`）。

五条可证伪性检查证明这些绿能变红：秘密扫描十三条变异全检出且无误报；`SHA256SUMS` 改一个字节
即 MISMATCH；HTTPS 用另一张根证书验证以 `curl: (60)` 失败、用本次安装的根则 exit 0；卸载脚本
拒绝在无 `-AllowProductionService` 时动生产服务；安装回滚在一次真实失败后清干净了服务、安装
目录与数据目录。

### 本轮修掉的三个缺陷

1. `[IO.Path]::GetFullPath` 按进程 CWD 而非 PowerShell 位置解析，操作员传的相对路径会被静默挪到
   无关目录（`4c13ea0`，四个脚本）。
2. 安装把自签根导入 `CurrentUser\Root` 会弹 Windows 信任对话框，非交互会话下必然失败，而产品
   根本不查该存储（车载端钉 `serverCertificateSha256`）。改为导出 PEM 并用 `curl --cacert` 钉住
   校验，信任存储导入降级为可选开关（`a5698da`）。
3. 服务无持久日志——Serilog 只配了 Console sink，Windows 服务下写向虚空。安装生成的
   `appsettings.Production.json` 现在加了 Compact JSON 文件 sink，没写出日志文件即安装失败。

### 报告但未修的四项发现

1. 车载端默认 `appsettings.json` 的 `wireToGate.onboardBuildCommit` 是较早的 `a6f05fbc`，与本包
   构建 commit 不符。**二进制本身是对的**（启动日志 `version=…+304e6ad9…`），这是握手用的配置
   默认值，仓库自带的 `appsettings.Production.example.json` 本就要求操作员替换。发布脚本因此
   额外产出已填入真实 commit 的 `appsettings.Production.template.json`，并在 manifest 里记录
   `declaredBuildCommitMatchesBuild=false`。车载端仓只读，未在该仓修改。
2. 车载端仓没有 `global.json`，干净克隆会用机器上第一个 SDK。发布脚本在一次性克隆中钉 `8.0.424`
   并记录 `sdkPinnedByReleaseScript=true`；在仓内固化是车载端负责人的决定。
3. 三个自研包 `RIoT.Sdk.Core`／`Facade`／`Generated`（`0.1.0-controlserver.2`）无许可证元数据；
   其余 104 个包解析为 MIT／Apache-2.0／BSD-3-Clause 或 dotnet 许可证 URL。
4. `CurrentUser\Root` 里有一张 2026-08-27 遗留的孤儿开发根证书
   （`8CEF9E6B09A7202AB6B8DF5323E6A48E3CE47003`），不属于当前生产实例，未擅自删除。

### 「无原会话上下文」检查的真实边界

按用户选择，用的是**本机隔离实例**而不是 Hyper-V VM。每一步都只从发布产物目录内的脚本与手册
执行，没有回到任何仓库工作副本；但**没有用第二台物理或虚拟主机，操作者也是编写该手册的同一个
会话**。这条限制已写进证据的「What this does not establish」，不得表述为独立第三方安装验证。

「运行核心测试场景」一项按实际情况处理：发布包只含二进制、不含测试宿主，因此
`RELEASE-CANDIDATE.md` §12 记录了从公开仓库运行单元测试、逐切片 G2 与三个 staged G3 runner 的
精确入口，本票未重跑它们。

### 仍阻断目标硬件与现场使用的外部条件

见 `docs/RELEASE-CANDIDATE.md` §11：真实车辆动作的逐次授权与现场安全 GO、RIoT 环境与车辆／
Map／站点绑定、可达的 MesIngest、真实八仓 IO 资格、受控签发的 TLS 证书、车载端仓只读、协议仓
审批门禁。

### 这不构成什么

- **不构成发布物已推送远程。** RC 是 272 MB 二进制，不进 Git；本票交付的是「从两个公开 commit
  加一个已提交脚本可复现」。创建 GitHub Release 资产属对外发布动作，需用户授权，留给票据 12／15。
- **不构成 RC 通过。** W2G-IS-00～07 与 RC 门禁仍全部 `INCONCLUSIVE`。本票只证明包能建、能装、
  能起、能停能重启、有日志、能回滚。
- **未建单、未动车、未触 RIoT。** 全程 `JourneyRuntime.enabled=false`，结果 JSON 的
  `riotMutationPerformed`／`orderCreated`／`vehicleMoved` 均为 `false`。
- 本轮只改 `scripts/`、`docs/` 与 `evidence/`，未触产品代码或测试项目，因此未跑 tier 1。
