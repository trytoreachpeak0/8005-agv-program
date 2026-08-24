# 25 — 只删除已证明的精确旧库

**What to build:** 在 MesIngestCutoverRun 的全部同窗门禁通过后，使用仅本次运行有效的临时权限自动删除精确旧库，并在成功、失败或异常结束后撤销权限。

**Blocked by:** 23 — 播种墓碑并运行无删除切换门禁.

**Status:** ready-for-human

- [x] 删除能力只存在于一次性 CutoverRunId 运行，日常 Host、Watch 和 reference consumer 永远不拥有或调用该能力。
- [x] 删除前重新验证全部门禁仍属于当前运行，旧库显式名称、schema/contract、文件目录、连接状态和新库排除条件仍成立。
- [x] 不允许通配、名称前缀、自动猜测、系统库、新库或无法解析文件目录的目标。
- [x] 临时提升权限在成功、门禁失败、删除失败、取消和异常退出后都被撤销并留下审计。
- [x] 任一检查或删除失败时不后台重试，保留能够保留的新旧数据库，只有新的明确运行才能再次尝试。
- [x] 所有目标身份和门禁拒绝分支先通过无删库 dry-run/策略测试证明；不为每个拒绝条件创建并真实删除数据库。
- [x] 真实删除只在隔离实例运行一个完整成功路径和一个删除失败/权限撤销路径，其余失败矩阵复用 Ticket 23 证据。
- [x] 删除成功证据在数据库外和 Windows 事件日志中完整存在，且不声称有备份或回滚路径。
- [x] 复用 Ticket 23 的 CutoverRun、身份解析、证据和现有 cutover SQL 工具，不建设通用数据库管理框架。
- [x] 开发期运行聚焦拒删/权限/证据测试，关闭时运行一次真实 SQL Server Tier 1；正常验证目标在 60 分钟内完成并保持 Failed: 0、Skipped: 0。

## Comments

- 2026-08-25：在 Ticket 23 的 `CutoverRunId`、数据库身份解析、墓碑 proof、同窗 gate、不可覆盖 JSON/Markdown 与 Windows Event 工具上完成一次性精确删除。破坏性入口重新消费原始 gate/旧新身份/墓碑 proof，并在临时授权后再次解析旧库与新库的 database id、create date、schema/contract、HistoryEpoch、解析目录、墓碑集合及旧库全局连接状态；`DROP DATABASE` 不使用 `ROLLBACK IMMEDIATE`，竞态连接使删除失败而不会被强制断开。
- 2026-08-25：临时 principal 固定绑定 RunId，创建后立即 `DISABLE` 并 `DENY CONNECT SQL`，只映射到精确旧库并获得 `CONTROL`；成功、删除失败和异常路径都关闭 impersonated session、按精确 principal 名同步清理最多三次并复核不存在。Host、Watch、reference consumer 及安装/卸载入口均无该调用或 `DROP DATABASE`。
- 2026-08-25：聚焦 cutover/发布包验证为 15 passed / 0 failed / 0 skipped。真实 SQL Server 16 / compatibility 160 的成功路径只删除 `MesIngest_Ticket01_fc5b7b2e07764dc7aeaaaaba3bb29532`，保留新库 `MesIngest_Ticket01_585d20da22b848149cbba6c4bcd52ff3`；故意由精确 DDL trigger 阻断的失败路径保留旧库 `MesIngest_Ticket01_9bbd49ab71b04886b0587819fff4ff42` 与新库 `MesIngest_Ticket01_77cbaa464bd14b92b757b26a7a9de04d`。两条路径的 `MesIngestCutover_<RunId>` principal 均为 `REVOKED_AND_PRINCIPAL_DROPPED` 且复核不存在。
- 2026-08-25：两轴 code review 在修复授权对象伪造、`CREATE LOGIN` 结果不明、授权后 TOCTOU、活动连接强制断开、事件字段/顺序和拒删矩阵后均为 Pass。最终 Tier 1 从 `mes/ingest/csharp` 使用本机默认非 LocalDB SQL Server 16 / compatibility 160 执行 `dotnet test MesIngest.Tests`：878 passed / 0 failed / 0 skipped，10m58s。Ticket 25 未改 Watch UI，未运行 Tier 2/3。完整证据见 `.scratch/mes-ingest-bounded-storage-low-memory/evidence/ticket25-delete-only-proven-old-database-2026-08-25.md`。
