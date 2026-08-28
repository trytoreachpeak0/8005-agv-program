# 24 — 已并入 Ticket 23

**What to build:** 本票不再单独实现；CutoverRunId、三轮投影、API、目录、数据库身份、失败退出和外部证据门禁已并入 Ticket 23，且合并后的实现仍然没有删库能力。

**Blocked by:** 23 — 播种并证明归档键墓碑.

**Status:** wontfix

- [x] 原有无删除切换门禁验收项已完整转移到 Ticket 23。
- [x] Ticket 25 的 blocker 已改为 Ticket 23，不需要执行或关闭本票后才能继续。

## Comments

- 2026-08-23：为共享一次 CutoverRun 与真实 SQL Server 测试，本票并入 Ticket 23；wontfix 只表示不再单独实施，不表示安全门禁被取消。
