# 当前停靠作业清单使用带版本的完整快照

同事初稿 §2.2 将站点任务归服务端，§5.1 只描述单次 SUBLOT 输入，§10 没有车载端展示当前停靠全部装卸作业的消息。车载端不拥有任务事实，但必须知道当前到达站点有哪些待装、待卸和复合作业；服务端以完整 CurrentStopWorklistSnapshot 下发，不采用逐条新增、修改和删除事件。

snapshot payload 至少包含：

- `stationId`
- `worklistRevision`
- `items`

其中 items 每项按 ADR-cross-0047 至少包含 `demandId`、`sublot`、`operationType`、`expectedBasketCount`、`completedBasketCount`、`remainingBasketCount`、起终点、`status`、`availableActions` 和 `slotNumbers`。`operationType` 区分装货与卸货；复合停靠可以同时存在两类项目。空作业清单也必须以 `items=[]` 的完整快照表达，不能靠消息缺失推断。

CurrentStopWorklist 只包含本次停靠计划中的待装任务，以及车上目标为当前站点的待卸任务；不得把所有“任务类型允许在本站处理”的全局任务铺入清单。操作员输入一个未预先列出的 SUBLOT 时，服务端仍可按 StationTaskTypeAdmission 校验；服务端接受并纳入本次停靠后，才通过更高版本快照把该任务加入清单。

服务端在车辆到站、作业清单变化、任务取消完成、临时 SUBLOT 获准纳入以及 RecoveryHandshake 后生成并可靠发送最新快照。worklistRevision 针对当前 AGV 与站点单调递增并由服务端持久化。车载端只接受更高 revision 并原子替换整个显示列表；相同 revision 幂等 ACK，更低 revision 丢弃并返回当前已采用版本。

CurrentStopWorklistSnapshot 属于 ADR-cross-0032 的可替换状态快照：服务端只需保留和重发最新未确认版本，不必补发中间每一次列表变化。断线或车载重启后可以保留最后快照供操作员查看，但必须醒目标记为过期，只读显示且不得据此开始、取消或扩展新的业务；活动仓位操作另按 OnboardExecutionJournal 和断联安全规则展示及收敛。恢复对账完成并取得当前完整快照前不得解除过期标记。

取消等请求只提交 DemandId，并可附带操作员所见 worklistRevision 用于诊断；服务端必须根据当前权威状态重新检查 availableActions，不能信任旧界面的可操作标记。

**Status**: accepted

**Considered Options**:
- 下发作业增删事件并由车载端长期合并（拒绝：事件漏报会形成幽灵任务或漏显示任务）
- 每次刷新发送无版本的完整列表（拒绝：乱序响应可能让旧列表覆盖新列表）
- 使用带单调 revision 的完整快照，车载端整体替换（采纳）

**Consequences**:
- 初稿 §10 需要新增 CurrentStopWorklistSnapshot 及其 ACK。
- 服务端是作业纳入、排序、状态和 availableActions 的唯一计算方；车载端不得修改列表项。
- 当前站点变化后，旧 stationId 的快照即使 revision 更高也不能覆盖新站点界面。
- 取消、任务完成或新增任务会产生新 revision；车载界面不做乐观本地删除。
- 任务数较小，完整快照的数据开销可忽略，换取更简单可靠的恢复行为。
- 车载端“知道并展示任务”不等于拥有任务生命周期或调度裁决权。
