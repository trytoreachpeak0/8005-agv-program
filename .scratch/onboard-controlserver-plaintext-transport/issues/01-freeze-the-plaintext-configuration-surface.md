# 冻结两端安全校验的放开形态与配置面终态

Type: grilling
Mode: HITL
Status: resolved
Blocked by:

## Question

四处硬校验要「放开」，但放开有三种截然不同的形态，它们的可回退性、误配风险和转交件内容都不同。
本票冻结形态，后续所有实现票与转交件都按它执行。

服务端两处（可写）：

- `OnboardTcpServer.cs:141` — `if (!tlsEnabled && (!IPAddress.IsLoopback(address) || !_options.AllowInsecureLoopback))`
- `OnboardSafetyProjectionOptions.cs:23` — `if (!options.RequireHttps) failures.Add("OnboardSafetyProjection.RequireHttps must remain true.")`

车载端三处（只读，交王昆）：

- `WireToGateSessionClient.cs:1850` — 非 TLS 只允许 loopback
- `Configuration.cs:152` — endpoint scheme 必须 https
- `ControlServerVehicleSafetySignalProvider.cs:95` — 运行时二次校验 https

候选形态：

1. **彻底删除**。移除 TLS/HTTPS 代码路径本身：`OnboardTlsCertificateLoader`、`SslStream` 分支、
   Kestrel `ConfigureHttpsDefaults`、`serverCertificatePath`／`useTls`／`serverCertificateSha256`／
   `requireHttps` 等配置字段一并消失。最简单、最不可能误配，但**不可回退**——将来若要恢复 TLS
   需要重新实现。
2. **保留代码路径，反转默认并放开守卫**。TLS 仍可通过配置启用，只是默认关闭且不再限制 loopback。
   可回退，但保留了两端各一套已不再被任何测试覆盖的分支，且 `serverCertificatePath` 之类字段仍留在
   配置文件里，与「部署时不该看到证书」的动机相冲突。
3. **删除服务端 TLS，车载端保留开关**。不对称，会让两端配置面语义分叉。

还要一并冻结的配置面细节：

- `OnboardTransport` 中 `serverCertificatePath`、`serverCertificatePasswordEnvironmentVariable`、
  `allowInsecureLoopback` 三个字段的去留；`listenAddress` 默认值是否要从 `127.0.0.1` 改为可绑定
  非 loopback（异机必需）。
- `OnboardSafetyProjection.requireHttps` 字段去留；`Health:url` 已是 `http://127.0.0.1:58007`，
  异机访问是否需要改绑定地址。
- 车载端 `wireToGate.useTls`、`wireToGate.serverCertificateSha256`、`vehicleSafety.endpoint` 的
  终态形状——这三项要写进给王昆的转交件，必须与服务端形态严格对齐，不能出现一端删字段、另一端仍
  要求该字段的情况。
- 两端在明文形态下的**误配保护**：删掉 loopback 守卫后，配置写错 IP 会静默连到错误主机而不再有
  证书身份校验兜底。是否需要用别的东西替代（例如握手时校验 `agvId`／`vehicleKey` 是否匹配，或
  完全不加）。

本票不写代码，只产出一份两端对齐的形态决定与配置面清单。

## Answer

用户 2026-08-31 在四轮问询中逐条选定推荐值。形态冻结如下，后续所有实现票与转交件按此执行。

### 0. 事实更正：硬校验是「5 + 4」，不是「2 + 3」

本票开票时的清单不全。实际核查（服务端 `e5ee065`，车载端 `bbfbc52`）：

**服务端五处**（`8005-agv-control-server`，可写）：

| 位置 | 内容 |
| --- | --- |
| `OnboardTcpServer.cs:141` | 非 loopback 明文抛 `A non-loopback Onboard listener requires a configured TLS server certificate.` |
| `OnboardSafetyProjectionOptions.cs:23` | `RequireHttps must remain true.` |
| `OnboardSafetyProjectionOptions.cs:24` | `Health:url` 必须是 https，否则投影拒绝启动 |
| `OnboardSafetyProjectionOptions.cs:29` | `OnboardTransport:serverCertificatePath` 为空则投影拒绝启动 |
| `OnboardVehicleSafetyEndpoints.cs:38` | 运行时 `!context.Request.IsHttps` → 拒绝 |

关键结构事实：`Program.cs:24-32` 里 Kestrel 的 HTTPS 证书**取自 `OnboardTransport:serverCertificatePath`**。链路 A 与链路 B 共用同一张 PFX，不是两套证书机制；删掉该字段同时拆掉两条链路。

**车载端四处**（`8005-agv-onboard-hmi`，只读）：

| 位置 | 内容 |
| --- | --- |
| `WireToGateSessionClient.cs:1849` | `!options.UseTls && !IsLoopback(options.Host)` → 抛 `非TLS WIRE_TO_GATE连接只允许loopback地址。` |
| `Configuration.cs:152` | `VehicleSafetySettings` endpoint scheme 必须 https |
| `ControlServerVehicleSafetySignalProvider.cs:95` | 运行时 https 二次校验 |
| `Configuration.cs` `WireToGateSettings.Validate(production: true)` | production 下强制 `ServerCertificateSha256` 非空且非全零，**且该检查不看 `UseTls`** |

第四处是开票时漏掉的。它与 `UseTls` 无关，漏改则 production 启动直接抛
`Production环境的ControlServer地址、构建commit或TLS指纹仍是本机/占位配置。`，前三处全部白改。

另一处影响验收方式的事实：`ControlServerVehicleSafetySignalProvider.cs:95` 漏改的表现不是崩溃，而是
fail-closed 到 `UnknownSignal("HTTPS_REQUIRED")`。现场症状是「车辆安全信号恒为 UNKNOWN、永不放行」，
没有异常、没有崩溃。转交件必须写明这个静默症状。

### 1. 形态：彻底删除（候选 1）

移除 TLS/HTTPS 代码路径本身，不保留开关。

理由：动机是部署复杂度，保留 `serverCertificatePath` 就意味着现场 `appsettings.Production.json` 里
仍然看得见证书路径，动机没有兑现；「可回退」在此是伪价值——git history 保留完整实现，且将来真要恢复
加密也大概率不是回到自签 PFX + 系统信任存储这一套。附带代价：`OnboardTlsCertificateLoaderTests.cs`
是一个真做 Schannel 握手的集成测试，保留代码路径就要连它一起养着，而它测的是一条部署上永不启用的分支。

### 2. 服务端配置面终态

`appsettings.json` 与安装脚本写出的 `appsettings.Production.json` 同构：

```
OnboardTransport:
  enabled, listenAddress, port, maxLineBytes, credentialEnvironmentVariable   保留
  serverCertificatePath                                                       删
  serverCertificatePasswordEnvironmentVariable                                删
  allowInsecureLoopback                                                       删
OnboardSafetyProjection:
  enabled, credentialEnvironmentVariable                                      保留
  requireHttps                                                                删
Health:
  url                                                                         保留键名，值改 http
```

- `OnboardTransportOptions.ListenAddress` 的代码默认值保持 `127.0.0.1`。
- `OnboardSafetyProjectionOptionsValidator` 改到只剩「凭据环境变量已填充」一条检查。
- `allowInsecureLoopback` 删除的理由：守卫消失后它既不能收紧也不能放开任何东西，留着是纯噪音。

### 3. 对外绑定形态：单一绑定，安装参数化，默认仍 loopback

`Health:url` 是 Kestrel 的唯一绑定（`Program.cs:21` 的 `UseUrls`），`/health/live`、`/version` 与
`/api/onboard/v1/vehicle-safety` 全挂在其上。异机要求投影可达，故必须绑非 loopback，health 与 version
随之一并暴露到厂内网。

- 采用单一绑定（例如 `http://0.0.0.0:58007`），**不**做端点级分离。按本地 IP 过滤端点的中间件是往一个
  以「删机制」为目标的改动里新加机制，方向相反。
- `Install-ControlServerLocal.ps1` 新增 `-ListenAddress` / `-HealthBindAddress` 参数，**默认仍为
  `127.0.0.1`**；异机部署显式传入。当前脚本把 `listenAddress` 硬写为 `127.0.0.1`（第 288 行）、
  healthOrigin 硬写为 `https://localhost:$HealthPort`（第 39 行），两处都要参数化。
- health 与 version 的对外暴露是本轮新增的暴露面，进已知限制（票 11）。

### 4. 误配保护：不加

删掉 loopback 守卫后的实际缺口比开票时设想的小：服务端在 `SessionHello` 校验 `credentialProof`
（`OnboardMessageProcessor.cs:488`）与 `agvId`，连到任何非本系统主机会在 TCP 层或握手层直接失败。
真实残余风险只剩一种——厂内存在第二台共享同一密钥的 ControlServer，此时车载端会静默连上错误的那台。

该前提在单服务端工厂不成立，而加握手期 `vehicleKey` 交叉校验要动会话流程，超出「只改传输层安全形态」
的范围。**若将来出现多台服务端，此条须重新决定。**

### 5. 已装机器的证书遗留物

- `Update-ControlServerLocal.ps1` 主动删除 `%ProgramData%\8005\ControlServer\certs\` 与 machine 级
  环境变量 `CONTROL_SERVER_ONBOARD_CERTIFICATE_PASSWORD`。
- `CurrentUser\Root` 里的自签根证书（当初用过 `-InstallCurrentUserRoot` 才有）**不由脚本删除**：它在
  执行安装的那个用户账户作用域下，服务账户升级时未必够得着。改为写进发布手册的人工清理步骤，并注明
  指纹来源。否则会出现「脚本报告清理成功、根证书其实还在」的假绿。

### 6. 过时配置键：启动期显式拒绝

.NET options 绑定会静默忽略未知键。升级后若现场手工保留了 `serverCertificatePath`，运维看着配置里
有证书路径，会以为链路仍然加密，实际是明文。

`OnboardTransportOptions` 的验证器新增一条：检测到 `serverCertificatePath`、
`serverCertificatePasswordEnvironmentVariable`、`allowInsecureLoopback`、
`OnboardSafetyProjection:requireHttps` 任一键存在即**拒绝启动**，消息直指「该键已在本版本移除，传输
为明文」。

这看似与「删机制」相悖，但它删除的是**误解**而非功能——静默忽略正是本轮已知限制最危险的放大器。

### 7. 新旧两端互连：不做协商，改为可识别的失败

明文服务端与 TLS 车载端互不兼容，反之亦然。老车载端连新服务端会把 ClientHello 当 NDJSON 行发出，
服务端报行解析错；新车载端连老服务端则被 `SslStream` 拒。两个方向都失败，但错误文本晦涩，现场容易
误判为「网络不通」。

不在 `SessionHello` 层加版本/能力协商（要动协议仓，触发双人批准门禁）。改为：

- 票 07 联调时**特意跑一次双向错配**，把两个方向的真实错误文本记入证据；
- 票 04 的发布手册写明「两端必须同版本升级」，并附该错误对照表。

### 8. 车载端转交件的字段终态与「不要动」清单

**要改的四处**：即上文第 0 节车载端表格的四行，第 4 行（production 强制指纹）必须与前三行同时改。

**配置字段**：`wireToGate.useTls` 与 `wireToGate.serverCertificateSha256` 两键删除；
`vehicleSafety.endpoint` 改 `http://`；`appsettings.json` 与 `appsettings.Production.example.json`
同步。

**明确不要动**：`IsForbiddenProductionHost`（`Configuration.cs` 内两处，production 禁 loopback/占位
主机）保留。异机形态本来就满足它，它拦的是「生产配置忘了改样例值」，与本轮无关。转交件里「不要动」
一节要写得与「要改」一节同样具体，防止顺手多改。

### 9. 测试与切片规格的删改范围

- `tests/ControlServer.Tests/OnboardTlsCertificateLoaderTests.cs` — 整个文件删除（被测类消失）。
- `tests/ControlServer.Tests/OnboardVehicleSafetyEndpointsTests.cs` — 第 37/59 行 `Request.Scheme`
  改 `http`；第 96–102 行 `RequireHttps=false` 触发验证失败的断言删除；第 116 行构造改掉。
- **新增两条**覆盖本轮真正放开的行为：非 loopback 明文监听能启动、http 请求能通过投影端点。按证据
  规则，这两条须在改产品代码**之前**先跑一次并且**必须红**，红侧文本进证据。
- `docs/ai-spec/slices.md` 的 W2G-IS-00 行「最小持久边界与接口」栏写着 `TLS peer`，改为明文 peer 的
  表述。这是本仓自己的 G2 验收规格，明文化后该定义失效。
- W2G-IS-00 这个 trait 由多个测试共享（`JourneyRuntimeWorkerTests` 等也带），删掉 TLS 那条不会让切片
  失去覆盖。但删除后**本仓再无任何测试触及 Schannel**，票 08 重建候选时须在证据中显式说明这处与上一轮
  的差异，避免看起来像覆盖率无声下降。

### 10. 协议仓：确认零规定（现场复核，非复述）

在 `8005-agv-protocol` HEAD `1531489`（即 `protocol-v0.1.1` 那条线）的 tracked 文件中搜
`tls|ssl|certificate|encrypt|证书|加密`，**命中数为 0**；表面命中全部是 JSON Schema 自身的
`$id`/`$schema` URL 与 `THIRD-PARTY-NOTICES.md` 的 GitHub 链接。`transport` 仅以 `transportDedupKey`
（值恒为 `messageId`）与 `transportDemandKey` 出现，是消息去重键。`58005` 在协议仓零出现——端口属两端
部署配置。

与凭据相关的唯一规定：`SessionHello.schema.json:73` 定义 `credentialProof` 为 `minLength: 1` 的字符串，
并列于 payload `required`（第 87 行）。协议只要求该字段存在，对其取值方式与保护方式无任何规定。

结论：本轮不触发协议变更，`protocol-v0.1.1` 保持不动，不触发双人批准门禁。

**顺带更正地图 Out of scope 第一条的理由**：改挑战应答／HMAC 并**不**需要动协议仓——`credentialProof`
是不透明字符串，换成 HMAC 结果同样满足 schema，`additionalProperties: false` 也拦不住（字段还是那一个）。
真正挡路的是两端实现与一次协调升级，不是治理门禁。该项仍然 out of scope（用户已否决，且与本轮简化动机
相反），但理由须改准。
