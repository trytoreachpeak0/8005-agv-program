# 03 — 固化 SQL Server 低内存运行配置

**What to build:** 让部署与维护人员能够可靠应用并验证 MesIngest 的 SQL Server 内存包络：常态 1536 MB、受控维护期 2048 MB，并拒绝已知不可运行的 800 MB 配置。

**Blocked by:** 02 — 建立规模数据与查询证据门禁.

**Status:** ready-for-human

- [x] 生产常态配置将 max server memory 固定为 1536 MB，并验证 sqlservr 稳态进程目标约不超过 2 GB。
- [x] 维护入口只能显式临时提升到 2048 MB，记录操作者、原因和时间，并在成功、失败或取消后恢复 1536 MB。
- [x] 配置校验明确拒绝 800 MB 及更低的 MesIngest 运行配置，不再次用生产负载重现已知 Error 701。
- [x] 运行诊断公开已提交内存、workspace memory、grant 等待、RESOURCE_SEMAPHORE、Error 701 和 spill 的可审计摘要。
- [x] 无权限、错误实例、配置读取失败或恢复失败时安全退出，不把部分应用报告为成功。
- [x] 隔离 SQL Server 测试证明常态、维护、拒绝和恢复路径，并保持 Failed: 0、Skipped: 0。

## Comments

- 2026-08-23：新增包内 `scripts/maintenance/Invoke-SqlServerMemoryProfile.ps1`，提供
  `Validate`、`ApplyNormal`、`RunMaintenance` 和只读 `Diagnose`。入口只接受 1536 MB
  常态与 2048 MB 维护配置；其它值（包括已知不可运行的 800 MB 及以下）在 SQL 连接前拒绝。
- 写操作要求指向 `master` 的 `MES_INGEST_SQLSERVER_ADMIN`、真实非 LocalDB 实例、精确
  `MachineName\InstanceName` 确认以及 `ALTER SETTINGS` / `VIEW SERVER STATE` 权限。
  JSON/Markdown 证据记录操作者、原因、UTC 时间、配置前后值、恢复状态、committed/workspace
  memory、grant、RESOURCE_SEMAPHORE、Error 701、spill 和 sqlservr 进程包络，不写凭据、连接串
  或错误日志原文。
- `SqlServerMemoryProfileTests` 在真实 SQL Server 上覆盖 1536 MB 常态与三次进程采样、2048 MB
  维护成功/失败/取消、超时终止后恢复、错误实例、连接失败、800/512 MB 预连接拒绝及发布接线；
  聚焦结果为 Failed 0 / Passed 10 / Skipped 0。
- 最终真实 SQL Tier 1 由 `Invoke-RuntimeFeedbackTier1.ps1` 执行：Failed 0 / Passed 740 /
  Skipped 0 / Total 740，耗时 8 分 19 秒。证据位于
  `mes/ingest/csharp/.artifacts/ticket03-tier1/run-20260823T100507Z/`，TRX SHA-256 为
  `de1e43c396d00f0712cc392df4411339fd717c1c126b7ade1518b84d9a9f35c2`。运行后实例配置复核为
  1536/1536 MB。
- `/code-review` 最终复审为 Standards 0 个硬问题、Spec 0 个高置信度缺口；保留的两个判断性
  建议是 PowerShell SQL command setup 重复与 `Action` 分支分散，本票不为尚不存在的新 profile
  提前引入抽象。
- 完整发布冒烟在新脚本已复制到 `scripts/maintenance` 后，被既存第 2 票问题阻断：
  `validation/Invoke-ScaleAndQueryEvidence.ps1` 的受控测试库删除被旧
  `Test-ReleasePackage.ps1` 误判为 cutover 外删库入口。本票没有放宽该安全白名单；该阻断不影响
  `ReleasePackageValidationTests` 22/22 或本票真实 SQL Tier 1，但整包发布需由第 2 票后续修复。
