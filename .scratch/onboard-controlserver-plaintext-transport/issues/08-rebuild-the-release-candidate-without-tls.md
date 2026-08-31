# 重建不含证书机制的发布候选

Type: task
Mode: AFK
Status: resolved
Blocked by: 04, 07

## Question

现有 `w2g-mvp-rc-0.1.1` 绑 TLS 形态（服务端 `9daeef4` + 车载端 `31263b1` + `protocol-v0.1.1`）。
本票用 `New-WireToGateReleaseCandidate.ps1` 从改后的两端 commit 重建候选。

需要在本票冻结并据实记录的：

- 候选版本号与既有 release 的关系（`0.1.2` 或别的；`0.1.0`／`0.1.1` 是否保留、是否需要在其说明中
  回指本次传输层变更）。这一项在票 08 之前属 fog，此处定下；
- 车载端从**一次性克隆**构建，该仓零写入，沿用上一轮做法；
- 协议身份从产物**读回**而非重述，`protocol-v0.1.1` 的四个字段应与 0.1.1 逐字相同——本轮不动协议仓，
  若出现差异说明有别的东西变了，必须查清而不是记录了事。

判据设计，直接继承上一轮已被证伪的教训：

- **`.dll` 哈希不构成内容证据**。同源同 SDK 的托管构建每次新 MVID，「哈希变了」什么都不证明。
  证明改动进了二进制要用**符号级判据**：票 02 移除的 `OnboardTlsCertificateLoader` 之类符号在新产物
  应 ABSENT、在 0.1.1 产物 PRESENT，同时取一个两侧都应存在的既有符号作对照，确保 ABSENT 是真阴性
  而不是探测器坏了；
- 全量文件 SHA-256 校验必须证明会红（副本改一字节应从 OK 变 MISMATCH）；
- 发布脚本的扫描闸门（票 24 建立的 `Assert-ReleaseScanGate`）必须通过，允许清单仍只有三个具名的
  自建 RIoT SDK 包；**拆证书不得顺手放宽这道闸门**；
- 两端 Release 构建 0 warning；
- **W2G-IS-00 覆盖差异须显式说明**（票 01 第 9 节）：删除 `OnboardTlsCertificateLoaderTests.cs` 后本仓
  再无任何测试触及 Schannel，该切片的 G2 证据与上一轮不可逐条对比。证据里要写明这是形态变更的必然
  结果，不能让它看起来像覆盖率无声下降。

本票不安装、不启动、不跑旅程——那属票 09／10。旧候选不删。

## Answer

候选已重建并冻结。产物 `C:\Users\szy\Desktop\w2g-rc-20260901-238b46e`（一次性车载端克隆在
`…-238b46e-onboard-src`），逐条证据在服务端仓
`evidence/rc/20260901-rc020-plaintext-238b46e/SUMMARY.md`，提交 `ControlServer_MVP@eaaa5b1`（已推）。
本节只给结论与判据形态，细节不在此重复。

### 0. 三项冻结的决定（用户 2026-09-01 选定）

| 项 | 定为 | 理由 |
| --- | --- | --- |
| 候选版本号 | **0.2.0**（tag `w2g-mvp-rc-0.2.0`） | `0.1.0→0.1.1` 只动车载端且仍可互通；本轮是传输形态断裂——两个方向都握不上手（票 07），且 0.1.1 的站点配置现在会被两端**显式拒绝启动**。patch 位会被读成可就地替换。 |
| `0.1.0` / `0.1.1` | 保留、不可变，并在 0.1.1 说明里加回指 | 两份资产是已验收形态的记录。回指让装了 0.1.1 的人知道为什么连不上新服务端。**编辑动作归票 11**，本票只冻结决定。 |
| 车载端 `238b46e` 测试状态 | 实测，不推定 | 见第 6 节。原为雾区条目，本票按「自己在一次性克隆里跑」处理。 |

写 tag 的人注意：车载端程序集自身的 `InformationalVersion` 已经是
`0.2.0-safety-mock-travel+<commit>`。那是该应用的私有版本号，与联合候选号无关，两个 0.2.0 不得混为一谈。

### 1. 身份（从产物读回，不是重述）

- 服务端 `ControlServer_MVP@56d4b1cc2f26325ca853acc4e7278bbde8651874`；
- 车载端 `OnboardHmi_MVP@238b46eb2c9ae90584e4288a782176f66b7de942`（构建前远端头核过，王昆未推新提交）；
- 协议 `protocol-v0.1.1 @ 1531489e…`，**九个身份字段与 0.1.1 逐字相同**（票的要求是四个，实际把
  `tag`/`releaseVersion`/`profileId`/`protocolVersion`/`approvalStatus` 一并比了）。协议仓本轮不动，
  相同即预期；有差异才需要查。
- manifest SHA-256 `bfc1d7d4…`，SHA256SUMS SHA-256 `6bb268c9…`。归档副本重算仍等于该值
  （`.gitattributes` 早有 `evidence/rc/*/release-artifacts/** -text`，签出是字节级）。

### 2. 门禁：过了，且没被顺手放宽

`Secret scan findings: 0; key material files: 0`，`Scan gate: PASS`，两端 `buildWarnings=0`。

「不得顺手放宽 `Assert-ReleaseScanGate`」的判据不是「看起来没改」，而是
`git diff 9daeef4 56d4b1c -- scripts/New-WireToGateReleaseCandidate.ps1` **为空**——闸门函数、六条
密钥规则、六个密钥材料扩展名、三包允许清单与造出 0.1.1 的那份脚本逐字节相同。manifest 里的允许
清单仍是 `riot.sdk.core, riot.sdk.facade, riot.sdk.generated` 三个具名包，
`unexpectedUnresolvedLicenses` 为空。

### 3. 符号级判据：十消失、二新增、四对照

`symbol-probe/`。扫每个组件目录下全部 `.dll`/`.exe`（373 与 468 个文件），原始字节按 Latin-1 解码后
做**大小写敏感**的 ordinal 查找——UTF-16 用户字符串字面量（如 `"serverCertificatePath"`）无法与
ASCII 符号名互相冒充。

- 消失（老包 PRESENT → 新包 ABSENT）：服务端 `OnboardTlsCertificateLoader`、
  `CreateTransportStreamAsync`、`AllowInsecureLoopback`、
  `ServerCertificatePasswordEnvironmentVariable`、`RequireHttps`；车载端
  `ValidateServerCertificate`、`CreateTrustedHttpClient`、`ServerCertificateSha256`、`UseTls`、
  `CreateTransportStreamAsync`。
- 新增（老包 ABSENT → 新包 PRESENT）：`OnboardTransportOptionsValidator`、`RejectRemovedTransportKeys`。
- 对照（两侧都 PRESENT）：`OnboardTcpServer`、`HandleClientAsync`、`WireToGateSessionClient`、
  `ControlServerVehicleSafetySignalProvider`。

ABSENT 是真阴性的依据有两条，不止票里要求的一条：同一读取器在**两个包**里都能找到四个对照符号；
且它在新包里能找到本轮**新增**的两个符号。检测器被证明在两个方向上都会响，而不是一律沉默。

一个必须具名的框架携带者：`RequireHttps` 在 `Microsoft.AspNetCore.Mvc.Core.dll` 里也在（ASP.NET Core
自己的 `RequireHttpsAttribute`），两个包都带且未变。判定按两端**自有程序集**做，
`ControlServer.Host.dll` 里它是 PRESENT→ABSENT；`symbol-probe.json` 同时记录产品级与整包级状态，
没有把这个命中藏起来。

**过程中翻过一次车，据实记录**：探测器第一版把十六个符号全报 PRESENT，包括只存在于新包的那两个。
那是检测器坏了而不是发现——PowerShell 里 `@($hashtable[$missingKey])` 是 `@($null)`，`Count` 为 1，
未命中被读成命中。修法与注释都在归档脚本里；上面的结论出自修好后的那次。是「不可能的全绿」暴露了它。

### 4. 配置面：证书字段在运维实际要改的文件里消失了

- `controlserver/appsettings.json` 少了 `serverCertificatePath`、
  `serverCertificatePasswordEnvironmentVariable`、`allowInsecureLoopback`、
  `OnboardSafetyProjection.requireHttps`；
- `onboard-hmi/appsettings.Production.template.json` 少了 `useTls` 与 `serverCertificateSha256`，
  投影端点从 `https://REPLACE_CONTROL_SERVER_HOST/…` 变 `http://…`；
- manifest 的 `remainingSitePlaceholders` 由七项减为六项，少掉的正是
  `REPLACE_WITH_64_CHARACTER_SHA256`。

### 5. 全量哈希 868/868，红侧证明会响

`ok=868, mismatch=[], missing=[]`，且 `unlistedFilesInReleaseRoot=[]`——发布根里没有未被哈希的载荷。
红侧：把 `controlserver/appsettings.json` 复制到**发布根之外**再追加一个字节，同一比对从 `OK`
翻成 `MISMATCH`（`e6557aad…` → `8a3ee06c…`）；产物本身未被改动，事后重算仍等于记录值。

### 6. 车载端 `238b46e` 测试：113 绿 0 跳过（原雾区条目，已实测）

在发布脚本已经做好的一次性克隆里跑——即产出这批二进制的那份源码树：
`SQCD.Agv.UnitTests` 89 绿，`SQCD.Agv.WireToGateG2Tests` 24 绿，两者 Failed 0 / Skipped 0。
原始输出与两份 `.trx` 在 `onboard-tests/`。

对只读仓写入仍为零：`C:\Users\szy\Desktop\8005-agv-onboard-hmi` 的 `git status --porcelain` 为空，
仍停在 `OnboardHmi_MVP@bbfbc52`；一次性克隆的 tracked 文件零改动，唯一未跟踪项是发布脚本为钉 SDK
写的 `global.json`。

### 7. W2G-IS-00 覆盖差异：形态变更的必然结果，不是无声下降

`OnboardTlsCertificateLoaderTests.cs` 在 `9daeef4` 存在、在 `56d4b1c` 已删。删掉之后
`git grep -niE 'schannel|sslstream|x509|tls' -- tests/` **零命中**——本仓再无任何测试触及传输层安全。
仅剩的两处证书相关是覆盖的**反面**：新增的否定测试
（`RemovedCertificateKeysAreRejectedInsteadOfSilentlyIgnored`、
`EnabledProjectionNoLongerDependsOnCertificateOrHttpsConfiguration`），断言残留键会让启动失败。
因此该切片与 0.1.1 的证据无法逐条对比：已经没有 TLS 代码路径可供覆盖。

### 8. 未跑 tier 1，且不该跑

`git diff ae4a17d 56d4b1c -- src/ tests/` 为空。最后一次 tier 1（249 绿 0 跳过）在 `ae4a17d`，此后的
提交只动了脚本、文档与证据。候选的产品源码正是那次覆盖过的源码。本票也未改任何产品代码。

### 9. 与 0.1.1 的文件级差异，以及 apphost 那两行

`controlserver/` 372 同 11 变，`onboard-hmi/` 464 同 13 变，两包文件数与 0.1.1 相同（383 / 477），
零增零删。托管程序集的 DIFF 是重建噪声（每次新 MVID），不承担任何内容主张——内容主张在第 3 节。

本轮比 0.1.1 那次多出的两项是两个 apphost `.exe`。它们不由本仓源码编译，值得一句解释：两者与 0.1.1
的副本**逐字节相同**，只有一段 79 字节区间不同（39 / 40 个差异字节，隔字节分布），即 Win32 版本资源里
UTF-16 的 `InformationalVersion` 字符串——服务端 `1.0.0+9daeef4…`→`1.0.0+56d4b1c…`，车载端
`…+31263b1…`→`…+238b46e…`。这恰好是唯一一个哈希差异**能**证明 commit 绑定的文件。

### 10. 交给后续票的具体值

- 票 09／10 的候选根：`C:\Users\szy\Desktop\w2g-rc-20260901-238b46e`；旧候选未删。
- 票 11 的 tag 目标 commit：`56d4b1cc2f26325ca853acc4e7278bbde8651874`（40 位全 SHA，票 28 的教训）。
  注意证据提交 `eaaa5b1` 在候选之后，**不是**候选身份。
- 票 13 的 `ControlServerCommit`：同上 `56d4b1c…`；`OnboardCommit` 仍是 `238b46e…`（票 12 已锁，未变）。

### 不在本票范围

未安装、未启动、未跑旅程（票 09／10）；未发布、未建 tag、未改 0.1.1 的 release 说明（票 11）。
