# 装货补偿后重试使用新的仓位操作尝试编号（已废止）

同事初稿 §20 规定相同 SlotOperationAttemptId 和相同内容只能返回已有状态或结果，内容不同则拒绝；§21 规定断线重连后补报原结果。SlotOperationAttemptId 因此标识一次物理操作尝试，而不是长期标识任务或子批号。

本 ADR 原决定在车辆硬件故障完成 LoadCompensationRecovery 后保留原 DemandId，并在健康车辆上创建新的 SlotOperationAttemptId 重试。该决定现已废止：现场整批取出通常意味着产品由人工送达或转入异常处理，因此不论 LoadCompensationReasonCode 为何，补偿安全完成后都终结原搬运需求，不再为同一 DemandId 创建补偿后重试尝试。

ACK 超时重发、断线补报、暂停后继续以及未结操作恢复仍属于同一次尝试，必须使用原 SlotOperationAttemptId。车载端收到已经处于终态的旧 SlotOperationAttemptId 时，内容相同则返回已保存的终态结果，不重新开仓；内容不同则按初稿 §20 返回内容冲突。卸货中途失败仍沿用原 SlotOperationAttemptId 继续到全部取空。

**Status**: superseded by ADR-cross-0039

**Considered Options**:
- 同一任务永远使用同一 SlotOperationAttemptId（拒绝：无法区分通信重发与补偿后的真正重新执行）
- 每次网络重发都使用新 SlotOperationAttemptId（拒绝：会绕过去重并造成重复开仓）
- 车辆硬件故障补偿后保留原需求并在健康车辆上创建新尝试（原采纳，现废止）
- 所有 LoadCompensationRecovery 完成后统一终结原搬运需求（现由 ADR-cross-0039 采纳）

**Consequences**:
- 车载端去重记录不能在补偿完成后立即删除，否则迟到的旧消息可能被误当作新操作。
- LoadCompensationRecovery 不再产生 `retryOfSlotOperationAttemptId`；对应 TransportDemandKey 被调度永久抑制。MES 在人工扫码过站前继续返回同一候选时，MesIngest 仍照常投影，但调度不得创建补偿后重试任务。
