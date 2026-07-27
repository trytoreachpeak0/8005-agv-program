# 02 — TransportDemand 出现、消失与再现生命周期

**What to build:** 完整出现/消失/再现路径可演示：仍在快照中则刷新最后见到时间并清零消失计数；仅完整成功轮累计缺席；失败或不完整轮不推进消失；达阈值后转 GONE；GONE 后再现发新 DemandId 并告警；HTTP 可按 VISIBLE/GONE 过滤。

**Blocked by:** 01 — 录制快照到只读 API 的最小纵切片

**Status:** ready-for-agent

- [ ] 仍存在的 VISIBLE 在成功全量快照中刷新 mes_last_seen_at 并将消失计数归零
- [ ] 仅完整成功查询累计消失次数；超时、失败或不完整结果不累计、不标 GONE
- [ ] 连续成功缺席达到可配置阈值（默认 2）后状态变为 GONE
- [ ] 一期 GONE 不依赖装载/派车保护规则
- [ ] 同键在 GONE 后再现时发放新 DemandId 并产生告警，不复活旧实例
- [ ] 只读 HTTP 可按 status（VISIBLE/GONE）过滤需求列表
- [ ] Reconciler 与 HTTP 测试覆盖成功缺席、失败不计数、GONE、再现新 DemandId
