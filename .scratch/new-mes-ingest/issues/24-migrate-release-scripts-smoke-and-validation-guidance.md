# 24 — 迁移发布脚本、smoke 和验证说明

**What to build:** 让发布、安装、smoke 和验证工作流只使用已冻结的新版 MesIngest 契约，从发布包启动真实 Service 与 Watch 后能够验证单条正式 Oracle 查询、SQL Server 持久化、版本化读取、CatalogRevision 条件读取和关键 Watch 行为，而不再调用或教授旧 Demand、IngestAlert incident 或 DemandChangeFeed 流程。

**Blocked by:** 15 — 正式单语句 Oracle Round source；17 — 冻结完整新版 API/OpenAPI 契约、旧端点暂留；23 — 共享黄金机 UI 集成验收与基线

**Status:** ready-for-human

- [x] 发布、安装、卸载、release smoke、Watch acceptance、工厂验证和返回清单统一使用新版契约发现、轮询证据、需求系列、资格审计、错误检索、当前关注、概览和 ExternallyReadableDemandCatalog 能力。
- [x] 所有已知打包与验证调用方停止请求旧 DemandChangeFeed、bootstrap high-watermark、SYNC_CURSOR_EXPIRED、旧 IngestAlert incident、字段冻结和旧分页 DTO；验证文本不再建议下游持久业务镜像。
- [x] 发布包只包含一份正式 MES_TASK_UNION 查询原稿，并能证明 Service 和 Watch 使用同一版本化契约；文件或脚本化轮次可以在无工厂 Oracle 时驱动同一生产入口做可重复 smoke。
- [x] smoke 验证首次目录正文、CatalogRevision/ETag、同修订 304、新版只读 API 鉴权、契约严格匹配、SQL Server 重启持久化，以及关闭 Watch 后 Service 继续轮询和提供 API。
- [x] 验证说明明确区分本机或黄金机证据、真实兼容 SQL Server 门禁和工厂 Oracle 验收；未运行的外部门禁必须记录为具名 skip，不能把替代环境通过写成现场通过。
- [x] 配置模板、命令输出和证据不包含 Oracle、SQL Server、API 或黄金机凭据；远程绑定缺少共享密钥时拒绝启动或拒绝业务数据访问，日志与返回包遵循脱敏边界。
- [x] 包装后的 Watch smoke 若需要启动、操作或截图真实 WPF，必须通过 gpt_win11 交互计划任务执行；PowerShell Direct 只做部署、监控和证据取回。
- [x] 当票 23 已批准的 PNG/XML/UIA/DPI 输出未变化时，包装 smoke 只验证已发布二进制的启动、连接和关键功能，不重复像素候选、10 次稳定、基线提升或 DPI clone；若包装差异造成 UI 输出变化，则明确使相应票 23 场景失效并只重跑受影响门禁。
- [x] 自动化校验发布包中不再出现旧端点、旧配置项或旧契约说明，并证明运行时 OpenAPI 与包内版本化 OpenAPI 一致。

## 实现记录（2026-08-19）

### 无工厂 Oracle 的可重复轮次

新增 `MesIngest.Core/ReplayedMesTaskUnionStatementExecutor.cs`：从 JSON 录制文件回放
MES_TASK_UNION 结果集。它**只**替换 Oracle 语句结果，canonical 查询原稿、
`OracleMesTaskUnionRoundSource`、`MesTaskUnionPollRunner` 和 ProjectionCommit 边界全部是发布态代码，
因此录制轮次驱动的是同一条生产入口。

防止被误当作现场证据的三道闸：

- driver 报告 `FILE_REPLAY`，`RuntimeState` 恒为 `Unverified`，所以探针与工厂采集器仍判 `NOT_EXECUTED`；
- 录制声明的 queryVersion 与 Host 加载的 canonical 原稿不一致时，该轮直接是 Failure，不投影；
- `MesIngest:ReplayRoundsFromRecordingPath` 必须配套
  `MesIngest:ReplayRoundsAcknowledgement=RELEASE_SMOKE_NOT_FACTORY_EVIDENCE`，
  配置了录制时 `--probe-oracle` 拒绝执行，非 V2 Oracle 运行时配置了录制则拒绝启动。

### 发布烟测新增的验证

`pack/validation/Invoke-ReleaseSmoke.ps1` 在原有契约身份 / OpenAPI 一致 / 旧面 404 之上补齐：
目录首次正文与 `CatalogRevision` 弱 ETag、同修订 304 且无正文、受限原始证据缺密钥与错密钥均 403、
非本机绑定缺 SharedSecret 拒绝启动（并核对拒绝原因，避免端口冲突冒充通过）、
无 Watch 时 `pollTraceHighWater` 持续前进、SQL Server 强杀重启后目录条目集合不变且重启后两次读取同 ETag。
`-IncludePackagedWatch` 才实际启动关闭包内 WPF（要求交互桌面，并使用烟测自有的 `LOCALAPPDATA` 配置根，
不污染黄金机用户配置）；默认记为具名 skip `PACKAGED_WATCH_PROCESS_INDEPENDENCE`。

### 打包与文档门禁

- `pack/Test-ReleasePackage.ps1` 新增两项：包内文档与配置的**退役契约扫描**
  （同一行说明其已退役才放行），以及 `service\MesIngest.Core.dll` 与 `watch\MesIngest.Core.dll`
  字节一致 —— `NewMesIngestContract` 在 MesIngest.Core，字节一致即 Service 与 Watch 同一版本化契约；
  该哈希写入 `RELEASE-MANIFEST.json.sharedContract`，烟测再次核对。
- `MesIngest.Host/appsettings.json` 与 `appsettings.Local.json.example` 移除旧配置项
  （`SnapshotCsvPath`、`SqlServerConnectionString`、`ChangeFeedRetentionHours`、`AlertRetentionDays`）
  及旧契约说明；模板改写为 V2 分页与条件读取说明。
- `Invoke-WatchAcceptance.ps1` 默认改为 `watch-production-preview`（非像素的
  `watch-vm-tests` + `watch-ui-journeys`）；`Invoke-GoldenRendererValidation.ps1-Suite watch-package-release`
  相应只要求两份 runner log，并在 summary 记录复用票 23 视觉验收的依据。
- `FACTORY-VALIDATION.md` 新增「证据分级」（本机/黄金机、真实兼容 SQL Server、工厂 Oracle 三类互不替代，
  未运行必须写具名 skip）；`RETURN-CHECKLIST.md` 同步要求。

### 已跑的验证

Tier 1：`dotnet test MesIngest.Tests` → **835 passed / 0 failed / 99 skipped**。
99 个 skip 全部是本机无 LocalDB 的 SQL Server 与 SchemaUpgrade 测试，属 AGENTS.md 允许的 tier 1 skip。

`MainWindowUiAutomationTests.Fluent_title_bar_supports_uia_keyboard_double_click_and_mouse_drag`
在本机全量跑中偶发红（合成鼠标拖拽依赖真实桌面输入状态）。已在 `HEAD`（85adc7c，不含本票任何改动）
的独立 worktree 连跑两次复现同样失败，确认与本票无关，属既有不稳定项。

### 打包发布门禁已通过（2026-08-19）

第 4 条的现场证据已取得。`Invoke-GoldenRendererValidation.ps1 -Suite watch-package-release`
在校准黄金机 `gpt_win11` 上通过：计划任务退出码 0、`GOLDEN_RENDERER_VALIDATION_PASSED`、
`release-gates-passed.json` 为 `READY_FOR_HOST_CLEANUP_AND_FINALIZATION`。

- 发布烟测 PASSED，对着真实 SQL Server（专用可丢弃空库，启动前 0 张用户表）；
- 全量回归 **937 / 937 通过 / 0 失败 / 0 skip**；
- 打包 Watch 验收跑非像素两套，228 项 0 失败，5 个 skip 精确匹配具名集合；
- 人工验收由 Zhengyu Shao 于 2026-08-19 17:57 签署；
- 清理完成、原机复核 1920x1080 / 96 DPI / session 1，`Differences: []`。

完整证据与逐项实测见
[`.artifacts/ticket24-acceptance/EVIDENCE-INDEX.md`](../../../.artifacts/ticket24-acceptance/EVIDENCE-INDEX.md)。

达成过程共 15 轮，前 14 轮的红全部是真问题并逐条修复（录制数据不合域格式、启动超时与
目录竞态、窗口句柄竞态、负向路径参数、黄金机 SDK 的 C# 12 解析歧义、门禁从未注入
`MES_INGEST_TICKET01_SQLSERVER` 导致 80 个 V2 测试长期静默 skip、六个 WPF 测试类的并行
竞态、413/400 契约期望写反、令牌篡改手法有 3% 概率无效、UI skip 判据过于绝对、
`startup-within-10-seconds` 无测量支撑）。逐条说明见证据索引末节。

### 遗留（不属于本票）

- 打包 Watch 冷启动耗时呈双峰（6.3 s / 14.0 s），已开
  [票 27](27-packaged-watch-cold-start-cost.md)。
- 旧 `MainWindow` 及其测试仍在，属票 25 的旧模型收缩范围。
