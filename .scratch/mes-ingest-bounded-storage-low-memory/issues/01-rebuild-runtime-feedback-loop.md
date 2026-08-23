# 01 — 重建真实运行反馈环

**What to build:** 重新建立能够回答“现在到底运行着什么、失败在哪里、后续改变是否改善”的只读反馈环，让开发从当前 Host、SQL Server、部署包和真实 SQL 集成测试状态出发，而不是沿用 2026-08-22 的旧观察。

**Blocked by:** None — can start immediately.

**Status:** ready-for-human

- [x] 记录 Host 服务、进程、监听端点、部署程序集身份、契约身份、SQL Server 服务与实例状态；输出不得包含凭据或连接字符串。
- [x] 验证契约发现端点和主要当前读取端点的真实响应，并区分 Host 可监听、SQL 不可用、查询超时和契约不匹配。
- [x] 记录 SQL Server 当前 max server memory、恢复模式、数据库文件、错误日志中的 Error 701、17300/17312、RESOURCE_SEMAPHORE 与 spill 信号。
- [x] 使用 run-tests skill 取得真实 SQL Server Tier 1 命令，证明 SQL 集成测试可以实际执行，并在证据中明确 Failed、Passed、Skipped 和 Total。
- [x] 建立不修改服务、数据库和生产配置的可重复诊断入口，重复运行能比较前后结果。
- [x] 识别当前脏工作区中与本优化有关和无关的在途改动，不清理、重置、覆盖或把既有 diff 归入本票。

## Comments

- 2026-08-23：新增包内只读入口 `validation/Invoke-RuntimeFeedbackLoop.ps1`、源码真实 SQL
  Tier 1 固定命令入口 `Invoke-RuntimeFeedbackTier1.ps1`、Windows PowerShell 5.1 行为测试和安装说明。
  最终当前快照见
  [`runtime-feedback.md`](../evidence/runtime-feedback/run-20260823T053342Z-d9cbd210/runtime-feedback.md)，
  JSON 与 Markdown 均有 SHA-256 inventory，凭据模式扫描无命中。
- 当前实况是 `HOST_LISTENING + CONTRACT_OK + SQL_UNAVAILABLE + QUERY_TIMEOUT`：Host 服务运行且
  `127.0.0.1:5088` 监听；契约 `2026.08.new-mes-ingest.v2.0`、schema `17`、capability `9/9`
  与部署包精确匹配；四个主要当前读取均在 3 秒请求门槛超时；`MSSQLSERVER` 服务为 Stopped，
  只读连接失败。
- SQL 停止时不能把旧值冒充当前配置：当前 max server memory、恢复模式、数据库文件和 DMV
  资源证据明确标为 unavailable。Windows SQL 事件只能证明最近一次配置事件把 max server
  memory 从 4096 MB 改为 800 MB，并在 168 小时窗内观察到 Error 701 共 22 次、17300 共 12 次、
  17312 共 7 次；这些是带时间的最后观测，不是当前运行配置权威。RESOURCE_SEMAPHORE 与 spill
  事件信号均为 0，但 SQL DMV 不可用，因此不能宣称资源门禁通过。
- 最终 Tier 1 为 `Failed 0 / Passed 643 / Skipped 82 / Total 725`。收集器按
  `Total - Executed` 计算 skip（VSTest 的 `notExecuted` counter 对这 82 项错误地保持 0），并正确
  写入 `REAL_SQL_TIER1_TRX_NOT_FULL_SUITE`，没有把 `Failed 0` 冒充真实 SQL 通过。
- 2026-08-23：用户批准维护窗口和 SQL 实例配置后，先停止 Host，再启动真实 `MSSQLSERVER`，并把
  已知禁止的 800 MB 实例上限恢复为规范常态 1536 MB；这些维护动作在只读收集器之外执行。测试后
  无残留 `MesIngest_Ticket01_*` 数据库，Host 已恢复运行。
- 真实 SQL Server 16 / compatibility 160 Tier 1 通过：`Failed 0 / Passed 725 / Skipped 0 / Total 725`，
  耗时 7 分 22 秒；原始
  [脱敏 TRX](../evidence/runtime-feedback/run-20260823T070216Z-34150355/runtime-feedback-tier1.redacted.trx)、
  [`attestation`](../evidence/runtime-feedback/run-20260823T070216Z-34150355/runtime-feedback-tier1-attestation.json)
  与[脱敏清单](../evidence/runtime-feedback/run-20260823T070216Z-34150355/runtime-feedback-tier1-redaction.json)
  已随最终快照保存并纳入 SHA-256 inventory；清单保留 attestation 绑定的原始 TRX 哈希，脱敏副本只移除
  4 处凭据扫描器合成测试参数，不改变 725 个结果或计数。
- 最终当前快照见
  [`runtime-feedback.md`](../evidence/runtime-feedback/run-20260823T070216Z-34150355/runtime-feedback.md)：
  Host、监听、契约和 SQL 均可用，契约仍与部署包精确匹配，真实 SQL 证明校验为 `True`。当前
  `MesIngest_V2` 为 FULL recovery，数据文件 7112 MB、日志 840 MB，max server memory 为
  1536/1536 MB；SQL error log 中当前 701/17300/17312 均为 0，168 小时 Windows 事件仍保留历史
  26/12/7 次信号。
- 反馈环还识别出后续票据必须处理的红色事实：`watch-overview` 与 `demand-series` 在 10 秒门槛超时，
  当前缓存计划 `total_spills=963`、`max_last_spills=546`；采样时 RESOURCE_SEMAPHORE 等待和 waiter
  均为 0。故本票只宣称反馈环和真实 SQL 门禁已重建，不宣称查询性能已经修复。
