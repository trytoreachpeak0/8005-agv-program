# 23 — 播种墓碑并运行无删除切换门禁

**What to build:** 在一个没有删库能力的 MesIngestCutoverRun 中完成旧库墓碑播种、数量/哈希证明、三轮投影、API、目录和精确数据库身份门禁，并生成数据库外证据。

**Blocked by:** 21 — 完成 Watch 刷新与保护状态呈现.

**Status:** ready-for-human

- [x] 旧库读取严格只选择构造 ArchivedDemandKeyTombstone 所需的已归档键与最小身份事实。
- [x] 不迁移当前投影、PollTrace、DemandRawObservation、DemandSeries 详细图、事件、错误历史或业务原文。
- [x] 对规范化墓碑集合计算稳定数量和哈希，旧库导出、新库导入与复核使用同一算法和版本。
- [x] 新库导入幂等，重复键不产生重复墓碑，冲突身份使整次播种失败。
- [x] CutoverRunId 绑定所有门禁、结果、证据、旧/新数据库身份和 HistoryEpoch。
- [x] 门禁证明旧 Host 已停止、旧库无业务连接、墓碑证明一致、新 contract/schema 精确匹配且连续三轮投影成功。
- [x] 主要 Watch API、ExternallyReadableDemandCatalog 和 reference consumer 在同一运行中通过，新目录不含墓碑键。
- [x] 精确旧库身份门禁验证显式名称、非系统库、非新库、预期旧 schema/contract 和解析后的 SQL 数据目录。
- [x] 任一读取、播种或门禁失败都保留新旧库、失败退出、不后台重试且不生成删除授权。
- [x] 在数据库外写不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，不包含业务原文。
- [x] 复用既有 cutover SQL 工具、发布包验证、Host/reference consumer fixtures 和 Ticket 15 墓碑模型；不建设通用迁移引擎或新的部署编排平台。
- [x] 哈希的大集合与顺序无关性使用内存生成数据验证；真实 SQL Server 只使用不超过 20 个墓碑的旧/新库，覆盖成功路径和一个代表性失败路径。
- [x] 其余冲突、连接、身份、目录和门禁拒绝分支使用确定性 dry-run/策略测试，不为每个拒绝条件重复启动整包或创建数据库。
- [x] 开发期运行聚焦 cutover/tombstone/gate 测试，关闭时运行一次真实 SQL Server Tier 1；正常验证目标在 90 分钟内完成并保持 Failed: 0、Skipped: 0。
- [x] 生产 Host 与本票运行身份均不具备删库权限；时间目标不能放宽无删除边界。

## Comments

- 2026-08-25：保留并完成既有 `CutoverSqlTools.ps1` / `MesIngestCutoverRunTests.cs` WIP。新增一次性、无删除能力的 `Invoke-MesIngestCutoverRun.ps1`：旧库只导出最小墓碑字段，使用显式版本化的稳定 proof 与权威 TransportDemandKey 固定向量，事务性幂等播种；播种后冻结 PollTrace high-water，前台有界等待三轮新成功投影；同一 CutoverRunId 绑定精确数据库身份、HistoryEpoch、V2 contract/OpenAPI、主要 Watch API、目录与生产 reference consumer。最终证据前重新检查旧 Host、全局 session 可见权限、旧库连接、数据库身份及新旧墓碑 proof。失败不重试、不删除、不产生删除授权。
- 2026-08-25：真实 SQL Server 聚焦回归使用本机默认 `MSSQLSERVER`（ProductVersion 16.0.1190.2、EngineEdition 3、compatibility 160，非 LocalDB）；42 passed / 0 failed / 0 skipped。真实旧/新隔离库仅播种 3 个墓碑，覆盖成功、重复幂等、播种后三轮投影、过期 baseline 拒绝及冲突身份整事务失败；其余门禁拒绝矩阵使用确定性策略测试。
- 2026-08-25：两轴 code review 完成并修复首轮 Standards 2 项 hard violations（播种前三轮可误通过、KeyToken 未复算）及 Spec 3 项 P1（同运行因果边界、DMV 可见性误通过、最终 Host/session 门禁陈旧）；最终 Standards 0 findings，Spec 0 findings / scope creep 0。
- 2026-08-25：最终一次 Tier 1 从 `mes/ingest/csharp` 运行 `dotnet test MesIngest.Tests`，显式设置真实 SQL Server、ProductMajor 16、compatibility 160；875 passed / 0 failed / 0 skipped，12 分 24 秒。TRX：`mes/ingest/csharp/.artifacts/ticket23-tier1/ticket23-tier1.trx`，SHA-256 `d90fb3c6abeb9b7fdd3da4d26fff4f6bc1b5900ef4290c3790372a934d8b92ad`；TRX counters 与 875 个 UnitTestResult 均确认 non-passed/not-executed 为 0。
- 2026-08-25：最终 win-x64 `-SkipWatch` 实际发布包通过 `Test-ReleasePackage.ps1`；manifest：`mes/ingest/csharp/.artifacts/ticket23-release-package/RELEASE-MANIFEST.json`，SHA-256 `6d27441f9283cdc4cfc6f5df9b2330df1bbf2543466ae046b7360529584d8436`。本票未改 Watch UI，未运行 Tier 2/3；未执行 ticket 25 删除，也未对任何生产数据库运行 cutover。
