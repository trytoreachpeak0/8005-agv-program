# 08 — 完成 IngestAlert 到 TransportDemand 的精确定位

**What to build:** 让操作员从 IngestAlert 的上下文准确进入相关 TransportDemand，而不把业务键、旧实例和当前实例混为一谈，尤其能分别检查 REAPPEAR_AFTER_GONE 的先前 GONE 与当前再现实例。

**Blocked by:** 05 — 完成独立 GONE TransportDemand 浏览; 06 — 完成 TransportDemand 详情、选择与复制; 07 — 完成 IngestAlert 浏览与非模态详情

**Status:** ready-for-agent

- [ ] 告警有 DemandId 时先执行精确 Demand 读取，再进入返回实例的实际 status 标签，以 DemandId 提交第 1 页查询并选中目标。
- [ ] REAPPEAR_AFTER_GONE details 同时含旧/新 DemandId 时，分别标注“先前 GONE”“当前再现”，并为两者提供独立复制和精确查看操作。
- [ ] 只有 TASK_TYPE + SUBLOT 时提供用户明确触发的“按业务键查任务”，进入 VISIBLE 并提交组合筛选，但不得宣称定位到唯一历史实例。
- [ ] 没有任何 Demand 关联信息时不显示不可用操作；精确读取或后续查询失败时保留原页面状态并显示具体失败，不伪造选中结果。
- [ ] Alert → Demand 导航成功后目标标签、已提交查询、页码、选中行和详情一致；导航导致的旧页面取消不额外记为连接故障。
