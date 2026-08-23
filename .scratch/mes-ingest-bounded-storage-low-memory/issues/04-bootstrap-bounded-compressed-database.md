# 04 — 建立新空库的存储默认值

**What to build:** 让新 MesIngest 空库从创建时就使用 SIMPLE 恢复、PAGE 压缩和有界热字段，并由严格 schema 校验防止部署后漂移。

**Blocked by:** 03 — 固化 SQL Server 低内存运行配置.

**Status:** ready-for-human

- [x] 空库 bootstrap 将恢复模式设为 SIMPLE，且不创建完整、差异或事务日志备份。
- [x] DemandRawObservation 的主要聚集与非聚集索引默认使用 PAGE 压缩，schema validation 精确验证该属性。
- [x] 当前投影字段、筛选列、索引键和临时结构使用由真实数据与明确上限证明的有界类型。
- [x] DemandRawObservation 原始证据保持无损；超界值产生可诊断失败，不截断、回填或任选。
- [x] 已含未知对象、错误恢复模式、缺失压缩或不匹配字段边界的数据库被拒绝且不被静默修补。
- [x] 空库集成测试证明 bootstrap 幂等、严格 validation、压缩节省和 LDF 可重用状态，SQL 测试不得跳过。

## Comments

- 2026-08-23：空库 schema 身份提升到 18。bootstrap 在 session schema lock 下只对真正空库设置
  SIMPLE；已有库只做严格验证，不自动修复 FULL、未知顶层对象、未知普通索引、错误字段宽度、
  非聚集原始观测主键或压缩漂移。三个 DemandRawObservations 主要索引均要求 PAGE，主键还必须保持
  clustered。
- AREA、EQP、STEP、PACKAGE 的当前投影、原始观测、Catalog、SQL 参数和热临时结构采用 512
  字符上限，DATES 原文采用 128；筛选 JSON 参数采用 4000 字符包络，当前条件聚合采用 2048。
  真实边界依据见 `evidence/storage-bootstrap/field-boundaries.md`：客户 10 轮、6720 行实测最大
  PACKAGE 48、STEP 18 UTF-8 字节，旧 Oracle 字典声明 STEP 最大 255 byte。
- `EmptyDatabaseBootstrapTests` 在真实 SQL Server 16 / compatibility 160 上覆盖 17 个用例实例，
  包括幂等、SIMPLE、无备份、`log_reuse_wait_desc = NOTHING`、PAGE/NONE 实际页对照、512 字符
  Unicode 原文往返、513 字符预写拒绝、超大筛选拒绝以及全部漂移拒绝路径。
- 最终 Tier 1：Failed 0 / Passed 755 / Skipped 0 / Total 755，耗时 9 分 47 秒。TRX 位于
  `mes/ingest/csharp/.artifacts/ticket04-tier1-reviewed/ticket04-tier1-reviewed.trx`，SHA-256 为
  `7d6bdaa1752d2a1341a3751b255902cb8db20702e88a0000157486d7f182c734`。最终非增量 Release
  全解决方案构建为 0 warning / 0 error。
- `/code-review` 最终复审：Standards 0 个硬违规、Spec 0 个剩余缺口。保留的判断性建议是把
  AREA/EQP/STEP/PACKAGE 的重复参数绑定进一步收拢；本票维持各 SQL 写路径的显式局部绑定。
