# 11 — Watch 延迟 `.log` 纳入保留，写盘失败不拖垮刷新

**What to build:** Watch 延迟遥测的 `.log` 须纳入与 `.jsonl` 同等的保留/体积策略；遥测同步写盘失败不得把一次已成功的 HTTP refresh 变成 UI 失败。

**Blocked by:** None — can start immediately

**Status:** ready-for-human

## Parent / References

- Issue: `.scratch/mes-ingest-watch-operations/issues/03-end-to-end-latency-telemetry.md`
- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（Watch local event / log retention）
- Handoff finding: unbounded `.log`；sync write can fail UI on disk errors

不重新定义分阶段耗时字段；本票补齐保留与故障隔离。

## Repro

1. 长时间运行 Watch，观察延迟 `.log` 是否只增不减、是否脱离既有保留清理。
2. 将日志目录置为只读或模拟写失败，触发一次本来会成功的 refresh。

期望失败态（现状）：`.log` 不在 `.jsonl` 保留逻辑内；写盘异常可表面成刷新失败。

## Regression tests

- [ ] 保留任务同时约束 `.log` 与 `.jsonl`（按天/体积策略与 ticket 03 / spec 一致）
- [ ] 遥测写失败：HTTP 成功时 UI 仍展示数据；失败记入本地事件/诊断，不丢主路径
- [ ] 不记录 SharedSecret 或完整连接串（既有红线）

## Acceptance criteria

- [ ] `.log` 有界保留，不再无限增长
- [ ] 遥测 IO 错误不掩盖成功的 Host 拉取
- [ ] 保留与故障隔离有自动化或可重复手工验收步骤
