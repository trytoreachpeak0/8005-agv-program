# 按冻结形态改掉服务端产品代码的 TLS/HTTPS

Type: task
Mode: AFK
Status: open
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

需要一并处理但范围未定的：服务端测试里绑在 TLS 形态上的部分。改完先让测试红一次，据实记录哪些
断言是在证明 TLS 行为、哪些只是被 TLS 形态连带影响，再决定删除还是改写——**不得为了让测试变绿而
删掉仍在保护真实行为的断言**。

完成判据：Release 构建 0 warning、`dotnet format` 干净、tier 1 全绿且据实报出 skip 数；服务端在
非 loopback 地址上以明文启动成功，`/health/live` 经 HTTP 返回 200，安全投影端点经 HTTP 可达且无
凭据仍返回 401。判据必须是回读取证，不得以「构建成功」代替行为证据。

不推送远程由本票决定；未经票 08 之前的改动是否推送，按当轮实际情况在答案中据实记录。
