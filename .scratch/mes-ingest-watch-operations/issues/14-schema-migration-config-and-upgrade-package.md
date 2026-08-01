# 14 — SQL Schema 迁移、配置样例与可回滚升级包

**What to build:** 将增量投影、Alert incident、ChangeFeed 和新 Watch 配置作为可重复、安全的现有安装升级交付，不丢失永久 GONE/DemandId 历史。

**Blocked by:** 02 — Watch 配置; 04 — 增量 store; 06 — ChangeFeed; 10 — Alert schema; 12 — OpenAPI

**Status:** done

- [x] schema upgrade 幂等且在失败时不留下半迁移；禁止通过 DROP/重建丢失 TransportDemand 历史
- [x] 在修改 IngestAlerts 前定义 legacy 数据迁移/保留策略并测试已有数据库升级
- [x] 新索引、ChangeFeed、incident 字段/表和 retention cleanup 可重复部署
- [x] appsettings/Local example 包含 RequestTimeoutSeconds、Watch log retention、Alert retention、ChangeFeed retention/page limits
- [x] Watch 与 Host 发布物版本不匹配时给出明确 contract/version 错误，不显示空板
- [x] 发布包带静态 OpenAPI、升级说明、备份前置条件和恢复步骤
- [x] 自动测试从 Phase-1 schema fixture 升级并保留 DemandId、VISIBLE/GONE、pause、alerts、poll health
- [x] 不修改或部署任何 Oracle DDL/索引/视图；客户 MES query 文件保持批准原稿

## Comments

- The workspace may have existing production-like SQL Server data; migration safety is a product acceptance condition, not a cleanup convenience.
- 2026-08-01: Implemented Phase-1→current EnsureSchema upgrade with `IngestAlerts_LegacyArchive` before incident columns, `MesIngestSchemaVersion`, `/api/contract` + Watch `CONTRACT_VERSION_MISMATCH`, Host/Watch Local examples, `pack/UPGRADE.md` (backup/restore), static OpenAPI update. DDL steps remain additive/idempotent (re-run Host after failure); rollback uses pre-upgrade DB backup.
