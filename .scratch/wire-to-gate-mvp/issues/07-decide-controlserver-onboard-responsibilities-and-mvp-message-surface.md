# 决定 ControlServer—OnboardHmi 职责边界与 MVP 消息面

Type: grilling
Status: resolved
Blocked by: 04, 05, 06

## Question

在已接受的「服务端拥有任务、站点、仓位集与移动决策；车载端独占 IO、机构安全与物理执行」边界下，WIRE_TO_GATE MVP 端到端状态机需要哪些最小的请求、响应、可靠事件、可替换快照、心跳和诊断消息？

决策必须对每个 messageType 固定业务权威、发送方、交付类别、关联或去重身份、持久化承诺、断联行为和 RecoveryHandshake 中的对账角色，不得让两个实现仓库各自补齐未写明的语义。

## Answer

用户于 2026-08-25 先逐项采用本票第一轮 Q1～Q4 推荐值，随后明确授权“这个 ticket 全部使用推荐值”，因此以下内容共同构成 `WIRE_TO_GATE` MVP 的跨端消息面决定。

### 1. 权威与协议剖面

1. ControlServer 独占 Demand、AcceptedDemandSnapshot、TransportDemandKey 防重、站点与停靠、完整仓位集、OperationSession、业务就绪与保持、ExceptionRecoverySession、RIoT 移动和最终业务提交权威。OnboardHmi 不创建、改绑、排序、取消或完成业务任务。
2. OnboardHmi 独占实时 IO、SlotPhysicalState、开锁与门序列、OnboardExecutionJournal、逐仓物理结果、抽象安全状态和机构安全拒绝权。ControlServer 不发送 IO 通道或绕过车载安全裁决。
3. 采用 `WireToGateMvpProtocolProfile`：它是精确 `ProtocolVersion = 1` 内的显式 allowlist，不是新协议版本。两端只能实现和接受本票列出的 messageType；剖面外或未知类型以稳定 `ProtocolProblem` 拒绝并 fail-closed，不能“尽量兼容”。
4. 全部消息继续使用 ADR-cross-0030 的 NDJSON `ProtocolEnvelope`。不增加单体 `WireToGateExecutionSnapshot`；OnboardHmi 组合各自权威明确的会话、能力、安全、业务状态、当前作业、后续停靠与本地执行状态，不把组合视图变成新的事实源。
5. `SafetyStateChanged` 在服务端已授权移动期间从安全转为不安全时，同时构成 DepartureSafetyRevoked；线协议不再发送一条重复的 `DepartureSafetyRevoked`。能力全量消息统一命名为 `CapabilitySnapshot`，不再混用 `OnboardCapabilitySnapshot`。

### 2. 完整 messageType allowlist

表中 `C` 表示 ControlServer，`O` 表示 OnboardHmi。`可靠` 使用 `DurableAck`；`快照` 使用 `SnapshotAppliedAck`；`请求` 以 correlationId 关联类型化响应；`遥测` 不 ACK；`存活` 只参与连接存活判断。

#### 2.1 会话、同步、存活与安全

| messageType | 方向／类别 | 权威、身份与承诺 |
| --- | --- | --- |
| `SessionHello` | O→C／请求 | O 声明 agvId、启动实例和 ProtocolVersion；会话前 sessionGeneration 为 null。每次新建连尝试使用新 MessageId。 |
| `SessionAccepted`、`SessionRejected` | C→O／响应 | C 验证 VehicleCredential、精确版本和单车唯一会话；Accepted 先持久化新 sessionGeneration，Rejected 不授予代次或业务能力。 |
| `Heartbeat`、`HeartbeatAck` | O→C、C→O／存活 | Heartbeat payload 只含 capabilityVersion 与 safetyStateVersion；2 秒发送、6 秒无合法消息或 TCP 明确断开即失联。不得据此提交业务、安全或能力事实。 |
| `CapabilitySnapshotRequested` | C→O／请求 | C 在握手、版本未知或缺口时请求一次完整能力；重复 MessageId 返回同一已捕获响应，新一次观测使用新请求。 |
| `CapabilitySnapshot` | O→C／快照 | O 的完整抽象能力权威，以 capabilityVersion 替换；不含原始 IO 映射。O 保留最新未采用版本，C 原子保存采用版本后 `SnapshotAppliedAck`。 |
| `RecoveryStateReport` | O→C／可靠 | O 从 OnboardExecutionJournal、实时 IO 与当前 ForcedRecoveryGeneration 形成报告；明确列出无或有未结 SlotOperationAttemptId、ProvenRecoveryCheckpoint 与待确认结果。C 持久接受后 ACK。 |
| `SessionReadiness` | C→O／可靠 | C 在恢复对账后只发布 `READY` 或 `RECOVERY_REQUIRED` 及稳定原因码；先持久化裁决再发送。仅 READY 授予 VehicleBusinessReadiness。 |
| `SafetyStateChanged` | O→C／可靠 | O 发布递增 safetyStateVersion、DepartureSafe、受影响仓位、稳定原因码与 observedAt；C 持久化非权威 SafetyStateProjection 后 ACK。false 可立即阻断，true 不能代替发车核验。 |
| `SafetyStateSnapshotRequested` | C→O／请求 | C 在握手或发现 safetyStateVersion 缺口时请求完整抽象安全状态；同一请求返回同一观测快照。 |
| `SafetyStateSnapshot` | O→C／快照 | O 的当前完整抽象安全权威，以 safetyStateVersion 替换，不包含原始 DI/DO 或 IO 映射。C 对账并原子采用后 `SnapshotAppliedAck`。 |
| `PreDepartureSafetyCheck` | C→O／请求 | 每次移动前由 C 生成唯一 PreDepartureSafetyCheckId；同一 MessageId 重试不得重新解释成一次新检查。 |
| `PreDepartureSafetyCheckResult` | O→C／响应 | O 基于请求处理时的实时 IO 返回同一检查 ID、observedAt、safetyStateVersion、短有效窗口和抽象安全摘要；重复请求返回首次结果。结果不持久授权移动，过期或被新安全版本取代即失效。 |

#### 2.2 服务端业务投影与正常旅程

| messageType | 方向／类别 | 权威、身份与承诺 |
| --- | --- | --- |
| `VehicleBusinessStateSnapshot` | C→O／快照 | C 以 vehicleBusinessStateRevision 发布完整业务就绪、ManualChargingHold、电量事实未知和结构性阻断；不复制 Demand、计划、安全或物理执行。 |
| `CurrentStopWorklistSnapshot` | C→O／快照 | C 以 stationId + worklistRevision 发布当前停靠完整清单；MVP 为 0 或 1 个当前 Demand。O 只接受当前站点更高版本并整体替换。 |
| `UpcomingStopPlanSnapshot` | C→O／快照 | C 以 planRevision 发布严格串行的 TO_PICKUP／TO_GATE 业务停靠投影；O 不编辑、重排或推导 RIoT 路线。 |
| `SublotEntryRequested` | C→O／可靠 | C 只在 StationOperationArrivalGate、OperationSession、当前 Demand 和业务就绪均有效时开放输入；绑定 DemandId、OperationSession 与机台站。断联或投影过期时不得继续使用。 |
| `SublotSubmitted` | O→C／请求 | 扫码与键盘共用此类型；MessageId 是提交幂等身份，payload 绑定当前 DemandId、OperationSession 和操作员所见 revision。C 必须重新做最终权威校验。 |
| `SublotRejected` | C→O／响应 | 失败时返回稳定业务原因码与非权威文案，不改变原 Demand、不分仓、不产生 IO。相同提交重放返回原拒绝。 |
| `SlotOperationCommand` | C→O／可靠 | 成功提交 Sublot 时它以 correlationId 响应 `SublotSubmitted`；关卡卸货则由 C 直接发送。C 先冻结并持久化 DemandId、SlotOperationAttemptId、操作类型、完整 slots、ExpectedBasketCount 与内容摘要。 |
| `SlotOperationCommandRejected` | O→C／响应 | O 仅在指令结构、目标能力、重复仓位或同一 SlotOperationAttemptId 内容冲突时类型化拒绝，且不得产生 IO；实时机构无法执行则接受命令后以 OperationResult 报告失败或未知。 |
| `OperationProgress` | O→C／遥测 | 只用于实时显示和诊断，不 ACK、不补发、不修改 SlotBusinessState；丢失不影响结果语义。 |
| `OperationResult` | O→C／可靠 | O 先写 OnboardExecutionJournal，再按原 SlotOperationAttemptId 报告全部目标仓位的完成、失败或未开始事实。C 持久化并按操作类型提交业务后 ACK；重复结果不得重复入账。 |
| `ManualChargingReturnToServiceRequested` | O→C／请求 | 仅具名 MaintenanceAdministrator 或 SystemAdministrator 在 ManualChargingHold 中提交；MessageId 固定一次重新投运请求，普通操作员和电量上升不能替代。 |
| `ManualChargingReturnToServiceResult` | C→O／响应 | C 完成电量、非充电、停稳、订单、位置、Guard、仓位操作、能力、安全与恢复对账后返回成功或稳定拒绝；成功只恢复资格评估，不承诺某个 Demand。 |

#### 2.3 纠错、普通取消与装货补偿

| messageType | 方向／类别 | 权威、身份与承诺 |
| --- | --- | --- |
| `LoadCorrectionRequested`、`LoadCorrectionRejected` | O→C／请求—响应 | StopClosureCommit 前由已核验操作员选择原 Demand、原 SlotOperationAttemptId 和原仓位；C 以稳定 CorrectionId 去重并重新校验。拒绝不产生开仓。 |
| `LoadCorrectionCommand` | C→O／可靠 | C 先持久化原仓位纠错授权再发送；使用新 MessageId，但不得改变原 Demand、SlotOperationAttemptId、仓位集或已提交 LoadBatch 历史。 |
| `LoadCorrectionResult` | O→C／可靠 | O 先记录原仓位 `OCCUPIED→EMPTY→OCCUPIED`、锁闭与输出复位闭环再发送；C 持久化追加审计后 ACK。 |
| `LoadCancellationStartRequested`、`LoadCancellationAuthorization` | O→C／请求—响应 | C 以 CancellationId 返回 `AUTHORIZED` 或 `REJECTED`；授权固定 DemandId、可空原 SlotOperationAttemptId 和完整目标范围。AUTHORIZED 只允许开始清空，不表示已取消。 |
| `LoadCancellationResult` | O→C／可靠 | O 可靠报告授权范围 ALL_EMPTY 的逐仓闭环；C 持久接受后才原子提交 `CANCELLED_BY_OPERATOR`、TransportDemandSuppression 和新版作业投影。 |
| `LoadCompensationRequested`、`LoadCompensationRejected` | O→C／请求—响应 | ExceptionRecoverySession 已记录整批清空选择后，现场人员显式请求开始；C 以 RecoveryActionId、原 DemandId 和原 SlotOperationAttemptId 校验。不得因选择本身自动开仓。 |
| `LoadCompensationCommand` | C→O／可靠 | C 持久化授权范围后发送，沿用原 SlotOperationAttemptId、新 MessageId；O 不得扩大至替代仓位。 |
| `LoadCompensationResult` | O→C／可靠 | O 先记录完整目标集合 EMPTY、锁闭与输出复位，再可靠上报；C 只有在终态与永久抑制可原子提交时 ACK 并释放预留。 |

`OperationCancelCommand`、`LoadCancellationCommand` 和 `LoadFinalConfirmation` 明确不在剖面中。装卸继续共用 `SlotOperationCommand`，不增加 `UnloadCommand`；成功的 Sublot 提交不增加 `SublotAccepted`。

#### 2.4 最小 ExceptionRecoverySession

| messageType | 方向／类别 | 权威、身份与承诺 |
| --- | --- | --- |
| `ExceptionRecoverySessionRequested` | O→C／请求 | 具名管理员提交一次个人认证证明和固定事件、车辆、Demand/仓位范围；凭证不得进入普通日志或响应。 |
| `ExceptionRecoverySessionOpened`、`ExceptionRecoverySessionRejected` | C→O／响应 | C 独占权限、范围与会话生命周期裁决；Opened 返回稳定 ExceptionRecoverySessionId，Rejected 返回原因且不开启任何恢复能力。 |
| `ExceptionRecoverySessionSnapshot` | C→O／快照 | C 以 recoverySessionRevision 发布会话人员、事件、固定范围、当前选择、允许动作和阻断原因；O 只能整体采用，不能本地扩围。 |
| `RecoveryActionSubmitted` | O→C／请求 | 使用稳定 RecoveryActionId，只允许 `RESUME_AFTER_REPAIR`、`COMPENSATE_LOAD_ALL_EMPTY`、`FAULT_CARGO_HANDOFF`、`FORCED_MECHANICAL_RECOVERY` 四种已批准选择。 |
| `RecoveryActionAccepted`、`RecoveryActionRejected` | C→O／响应 | C 持久化接受或拒绝；Accepted 只记录业务路径，不自动产生 IO。后续物理动作必须由本表具名命令授权。 |
| `HardwareRecoveryRecordSubmitted`、`HardwareRecoveryRecordResult` | O→C／请求—响应 | 记录具名人员检查与处理事实；C 保存审计并重新核验。记录不是审批，也不能替代实时锁、光幕、输出回读或 IO 有效性。MVP 不再使用旧 `HardwareRecoveryConfirmation` 语义。 |
| `SlotOperationResumeCommand` | C→O／可靠 | 仅在原 Demand、原 SlotOperationAttemptId、唯一 ProvenRecoveryCheckpoint、硬件与业务事实一致时授权继续；O 仍可因实时安全拒绝扩大动作，完成沿用 OperationResult。 |
| `FaultCargoRecoveryCommand`、`FaultCargoRecoveryResult` | C→O、O→C／可靠 | C 固定原 Demand、车辆和完整载货仓位；O 执行受控取货并可靠报告电子闭环与具名交接。C 核验后才提交 FaultCargoRecoveryRecord、故障交接终态与永久抑制。 |
| `ForcedMechanicalRecoveryCommand`、`ForcedMechanicalRecoveryResult` | C→O、O→C／可靠 | C 先建立新的 ForcedRecoveryGeneration 并冻结旧命令资格；O 停止重复 DO，只记录隔离、机械取出和具名交接。结果不能证明电子空仓、仓门安全或车辆恢复。 |

MVP ExceptionRecoveryPermission 采用票据 05 已批准的简化角色模型：MaintenanceAdministrator 或 SystemAdministrator 在一次个人认证的固定会话内可独立完成系统操作，不恢复旧 ADR 中 R-09/R-11 双权限、逐动作二次认证或 `HardwareRecoveryConfirmation`。现场物理资质和所有实时安全门禁仍不可由角色覆盖。

#### 2.5 通用确认与诊断

| messageType | 方向／类别 | 语义 |
| --- | --- | --- |
| `DurableAck` | 接收方→发送方／可靠确认 | correlationId 指向可靠原消息；只有 DurableAcceptance 后才能发送。它不携带业务拒绝、不表示命令执行、结果成功或快照采用。 |
| `SnapshotAppliedAck` | 接收方→发送方／快照确认 | correlationId 指向快照并携带 snapshotKind 与已采用 revision；旧 revision 可丢弃但不能确认成当前。 |
| `ProtocolProblem` | 任一方→对端／诊断响应 | 只在外壳可解析且能够安全关联时返回稳定协议原因码、字段路径和非权威显示文案；未知/剖面外类型、Schema、内容哈希、会话代次等错误 fail-closed。TLS、认证或 JSON 外壳无法安全解析时直接拒绝/关闭连接，不伪造响应。 |

不再创建 `OperationCommandAck`、`OperationResultAck`、`LoadCompensationCommandAck` 等逐类型 ACK；它们统一由 `DurableAck` 取代。所有业务拒绝保留类型化响应，不能塞入 ACK 或通过解析文案判断。

### 3. 去重、持久化与断联规则

1. **传输身份统一使用 MessageId。** 相同语义消息的发送重试沿用原 MessageId、payload 与规范化内容摘要；改变业务语义必须使用新 MessageId。correlationId 只关联请求、响应或确认，不能代替 DemandId、SlotOperationAttemptId 或 RecoveryActionId。
2. **跨重连保持语义身份。** 新连接必须使用当前 sessionGeneration 重新封装仍需补报的原语义消息，但沿用原 MessageId 与 payload；旧 sessionGeneration 的迟到消息一律拒绝。sessionGeneration 是传输围栏，不是业务幂等键。
3. **业务层二次去重。** Demand 生命周期使用 DemandId；同键永久防重使用 TransportDemandKey；多仓物理操作使用 SlotOperationAttemptId；发车核验使用 PreDepartureSafetyCheckId；纠错、取消和异常选择分别使用 CorrectionId、CancellationId、RecoveryActionId；异常会话使用 ExceptionRecoverySessionId；强制机械处置后使用 ForcedRecoveryGeneration。相同业务 ID 携带不同规范化内容必须稳定拒绝并告警。
4. **可靠消息先持久化后 ACK。** 命令发送方先保存意图与完整内容；接收方先保存消息、去重键及承担的处理责任后发送 `DurableAck`。OnboardHmi 在保存到 OnboardExecutionJournal 前不得 ACK 会产生 IO 的命令；ControlServer 在保存逐仓结果和业务提交依据前不得 ACK 结果。
5. **请求结果可恢复。** 会产生承诺、授权、取消、重新投运或恢复选择的请求必须持久化原 MessageId、规范化请求和首次结果；重复请求返回首次结果，不重新消费认证、不重新分配仓位或产生第二个副作用。PreDepartureSafetyCheck 只在其短有效窗口内保留原结果，过期后必须创建新检查。
6. **快照只保留当前版本。** 发送方保留并重发最新未确认 revision；接收方原子采用更高版本并返回 `SnapshotAppliedAck`。同 revision 同内容幂等确认，同 revision 不同内容或版本回退进入协议/状态缺口处理。OnboardHmi 重启后不依赖旧业务投影，恢复握手必须重新取得最新版本。
7. **断联不扩大物理副作用。** `OperationProgress` 丢弃；尚未开始的请求、命令或 UI 操作冻结；已经发送或结果未知的 ActiveUnlockSet 只执行 SafelyFinishActiveUnlockSet。服务端命令不能在重连后盲目续发，必须先沿原业务 ID 对账并证明仍是唯一合法下一步。
8. **离线投影只读且显式过期。** CurrentStopWorklistSnapshot、UpcomingStopPlanSnapshot 和 VehicleBusinessStateSnapshot 可保留供查看，但不得开始扫码、取消、恢复、开仓或移动。车载实时安全显示继续以本地 IO 为权威。

### 4. RecoveryHandshake 中的消息顺序

1. `SessionHello` → `SessionAccepted` 建立当前会话代次；Heartbeat 随即持续。
2. OnboardHmi 发布完整 `CapabilitySnapshot`；若 safetyStateVersion 未知或缺口，ControlServer 同阶段发出 `SafetyStateSnapshotRequested` 并取得完整 `SafetyStateSnapshot`。
3. OnboardHmi 可靠发送 `RecoveryStateReport`，包括显式空报告、未结 SlotOperationAttemptId、ProvenRecoveryCheckpoint、ForcedRecoveryGeneration 和待确认结果索引。
4. OnboardHmi 沿用原 MessageId 与 SlotOperationAttemptId 补报 `OperationResult`、纠错/取消/补偿或恢复结果；ControlServer 逐条 DurableAcceptance 并 ACK，双方对物理与业务事实收敛。
5. ControlServer 只有在能力、安全、未结命令、积压结果、SlotPhysicalState/SlotBusinessState、业务保持和移动保护全部唯一可解释时发送 `SessionReadiness(READY)`；否则发送 `RECOVERY_REQUIRED`。READY 后再发布最新 VehicleBusinessStateSnapshot、CurrentStopWorklistSnapshot 和 UpcomingStopPlanSnapshot。投影采用前相应 UI 操作仍禁用。

握手中再次断线时，新会话取得新代次并从第一步重做；任何一方不能把“TCP 恢复”“Heartbeat 正常”“快照已显示”或“ACK 已收到”单独解释成业务继续授权。

### 5. 留给后续票据的边界

本票已经固定完整 messageType、方向、权威、交付类别、主要关联/去重身份、持久承诺、断联规则和恢复角色。每个 payload 的精确字段、JSON 类型、必填/可选约束、枚举全集、稳定错误码表、Schema 文件组织、内容 SHA-256、合法/非法样例和一致性向量由[决定共享协议仓库的发布内容与变更治理](09-decide-shared-protocol-repository-release-and-change-governance.md)在本决定之上序列化，不得重新改变本票语义。
