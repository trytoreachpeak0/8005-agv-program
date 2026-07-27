# 04 — 按任务类型的零骤降保护

**What to build:** 某 TASK_TYPE 在上一轮健康非零数量达到阈值后本轮成功变为 0 时进入 PAUSED_ZERO_DROP，仅暂停该类型的消失计数与 GONE；其它类型照常对账；连续两轮成功非零后自动解除，无人工解除入口；API/健康可看出暂停态。

**Blocked by:** 02 — TransportDemand 出现、消失与再现生命周期

**Status:** ready-for-agent

- [ ] 当某类型上一轮成功非零数量 ≥ 可配置阈值（默认 10）且本轮成功计数为 0 时进入 PAUSED_ZERO_DROP
- [ ] 暂停期间该类型不累计消失、不标 GONE；其它 TASK_TYPE 不受影响
- [ ] 该类型连续 2 轮完整成功且计数 > 0 时自动解除暂停
- [ ] 不提供人工解除 PAUSED_ZERO_DROP 的入口
- [ ] 只读 API/健康资源能反映各类型暂停状态
- [ ] Reconciler 测试覆盖进入、隔离影响、自动解除
