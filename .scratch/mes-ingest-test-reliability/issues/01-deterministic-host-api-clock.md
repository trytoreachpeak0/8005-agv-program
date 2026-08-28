# 01 — Host API 使用可控时钟保证时间契约测试确定性

**What to build:** 让 MesIngest Host 的 Demand 有界读取与 DemandChangeFeed 保留判断在生产环境继续使用真实 UTC，同时允许测试固定同一个“当前时间”，使 GONE 最近 24 小时与 ChangeFeed 保留期的行为可重复验证，不再随日历推进失效。

**Blocked by:** None — can start immediately

**Status:** done

- [x] 生产运行默认使用系统 UTC，不改变 GONE 默认最近 24 小时、所有 VISIBLE 永远可见以及 ChangeFeed 默认保留 48 小时的既有契约。
- [x] Host 的 Demand 查询与 DemandChangeFeed 查询共享一个可替换的当前时间来源，测试可以固定或推进该时间。
- [x] Demand 状态筛选、Demand 关联 Alert、权威 Bootstrap 三个场景使用确定性时间后稳定通过，不依赖执行当天日期。
- [x] ChangeFeed 保留与游标过期相关 API 测试不会因固定夹具跨过真实日历 48 小时边界而产生新的失败。
- [ ] MesIngest Release 完整测试套件通过，且保留独立覆盖 GONE 默认 24 小时窗口的契约测试。

## Comments

- Implemented a Host-wide `TimeProvider`: production uses `TimeProvider.System`; tests replace it with an adjustable UTC provider. Demand queries, DemandChangeFeed queries, the ingest runner, and both stores now observe the same clock.
- Deterministic HTTP contract tests: 27 passed, including GONE status filtering, Demand-related Alerts, authoritative Bootstrap, retention, cursor expiry, and the standalone default 24-hour GONE window.
- Release suite outside the sandbox: 426 passed, 1 failed. The sole failure is the pre-existing CRLF/LF OpenAPI comparison tracked independently by ticket 02; no ticket-01 time-contract tests failed.
