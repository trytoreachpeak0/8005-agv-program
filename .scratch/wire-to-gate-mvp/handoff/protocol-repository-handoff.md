# 共享协议仓库初始化交接

## 仓库用途

实施阶段必须创建一个独立、轻量的协议仓库，而不是在本规划任务中创建。它是唯一可执行契约权威，不包含生产 ControlServer／OnboardHmi 代码、不包含共享的特定语言业务 SDK，也不包含第三套 Fake 实现。

每个不可变 release 必须由完整复合身份标识：ProtocolVersion、profile ID、release 版本／tag、完整 commit、协议 manifest SHA-256、Schema bundle SHA-256、错误码 registry SHA-256、样例／向量集 SHA-256，以及 runner-contract 身份。仅凭 tag、分支、包版本或 ProtocolVersion 均不足以确认身份。两个实现必须锁定不可变 release，绝不能跟踪 `main` 或使用 Git submodule。

## 必须具备的 release 目录树

```text
protocol-manifest.json
schemas/envelope.schema.json
schemas/common/*.schema.json
schemas/messages/<messageType>.schema.json
examples/valid/<messageType>/*.json
examples/invalid/<messageType>/*.json
errors/error-codes.json
vectors/messages/*.json
vectors/trajectories/*.json
runner/runner-contract.schema.json
runner/result.schema.json
integration-slices/index.json
compatibility/compatibility.json
approvals/release-approval.json
```

manifest 中每个 messageType 的条目都必须固定：发送方、接收方、交付类别、关联规则、传输去重键 `messageId`、业务去重键、发送前持久化、ACK 前持久化，以及恢复角色。

## 允许的消息面

精确 payload 字段和跨字段规则以已解决的协议治理决策为规范。release 只能包含以下消息族：

- 会话／安全：`SessionHello`、`SessionAccepted`、`SessionRejected`、`Heartbeat`、`HeartbeatAck`、`CapabilitySnapshotRequested`、`CapabilitySnapshot`、`RecoveryStateReport`、`SessionReadiness`、`SafetyStateChanged`、`SafetyStateSnapshotRequested`、`SafetyStateSnapshot`、`PreDepartureSafetyCheck`、`PreDepartureSafetyCheckResult`；
- 业务／旅程：`VehicleBusinessStateSnapshot`、`CurrentStopWorklistSnapshot`、`UpcomingStopPlanSnapshot`、`SublotEntryRequested`、`SublotSubmitted`、`SublotRejected`、`SlotOperationCommand`、`SlotOperationCommandRejected`、`OperationProgress`、`OperationResult`、`ManualChargingReturnToServiceRequested`、`ManualChargingReturnToServiceResult`；
- 纠错／取消／补偿：`LoadCorrectionRequested`、`LoadCorrectionRejected`、`LoadCorrectionCommand`、`LoadCorrectionResult`、`LoadCancellationStartRequested`、`LoadCancellationAuthorization`、`LoadCancellationResult`、`LoadCompensationRequested`、`LoadCompensationRejected`、`LoadCompensationCommand`、`LoadCompensationResult`；
- 恢复：`ExceptionRecoverySessionRequested`、`ExceptionRecoverySessionOpened`、`ExceptionRecoverySessionRejected`、`ExceptionRecoverySessionSnapshot`、`RecoveryActionSubmitted`、`RecoveryActionAccepted`、`RecoveryActionRejected`、`HardwareRecoveryRecordSubmitted`、`HardwareRecoveryRecordResult`、`SlotOperationResumeCommand`、`FaultCargoRecoveryCommand`、`FaultCargoRecoveryResult`、`ForcedMechanicalRecoveryCommand`、`ForcedMechanicalRecoveryResult`；
- 通用：`DurableAck`、`SnapshotAppliedAck`、`ProtocolProblem`。

以下明确禁用的名称必须各自具有一个 `PROFILE_MESSAGE_NOT_ALLOWED` 向量，且不得出现在 allowlist 中：`OperationCancelCommand`、`LoadCancellationCommand`、`LoadFinalConfirmation`、`UnloadCommand`、`SublotAccepted`、特定类型 ACK 名称、`WireToGateExecutionSnapshot`、`DepartureSafetyRevoked`、`OnboardCapabilitySnapshot`。

## 交付与错误规则

可靠消息只有在完成持久接受后才能使用 DurableAck；快照只有在原子采用后才能使用 SnapshotAppliedAck；请求必须持久化并重放首个响应；遥测既不 ACK，也不参与业务记账；心跳只用于建立连接存活。新的 sessionGeneration 隔离传输，但不得改变业务 ID 或待处理 MessageId。

必须冻结协议治理决策规定的最小错误码 registry，包括：协议／envelope／release／哈希／关联冲突；凭证／session／握手／版本缺口；业务／当前 Demand／站点／worklist／Sublot／仓位／动作冲突；以及能力／仓位／锁／输出／发车／恢复／认证／代次安全失败。错误码只能追加。含义、类别和重试处置不得就地改变；本地化显示文案永远不能作为决策输入。

## 发布流程与真实批准

1. ProtocolChangeProposal 必须声明精确 base／target 身份、语义差异、兼容性分类、双仓库迁移及向量影响。
2. Schema、样例、错误码 registry、向量、兼容性信息和 manifest 必须同步更新，然后运行 G1。
3. required、类型、枚举、含义、方向、交付、去重、持久化、恢复、错误或副作用的任何变化都属于 breaking change：必须提升 ProtocolVersion 和 release major；运行时不得协商。
4. 真实 ControlServer 开发者和真实 OnboardHmi 开发者必须分别本人确认精确 commit 与 manifest。用户与车载端同事对共同 release 的确认也必须作为受治理记录保存。AI 不得签署或推断批准。
5. 只有完整真实批准后才能创建不可变 tag／release。所有历史及失败证据必须保留。缺陷只能产生新 release，不得覆盖或强推历史。

本交接包不是首个 release，也不提供任何真实批准记录。
