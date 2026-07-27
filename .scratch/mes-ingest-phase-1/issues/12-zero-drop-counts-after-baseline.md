# 12 — 零骤降计数须按上线基线过滤

**What to build:** `PAUSED_ZERO_DROP` 的 `countsByType` 与创建分支使用同一套上线基线过滤：只统计 `Dates >= goLiveBaseline` 的行。避免投影为空时漏进暂停，以及基线前键仍抬升 DUPLICATE / 健康基线。

**Blocked by:** None — can start immediately（04 已完成；本票为 review Spec C1 跟进）

**Status:** done

- [x] `TransportDemandReconciler` 中 `countsByType` 仅统计通过 `goLiveBaseline` 的行（与 create 分支 `row.Dates < goLiveBaseline` 过滤一致）
- [x] 快照内全部行均早于基线时，该类型计数为 0（相对投影为空），不会因 raw `snapshot.Rows` 非零而漏进 / 误维持零骤降语义
- [x] 仅基线前键重复时，不因未过滤的 raw 计数抬升 `LastHealthyNonZeroCount` 或触发与投影无关的零骤降进入
- [x] Reconciler 测试覆盖：基线前多行 vs 基线后空 / 非空，进入与不进入 `PAUSED_ZERO_DROP` 的对照

## Comments

- 2026-07-27: From `/code-review ffe1f49` Spec C1 (medium). Evidence: `TransportDemandReconciler.cs` ~44–46 builds `countsByType` from raw `snapshot.Rows`; create path ~142–145 skips `row.Dates < goLiveBaseline`. Spec stories 17–20 / ticket 04. Prefer `/implement` first among 12–16.
- 2026-07-27: Implemented. `countsByType` filters `Dates >= goLiveBaseline`; three reconciler contrast tests. Note: `DUPLICATE_RECONCILE_KEY` still uses raw rows (create already skips pre-baseline); acceptance targeted healthy-count / pause enter, not duplicate alert suppression.
