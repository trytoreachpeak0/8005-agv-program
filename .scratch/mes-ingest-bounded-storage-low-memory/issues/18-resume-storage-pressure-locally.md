# 18 — 已并入 Ticket 17

**What to build:** 本票不再单独实现；MesIngestLocalAdministration 的 StoragePressurePause 恢复、授权、审计和失败行为已并入 Ticket 17 的完整状态机。

**Blocked by:** 17 — 实施 StoragePressurePause.

**Status:** wontfix

- [x] 原有本地恢复验收项已完整转移到 Ticket 17。
- [x] Ticket 19 的 blocker 已改为 Ticket 17，不需要执行或关闭本票后才能继续。

## Comments

- 2026-08-23：为一次实现和测试完整暂停/恢复状态机，本票并入 Ticket 17；wontfix 只表示不再单独实施，不表示功能被取消。
