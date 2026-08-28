# 车载端清空全部目标仓位后服务端才完成取消

同事初稿 §2.3 将实时 IO、逐仓门序列和安全互锁归车载端，§23 的通用 OperationCancelCommand 又无法表达“必须先取出全部产品”的现场规则。装货取消采用“服务端授权开始、车载端完成物理清空、服务端终结业务任务”的交互。

车载界面将操作显示为“清空并取消”。已核验操作员确认后，车载端发送 `LoadCancellationStartRequested`，至少包含 demandId。服务端根据当前权威业务状态返回 LoadCancellationAuthorization：

- `AUTHORIZED`：携带 demandId、可空的 slotOperationAttemptId 和该任务的完整目标仓位范围；服务端进入 LoadCancelPending。
- `REJECTED`：携带稳定 reasonCode 和可展示 message；车载端不开始新的开仓动作。同车另一 SUBLOT 正处于物理仓位操作时使用稳定的忙碌原因码，待其到达稳定边界后由操作员重新发起。

本 ADR 只适用于正常离站前清空并取消。LoadBatch 因锁 DI 等关键硬件故障处于 VehicleRecoveryRequired 时，普通操作员不能用本流程绕过生产决策权限；服务端必须拒绝普通 LoadCancellationStartRequested，先按 ADR-cross-0039 取得 R-09 或等效生产管理权限作出的 LoadCompensationDecision，再进入专用补偿恢复。

获得 AUTHORIZED 后，物理清空状态机归车载端：

- 根据原 SlotOperationAttemptId 的 OnboardExecutionJournal 与当前 SlotOccupancyState 核对完整目标仓位。
- 当前装货仓门已经打开的，允许操作员直接取出或不再放入花篮，并以 `EMPTY + 锁闭 + 开锁输出已复位` 完成本仓取消清空；不要求先完成 OCCUPIED 装货再重新开门。
- 已经 EMPTY 的仓位不打开。
- OCCUPIED 的仓位形成 BatchUnlock 集合并一次性打开，引导用户全部取出；同模块多线圈写和跨模块分组语义遵守 ADR-cross-0035。
- UNKNOWN、授权范围与执行日志不一致或机构故障时暂停并进入恢复，不猜测完成。
- 最终必须确认所有目标仓位 EMPTY、由锁传感器确认仓门锁闭、开锁输出回读确认为复位且安全状态有效。

授权范围严格限定为所选 DemandId 的完整目标仓位。车辆上其它 SUBLOT 的仓位即使为 OCCUPIED 也不得加入本次 BatchUnlock，不得更改其 SlotBusinessState、任务状态、确认记录或预留。

全部满足后，车载端发送可靠 `LoadCancellationResult(status=ALL_EMPTY)`，携带逐仓结果和 safetyStateVersion。服务端达到 DurableAcceptance 后才把 DemandId 终结为 `CANCELLED_BY_OPERATOR`，随后下发更高 revision 的 CurrentStopWorklistSnapshot。车载端在新快照到达前显示“取消完成，等待作业清单更新”，不得本地删除任务。

只有包含取消终态与已释放仓位的新版 CurrentStopWorklistSnapshot 到达后，车载端才允许以这些仓位开始新的 SUBLOT；本地观察到 EMPTY 或服务端仅 ACK 结果都不足以提前复用。

没有 SlotOperationCommand、slotOperationAttemptId 或目标仓位的待办任务，也走同一流程：服务端返回 AUTHORIZED 与空范围，车载端立即报告 ALL_EMPTY，不另设 DIRECT_CANCEL 分支。

**Status**: accepted

**Considered Options**:
- 服务端判断 DIRECT_CANCEL 或 CLEAR_REQUIRED 并逐仓下发清空命令（拒绝：服务端不拥有实时物理占用事实，交互分支也重复）
- 车载端不经服务端授权直接开仓清空并取消（拒绝：业务任务状态和取消资格归服务端）
- 服务端授权取消范围，车载端自主完成清空，服务端依据 ALL_EMPTY 结果终结任务（采纳）

**Consequences**:
- 协议不再需要 DIRECT_CANCEL、CLEAR_REQUIRED 或 LoadCancellationCommand。
- LoadCancellationStartRequested 属于请求—响应消息；LoadCancellationResult 属于可靠业务结果。
- AUTHORIZED 是开始物理清空的授权，不表示业务已经取消。
- 当前开锁仓位只有在 AUTHORIZED 到达后才能从装货切换为取消清空；请求被拒绝、等待授权或断联时不得自行改变原操作语义。
- 取消清空批量开锁，但逐仓形成 EMPTY、锁闭与输出复位证据；任何一仓未完成都保持 LoadCancelPending。
- 同车可以保留其它已装 SUBLOT；完成判定只要求本次授权范围全部清空，不要求整车 EMPTY。
- 服务端只在同车没有其它活动物理仓位操作时授权；不同 SUBLOT 的开锁集合不得并存。
- 取消期间断线时按 ADR-cross-0003 进入断联仓位操作收敛；只执行当前开锁集合安全收尾。重连后须重新对账并由服务端授权续行。
- 后续接口确认稿应以本流程替换 §23，并明确“清空并取消”的车载界面文案。
