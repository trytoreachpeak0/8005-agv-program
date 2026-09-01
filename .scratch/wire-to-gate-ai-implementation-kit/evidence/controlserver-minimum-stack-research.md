# ControlServer 最小技术栈研究与冻结

**研究日期**：2026-08-25  
**适用目标**：Windows 11、`win-x64`、单车 WIRE_TO_GATE MVP RC、截止 2026-08-28 17:00  
**结论状态**：冻结；除非发现与 accepted ADR、真实 RIoT SDK 或 MesIngest V2 的硬冲突，否则实施票不得重新选型。

## 决定

冻结为一个 **C# / .NET 8 单体 Windows Service**：同一 `WebApplication`/Generic Host 进程承载业务状态机、MesIngest V2 只读适配器、RIoT SDK 适配器、SQLite 持久化、Onboard TCP listener 和仅回环可见的 Minimal API 健康端点。

- 目标框架 `net8.0`；构建 SDK 锁定 `8.0.424`，自包含运行时锁定 `8.0.30`，RID 为 `win-x64`。这是 2026-08-11 的 .NET 8 安全修补版；.NET 8 仍受支持到 2026-11，但 RC 后必须建立迁移到 .NET 10 LTS 的票，不能把本次赶工锁定当长期平台决定。[.NET 8 下载页](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)列出 SDK 8.0.424/runtime 8.0.30；[.NET 支持策略](https://learn.microsoft.com/en-us/dotnet/core/releases-and-support)列出 .NET 8 的支持期。
- 宿主使用 `Microsoft.NET.Sdk.Web` + `Microsoft.Extensions.Hosting.WindowsServices`。Windows Service 可无 IIS 自动随系统启动；`AddWindowsService`/`UseWindowsService` 处理 service lifetime 和 content root，[Microsoft 的 Windows Service 指南](https://learn.microsoft.com/en-us/dotnet/core/extensions/windows-service)即采用该模型。
- **进程模型是一服务、一进程、一活动实例**。现有 MesIngest 仍是独立 Windows Service；ControlServer 只通过其本机 V2 HTTP 合同读取，不链接其数据库、不复制投影、不把 MesIngest 拉进本进程。
- HTTP 面只绑定 `http://127.0.0.1:58005`，提供 `GET /health/live`、`GET /health/ready`、`GET /version`；没有管理后台、Swagger UI 或业务写 API。Minimal API 是 Microsoft 对新 HTTP API 的推荐轻量路径；readiness 与 liveness 应分开表达。[Minimal API 选择指南](https://learn.microsoft.com/en-gb/aspnet/core/fundamentals/apis?view=aspnetcore-9.0)、[ASP.NET Core health checks](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks?view=aspnetcore-10.0)。
- Onboard 链路继续使用独立端口（默认 `0.0.0.0:58006`，部署可改）上的 `TcpListener -> NetworkStream -> SslStream`，Onboard 主动连接；服务端证书固定信任、每车共享密钥认证、每车单会话 fencing、UTF-8 严格 NDJSON、精确 `protocolVersion = 1`、2 秒心跳/6 秒 liveness 全部原样实现。`SslStream` 官方说明其通常与 `TcpClient`/`TcpListener` 配合并为流提供机密性、完整性及端点认证。[SslStream](https://learn.microsoft.com/en-us/dotnet/api/system.net.security.sslstream?view=net-10.0)、[TcpListener](https://learn.microsoft.com/en-us/dotnet/api/system.net.sockets.tcplistener?view=net-10.0)。
- 不使用 SignalR、WebSocket 或 gRPC 作为车载 wire。SignalR 是 HTTP transport + Hub protocol/RPC 抽象，可在 WebSockets/Long Polling 等 transport 间选择并另加 JSON/MessagePack Hub protocol；这会改变已经接受的原始 TLS 字节流、NDJSON framing、会话/ACK/心跳语义，而不是实现细节。[SignalR 配置](https://learn.microsoft.com/en-us/aspnet/core/signalr/configuration?view=aspnetcore-10.0)、[SignalR Hub protocol 类型](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.signalr.protocol?view=aspnetcore-10.0)。
- 持久化为单个本机 `%ProgramData%\8005\ControlServer\data\controlserver.db`，使用 EF Core SQLite `8.0.30`、显式唯一索引/外键和短事务。所有写入经一个应用级 writer 串行化；可靠消息只有在 inbox/业务承担已提交后 ACK，outbox 意图必须先提交再调用 RIoT 或发往 Onboard。Microsoft 说明 SQLite 同时只允许一个未提交 writer，事务默认 serializable，事务可将多条语句作为一个原子单元。[Microsoft.Data.Sqlite transactions](https://learn.microsoft.com/en-us/dotnet/standard/data/sqlite/transactions)。
- RC 明确使用 `journal_mode=DELETE; synchronous=FULL; foreign_keys=ON; busy_timeout=5000`，**不启用 WAL**。SQLite 的 WAL 仍只有一个 writer，而且 2026-08-24 更新的一手说明披露 WAL-reset 数据竞争在若干版本中可致损坏并要求升级到已修复引擎；三天内无法证明 EF 8 transitive native SQLite 恰好绑定已修复版本，因此 rollback journal 是更小的资格面。[SQLite WAL 一手说明](https://sqlite.org/wal.html)。后续若要 WAL，必须先把 native SQLite 锁到已修复版本并跑断电/并发/恢复资格测试。
- Schema 由 EF migrations 管理，但服务启动时**不得**自动 `Migrate()`/`EnsureCreated()`。发布物带 self-contained `efbundle.exe`，安装/升级脚本在服务停止、取得安装互斥锁并备份数据库后执行一次。EF 官方把 migration bundle 定位为无需 SDK/source 的部署产物；SQLite 不支持 idempotent migration script，且其部分 schema 变更需 rebuild。[应用迁移](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying)、[SQLite provider 限制](https://learn.microsoft.com/en-us/ef/core/providers/sqlite/limitations)。
- 日志使用 `ILogger<T>` 调用，经 Serilog 写 newline-delimited compact JSON rolling file 至 `%ProgramData%\8005\ControlServer\logs\controlserver-.jsonl`；按天且 100 MiB 滚动、保留 14 个文件，启动阶段也有 bootstrap logger。每条关键记录结构化携带 `runId`、`agvId`、`sessionGeneration`、`demandId`、`messageId`、`movementLegId`、`slotOperationAttemptId`，但绝不记录共享密钥、CallApiKey、证书私钥/PFX 密码、Authorization header 或完整秘密配置。Serilog.AspNetCore 8.x 与 net8 对齐，并支持统一 `ILogger`、JSON 和 rolling file。[Serilog.AspNetCore 8.0.3 一手包文档](https://www.nuget.org/packages/Serilog.AspNetCore/8.0.3)。技术日志不是不可改写业务审计；管理员动作、DurableAcceptance、状态转换和外部副作用证据仍写 SQLite 事实表。
- JSON 编解码冻结为 self-contained runtime `8.0.30` 内置的 `System.Text.Json`，Host 不另加 `System.Text.Json` PackageReference；Microsoft 说明该库从 .NET Core 3.0 起属于 shared framework（[System.Text.Json overview](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview)）。Host 使用 UTF-8、camelCase、字符串 enum、大小写敏感、`UnmappedMemberHandling.Disallow`、`MaxDepth = 32`，拒绝注释、尾逗号、NaN/Infinity 和从字符串宽松读数字；NDJSON 单行上限冻结为 1 MiB，超限在分配完整 payload 前拒绝。
- Draft 2020-12 Schema 一致性验证冻结 `Corvus.Json.Validator 4.6.7`，但**只进入 G1/G2 conformance/tool 测试进程，不进入 Host**。其 V4 engine 支持 net8 及 Draft 4～2020-12，包为 Apache-2.0（[upstream 支持表](https://github.com/corvus-dotnet/Corvus.JsonSchema#supported-schema-dialects)、[NuGet 4.6.7](https://www.nuget.org/packages/Corvus.Json.Validator/4.6.7)）。隔离是必要的：该 net8 package graph 声明 `System.Text.Json >= 10.0.4` 等 transitive dependencies；若与 Host 同进程就不再是 runtime 8.0.30 JSON 栈。conformance 项目的完整 transitive graph 仍须单独锁进 `packages.lock.json`/SBOM。它必须离线加载已批准 protocol bundle，跑完官方/shared valid+invalid vectors，并额外覆盖 1 MiB±1、深度 32±1、未知字段、`format` assertion、整数/小数边界、溢出、重复/缺失 required 和非法 UTF-8；Host 对同一用例的严格 parser 结果必须一致。
- HTTP resilience 只给两个命名客户端 `MesIngestV2` 与 `RIoT` 使用 `Microsoft.Extensions.Http.Resilience 8.10.0`，不包裹 Onboard TCP。无 hedging；仅安全只读 `GET`/`HEAD` 可对连接失败、408、429、5xx 或 attempt timeout 做最多 2 次指数退避+jitter 重试。`POST`/`PUT`/`PATCH`/`DELETE`/`CONNECT` 全部禁用 retry；Microsoft 明确警告默认 handler 会重试所有方法并可能让 POST 重复插入，提供 `DisableForUnsafeHttpMethods()` 关闭这些方法（[HTTP resilience 指南](https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience)）。RIoT 任何写动作即使接口错误地使用安全 HTTP verb，也不得盲重试：先持久化 `OrderIntent`，沿稳定 `upperId` 查询对账，只有可靠证明不存在且原前提仍成立时才按业务规则重试。
- 非秘密默认值进入 Git 中的 `appsettings.json`；部署覆盖放 `%ProgramData%\8005\ControlServer\config\appsettings.Production.json`。秘密只放外部 `%ProgramData%\8005\ControlServer\secrets\secrets.json` 与 PFX，安装器将 ACL 限制为 Administrators、SYSTEM 和服务身份，且 `reloadOnChange=false`；CI/开发可用 `ControlServer__...` 环境变量覆盖。环境变量通常是未加密明文，因此不是默认生产 secret store。[ASP.NET Core secret 指南](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-10.0)。启动用 Options validation fail-fast，任何必需身份、端点、协议 manifest、证书或密钥缺失都不得进入 ready。
- 发布为 **self-contained folder**，不 trim、不 NativeAOT、不单文件。这样目标机无需安装 .NET，同时避免 SQLite native library 的单文件解包面；配置、协议 manifest、`efbundle.exe` 和安装脚本本来也必须作为独立文件交付。`RuntimeFrameworkVersion=8.0.30` 固定实际嵌入版本；Microsoft 说明 self-contained 在发布时选 runtime，而该属性可精确固定 patch。[runtime 选择](https://learn.microsoft.com/en-us/dotnet/core/versions/selection)、[`dotnet publish`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish)。安装物为 zip + 提权 PowerShell install/uninstall/upgrade/smoke 脚本，不在本周引入 WiX/MSI。

## 精确版本锁

在 ControlServer 新仓库提交 `global.json`、`Directory.Packages.props`、`.config/dotnet-tools.json` 和每项目 `packages.lock.json`；禁止 floating version，CI 只执行 `restore --locked-mode`。

| 项目 | 冻结版本/身份 |
|---|---|
| .NET SDK | `8.0.424`，`rollForward: disable` |
| Target/runtime/RID | `net8.0` / `8.0.30` / `win-x64` |
| `Microsoft.Extensions.Hosting.WindowsServices` | `8.0.1` |
| `Microsoft.EntityFrameworkCore.Sqlite` | `8.0.30` |
| `Microsoft.EntityFrameworkCore.Design`、local tool `dotnet-ef` | `8.0.30` |
| `Serilog.AspNetCore` | `8.0.3` |
| Host JSON | runtime/shared-framework `System.Text.Json 8.0.30`；Host 禁止显式 package override |
| `Corvus.Json.Validator` | `4.6.7`，仅 Conformance/测试；其完整 transitive graph 单独锁定 |
| `Microsoft.Extensions.Http.Resilience` | `8.10.0` |
| `Microsoft.AspNetCore.Mvc.Testing` | `8.0.30` |
| `xunit.v3` | `3.2.2`（复用当前仓库已验证版本，不在截止前三天切刚发布的 4.0） |
| `Microsoft.NET.Test.Sdk` | `18.8.1`（复用当前仓库已验证版本） |
| RIoT C# SDK | 当前干净源码树 `f09905868c655934d25faf1223d94714e8069431`，来自根 commit `c65ba6bd357bfb41a663c1bf700f8f57885e7169`；生成层/Facade 的 Kiota `1.17.4` 不另行升级 |
| MesIngest | 运行时精确校验现有 V2 `contractVersion`/`HistoryEpoch`；仅 HTTP 读，不新增包依赖 |
| shared protocol | 只能锁两名负责人批准后的完整 `ProtocolReleaseIdentity`；本研究不虚构 release/tag/hash |

Microsoft 的 NuGet 包页确认 EF Core SQLite `8.0.30` 是 net8 provider 且依赖 SQLite native bundle；[provider package](https://www.nuget.org/packages/Microsoft.EntityFrameworkCore.Sqlite/8.0.30)、[design package](https://www.nuget.org/packages/Microsoft.EntityFrameworkCore.Design/8.0.30)。

## 依赖维护、许可、安全与升级矩阵

| 组件 | RC 锁定/维护主体 | 许可与发布义务 | 安全/升级门禁 |
|---|---|---|---|
| .NET runtime/SDK | SDK `8.0.424`、runtime `8.0.30`；Microsoft/.NET Foundation，.NET 8 支持到 2026-11 | MIT；发布物保留版权/许可文本（[runtime LICENSE](https://github.com/dotnet/runtime/blob/main/LICENSE.TXT)） | RC 前不换 major；跟进 net8 security patch，RC 后优先迁移 .NET 10 LTS。每次 runtime patch 重发 self-contained 包并重跑 G2/G3。 |
| ASP.NET Core/Kestrel/Minimal API | 随 `Microsoft.AspNetCore.App 8.0.30` shared framework 嵌入 self-contained 发布；Microsoft/.NET Foundation | MIT（[ASP.NET Core LICENSE](https://github.com/dotnet/aspnetcore/blob/main/LICENSE.txt)） | 与 runtime patch 同步，不单独混用 9/10 组件；重跑 HTTP health、Windows Service 启停和 TLS/TCP 并行宿主测试。 |
| EF Core SQLite | `Microsoft.EntityFrameworkCore.Sqlite`/`Design 8.0.30`；Microsoft EF Core | MIT（[EF Core LICENSE](https://github.com/dotnet/efcore/blob/main/LICENSE.txt)） | provider 与 EF major 必须一致；patch 升级先检查 migration SQL/模型差异，再跑原子提交、唯一约束、崩溃恢复和 bundle 升级/回滚测试。 |
| Microsoft.Data.Sqlite | transitive `8.0.30`；Microsoft EF Core | MIT；包页列明维护者和精确发布（[Microsoft.Data.Sqlite.Core 8.0.30](https://www.nuget.org/packages/Microsoft.Data.Sqlite.Core/8.0.30)） | 必须在 lock/SBOM 中单列；任何 patch 都要重跑 locking、busy timeout、disk-full、事务和 native loading 测试。 |
| SQLite native/SQLitePCLRaw | candidate 锁 `SQLitePCLRaw.bundle_e_sqlite3`/`lib.e_sqlite3 2.1.12`；SourceGear/SQLitePCLRaw，实际 native engine 版本另以 SBOM + 启动时 `select sqlite_version()` 冻结 | wrapper/bundle Apache-2.0（[bundle](https://www.nuget.org/packages/SQLitePCLRaw.bundle_e_sqlite3/2.1.12)、[native package](https://www.nuget.org/packages/SQLitePCLRaw.lib.e_sqlite3/2.1.12)）；SQLite 本体为 public domain（[SQLite copyright](https://sqlite.org/copyright.html)） | EF 只给 `>=2.1.12` 下限，不能把它当 native 身份；RC 必须记录解析后的 exact packages、DLL SHA-256、`sqlite_version()` 和 RID。若审计要求升 `2.1.13`/3.x，显式锁定后重跑 native/恢复测试；WAL 仍保持关闭。 |
| WindowsServices | `Microsoft.Extensions.Hosting.WindowsServices 8.0.1`；Microsoft | MIT（[NuGet package](https://www.nuget.org/packages/Microsoft.Extensions.Hosting.WindowsServices/8.0.1)） | 与 net8 保持同 major；升级须重跑 SCM install/start/stop/restart、content root、非零退出恢复和 LocalService ACL 测试。 |
| Serilog | `Serilog.AspNetCore 8.0.3` 及 lock file 解析出的 sinks/configuration；Serilog project | Apache-2.0（[package/upstream metadata](https://www.nuget.org/packages/Serilog.AspNetCore/8.0.3)），发布 `THIRD-PARTY-NOTICES.md` 保留所需 NOTICE/许可 | 与 TFM 同 major；升级须验证 bootstrap/fatal、JSON schema、滚动/保留、flush 和 secret-redaction，不能改变业务审计语义。 |
| System.Text.Json | Host 使用 runtime `8.0.30` 内置实现；Microsoft/.NET Foundation | MIT，随 runtime notices（[官方 overview](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview)） | Host 禁止 transitive/direct package 漂到 9/10；runtime patch 升级重跑全部 serialization/vectors/严格性边界。 |
| Corvus JSON Schema validator | `Corvus.Json.Validator 4.6.7`，仅 Conformance；Endjin/Corvus | Apache-2.0；V4 net8 engine 与 2020-12 支持见 [upstream](https://github.com/corvus-dotnet/Corvus.JsonSchema#supported-schema-dialects) 和 [package](https://www.nuget.org/packages/Corvus.Json.Validator/4.6.7) | 单独锁 full transitive graph；升级要跑 protocol 全部 vector/边界并比较 validator/Host parser verdict。不得把其 STJ 10 transitive graph带进 Host。 |
| HTTP resilience | `Microsoft.Extensions.Http.Resilience 8.10.0`；Microsoft | MIT（[package](https://www.nuget.org/packages/Microsoft.Extensions.Http.Resilience/8.10.0)） | 仅 named HTTP clients；升级重跑 retry classification、timeout/circuit-breaker、429/5xx 和“写请求零自动重试”测试，并审完整 Polly/transitive graph。 |
| xUnit | `xunit.v3 3.2.2`；xUnit.net/.NET Foundation | Apache-2.0（[xunit.v3 3.2.2](https://www.nuget.org/packages/xunit.v3/3.2.2)） | test-only，不进入 Host 发布目录；截止前不升刚发布的 4.0，后续单票迁移并比较测试发现数。 |
| Microsoft.NET.Test.Sdk | `18.8.1`；Microsoft/vstest | MIT（[package](https://www.nuget.org/packages/Microsoft.NET.Test.Sdk/18.8.1)） | test-only；升级必须比较 discovered/executed/skipped 数及 TRX，不能用“0 tests”冒充 PASS。 |
| Kiota runtime | 本地 RIoT C# SDK 引用 `Microsoft.Kiota.Bundle 1.17.4`；Microsoft Kiota | MIT（[Kiota LICENSE](https://github.com/microsoft/kiota/blob/main/LICENSE)、[bundle 1.17.4](https://www.nuget.org/packages/Microsoft.Kiota.Bundle/1.17.4)） | 本 RC 不单升 runtime 或 generator；升级必须以同一 OpenAPI 输入重新生成、审 diff，并跑 RIoT Facade、序列化、鉴权和真实只读/受控调用测试。 |
| 本地 RIoT SDK | 源码树 `f09905868c655934d25faf1223d94714e8069431`；8005 项目所有者自行维护 | **`rcs/riot-sdk` 当前没有仓库自有的 LICENSE/LICENCE/NOTICE/COPYING 文件。** 因而本决定不推定任何开源/再分发许可：只允许在所有者控制的私有项目仓库内复用；任何外部或公开再分发前，必须由所有者添加/批准明确许可证并确认所需 third-party notices。虚拟环境内第三方包自带的 LICENSE 不构成 RIoT SDK 的许可证。 | 锁源码 tree、OpenAPI specs、生成脚本和 Kiota graph；任何改动先审生成 diff，跑 SDK 全测与 ControlServer RIoT adapter G2，并由所有者确认分发边界。 |

RC 构建必须提交并使用 `packages.lock.json`，将 direct/transitive managed package、SQLite native bundle、runtime/framework、工具版本及其 SHA-256 写入 SPDX SBOM；Microsoft 的 [SBOM Tool](https://github.com/microsoft/sbom-tool)可从发布目录和工程生成 SPDX。发布前至少运行 `dotnet restore --locked-mode`、`dotnet list ControlServer.sln package --include-transitive --vulnerable --format json`，并对 SBOM/native DLL 再做漏洞扫描；NuGet 官方说明 restore audit 和 `--vulnerable` 同时覆盖 direct/transitive dependency（[NuGet audit](https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages)）。任一 NU1901～NU1904、native advisory、未知组件版本、缺失许可/NOTICE 或未解释 suppress 都阻断 RC；修复后产生新 build/SBOM/hash 并使旧 G2/G3 证据失效。

## 最小项目布局

```text
global.json
Directory.Packages.props
.config/dotnet-tools.json
ControlServer.sln
src/
  ControlServer.Domain/          # 状态、不变量、稳定身份；无 IO/EF
  ControlServer.Application/     # use cases、单 writer、clock/ports
  ControlServer.Infrastructure/  # EF SQLite、MesIngest、RIoT、TLS/NDJSON、outbox
  ControlServer.Host/            # Windows Service、hosted loops、loopback health/version
tests/
  ControlServer.Tests/           # unit + SQLite/TCP/HTTP integration，真实 SQLite temp file
tools/
  ControlServer.FakeOnboard/     # 脚本化协议对端，不冒充真实 HMI/IO
  ControlServer.Conformance/     # test-wire-to-gate G2 非交互入口
pack/
  Install-ControlServer.ps1
  Upgrade-ControlServer.ps1
  Uninstall-ControlServer.ps1
  Invoke-ControlServerSmoke.ps1
requirements/acceptance/wire-to-gate/integration-slices/
```

不再增加 CQRS framework、MediatR、AutoMapper、repository-per-entity、消息 broker 或 event-sourcing 框架。`DbContext` 是 unit-of-work；应用端口只隔离真实外部副作用和时钟。

## 标准命令（从仓库根执行）

```powershell
dotnet --version                         # 必须恰为 8.0.424
dotnet restore ControlServer.sln --locked-mode
dotnet build ControlServer.sln -c Release --no-restore
dotnet test ControlServer.sln -c Release --no-restore --logger "trx;LogFileName=controlserver.trx"

dotnet tool restore
dotnet ef migrations has-pending-model-changes `
  --project src/ControlServer.Infrastructure `
  --startup-project src/ControlServer.Host
dotnet ef migrations bundle --configuration Release --self-contained `
  --target-runtime win-x64 --force --output artifacts/efbundle.exe `
  --project src/ControlServer.Infrastructure `
  --startup-project src/ControlServer.Host

dotnet publish src/ControlServer.Host/ControlServer.Host.csproj `
  -c Release -r win-x64 --self-contained true --no-restore `
  -p:RuntimeFrameworkVersion=8.0.30 `
  -p:PublishSingleFile=false -p:PublishTrimmed=false -p:PublishReadyToRun=false `
  -o artifacts/publish/win-x64
dotnet publish tools/ControlServer.Conformance/ControlServer.Conformance.csproj `
  -c Release -r win-x64 --self-contained true --no-restore `
  -p:RuntimeFrameworkVersion=8.0.30 -p:PublishSingleFile=false `
  -o artifacts/tools/win-x64

.\pack\Install-ControlServer.ps1 `
  -Source .\artifacts\publish\win-x64 `
  -MigrationBundle .\artifacts\efbundle.exe `
  -ProtocolManifest <approved-release.json> `
  -CertificatePfxPath <external-pfx> `
  -SecretsPath <external-secrets.json>
.\pack\Invoke-ControlServerSmoke.ps1 -ServiceName '8005.ControlServer'

.\artifacts\tools\win-x64\ControlServer.Conformance.exe `
  test-wire-to-gate --gate G2 --slice affected `
  --protocol-manifest <immutable-path> --output <new-run-directory>
```

安装脚本必须：要求管理员；拒绝发布目录内出现秘密；安装只读程序到 `%ProgramFiles%\8005\ControlServer`；创建/收紧 `%ProgramData%` data/config/secrets/logs ACL；使用 `NT AUTHORITY\LocalService` 而非 LocalSystem；服务停止时复制数据库备份并执行 bundle；创建 Automatic Windows Service、配置非零退出自动重启；启动后同时检查 SCM、`/health/live`、`/health/ready`、数据库 schema/protocol identity 和新日志。升级失败不得删除旧二进制或数据库；数据库迁移后只有经过向后兼容证明才能直接降级二进制。

## 测试冻结

- domain/application 纯单元测试使用注入的 `TimeProvider`/手动虚拟时间；不得靠 `Thread.Sleep` 验证 2 秒/6 秒协议。
- integration 使用真实临时 SQLite 文件、真实 `TcpListener`/`SslStream` 和测试时临时证书；HTTP 使用 `WebApplicationFactory`。EF InMemory 不能替代 SQLite 的约束、事务、唯一索引和崩溃语义。
- protocol conformance 必须用 Corvus 4.6.7 对 approved Draft 2020-12 bundle 运行所有官方/shared valid+invalid vectors及 size/depth/unknown-field/format/numeric-boundary 补充向量，再把同一 NDJSON 喂给 Host 严格 parser；两个 verdict 不一致即 FAIL。
- Fake MesIngest、Fake RIoT、Fake Onboard 都实现正式端口并记录 Fake identity；drop/delay/duplicate/disconnect/crash checkpoints 是测试输入，不在生产代码里加“测试后门”。
- 必须覆盖同 MessageId/业务键重放、同 ID 不同内容冲突、DurableAcceptance 前崩溃、outbox 调用结果未知、SQLite busy/disk-full、旧 session 迟到、TLS/密钥错配、最大 frame/非法 UTF-8/非法 JSON、重启恢复和原子完成。

## 被拒绝方案

| 方案 | 拒绝原因 |
|---|---|
| .NET 10 立即升级 | 长期更好，但现有 RIoT SDK、MesIngest 和本仓库测试均已在 net8；三天内迁移只增加未知。RC 后单开升级票。 |
| .NET 9 | 不是 LTS，支持期并不优于本次复用的 net8，且仍制造版本漂移。 |
| Python/FastAPI、Node、Java | 放弃现有 C# SDK/MesIngest 资产并增加第二运行时，没有期限收益。 |
| IIS、Docker、多个微服务 | Windows 11 单机单车不需要；增加安装、端口、身份、重启次序和分布式一致性。 |
| SignalR/WebSocket/gRPC 车载链路 | 改变 accepted raw TLS + NDJSON wire、心跳、ACK 和 session fencing；不是兼容实现。 |
| JsonSchema.Net | upstream 明示 NuGet binary 带 EULA，产生收入的组织/用户可能需按 package license 支付持续 maintenance fee；本项目没有预批准该商业/EULA 条款，因此不进入 RC（[json-everything upstream](https://github.com/json-everything/json-everything#project-funding--sponsorship)）。 |
| NJsonSchema | upstream 只概括为 draft v4+，而 Draft 2020-12 meta-schema/`const` 问题仍有公开缺口，`$defs` 支持在 2026 年仍以 PR 推进；完整 2020-12 conformance 未建立，不能承担协议 release gate（[package](https://www.nuget.org/packages/NJsonSchema)、[2020-12 issue](https://github.com/RicoSuter/NJsonSchema/issues/1667)、[`$defs` PR](https://github.com/RicoSuter/NJsonSchema/pull/1913)）。 |
| SQL Server/PostgreSQL | 可扩展但对单车单进程增加实例、schema/账号/安装依赖；MesIngest 的 SQL Server 库也不得被 ControlServer 共用。若未来多实例/多车并发成为范围，再迁移。 |
| Dapper/手写 SQL 全栈 | 运行时轻但需要自行建立 migrations、model drift 和大量映射；三天内不如 EF migration/unique constraint 可验证。关键事务仍应检查生成 SQL。 |
| SQLite WAL | native SQLite 修复版本尚未在本候选被证明，且当前一手披露存在 WAL-reset 风险；本负载不需要 WAL 的读写并发收益。 |
| 启动时自动迁移/`EnsureCreated` | 把 schema 权限和失败面带进每次启动，且 `EnsureCreated` 绕过 migrations；安装期 bundle 更可追溯。 |
| EF InMemory 作为 integration DB | 不提供 SQLite 的真实事务、约束、锁和 native 行为，只能用于极窄单元测试，默认不用。 |
| NativeAOT、trim、single-file、WiX/MSI | 都需要额外兼容/安装资格；folder self-contained + PowerShell 是 2026-08-28 前最短可回读路径。 |
| Serilog/数据库业务审计二选一 | 文件日志可诊断但可轮转、可删，不能承担不可改写业务事实；两者职责不同，均保留最小实现。 |

## 本地权威映射

本决定不改写业务设计，直接受根 `CONTEXT.md`、accepted ADR `cross/0023`～`0032`、`mes/0007`、ControlServer handoff、MVP specification 和 D1～D7 约束。尤其：原始 TCP/TLS/NDJSON、每车凭证、精确协议版本、单会话 fencing、DurableAcceptance、持久 inbox/outbox、五步恢复、未知结果对账和原子 TransportDemandCompletion 都是实现验收项，不是可由技术栈放宽的偏好。

**实施起点**：按以上版本/布局先建骨架与第一条失败的 SQLite 原子受理测试，再做 W2G-IS-00；不要继续调研框架。
