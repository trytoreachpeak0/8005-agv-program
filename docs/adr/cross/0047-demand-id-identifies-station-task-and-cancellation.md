# DemandId 标识站点任务，TransportDemandKey 负责取消抑制

同事初稿 §2.2 将站点任务归服务端，§5.1 使用 SUBLOT 进入装货流程。DemandId 是 MesIngest 分配的本地 TransportDemand 实例标识，不是 MES 的需求编号；CurrentStopWorklist 和取消请求继续使用 DemandId 精确选择当前实例，不再新增 stationTaskId。取消一旦完成，服务端还必须永久抑制该实例对应的 TransportDemandKey（任务类型 + SUBLOT），因为旁系统不回写 MES，同一候选会持续出现直到现场人工搬运并扫码过站；MesIngest 即使为跨 GONE 再现分配了新 DemandId，调度也不能借新实例绕过抑制。

CurrentStopWorklistSnapshot 的每一项至少包含：

- `demandId`
- `sublot`
- `operationType`
- `expectedBasketCount`
- `completedBasketCount`
- `remainingBasketCount`
- `status`
- `availableActions`
- `slotNumbers`

操作员取消的是 DemandId 对应的当前任务实例。服务端以 DemandId 持久化 `CANCELLED_BY_OPERATOR`，并以 TransportDemandKey 持久化无解除入口的抑制记录；MesIngest 继续照常投影和告警，调度命中同键抑制时不得创建或恢复业务任务、不得派车。

SUBLOT 继续用于操作员输入、业务查询和 SublotReservation，不能单独作为抑制键；否则会把该子批号在其它工序产生的不同任务类型一并拉黑。相同 SUBLOT 以后命中其它任务类型时属于新的 TransportDemandKey，可以正常接入。

LoadCompensationRecovery 使用 `CANCELLED_BY_LOAD_COMPENSATION`，普通 LoadTaskCancellation 使用 `CANCELLED_BY_OPERATOR`；两者都终结原 DemandId 并永久抑制对应 TransportDemandKey。取消状态解释原因，业务键决定调度是否接受后续 MesIngest 投影，不改变 MES 轮询与接入对账。

**Status**: accepted

**Considered Options**:
- 新建 stationTaskId（拒绝：与现有 DemandId 重复，增加无意义映射）
- 只抑制 DemandId（拒绝：MES 在人工扫码前仍持续返回同一业务候选，可能被分配新本地 ID 并再次派车）
- 直接按 SUBLOT 永久抑制（拒绝：会误伤该 SUBLOT 在其它工序命中的不同任务类型）
- DemandId 精确选择并审计当前实例，TransportDemandKey 在调度侧永久抑制同键业务任务（采纳）

**Consequences**:
- 车载界面详情、协议、服务端状态机和审计统一使用 demandId，不出现 stationTaskId；主列表可以优先显示 SUBLOT 与作业摘要。
- LoadBatch、SlotOperationAttemptId 和 DemandId 是不同层级：DemandId 标识业务需求，SlotOperationAttemptId 标识一次物理操作尝试。
- DemandId 取消终态与 TransportDemandKey 抑制记录都须跨断线、重启和轮询持久有效。
- MesIngest 不读取永久抑制；调度命中永久抑制键的投影时不得创建或恢复业务任务。同一 SUBLOT 的其它任务类型不受影响。
- 后续接口确认稿应在 §5、§10 和任务列表消息中增加 demandId。
