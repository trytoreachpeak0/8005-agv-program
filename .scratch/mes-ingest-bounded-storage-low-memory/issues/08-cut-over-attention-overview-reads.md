# 08 — 已并入 Ticket 07

**What to build:** 本票不再单独实现；CurrentIngestAttention 与 WatchOverview 的全部行为和验收项已并入 Ticket 07，以共享一次实现上下文、真实 SQL Server Tier 1 和代码审查。

**Blocked by:** 07 — 切换外部 Demand 目录热读取.

**Status:** wontfix

- [x] 原有 CurrentIngestAttention 与 WatchOverview 验收项已完整转移到 Ticket 07。
- [x] Ticket 09 的 blocker 已改为 Ticket 07，不需要执行或关闭本票后才能继续。

## Comments

- 2026-08-23：为减少重复上下文、Tier 1 和审查，本票并入 Ticket 07；wontfix 只表示不再单独实施，不表示功能被取消。
