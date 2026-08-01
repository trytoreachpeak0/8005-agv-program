# 06 — 默认 InMemory store 并发读写安全

**What to build:** 非 SQL 的默认 Host 在后台 poll 写投影与 API 读并发时，不得暴露半状态或因集合枚举失败而 500；InMemory 适配器对状态、alerts、change feed 的更新边界与读者所见一致。

**Blocked by:** None — can start immediately

**Status:** ready-for-human

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

- [x] 并发读者 + 单写者（模拟 poll）压力测试：固定轮次内无未处理异常，响应形态始终为合法 envelope
- [x] 单次写替换/事务边界对读者原子：不得读到“有 Demand 无对应 feed”或半截 alert 列表（按当前契约可观察的不变量）
- [x] 既有功能测试在加锁/不可变快照方案下仍绿

## Acceptance criteria

- [x] 默认 InMemory Host 在并发 API 读 + 后台 poll 下稳定
- [x] 不改变 SQL store 语义；不引入虚假写 API
- [x] 自动化并发回归可重复失败（修前）/通过（修后）

## Comments

- 2026-08-01 Phase 1 feedback loop (red, no prod fix yet):
  - Test file: `mes/ingest/csharp/MesIngest.Tests/InMemoryTransportDemandStoreConcurrencyTests.cs`
  - Repro command:
    ```
    dotnet test mes/ingest/csharp/MesIngest.Tests/MesIngest.Tests.csproj --filter "FullyQualifiedName~InMemoryTransportDemandStoreConcurrencyTests"
    ```
  - Observed (5/5 suite runs before trimming demand-page case; then 2/2 red after):
    - `Concurrent_alert_readers_and_replace_writer_do_not_throw` → `NullReferenceException` in `AlertListPaging.Order` (`AlertListQuery.cs:346`) while writer `ReplaceState` mutates `_alerts` via `Clear`/`AddRange`.
    - `Concurrent_change_feed_readers_and_replace_writer_do_not_throw` → `InvalidOperationException: Collection was modified` at `QueryChangeFeed` (`StoreAndRunner.cs:194`) and/or `NullReferenceException` / `IndexOutOfRangeException` in `PurgeChangeFeed` (`StoreAndRunner.cs:231`) while writer appends/purges `_changeFeed`.
  - Note: concurrent demand `QueryPage`/`List`/`GetState` against `_state` reference swap did **not** throw in the same stress window (not used as the red loop). Atomic half-state invariants (demand vs feed vs alerts) still open for a later regression once enumeration crashes are fixed.

- 2026-08-01 Implemented: `InMemoryTransportDemandStore` mirrors SQL `_gate` locking on all public read/write paths so `ReplaceState` publishes projection + change feed + alerts as one boundary; `QueryAlerts` pages a list snapshot. Regression nails kept in `InMemoryTransportDemandStoreConcurrencyTests` (throw stress + write-boundary). `dotnet test mes/ingest/csharp/MesIngest.sln --configuration Release` → 329 passed.
