# 02 — 重启屏障后零骤降健康计数排除无效行

**What to build:** 重启后首轮屏障记录的每类型健康基线，以及随后用于 `PAUSED_ZERO_DROP` 的比较，只统计通过 GoLiveBaseline 且会进入投影的有效行；不得把基线前行或重复键行计入“健康非零”，以免下一轮空快照误进暂停。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

## Parent / References

- Spec: `.scratch/mes-ingest-phase-1/spec.md`（stories 17–20；restart barrier；go-live baseline）
- Issues:
  - `.scratch/mes-ingest-phase-1/issues/04-paused-zero-drop.md`
  - `.scratch/mes-ingest-phase-1/issues/06-restart-recovery-barrier.md`
  - `.scratch/mes-ingest-phase-1/issues/12-zero-drop-counts-after-baseline.md`
- Handoff finding: Highest priority #2

不重新定义零骤降或重启屏障规则；本票对齐 runner 记录基线与 reconciler 计数过滤。

## Repro

1. 配置 GoLiveBaseline，使快照含大量 `Dates < baseline` 行和/或触发 DUPLICATE 的重复键行，但通过基线的有效 VISIBLE 为 0 或远低于阈值。
2. 重启 Host，完成屏障首轮成功 poll（runner 记录基线计数）。
3. 下一轮完整成功但该 TASK_TYPE 有效行为空（或仅剩会被过滤的行）。

期望失败态（现状）：runner 用 raw 快照计数抬高 `LastHealthyNonZeroCount`，随后空轮误判进入 `PAUSED_ZERO_DROP`。

## Regression tests

- [ ] 屏障轮：仅基线前行 / 仅重复键 → 记录的健康计数为 0（或不抬升持久健康基线），不满足进入阈值
- [ ] 屏障轮后下一空轮：不得仅因 raw 历史计数进入 `PAUSED_ZERO_DROP`
- [ ] 对照：基线后有效行 ≥ 阈值，再变 0 → 仍按既有规则进入暂停
- [ ] 与 ticket 12 的 `countsByType` 过滤语义一致（同一套 GoLiveBaseline 规则）

## Acceptance criteria

- [ ] 重启屏障采用的健康计数与 reconciler 零骤降计数使用同一有效行过滤
- [ ] 不会因基线前或重复键 raw 行虚假进入 `PAUSED_ZERO_DROP`
- [ ] Reconciler/runner 回归测试覆盖上述对照；既有暂停进入/解除用例仍绿
