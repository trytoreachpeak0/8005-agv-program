# 只读回读核验 owner 的车载端改动

Type: task
Mode: AFK
Status: resolved
Blocked by: 05

## Question

王昆改完并推送后，在**只读**前提下核验车载端改动确实落地且与服务端形态对齐，然后把该 commit 固定
为本轮候选的车载端身份。对 `8005-agv-onboard-hmi` 零写入：只 fetch 与 `git show`，不建分支、不提交、
不推送、不建 tag。

核验内容：

- **四处**校验在新 commit 上的实际形态，与票 01 冻结的形态逐条比对（不是「他说改了」，而是读到代码）。
  第四处 `WireToGateSettings.Validate(production: true)` 的指纹强制最容易被漏改，必须单独确认；
- 票 01 列入「不要动」的两处 `IsForbiddenProductionHost` 是否仍在——若被顺手删掉，生产配置忘改样例值
  的保护就没了，须回报给 owner 而不是默认接受；
- 配置模板中 `wireToGate.useTls`、`serverCertificateSha256`、`vehicleSafety.endpoint` 的终态与服务端
  票 02 的实现**互相能用**——特别要排除一端删了字段而另一端仍要求该字段的情况；
- 该 commit 与 `31263b1` 的关系（`merge-base --is-ancestor` 确认它包含票 27 那半可见性修复，
  不是从更早基线分叉出来的）；
- 车载端自身测试的状态：他是否跑过、结果如何。若无法从远程判断，据实记为未知而不是推定通过。

判据设计要求：红侧必须证明检测器会响。例如比对形态时，把目标形态的关键字符翻掉应当报出差异；
`merge-base` 判据要在一个已知不含 `31263b1` 的 commit 上验证会返回否定。

上一轮的教训直接适用：托管构建每次新 MVID，`.dll` 哈希不构成内容证据；要证明改动进了二进制得用
新增／消失的**符号名**。本票只核验源码与 commit 关系，二进制层面的核验归票 08。

## 票 05 交来的输入（2026-08-31）

待核验的 commit 是 **`OnboardHmi_MVP@238b46e`**（`238b46eb2c9ae90584e4288a782176f66b7de942`，
`refactor: switch onboard transports to plaintext`，Kun Wang，2026-08-31 22:11 +0800），是 `31263b1`
的**快进**一个提交。票 05 只看了元信息与 `--stat`，未读一行改动后的代码，因此下列全部仍未证。

`git diff --stat 31263b1..238b46e` 共 17 个文件、+172/−140。按转交件对照：

- **点名且已动**：`Configuration.cs`（+66/−…）、`WireToGateSessionClient.cs`（−68）、
  `ControlServerVehicleSafetySignalProvider.cs`、`appsettings.json`、
  `appsettings.Production.example.json`、`ConfigurationTests.cs`、
  `ControlServerVehicleSafetySignalProviderTests.cs`、`WireToGateG2Tests.cs`（4 行）、
  `scripts/run-staged-g3-recovery-ack-drop.ps1`（恰 −1 行）、以及 §7 的三个文档。
- **点名为「不要动」且确未动**：`evidence/g3/20260826-recovery-ack-drop-cc6e2b9-0455147/runner.ps1`
  不在 diff 里。
- **未点名却被他改了，本票须逐个判读**：`docs/LOCAL_VALIDATION_RUNBOOK.md`、
  `docs/WANG_KUN_FIRST_INTEGRATION_WORK_PACKAGE.md`、`scripts/run-local-validation.ps1`、
  `scripts/run-w2g-g2.ps1`、`src/SQCD.Agv.Wpf/WireToGateBusinessService.cs`。判据同上：读代码，
  不接受「大概是顺手改的」。`WireToGateBusinessService.cs` 尤其要看——它在 WPF 侧，是唯一被改到的
  非 Infrastructure 产品文件。

`merge-base --is-ancestor 31263b1 238b46e` 预期为真（快进）；按本票判据设计要求，仍须在一个已知
不含 `31263b1` 的 commit 上验证该判据会返回否定，否则这条判据没有红侧。

王昆**没有文字答复**，只推了提交。因此「他是否跑过车载端测试」目前是**未知**；若从远程判不出来，
据实记为未知，不得推定通过，也不要替他跑——该仓对 agent 只读，跑测试需要 checkout 到可写副本，
若要跑必须在仓外一次性克隆里跑并保证对该仓工作树零影响。

## Answer

**车载端改动核验通过，`OnboardHmi_MVP@238b46e` 固定为本轮候选的车载端身份。**
核验中发现一处**服务端仓**的跨端错配（票 03 遗留），已开票 12，车载端本身无缺陷。

对 `8005-agv-onboard-hmi` 的写入：**零**。全程只做 `git fetch --all --prune`、`git log/diff/show/grep <commit>`，
未 checkout、未建分支、未提交、未推送、未建 tag；`git status --porcelain` 事后为空，本地工作分支未动。

### 1. commit 身份与祖先关系（含红侧）

| 判据 | 结果 |
| --- | --- |
| `origin/OnboardHmi_MVP` tip | `238b46eb2c9ae90584e4288a782176f66b7de942` |
| 作者／时间 | Kun Wang <867963893@qq.com>，2026-08-31 22:11:03 +0800 |
| 提交信息 | `refactor: switch onboard transports to plaintext`（无正文） |
| `merge-base --is-ancestor 31263b1 238b46e` | **真** — 含票 27 的半可见性修复 |
| 红侧：`merge-base --is-ancestor 31263b1 304e6ad` | **假** — 该判据在不含 `31263b1` 的 commit 上确实返回否定 |

### 2. 四处硬校验的实际终态（逐条读代码，非 `--stat`）

| # | 位置 | 冻结形态 | 实际 | 判定 |
| --- | --- | --- | --- | --- |
| 1 | `WireToGateSessionClient.cs` | 删 loopback 守卫 | `if (!options.UseTls && !IsLoopback(...))` 整块删除；连带删 `CreateTransportStreamAsync` 的 `SslStream` 分支、`ValidateServerCertificate` 全方法、`IsLoopback`、`WireToGateSessionOptions` 的两个位置参数、三条 using（`System.Net`／`Net.Security`／`X509Certificates`），`using System.Security.Cryptography;` **按转交件 §3 保留**（内容哈希在用）。连接改为 `client.GetStream()` | 通过 |
| 2 | `Configuration.cs:190` | endpoint scheme 改 http | `Uri.UriSchemeHttps` → `Uri.UriSchemeHttp`，异常文案同步改「必须使用HTTP」 | 通过 |
| 3 | `ControlServerVehicleSafetySignalProvider.cs:95` | 运行时 scheme 校验改 http | 同上改法；`UnknownSignal("HTTPS_REQUIRED")` → `"HTTP_ENDPOINT_REQUIRED"`，`HTTPS_REQUEST_FAILED` → `HTTP_REQUEST_FAILED`；`CreateTrustedHttpClient` → `CreateHttpClient`，删掉「必须走 Windows 证书信任」的注释 | 通过 |
| 4 | `WireToGateSettings.Validate(production: true)` | **放开指纹强制** | `ServerCertificateSha256` 非空／非全零两条断言删除，`normalizedCertificateHash` 局部变量与 `(UseTls && …Length != 64)` 一并删；异常文案改为「Production环境的ControlServer地址或构建commit仍是本机/占位配置。」 | 通过 — **最易漏的一处确已改** |

`WireToGateSettings` 的 `UseTls`／`ServerCertificateSha256` 两个属性本身也已删除，`ToSessionOptions()` 的实参同步减两个。

### 3. 「不要动」清单

- `IsForbiddenProductionHost`：`238b46e` 上 `git grep -c` = **4**（`VehicleSafetySettings` 与 `WireToGateSettings`
  各一个定义＋一个调用），与 `31263b1` 的 **4** 相同，两处 production 守卫都在。
  红侧：把关键字翻成 `IsForbiddenProductionHostX` 后同一命令零命中，说明该判据会响。
- `evidence/g3/20260826-recovery-ack-drop-cc6e2b9-0455147/runner.ps1` **不在 diff 里**，历史证据快照原样保留
  （它第 278 行仍有 `useTls`，这是正确的）。

### 4. 转交件 §4.3 留给他定的问题：他选了「加」

车载端**对称实现了过时键拒绝**——`OnboardSettings.Load` 新增 `RejectRemovedTransportKeys(json)`，
在反序列化**之前**解析原始 JSON，`wireToGate` 下出现 `useTls` 或 `serverCertificateSha256`（大小写不敏感）
即抛「WIRE_TO_GATE配置键{name}已移除，当前版本固定使用明文TCP/HTTP传输。」

与服务端票 02 的形态一致，方向正确。**但它正是下面第 6 节那处跨仓错配的触发点。**

### 5. 配置面终态与服务端票 02 的互用性

车载端（`238b46e`）：`appsettings.json` 删 `useTls`（本就无 `serverCertificateSha256`），
`appsettings.Production.example.json` 删两键；两个文件 `vehicleSafety.endpoint` 改 `http://`。

服务端（`8005-agv-control-server@c80d2d3`，`src/ControlServer.Host/appsettings.json`）：
`OnboardTransport` 只剩 `enabled`／`listenAddress`／`port`／`maxLineBytes`／`credentialEnvironmentVariable`，
`OnboardSafetyProjection` 只剩 `enabled`／`credentialEnvironmentVariable`，`Health:url` = `http://127.0.0.1:58007`。
与票 01 §2 冻结的终态逐字相符。

逐项对表，**未发现「一端删了字段而另一端仍要求该字段」**：

| 车载端 | 服务端 | 判定 |
| --- | --- | --- |
| `wireToGate.host`／`port`（默认 58005，`ConfigurationTests` 断言 `DefaultControlServerPort == 58_005`） | `OnboardTransport.port` = 58005，`listenAddress` 已参数化 | 通过 |
| `vehicleSafety.endpoint` 强制 `http` | 投影挂在 `Health:url` 的 http 绑定上 | 通过 |
| `credentialEnvironmentVariable` = `CONTROL_SERVER_ONBOARD_CREDENTIAL` | 同名，两处一致 | 通过 |
| 两键删除且**存在即拒** | 服务端不再产出、不再要求任何证书字段 | 通过 |
| endpoint 为 `https` 时**拒绝** | 服务端不再提供 https | 通过 — 方向一致 |

一处非缺陷的观察，留给票 04：`appsettings.Production.example.json` 的占位 endpoint 是
`http://REPLACE_CONTROL_SERVER_HOST/api/onboard/v1/vehicle-safety`，**不含端口**，现场必须补 `:58007`。
这不是本轮引入的（TLS 期同样缺端口，默认 443 一样不对），但手册重写时应显式写出端口。

### 6. 发现的跨端错配（服务端仓，非车载端问题）

`8005-agv-control-server@c80d2d3` 的 `scripts/run-staged-g3-restart.ps1:508` 仍是**无条件赋值**：

    $settings = Get-Content -LiteralPath $onboardConfig -Raw | ConvertFrom-Json
    ...
    $settings.wireToGate.useTls = $false          # 第 508 行
    $settings | ConvertTo-Json -Depth 30 | Set-Content ... -Encoding utf8NoBOM

票 03 的提交 `991cb8e` 已经把另两处改成条件式（`run-staged-g3.ps1:2167`、
`Invoke-AuthorizedAbsentObservationShadow.ps1:558`，并写了「A TLS-era onboard build still carries these two
keys and a plaintext one will not」的注释），**唯独漏了 restart runner**——原因可查：那两处原本是
`useTls = $true`，改值时被看到；restart runner 本来就写 `$false`，值不需要改，于是整行被跳过，
`991cb8e` 对该文件只碰了环境变量段。`run-demand-bearing-g3-vectors.ps1` 无此赋值，不受影响。

**失效形态（本地实测取证，非推断）**。在 pwsh 7 上以同构输入验证：

    改前属性: enabled,host
    $settings.wireToGate.useTls = $false
      → SetValueInvocationException: The property 'useTls' cannot be found on this object.
    条件保护写法（另两个 runner 的形态）: 不报错，写回 JSON 不含 useTls

即**票 05 §5.4 的机理描述有误**：`ConvertFrom-Json` 产出的是 `PSCustomObject`，无条件赋值不存在的属性
**不会**「新增回该属性并写回配置」，而是**当场抛异常**。结论方向不变（runner 在明文车载端上跑不了），
但形态从「静默写回错键」变为「脚本硬失败」，反而更容易发现。脚本用 `utf8NoBOM` 编码，确认运行在
pwsh 7，与实测环境一致。

即便赋值侥幸通过，第二道也会挡：车载端第 4 节的 `RejectRemovedTransportKeys` 见到 `useTls` 即拒绝启动。

该缺陷在**服务端仓（可写）**，不在车载端，故不回报王昆。已开
[`把 G3 runner 对齐到明文车载端 238b46e`](12-align-g3-runners-to-the-plaintext-onboard-commit.md)。

### 7. 他多改的五个文件：全部无害，逐个读过

| 文件 | 改动 | 判定 |
| --- | --- | --- |
| `src/SQCD.Agv.Wpf/WireToGateBusinessService.cs` | 唯一被改的非 Infrastructure 产品文件，但**只是一行注释**：`TLS/session validation` → `Transport/session validation`。无代码变化 | 无害 |
| `docs/ONBOARD_DEVELOPER_HANDOFF.md` | TLS 措辞同步；**主动新增**一段已知限制：「明文传输会暴露 Bearer/credentialProof，并允许网络中间人篡改 STOPPED 投影；两端必须同版本切换，不能将明文 OnboardHmi 与旧 TLS ControlServer 混用」 | 无害，与票 01 §7 及票 11 方向一致 |
| `docs/LOCAL_INTEGRATION_MATRIX.md` | IS-03／IS-05 行的 TLS 措辞改明文，IS-03 外部门禁栏加「明文安全风险已知」 | 无害 |
| `docs/LOCAL_VALIDATION_RUNBOOK.md`／`scripts/run-local-validation.ps1`／`scripts/run-w2g-g2.ps1` | 三处收尾文案里的「现场 TLS/网络」→「现场明文网络」，`run-w2g-g2.ps1` 改的是证据 JSON 的 `knownLimitations` 字符串 | 无害，无逻辑变化 |
| `docs/WANG_KUN_FIRST_INTEGRATION_WORK_PACKAGE.md` | 分层描述里「TLS/NDJSON 协议客户端」→「明文 TCP/NDJSON」 | 无害 |

范围确实略大于转交件，但全部是措辞对齐与一条**主动补上的**已知限制，未引入本轮不想要的东西。

### 8. 测试改动：含红侧对照，质量高于转交件要求

- `ConfigurationTests.cs`：`EnabledVehicleSafetyProjectionRejectsPlainHttp` 反转为
  `…AcceptsPlainHttp`，并**新增** `EnabledVehicleSafetyProjectionRejectsHttps`；
  新增 `[Theory] RemovedTransportKeyIsRejectedInsteadOfSilentlyIgnored`（`useTls`／`serverCertificateSha256`
  两个 InlineData，断言异常含「已移除」与「明文TCP/HTTP」）；默认配置断言新增「两键不存在 ＋ endpoint scheme 为 http」。
- `ControlServerVehicleSafetySignalProviderTests.cs`：`HttpEndpointIsRejectedBeforeNetworkCall` 改为
  `HttpEndpointSendsRequestAndPublishesResponse`（断言真发了一次请求且解析出 `Stopped`），
  并**新增** `HttpsEndpointIsRejectedBeforeNetworkCall`（`RequestCount == 0` ＋ `HTTP_ENDPOINT_REQUIRED`）——
  即把原来的绿侧断言搬到了对侧，放开的行为与新收紧的行为**两侧都有测试**。
- `WireToGateG2Tests.cs` 4 行：endpoint 改 http、`WireToGateSessionOptions` 构造去掉两个实参。纯适配。

`238b46e` 全仓 `git grep useTls|serverCertificateSha256`：只剩 `Configuration.cs` 的拒绝逻辑本身、
`ConfigurationTests.cs` 的断言、以及那份不得修改的历史证据快照。`https://`／`SslStream`／`X509`／`Schannel`
在 `src`／`tests`／`scripts` 中的残留只有两处**故意的**负向测试 URL 与一条 pubxml 里的微软文档链接。无遗漏。

### 9. 他是否跑过车载端测试：**未知**（据实记录，不推定通过）

- 提交未附任何 evidence 目录、`.trx` 或测试摘要（`--stat` 只有 17 个源／配置／文档文件）；
- 仓内无 `.github/`、无 `azure-pipelines`、无 `.gitlab-ci`，没有能证明测试跑过的 CI；
- `evidence/` 下最新仍是 `g3/20260826-recovery-ack-drop-cc6e2b9-0455147`，本次未新增；
- 他没有文字答复。

因此「车载端 Unit 80/80、W2G G2 13/13」这条基线在 `238b46e` 上**未被证明仍然成立**。
未替他跑：该仓对 agent 只读，跑测试需 checkout 到可写副本。若票 08／09 需要这条证据，
须在仓外一次性克隆中跑并保证对该仓工作树零影响，或由用户向王昆索取。
**该未知项不阻塞本票**——本票的完成定义是源码与 commit 关系的只读核验，二进制与运行期证据归票 08 起。

### 10. 固定为候选身份

    OnboardCommit = 238b46eb2c9ae90584e4288a782176f66b7de942

票 08 的 `New-WireToGateReleaseCandidate.ps1 -OnboardCommit` 用此 40 位全长值
（脚本第 32 行强制 `^[0-9a-f]{40}$`）。
