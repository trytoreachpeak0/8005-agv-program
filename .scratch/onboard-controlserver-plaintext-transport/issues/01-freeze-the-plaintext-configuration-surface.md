# 冻结两端安全校验的放开形态与配置面终态

Type: grilling
Mode: HITL
Status: open
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
