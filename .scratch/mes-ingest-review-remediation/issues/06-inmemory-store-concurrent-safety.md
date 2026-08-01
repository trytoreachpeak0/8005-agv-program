# 06 — 默认 InMemory store 并发读写安全

**What to build:** 非 SQL 的默认 Host 在后台 poll 写投影与 API 读并发时，不得暴露半状态或因集合枚举失败而 500；InMemory 适配器对状态、alerts、change feed 的更新边界与读者所见一致。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

## Parent / References

- ADR: `docs/adr/mes/0006-mes-ingest-vs-dispatch.md`（Ingest Host 本地投影职责）
- Issue: `.scratch/mes-ingest-phase-1/issues/07-windows-service-single-flight-poll.md`（单飞 poll；不消除读写并发）
- Spec: phase-1 / watch-ops 只读 API 在 Host 进程内可用
- Handoff finding: Other confirmed — InMemory unsynchronized mutation

不把 SQL 持久化改成唯一模式；本票只让默认 InMemory 在并发下满足既有读模型契约。

## Repro

1. 以 InMemory store 启动 Host，缩短 poll 间隔。
2. 并行持续打 `/api/demands`、`/api/alerts`、`/api/demand-changes`（多连接）。
3. 观察间歇性异常、空/半页、或枚举修改异常。

期望失败态（现状）：无同步更新 `_state` / `_alerts` / `_changeFeed`，读写可竞态。

## Regression tests

- [ ] 并发读者 + 单写者（模拟 poll）压力测试：固定轮次内无未处理异常，响应形态始终为合法 envelope
- [ ] 单次写替换/事务边界对读者原子：不得读到“有 Demand 无对应 feed”或半截 alert 列表（按当前契约可观察的不变量）
- [ ] 既有功能测试在加锁/不可变快照方案下仍绿

## Acceptance criteria

- [ ] 默认 InMemory Host 在并发 API 读 + 后台 poll 下稳定
- [ ] 不改变 SQL store 语义；不引入虚假写 API
- [ ] 自动化并发回归可重复失败（修前）/通过（修后）
