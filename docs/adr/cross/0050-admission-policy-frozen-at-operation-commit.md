# 任务类型准入规则在操作承诺点冻结

同事初稿 §14 要求车载指令执行前完成校验，服务端又允许维护 ADR-cross-0049 的 StationTaskTypeAdmission。准入配置可能在 SUBLOT 提交与仓位操作执行之间变化，因此必须定义稳定生效边界。

服务端收到 SublotSubmitted 时按当前准入规则初步校验；在 OperationCommitPoint 前、与 DemandId 占用、完整仓位预留和指令 outbox 同一业务事务中，再按最新规则校验一次，并持久化 AdmissionDecisionSnapshot，至少包含：

- `stationId`
- `taskType`
- `admissionPolicyVersion`
- `admittedAt`
- `allowed=true`

只有第二次校验仍允许，服务端才能发送 SlotOperationCommand。指令一经发出，本次操作使用冻结快照，后续删除或修改 `(stationId, taskType)` 关系不能中断、取消或改变当前装货；纠错、取消清空和失败补偿也继续完成。新配置只影响尚未越过 OperationCommitPoint 的后续操作。

服务端的准入关系按 ADR-cross-0051 保存在 AdmissionPolicyStore；每次变更必须产生可持久化的单调 admissionPolicyVersion，业务审计能够回答某次 SlotOperationAttemptId 使用了哪一版规则。

**Status**: accepted

**Considered Options**:
- 每个仓位执行前都重新检查当前配置（拒绝：配置变化会让已经开始的物理操作悬空）
- 只在 SUBLOT 刚提交时检查一次（拒绝：到指令实际发出前可能已经失效）
- SUBLOT 提交时预检，OperationCommitPoint 前复检并冻结版本（采纳）

**Consequences**:
- 配置删除不是紧急停止机制；已经执行中的安全介入继续使用专门的安全状态和移动控制流程。
- pre-commit 复检失败时不得发送指令，并应释放尚未承诺的仓位与 SUBLOT 预留。
- AdmissionDecisionSnapshot 由服务端保存，不需要下发给车载端。
- 操作恢复和审计不得使用当前配置重新解释历史允许结论。
- 后续接口确认稿应在 §14 加入准入规则版本与承诺点复检。
