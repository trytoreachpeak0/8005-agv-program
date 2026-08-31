# 从安装、卸载、更新与 G3 runner 中拆除证书机制

Type: task
Mode: AFK
Status: claimed
Blocked by: 01

## Question

用户选择「全拆」而非「留着不用」：安装链里只要还会生成证书、还带 `-InstallCurrentUserRoot` 这类
参数，他要的部署复杂度下降就没有兑现。本票在 `8005-agv-control-server` 拆掉整条证书机制。

已定位的承载点：

- `scripts/Install-ControlServerLocal.ps1` — 生成自签根与 `localhost` 叶证书、导出 PFX 与 PEM、
  写 `certificate.caCertificateFile`／指纹进安装结果 JSON、健康检查钉扎根证书、
  `-InstallCurrentUserRoot` 参数、失败回滚时「移除导入的根证书」那一支；
- `scripts/Uninstall-ControlServerLocal.ps1` — 结果 JSON 里「根证书移除了几张」及相应逻辑；
- `scripts/Update-ControlServerLocal.ps1` — 同类证书处理；
- `scripts/run-staged-g3.ps1`、`scripts/run-staged-g3-restart.ps1`、
  `scripts/Invoke-AuthorizedAbsentObservationShadow.ps1` — `-InstallTemporaryCurrentUserRoot`
  授权、临时根证书的安装与 `finally` 移除；
- `scripts/New-WireToGateReleaseCandidate.ps1` — 打包时与证书相关的处理和校验。

拆除后健康检查改为直接经 HTTP 请求，不再需要钉扎任何根证书，也不再需要 `--ssl-revoke-best-effort`
之类的绕行参数。

票 01 冻结的三项直接落在本票（详见其 Answer 第 3、5 节）：

- `Install-ControlServerLocal.ps1` 新增 `-ListenAddress` / `-HealthBindAddress` 参数，**默认仍为
  `127.0.0.1`**。当前脚本把 `listenAddress` 硬写为 `127.0.0.1`（第 288 行）、healthOrigin 硬写为
  `https://localhost:$HealthPort`（第 39 行），两处都要参数化；异机部署显式传入；
- 脚本写出的 `appsettings.Production.json` 按票 01 第 2 节的字段终态生成（删三个 `OnboardTransport`
  证书字段与 `requireHttps`，`Health:url` 值改 http）；
- **升级路径主动清理遗留物**：`Update-ControlServerLocal.ps1` 删除
  `%ProgramData%\8005\ControlServer\certs\` 与 machine 级环境变量
  `CONTROL_SERVER_ONBOARD_CERTIFICATE_PASSWORD`。`CurrentUser\Root` 里的自签根证书**不由脚本删除**
  （在执行安装的那个用户账户作用域下，服务账户未必够得着），改为票 04 的手册人工步骤——否则会出现
  「脚本报告清理成功、根证书其实还在」的假绿。

风险与约束：

- 这三个 G3 runner **零测试覆盖，且承载上一轮全部证据**。上一轮票 24 曾拒绝改动它们，理由是风险
  不对称。本轮不得不动它们，因此改动要最小化，只摘证书相关分支，不顺手重构、不抽公共模块（那仍
  在 Out of scope）。
- 安装脚本的失败回滚路径必须保持完整：删服务、删安装目录、还原机器作用域环境变量。只移除其中
  「移除根证书」那一步，不得削弱其余回滚。

完成判据：在隔离实例上跑通安装→启动→停止→再启动→强制重启→卸载全流程，结果 JSON 据实记录服务
与目录状态，全程无任何证书生成、导入或移除动作，且**不弹出任何信任确认对话框**，可在非交互环境
完整跑完。生产服务全程不受影响。

## Progress（2026-08-31，未 resolved）

代码改动已全部落地并**已推送**：`8005-agv-control-server` `ControlServer_MVP@c7874f0`
（票 02 的 `ae4a17d` 随同推出，基线 `e5ee065`）。取证目录
`evidence/g2/20260831-plaintext-transport-ticket03/`（`SUMMARY.md` 是入口）。

**本票仍然 open 的唯一原因**：完成判据要求的隔离生命周期验收**没有跑**。
`Install-ControlServerLocal.ps1` 与 `Uninstall-ControlServerLocal.ps1` 都以 `Assert-Administrator`
开头，本轮会话不是管理员。验收脚本已写好并随证据入仓：
`evidence/g2/20260831-plaintext-transport-ticket03/Invoke-IsolatedLifecycle.ps1`，隔离服务名
`8005 AGV ControlServer Ticket03 Probe`、独立安装／数据／备份根、端口 58405／58407，并在安装前后
快照 `CurrentUser\Root` 指纹集、机器级证书口令变量与生产服务监听端口。下一个 session 在提权
PowerShell 7 里执行它，读回 `lifecycle-report.json` 即可收尾本票。

### 已改完的承载点

| 文件 | 处理 |
| --- | --- |
| `Install-ControlServerLocal.ps1` | 删自签根／叶生成、PFX/PEM 导出、`-InstallCurrentUserRoot`、根证书导入与回滚移除、`--cacert`／`--ssl-revoke-best-effort`；健康检查改明文 HTTP；新增 `-ListenAddress`／`-HealthBindAddress`（默认仍 `127.0.0.1`，通配绑定时本地检查回落 `127.0.0.1`）；结果 JSON 删整个 `certificate` 块，`httpsEndpoint`→`httpEndpoint`，`onboardTransportEndpoint` 由 `tls://` 改 `tcp://` |
| `Uninstall-ControlServerLocal.ps1` | 删 `-TrustedRootThumbprint` 参数、`Remove-CertificateByThumbprint` 与两个结果字段 |
| `Update-ControlServerLocal.ps1` | 删 `%ProgramData%\...\certs\` 与机器级 `CONTROL_SERVER_ONBOARD_CERTIFICATE_PASSWORD`（失败时回滚还原口令）；**新增沿用配置的迁移**；健康检查地址改从迁移后的 `Health:url` 推导而非硬写 `localhost:58007` |
| `run-staged-g3.ps1` | 删 `-InstallTemporaryCurrentUserRoot` 与 `New-/Remove-TlsMaterial`；harness 的 TLS 代理并入既有 `RunPlainProxyAsync`、TLS 连接器并入既有 `OpenPlaintextAsync`，指纹参数整条链路移除（−423／+58 行） |
| `run-staged-g3-restart.ps1`、`run-demand-bearing-g3-vectors.ps1` | 删 `OnboardTransport__serverCertificatePath=''` 等注入 |
| `Invoke-AuthorizedAbsentObservationShadow.ps1` | 删对已安装 PFX 与机器级口令的依赖、握手取指纹一段；投影端点改 http |
| `New-WireToGateReleaseCandidate.ps1` | **有意不改**，理由见下 |

安装脚本失败回滚路径按票要求保持完整：删服务、删安装目录、还原机器作用域 RIoT 值三段原样保留，
只移除了「移除根证书」那一支。

### 已取到的行为证据（红绿成对，同一检测器）

隔离端口 58305／58307、隔离 SQLite；生产服务全程 `Running`，监听仍为 `127.0.0.1:58005`／`:58007`。
两份被测配置与迁移函数都是用 PowerShell AST 从脚本里抽出后求值的，不是探针另写一份。

- **绿**：安装脚本现在写出的配置 → 明文启动，`127.0.0.1:58305`／`:58307` 实际在监听，
  `transport=plaintext`，`/health/live` 返回 `live`，启动日志零证书字样；
- **红**：`e5ee065` 版安装脚本生成的 TLS 期配置原样沿用 → 进程拒绝启动，四个已删键逐个报出，
  退出码 `-532462766`；
- **绿**：同一份文件经 `Convert-RetainedConfigurationToPlaintext` 迁移后 → 正常启动，
  `residualCertificateKeys: []`。

### 对本票 Question 的三处更正

1. **「三个 G3 runner 都带 `-InstallTemporaryCurrentUserRoot` 授权、临时根安装与 finally 移除」不
   成立**。全仓只有 `run-staged-g3.ps1` 有该开关。另两个 runner 的实际问题方向相反：它们注入
   `OnboardTransport__serverCertificatePath=''`，而票 02 的过时键校验比对的是**键名**，空值同样算
   键存在——**照原样它们在票 02 之后已经拉不起服务端**。两处注入已删。这也意味着票 02 之后、本票
   之前，这两个 runner 处于静默失效状态。
2. **升级路径不止是「清理遗留物」**。`Update-ControlServerLocal.ps1` 把已装的
   `appsettings.Production.json` 原样带进新安装目录，票 02 之后这等于把新二进制显式拒绝的键喂给
   它——升级必然启动失败并回滚。因此在票 01 第 5 节的两项清理之外，本票加了配置迁移（删四个键、
   `Health:url` 的 https→http）。这超出本票 Question 的字面范围，但不做它升级路径根本不通。上面的
   红侧就是这条的直接证据。
3. **`New-WireToGateReleaseCandidate.ps1` 无需改动**。本票把它列为承载点，但其中与证书相关的只有
   secret scan 的私钥块规则、`pkcs12-password-literal` 规则与 `.pfx/.p12/.pem/.key/.jks/.keystore`
   扩展名清单——那是阻止密钥材料进发布包的门禁，不是证书机制。删掉等于削弱发布门禁，与本轮方向
   相反。保留原样是有意决定。

### 本轮自己引入又修掉的一个回归

数据根此前是被 `New-Item -Path $certificateDirectory -Force` 顺带创建的。删掉证书目录后，全新安装
会在 `Set-RestrictedDirectoryAcl $dataRoot` 处失败。已补显式创建（`c7874f0`）。**该缺陷是静态核查
出来的，不是被某次运行证伪的**——生命周期验收仍然欠着，这正是为什么它必须真跑一次。

### 无法在隔离实例上排练的部分

`Update-ControlServerLocal.ps1` 把服务名、安装／数据／备份根硬写成生产值，没有对应参数，因此升级
流程**无法**在隔离实例上排练：唯一执行对象就是生产服务。这是既有属性而非本轮引入。本票只能以上面
的红绿对照覆盖迁移逻辑与产品行为，**未覆盖**证书目录删除、机器级口令清除与备份／回滚这三段的真实
执行。是否为该脚本补参数化留给票 09 决定。

### 留给票 04 的新增一条

`docs/RELEASE-CANDIDATE.md` 第 **245** 行的 `-TrustedRootThumbprint <安装结果里的指纹>` 不在票 04
已定位的段落清单里，该参数已被删除，实施票 04 时须一并处理。`README.md:92` 的
`-InstallCurrentUserRoot` 同理（票 02 已把 README 留给票 04）。
