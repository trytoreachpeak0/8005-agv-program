# 02 — 建立规模数据与查询证据门禁

**What to build:** 提供可重复、安全且接近生产分布的 SQL Server 规模数据与证据工具，使每个后续查询和存储改变都能在 0、7、30 天历史规模下比较，而不是凭 SQL 文本或单次秒表判断。

**Blocked by:** 01 — 重建真实运行反馈环.

**Status:** done

- [x] 在隔离测试数据库中生成保持真实键分布、重复观测、错误期间、活跃与归档 Series 比例的 0、7、30 天等效数据。
- [x] 数据生成入口必须显式指向隔离目标，拒绝系统库、生产库和无法证明身份的数据库，并能清理自己创建的测试数据库。
- [x] 对 DemandSeries、ExternallyReadableDemandCatalog、CurrentIngestAttention、Overview、ReadabilityAudit、ErrorSearch 和原始证据读取采集实际执行计划、STATISTICS IO/TIME、内存授予、spill 与延迟。
- [x] 报告分别记录逻辑已用空间、物理数据文件、LDF、表、聚集索引、非聚集索引和压缩状态。
- [x] 相同构建、配置、数据种子和查询参数能够重放并得到可比较结果；证据带构建身份、schema/contract、SQL Server 版本与数据规模。
- [x] 建立后续票据可复用的通过/失败判定，不把缺失执行计划、被跳过 SQL 测试或空数据库结果当作绿色证据。

## Comments

- 2026-08-23：新增包内入口 `validation/Invoke-ScaleAndQueryEvidence.ps1` 与
  `ScaleAndQueryEvidenceGateTests`。0/7/30 profile 固定 14 秒轮次、600 条/轮、600 Series、
  70% 活跃、30% 归档、10% 活动错误；7/30 天分别生成 43,200/185,142 个历史轮次和
  25,920,000/111,085,200 条历史原始观测。数据种子和锚点时间纳入重放清单。
- 入口只创建显式、尚不存在的 `MesIngest_Scale_*` 库，拒绝系统库、LocalDB、生产库、现有库与
  无法证明所有权的库。schema 只由同包生产 Host bootstrap；数据库扩展属性绑定精确 run ID，
  成功/失败清理都必须再次证明该 ID，日常 Host 不持有测试删库能力。
- 真实 SQL 0 天冒烟见
  `mes/ingest/csharp/.artifacts/ticket02-scale-smoke/scale-20260823T080914Z-94ad296e/`：
  600 RawObservation / 600 Series；七个查询面各自有 statement 与实际计划，合计 37 条 measured
  statement、419 个 `query_post_execution_showplan`；每面 spill 均为 0。存储证据包含 2 个物理
  文件与 35 个 allocation（19 clustered / 16 nonclustered）。Tier 1 attestation 为
  Failed 0 / Passed 725 / Skipped 0 / Total 725，证据凭据模式扫描 0 命中，隔离库已删除。
- 本票验证的是可重复工具和 fail-closed 证据契约；未在实现回合主动写入 2,592 万或 1.11 亿行。
  完整 7/30 天容量运行由第 27 票执行，24 小时并发稳定运行由第 28 票执行。
- 最终当前源码真实 SQL Tier 1 见
  `mes/ingest/csharp/.artifacts/ticket02-tier1/run-20260823T081251Z/`：
  Failed 0 / Passed 728 / Skipped 0 / Total 728，耗时 7 分 38 秒。
