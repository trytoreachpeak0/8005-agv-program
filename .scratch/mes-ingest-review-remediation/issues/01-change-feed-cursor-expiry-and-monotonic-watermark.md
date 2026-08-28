# 01 — Change-feed 游标过期返回 410，高水位保持单调

**What to build:** DemandChangeFeed 在保留裁剪后，过期或不可达游标必须返回 HTTP 410 `SYNC_CURSOR_EXPIRED` 并引导权威 Bootstrap；不得静默返回半段流。High watermark 在全部 feed 行被 purge 后仍保持单调，不得回落到 0。

**Blocked by:** None — can start immediately

**Status:** done

## Parent / References

- ADR: `docs/adr/mes/0009-demand-change-feed-and-authoritative-bootstrap.md`
- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（ChangeFeed 保留、410、Bootstrap）
- Issue: `.scratch/mes-ingest-watch-operations/issues/06-demand-change-feed-and-bootstrap.md`
- Handoff finding: Highest priority #1

不重新定义 ChangeFeed / Bootstrap 需求；本票只纠正实现与测试对上述契约的偏离。

## Repro

1. 写入若干 CREATED/GONE feed 行，记录当前 high watermark `H`。
2. 将保留窗口收紧（或直接裁剪）使最早可用 sequence `E` 升到 `> 1`；再分别用 `afterSequence` 为 `0`、`E-1`、以及介于已 purge 区间内的值拉取。
3. 继续裁剪直至 feed 表为空，再读 high watermark 与任意 `afterSequence < H` 的拉取。
4. 对 InMemory 与 SQL Server 两种 store 重复。

期望失败态（现状）：部分路径把 `afterSequence == 0` 特判成“从头读”，裁剪后返回半段流而非 410；全空时 watermark 回 0。现有测试曾祝福该行为，需一并纠正。

## Regression tests

- [x] 部分 purge：游标早于 earliest available → 410 `SYNC_CURSOR_EXPIRED`，body 含稳定错误码；不返回跳过缺口后的 items
- [x] 全部 purge：high watermark 仍 ≥ 裁剪前最后 sequence（单调）；过期游标仍 410，不因空表变成“空成功页 + watermark 0”
- [x] `afterSequence == 0` 与“从未消费”语义一致：若 0 已早于 earliest available，同样 410（不得特判绕过）
- [x] InMemory 与 SQL Server store 行为对齐；纠正后删除/改写原先祝福半流的用例
- [x] 合法游标（`afterSequence >= earliest - 1` 且在保留窗内）仍幂等分页，next/high watermark 契约不变

## Acceptance criteria

- [x] 过期游标一律 410 `SYNC_CURSOR_EXPIRED`，无静默半流
- [x] High watermark 在保留裁剪与空表场景下保持单调
- [x] 两种 store + API 契约测试覆盖部分/全部 purge
- [x] Release 下相关 ChangeFeed 测试全绿；不再依赖“半流也算成功”的断言

## Comments

- Implemented: removed `afterSequence > 0` special-case; empty-ledger watermark from InMemory `_nextSequence-1` / SQL `sys.identity_columns.last_value`; unified expiry via `contiguousFrom = earliest ?? highWatermark + 1`.
- `dotnet test mes/ingest/csharp/MesIngest.sln --configuration Release` → 282 passed.