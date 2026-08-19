# 25 — 删除旧模型并形成空库切换发布包

**What to build:** 在所有生产调用方都已迁到新版契约后收缩 expand 阶段的兼容脚手架，交付只认识新版 schema、领域语言、API 和 Watch 的完整发布包，并在一次性数据库上演练可审计的停机、备份、精确目标确认、旧库删除、新空库 bootstrap 与整套旧版回退。

**Blocked by:** 18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览；20 — DemandSeries 生产页面；21 — 资格审计与 AREA Variant A 生产页面；22 — Error Search Variant A 与接入告警生产页面；23 — 共享黄金机 UI 集成验收与基线；24 — 迁移发布脚本、smoke 和验证说明

**Status:** ready-for-agent

- [x] 删除旧 FrozenMesFieldSet/FieldDrift/ReappearAfterGone 语义、IngestAlert incident 生命周期、DemandChangeFeed、Feed Sequence、bootstrap high-watermark、SYNC_CURSOR_EXPIRED、旧 DTO/端点、旧配置和旧 schema 升级路径；领域、Host、Watch、OpenAPI、测试和文档不再引用这些契约。
- [x] 最终 schema 只从空数据库建立新版 PollTrace、ProjectionCommit、DemandSeries、TransportDemand 世代、原始观测、事件、当前条件、错误期间、资格、当前关注和 CatalogRevision 所需结构，不迁移或推测旧业务历史。
- [x] 运行时代码、Watch、常规安装和卸载逻辑绝不自动删除数据库；删除只存在于要求人工停机、备份和精确目标确认的受控切换演练。
- [ ] 在一次性目标数据库执行完整切换演练：停止旧 Host、Watch 和外部消费者，记录备份，核对精确实例和库名，删除旧库，由新 Host 建立空 schema，并以首个完整 SUCCESS bootstrap 可证明的新历史。
- [ ] 演练证明错误当前条件使用 BOOTSTRAPPED_CURRENT_CONDITION 而不伪造旧开始时间，旧 TransportDemand、IngestAlert 和 ChangeFeed 记录不会进入新库。
- [ ] 回退演练只通过停止新版并恢复整套旧程序、旧配置和独立旧数据库备份完成；新程序不得读取旧库，旧程序不得读取新库，也不宣称支持滚动或新旧混跑。
- [x] 最终包包含 Service、Watch、唯一正式查询、空配置模板、安装与卸载脚本、版本化 OpenAPI 和新版验证说明，且通过真实兼容 SQL Server 的主要 seam、事务、重启、鉴权和打包回归。
- [x] 票 23 的证据在最终包未改变视觉、XAML、UI Automation 或 DPI 输出时保持有效，本票只引用其冻结源和证据身份，不重复黄金机像素或 DPI 门禁；若本票引入相关输出变化，则标明失效场景并只重跑票 23 中受影响的预览、批准、稳定与清理要求。
- [x] 自动化证明仓库和发布产物不再包含真实凭据、旧契约入口或能够对未确认实例执行 DROP 的无人值守路径，并保存切换与回退演练的目标身份、结果和清理证据。

## 实现记录（2026-08-19）

### 旧模型删除范围

删除而不是关闭。领域侧移除 `Domain.cs`（旧 `TransportDemand`/`IngestAlert`/`AlertCodes`/
`RestartRecovery`）、`TransportDemandReconciler`、`StoreAndRunner`、`SqlServerTransportDemandStore`、
`DemandChangeFeed`、`AlertIncidentSync`、`AlertListQuery`、`DemandListQuery`、
`CsvFileMesSnapshotSource`、`OracleMesSnapshotSource`、`MesIngestApiContract`；`OracleSnapshotOptions.cs`
只保留新版轮次源仍需要的 `OracleClientMode` 与 `OracleSnapshotOptions`。

Host 侧移除 `PollHostedService`、全部旧 DTO 与 `/api/contract`、`/api/demands`、`/api/alerts`、
`/api/poll-health`、`/api/demand-changes` 端点，`MesIngestOpenApi` 收缩为只发布 `/openapi/v2.json`，
`pack/openapi/v1.json` 删除。Watch 侧移除 `MainWindow`、`AlertDetailWindow`、`UnifiedEventsWindow`、
旧 `MesIngestApiClient`/`WatchDtos`/`WatchHostSession`/`WatchApplicationComposition` 及其会话、
自动刷新、横幅、布局偏好；`WatchHostContract.cs` 保留 V2 客户端仍在用的
`WatchHostSettings`/`WatchHostFailureKind`/`WatchHostQueryException`/`WatchHostQueryFailure`/
`WatchEndpointFetchException`，`WatchOptions.cs` 保留 `WatchOptions` 与 `WatchHttpStageClassifier`。

UI 测试侧一并退役旧 shell 的证据面：`WatchXamlVisualTests` 与 `Baselines/`（19 个 Verify.Xaml 基线）、
`WatchWindowJourneyTests` 与它的 5 份旧 journey window 基线、`WatchCompositionRootTests`、
`ScriptedFakeHost` 的 V1 适配器与场景。`Invoke-WatchUiTests.ps1` / `Invoke-GoldenRendererValidation.ps1`
移除 `watch-xaml-visual` 与 `watch-xaml-stability` 套件，`Test-WatchXamlBaselineStability.ps1` 删除；
`watch-window-visual` 的 11 份票 19–22 生产基线未改动。共用的 journey 辅助方法移入
`WatchWindowJourneySupport.cs`，`watch-vm-tests` 继续排除桌面校准探针，套件构成与票 23 验收时一致。

### 旧配置拒绝启动而不是被忽略

`MesIngestHostOptions.RetiredConfigurationKeys` + `ValidateContractShape` 让带有
`SqlServerConnectionString`、`SnapshotCsvPath`、`ChangeFeedRetentionHours`、`AlertRetentionDays`、
`DisappearThreshold`、`GoLiveBaseline`、`EnableLegacyDevelopmentEndpoints` 的配置直接拒绝启动。
一份为旧契约写的部署文件因此不会"看起来被接受"而实际什么都没做。`SnapshotSource` 只接受
`Oracle` 或 `None`。`NewSqlServerConnectionString` 有意保留 `New` 前缀：旧配置文件不可能带这个键，
因此新程序不会因为键名重合而连上旧库。

发布烟测新增一项：注入一个已退役键启动包内 Host，必须非零退出且 stderr 出现 `retired keys`
（与共享密钥拒绝启动同样核对拒绝原因，避免端口冲突冒充通过）。

### 空库切换与整体回退

`pack/cutover/`（发布为 `scripts/cutover/`）是产品中唯一会删除数据库的地方；Host、Watch、
`install-service.ps1`、`uninstall-service.ps1` 都不删库。切换脚本必须走 `master` 连接，
从连接本身解析 `MachineName\InstanceName` 与库名，**要求操作员在控制台原样键入该身份**，
没有任何 `-Force`/`-NonInteractive` 开关；重定向或无人值守调用因此一定停在确认处。
确认后核对无其它用户会话 → `BACKUP ... WITH CHECKSUM` → `RESTORE VERIFYONLY` → 记录备份 SHA-256
→ `DROP DATABASE` → 新建空库并核对 0 张用户表 → 写 `cutover-evidence.json`。脚本不建 schema，
由新 Host 首次启动建立，首个完整 SUCCESS 是新历史最早可证明起点。

`Invoke-CutoverRollback.ps1` 先确认新版服务已停止或未安装，要求同样的键入确认，恢复独立备份后
核对恢复出来的库**不含**当前契约的 `mesingest` schema（否则是恢复了错误备份），并记录
`rollback-evidence.json` 与 `mixedModeSupported=false`。

### 自动化（第 9 条）

`RetiredContractAndCutoverSafetyTests`：
- 已发布程序集不再定义任何以退役契约命名的类型；
- 除受控演练外，没有任何可执行脚本或非测试源码能 `DROP DATABASE`；
- 安装/卸载脚本不含 `DROP`/`RESTORE DATABASE`/`SqlConnection`；
- 两个演练脚本都要求键入确认且没有绕过开关，确认来自 `Read-Host`；
- 扫描 `git ls-files` 覆盖的配置、模板、脚本和文档，不得出现真实凭据，并用一组正反例证明
  扫描本身不是空转。

`pack/Test-ReleasePackage.ps1` 对发布包做同一组检查（唯一 DROP 路径、演练不可绕过、
退役配置键与退役端点文本扫描），并把切换脚本列入必需文件。

### 已跑的验证

Tier 1：`dotnet test MesIngest.Tests` → **450 passed / 0 failed / 82 skipped**。
82 个 skip 全部是本机无真实 SQL Server 的 `Ticket01SqlServer` 门禁用例，其中包括本票新增的
`EmptyDatabaseBootstrapTests`（空库一次 bootstrap、非空库拒绝且不改动既有表）。

### 打包发布门禁已通过（2026-08-19）

第 7、8 条的现场证据已取得。`Invoke-GoldenRendererValidation.ps1 -Suite watch-package-release`
在校准黄金机 `gpt_win11` 上通过：计划任务退出码 0、`GOLDEN_RENDERER_VALIDATION_PASSED`、
`release-gates-passed.json` 为 `READY_FOR_HOST_CLEANUP_AND_FINALIZATION`。

- 发布烟测 PASSED，对着真实 SQL Server（专用可丢弃空库，启动前 0 张用户表）；
- 全量回归 **533 / 533 通过 / 0 失败 / 0 skip**（用例数由票 24 的 937 降至 533，
  是删除 48 个退役 shell 测试文件的直接结果，两侧计数一致）；
- 本票新增的两项现场实测：注入退役配置键后包内 Host **拒绝启动**（退出码非零且
  stderr 核对为 `retired keys`），七个退役路由全部 404；
- 打包 Watch 验收跑非像素两套，150 项 0 失败，5 个 skip 精确匹配具名集合；
- 人工验收由 Zhengyu Shao 于 2026-08-19 22:52 签署；
- 清理完成、原机复核 1920x1080 / 96 DPI / session 1，`Differences: []`。

第 8 条按「打包未改变已批准输出」复用票 23 的视觉验收，**未做像素比对**；该保留
说明已在签字时告知批准人并写入 `manual-acceptance.json`。若需更硬证据应另跑
`-Suite watch-window-visual`。

完整证据与逐项实测见
[`.artifacts/ticket25-acceptance/EVIDENCE-INDEX.md`](../../../.artifacts/ticket25-acceptance/EVIDENCE-INDEX.md)。

达成过程共 5 轮，前 4 轮的红全部是真问题并逐条修复：17 个 SQL 门禁测试仍注入
`EnableLegacyDevelopmentEndpoints`（80 红，本机因 skip 而看不见）、烟测库未清空、
以及本票新增的三个扫描依赖 `git ls-files` 而 payload 上没有 git（3 红）。逐条说明见证据索引。

### 尚未完成（需要 tier 3 现场运行）

第 4、5、6 条仍未勾选，它们要求在一次性数据库上真实运行：

- 一次性库上的完整切换演练与 `BOOTSTRAPPED_CURRENT_CONDITION` 证据；
- 整体回退演练。

两者按设计都要求操作员在控制台原样键入目标实例/库名，没有任何绕过开关，
因此**不能由代理代跑**，必须由现场人员执行，代理只负责准备参数与核对证据。
