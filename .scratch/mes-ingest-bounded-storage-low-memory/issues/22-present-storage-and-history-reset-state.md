# 22 — 已并入 Ticket 21

**What to build:** 本票不再单独实现；StoragePressurePause、HistoryEpoch、最早历史与 HistoryResetAcknowledgement 的 Watch 呈现已并入 Ticket 21，并共享一次 Tier 2 与视觉批准。

**Blocked by:** 21 — 调整 Watch 当前页刷新节奏.

**Status:** wontfix

- [x] 原有状态呈现、无写按钮、ScriptedFakeHost、Fluent 与 Golden Renderer 验收项已完整转移到 Ticket 21。
- [x] Ticket 23 的 blocker 已改为 Ticket 21，不需要执行或关闭本票后才能继续。

## Comments

- 2026-08-23：为只运行一次 Tier 2 和一次视觉批准，本票并入 Ticket 21；wontfix 只表示不再单独实施，不表示功能被取消。
