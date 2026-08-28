# 车载端展示后续停靠计划与四维车辆概览

车载端不仅需要知道当前停靠有哪些作业，还必须让现场操作员知道车辆接下来去哪些业务站点以及车辆当前处于什么状态。服务端拥有任务、调度和后续停靠计划事实；车载端以只读 UpcomingStopPlan 展示后续业务停靠，以 OnboardVehicleOverview 组合展示运行、通信与业务就绪、当前作业、安全与联锁四个互不覆盖的维度。RIoT 地图路径节点、转弯点和避障路径不属于 UpcomingStopPlan。

UpcomingStopPlan 由服务端通过完整 UpcomingStopPlanSnapshot 下发。snapshot 至少包含 `planRevision`、生成时间和按顺序排列的 PlannedStop；每个 PlannedStop 至少包含站点、顺序、停靠目的、关联任务数量与可展开的任务摘要、计划状态，并只在服务端取得可信数据时包含 ETA。服务端可以增删或重排尚未执行的停靠，车载端只接受更高版本并整体替换，不得本地编辑、锁定或根据旧任务推导路线。

断线时车载端保留最后一份 CurrentStopWorklistSnapshot 和 UpcomingStopPlanSnapshot 供查看，但必须醒目标记“离线数据，可能已过期”。过期投影不得用于开始、取消或扩展新的业务；已经开始的仓位操作只按断联安全规则收敛。OnboardVehicleOverview 中的安全与联锁维度不依赖这些旧投影，始终以车载实时 IO 事实为准，并在不安全时置顶显示“禁止移动”及受影响仓位和原因。

作业完成、开始行驶和到站是三个不同事件。操作员确认本站作业完成后，当前站仍显示“作业已完成，等待发车”；RIoT 确认车辆开始移动后显示“正在前往”下一计划停靠；只有可信到站确认后，才把该 PlannedStop 切换为当前站并启用新的 CurrentStopWorklist。

**Status**: accepted

**Considered Options**:
- 车载端只显示当前仓位操作，不显示业务任务、车辆状态或后续站点（拒绝：现场无法理解当前工作和车辆去向）
- 将全部信息压成一个车辆状态枚举并展示 RIoT 底层路线（拒绝：不同权威来源相互覆盖，且向现场暴露无用的导航细节）
- 展示当前作业、后续业务停靠和四维车辆概览，各自保留权威边界（采纳）

**Consequences**:
- 初稿中“车载端不理解任务”统一改为“车载端不拥有任务事实，但接收并展示服务端权威投影”。
- UpcomingStopPlanSnapshot 属于 ADR-cross-0032 的可替换状态快照，服务端可靠发送最新版本，车载端原子应用。
- CurrentStopWorklist 与 UpcomingStopPlan 必须在到站、任务变化、计划调整、离线和恢复场景下保持明确的新鲜度状态。
- OnboardVehicleOverview 不是单一状态机，也不要求所有维度来自同一数据源。
