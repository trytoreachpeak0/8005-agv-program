# 06 — 重启恢复与首轮安全屏障

**What to build:** 服务重启后恢复消失计数与每类型零骤降相关状态；重启后第一次完整成功查询可创建/刷新 VISIBLE，但不累计消失、不标 GONE；从第二次完整成功查询起恢复正常对账与零骤降规则（含已暂停类型的恢复/保持语义）。

**Blocked by:** 04 — 按任务类型的零骤降保护; 05 — SQL Server 持久投影

**Status:** done

- [x] 每个需求的连续消失计数跨重启持久恢复，不因启动清零
- [x] 每类型最后健康非零数量、恢复 streak、PAUSED_ZERO_DROP 状态跨重启持久恢复
- [x] 重启后第一次完整成功查询：可新建 VISIBLE、刷新仍存在键的 seen；不增加消失计数、不执行 GONE
- [x] 第一次查询某类型计数为 0 时，不得覆盖重启前持久化的最后健康非零数量
- [x] 从第二次完整成功查询起按正常规则累计消失、GONE 与零骤降进入/解除
- [x] 若重启前已处于 PAUSED_ZERO_DROP，按业务恢复规则在重启后前两轮非零时自动解除（或保持直至满足条件）
- [x] Reconciler/集成测试覆盖首轮屏障与第二轮恢复

## Comments

- 2026-07-27: Implemented restart recovery barrier on `TransportDemandReconciler` via `RestartRecovery` (BarrierRound / PostBarrierRound / Normal). `IngestRoundRunner` tracks successful rounds since process start (failed/incomplete do not consume the barrier) and records barrier-round per-type counts for post-barrier zero-drop baseline adoption. Persist disappear/pause across restarts remains store responsibility (ticket 05).