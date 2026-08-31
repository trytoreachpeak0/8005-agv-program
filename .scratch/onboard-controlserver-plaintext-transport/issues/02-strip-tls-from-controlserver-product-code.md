# 按冻结形态改掉服务端产品代码的 TLS/HTTPS

Type: task
Mode: AFK
Status: resolved
Blocked by: 01

## Question

在 `8005-agv-control-server`（可写）按票 01 冻结的形态落地服务端改动，使其在**非 loopback 绑定**下
以明文 TCP 提供业务协议、以明文 HTTP 提供车辆安全投影，并且启动时不再需要任何证书。

已定位的改动点：

- `src/ControlServer.Host/Transport/OnboardTcpServer.cs` — 第 108～125 行的 `SslStream` 服务端认证
  分支、第 141 行的明文守卫、第 153 行的 `TLS={TlsEnabled}` 日志、第 162～165 行的
  `OnboardTlsCertificateLoader`；
- `src/ControlServer.Host/Program.cs` — 第 24～32 行读取证书并 `ConfigureKestrel(... ConfigureHttpsDefaults ...)`；
- `src/ControlServer.Host/Runtime/OnboardSafetyProjectionOptions.cs` — 第 10 行默认值与第 23 行的
  `RequireHttps must remain true` 校验；
- `src/ControlServer.Host/Runtime/OnboardVehicleSafetyEndpoints.cs` — 第 38 行 `context.Request.IsHttps` 拦截；
- `src/ControlServer.Host/appsettings.json` — `OnboardTransport` 与 `OnboardSafetyProjection` 的
  字段与默认值，含 `listenAddress` 是否改为可绑非 loopback。

票 01 冻结后新增的三项（详见其 Answer 第 2、6、9 节）：

- `OnboardSafetyProjectionOptions.cs` 第 24 行的 `Health:url` 必须 https、第 29 行的
  `serverCertificatePath` 必需，两条校验一并删除，验证器只剩「凭据环境变量已填充」；
- **过时配置键在启动期显式拒绝**：读到 `serverCertificatePath`、
  `serverCertificatePasswordEnvironmentVariable`、`allowInsecureLoopback`、
  `OnboardSafetyProjection:requireHttps` 任一键即拒绝启动，消息直指该键已移除、传输为明文。理由是
  options 绑定会静默忽略未知键，让运维误以为链路仍加密；
- `docs/ai-spec/slices.md` 的 W2G-IS-00 行「最小持久边界与接口」栏含 `TLS peer`，改为明文 peer 的表述。

服务端测试的删改范围已由票 01 定明：删除 `OnboardTlsCertificateLoaderTests.cs` 整个文件，改写
`OnboardVehicleSafetyEndpointsTests.cs` 第 37/59/96–102/116 行，并新增「非 loopback 明文监听能启动」
与「http 请求能通过投影端点」两条。这两条须在改产品代码**之前**先跑一次并且**必须红**，红侧文本进证据。
仍然适用的原则：**不得为了让测试变绿而删掉仍在保护真实行为的断言**；G2／G3 向量与 fixture 的调整范围
不在本票，等测试红过一次后据实记录。

完成判据：Release 构建 0 warning、`dotnet format` 干净、tier 1 全绿且据实报出 skip 数；服务端在
非 loopback 地址上以明文启动成功，`/health/live` 经 HTTP 返回 200，安全投影端点经 HTTP 可达且无
凭据仍返回 401。判据必须是回读取证，不得以「构建成功」代替行为证据。

不推送远程由本票决定；未经票 08 之前的改动是否推送，按当轮实际情况在答案中据实记录。

## Answer

服务端产品代码已按票 01 冻结的形态改完并本地提交：`8005-agv-control-server`
`ControlServer_MVP@ae4a17d`（基线 `e5ee065`）。**未推送远程**——票 07 异机联调、票 08 重建候选都还在
上游，等票 03／04 落地后一并推更省一次校验。证据目录
`evidence/g2/20260831-plaintext-transport-ticket02/`（含 `SUMMARY.md`）。

### 1. 判据回读（不是「构建成功」）

| 判据 | 回读结果 |
| --- | --- |
| Release 构建 0 warning | `Build succeeded. 0 Warning(s) 0 Error(s)`，`TreatWarningsAsErrors=true` |
| `dotnet format --verify-no-changes` | 退出码 0 |
| tier 1 全绿并报 skip 数 | **Failed: 0, Passed: 249, Skipped: 0**，41 s |
| 非 loopback 明文启动 | 日志 `Onboard NDJSON listener started on 0.0.0.0:58105; transport=plaintext`；实际 listener 为 `0.0.0.0:58105` 与 `0.0.0.0:58107`；全程零证书 |
| `/health/live` 经 HTTP | `200`，body `{"status":"live"}` |
| 投影端点经 HTTP 可达、无凭据仍 401 | 匿名 `401` + `WWW-Authenticate: Bearer`；错误 Bearer 亦 `401` |

探针用隔离端口（58105／58107）与隔离 SQLite，已安装的生产服务全程未受影响（其监听仍是 loopback
58005／58007，改动前后一致）。

**红侧**（`red-side.txt`，改产品代码之前）：两条新测试都红，且红的正是被拆的两处守卫——
`A non-loopback Onboard listener requires a configured TLS server certificate.` 与
`Expected Ok<OnboardVehicleSafetyResponse> / Actual StatusCodeHttpResult`（426）。

**过时键拒绝**（票 01 第 6 节）另有一对红绿：同一二进制、同一配置，仅注入
`OnboardTransport__serverCertificatePath` 即
`OptionsValidationException: OnboardTransport:serverCertificatePath was removed in this version; the
Onboard transport is plaintext.`；不带该键的那次探针正常启动，所以这条红不是恒红。

### 2. 对票 01 与本票 Question 的五处更正

1. **`OnboardTransportOptions` 原本没有验证器，也没有 `ValidateOnStart`**（只有
   `Configure<OnboardTransportOptions>`）。票 01 第 6 节说的「验证器新增一条」实为新建
   `OnboardTransportOptionsValidator` 并把注册改成 `AddOptions().Bind().ValidateOnStart()`。附带效果：
   `OnboardTransport` 从本版本起参与启动期验证，之前不参与。
2. **检测「键是否存在」不能用 `configuration[key] is not null`，也不能用 `Section.Exists()`**。
   `appsettings.json` 里 `"serverCertificatePath": null` 这种写法两者都读不到，正是最需要拦的升级现场
   形态。改用 `GetSection(section).GetChildren()` 比对键名（`OrdinalIgnoreCase`）。
3. **`OnboardSafetyProjectionOptionsValidator` 的 `IConfiguration` 构造参数一并删除**——它只用于读
   `Health:url` 与 `serverCertificatePath` 两条已删校验。票 01 只写了「验证器只剩凭据一条」，未提这处
   签名变化，调用点与测试都要跟着改。
4. **端点的 `Results<>` 联合类型要删掉 `StatusCodeHttpResult`**：426 是它唯一的使用者，留着即为
   `TreatWarningsAsErrors` 下的死类型参数。`.Produces(Status426UpgradeRequired)` 的 OpenAPI 声明同删。
5. **`tools/ControlServer.FakeOnboard` 有一条票 01 与本票都漏列的 TLS 路径**：`--tls` 参数 +
   `SslStream` 客户端分支。全仓（scripts／docs／evidence／src）**零调用方**，是死参数，已一并删除。
   它是 G2／G3 的假车载端，留着就等于留了一条永不被测的 TLS 客户端。

### 3. 测试删改的实际形态（比票 01 更细）

- `OnboardTlsCertificateLoaderTests.cs` — 整个文件删除（被测类消失）。
- `PlainHttpIsRejectedBeforeCredentialOrRiotFactsAreRead` — 该行为已不存在，替换为
  `MissingExternalCredentialKeepsTheProjectionUnavailable`（凭据环境变量为空 → 503 fail-closed）。
  这条路径此前**无任何覆盖**，属净增而非净删。
- `AuthenticatedHttpsRequestReturnsFailClosedRiotProjectionWithoutExposingCredentials` 与新写的红侧
  测试合并为一条 `AuthenticatedPlainHttpRequestReturnsTheFailClosedRiotProjection`，被删测试的全部断言
  （reason codes、vehicleKey、`no-store`／`no-cache`、不泄凭据）原样保留。**据实说明**：红侧那次跑的是
  「http 能拿到 Ok」这一核心断言，其余断言是红跑之后从被删的 HTTPS 测试搬过来的，未重跑红侧。
- `EnabledProjectionRequiresHttpsCredentialAndCertificateConfiguration` 拆成两条：
  `EnabledProjectionRequiresOnlyAPopulatedCredentialVariable`（失败项恰好一条且是凭据）与
  `EnabledProjectionNoLongerDependsOnCertificateOrHttpsConfiguration`（凭据已填即 Succeeded）。
- 新增 `RemovedCertificateKeysAreRejectedInsteadOfSilentlyIgnored`（四个键各一例 Theory）与
  `PlaintextConfigurationPassesTheRemovedKeyCheck`（放行对照）。
- 新增 `OnboardTcpServerTests.NonLoopbackListenerStartsAndAcceptsPlaintextConnections`，带
  `IntegrationSlice=W2G-IS-00`。此前 `OnboardTcpServer` **零测试覆盖**。

### 4. 本仓再无测试触及 Schannel

删掉 `OnboardTlsCertificateLoaderTests.cs` 后，本仓不存在任何 Schannel／TLS 握手测试。其
`W2G-IS-00` trait 未失效：按该 trait 过滤仍选出 **24 条测试且全绿**。票 08 重建候选时须在证据中显式
写出这处与上一轮的覆盖差异，避免读起来像覆盖率无声下降。

### 5. 留给票 03／04 的边界

`README.md:28`「非 loopback Onboard 监听必须配置 TLS PFX」是产品行为陈述，本票已改；
`ControlServer.http` 的 `@baseUrl` 由 https 改 http。但 `README.md` 第 83／84／98／101 行描述的是
**安装脚本仍在做的事**（生成自签证书、装受信任根、保留 PFX），脚本没改之前改文档只会让 README 描述一个
不存在的行为，因此留给票 03 改完脚本后与票 04 一并处理。
