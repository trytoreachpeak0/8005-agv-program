# 研究并冻结 ControlServer 最小技术栈

Type: research
Mode: AFK
Status: resolved
Blocked by: 01

## Question

在 Windows 11 开发机、2026-08-28 17:00 截止、现有 C# RIoT SDK 和 .NET MesIngest 的条件下，哪套 ControlServer 技术栈最能在约三个工作日内交付持久、可测试、可安装的单车 WIRE_TO_GATE MVP？

研究必须比较运行时/宿主、进程模型、服务 API、持久化数据库与迁移、协议长连接、配置/秘密注入、日志、测试和发布方式，并优先复用已存在且兼容的 C#/.NET 资产及网上成熟库/官方工具。对于 TLS、JSON/JSON Schema、日志、配置、依赖注入、数据库迁移、重试和测试运行器等通用能力，禁止在已有可靠组件时另起炉灶；自行开发只保留给 WIRE_TO_GATE 特有状态机、事务/安全不变量和薄适配器。

选型必须联网核验官方文档或上游仓库中的当前版本、Windows/.NET 支持、维护活跃度、许可证、安全与升级路径，形成依赖清单和版本锁定；不采用来历不明代码、停止维护组件或仅因 AI 熟悉而选择的库。输出一个明确选择、最小项目结构、构建/测试/发布命令、复用/自研边界和被拒绝方案；不得以无结论调研消耗实施时间。用户此前允许采用推荐值，因此在未发现硬冲突时直接冻结证据最佳的推荐方案。

## Answer

冻结为一个自包含 `win-x64` 的 C# / `.NET 8` 单体 Windows Service：同一 ASP.NET Core `WebApplication` / Generic Host 进程承载业务状态机、MesIngest V2 只读适配器、RIoT SDK 适配器、Onboard TCP listener、持久化与仅回环健康端点；现有 MesIngest 继续作为独立服务运行。

- 版本：SDK `8.0.424`、target `net8.0`、runtime `8.0.30`；发布为不裁剪、非单文件的 self-contained folder，RID `win-x64`。
- 车载链路：严格沿用 accepted ADR 的 `TcpListener -> SslStream -> UTF-8 NDJSON`，服务端自签名证书固定信任、每车密钥、单会话 fencing、精确 `protocolVersion = 1`、2 秒心跳和 6 秒 liveness；拒绝 SignalR、WebSocket 与 gRPC 改写 wire。
- JSON/Schema：Host 只用 runtime `8.0.30` 内置 `System.Text.Json` 的严格、大小写敏感、拒绝未知字段配置；Draft 2020-12 一致性由隔离的 `Corvus.Json.Validator 4.6.7` G1/G2 conformance 进程验证，避免其 `System.Text.Json >= 10` 传递图污染 Host。
- HTTP：Kestrel 只在 `127.0.0.1:58005` 提供 live、ready、version；不在 MVP 新建管理后台、Swagger UI 或业务写 API。
- HTTP resilience：命名 MesIngest/RIoT 客户端使用 `Microsoft.Extensions.Http.Resilience 8.10.0`；只允许安全只读方法有限重试，unsafe 方法零自动重试。RIoT 写动作只走持久意图、稳定 `upperId` 和查询对账，不盲重试未知结果。
- 持久化：EF Core SQLite `8.0.30`，单机本地单库、应用级单 writer、短事务、显式唯一约束与外键；RC 固定 rollback journal、`synchronous=FULL`，不启用尚未完成 native 修复版本资格的 WAL。多实例、网络共享库或超出单机单车范围时重新决策 SQL Server，而不是把本次 MVP 选择外推为长期架构。
- 迁移：提交 EF migrations，并生成 self-contained `efbundle.exe`；只由安装/升级脚本在服务停止、互斥和备份后执行，应用启动不自动迁移，也不使用 `EnsureCreated`。
- 配置与秘密：非秘密默认值进 Git；生产覆盖、每车密钥、CallApiKey、PFX 与密码从 `%ProgramData%` 外部文件/环境注入并以 ACL 限制，缺少必需值时 fail-fast 且不得 ready。
- 日志与审计：`ILogger<T>` 经 Serilog 输出滚动 compact JSONL；秘密禁止入日志。不可改写的 DurableAcceptance、状态转换、管理员动作与外部副作用证据仍写数据库事实表，不能由文件日志替代。
- 测试：xUnit `3.2.2`，纯领域测试使用可控 `TimeProvider`；集成测试使用真实临时 SQLite 文件、真实 TCP/TLS/NDJSON 与 `WebApplicationFactory`，不得用 EF InMemory 代替事务、唯一约束、锁、崩溃和恢复语义。
- 工程：最小拆分为 Domain、Application、Infrastructure、Host、Tests、FakeOnboard、Conformance 与安装脚本；不加入 CQRS framework、MediatR、AutoMapper、消息 broker、event sourcing、Docker、IIS、MSI、NativeAOT 或微服务。
- 依赖治理：direct/transitive managed 与 native 依赖必须进入 lock、SPDX SBOM、许可清单和漏洞审计；任何未知版本、缺失 notice 或未解释的漏洞阻断 RC。本地 RIoT SDK 当前没有仓库自有 LICENSE/NOTICE，故只允许在所有者控制的私有项目仓库复用；公开或外部分发前必须由所有者补充/批准许可证和第三方 notices。

完整比较、精确包锁、最小目录、构建/测试/迁移/发布/安装命令、测试门禁和被拒绝方案见[《ControlServer 最小技术栈研究与冻结》](../evidence/controlserver-minimum-stack-research.md)，SHA-256 `e1e8835de02b34147cce20a4533f8b909eafc97b3d3aa221c065c4e06ede59ee`。

实施起点固定为：按该锁定先建骨架和第一条失败的 SQLite 原子受理测试，再进入 `W2G-IS-00`；不得继续用框架调研消耗 2026-08-25 的实施时间。
