# 14 — 已并入 Ticket 13

**What to build:** 本票不再单独实现；RetentionEligibleDemandSeries 资格、EligibilityAt、取消与重新计时已经并入 Ticket 13 的统一历史保留状态模型。

**Blocked by:** 13 — 实施 RawObservation 15 天过期契约.

**Status:** wontfix

- [x] 原有 RetentionEligibleDemandSeries 验收项已完整转移到 Ticket 13。
- [x] Ticket 15 的 blocker 已改为 Ticket 13，不需要执行或关闭本票后才能继续。

## Comments

- 2026-08-23：为共享时间、schema 与保留边界实现，本票并入 Ticket 13；wontfix 只表示不再单独实施，不表示功能被取消。
