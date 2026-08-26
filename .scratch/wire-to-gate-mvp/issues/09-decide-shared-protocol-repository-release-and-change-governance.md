# 决定共享协议仓库的发布内容与变更治理

Type: grilling
Status: resolved
Blocked by: 07

## Question

独立 `8005-agv-protocol` 仓库的目录结构、JSON Schema 组织、ProtocolVersion 与协议 release 版本关系、manifest、内容 SHA-256、合法/非法样例、错误码、一致性向量、Git tag、批准记录和兼容性规则应如何固定，才能让两个实现仓库只锁定一个不可变契约身份？

还需决定非破坏性可选字段、破坏性必填/语义/流程变更、两名开发者本人批准、AI 生成内容复核、过期 release 保留与两端升级失败时的拒绝规则。

本票必须把[决定 ControlServer—OnboardHmi 职责边界与 MVP 消息面](07-decide-controlserver-onboard-responsibilities-and-mvp-message-surface.md)已固定的每个 messageType、方向、交付类别、关联/去重身份、持久承诺和恢复角色逐一序列化为精确 payload 字段、JSON 类型、必填/可选约束、枚举、稳定错误码、合法/非法样例及一致性向量；不得在 Schema 阶段重新合并、改名或改变其语义。

## Answer

用户已明确授权本 Wayfinder 后续各票在完成事实核对、完整列出候选、推荐值与理由后采用全部推荐值。本票依该持续授权采用三轮共十四项推荐值；这不是伪造的逐项用户发言，也不是车载端开发同事或任何 AI 对真实 protocol release 的批准。2026-08-25 已核对根 `CONTEXT.md`、`docs/adr/cross/0023`～`0032`、本地图 Notes、已解决票 02～08 及原型票豁免边界。

### 1. 发布身份、仓库和权威

1. 独立仓库规范名为 `8005-agv-protocol`。两个实现仓库不得跟踪 `main`、使用 submodule 或维护平行协议副本，只能锁定一个 `ProtocolReleaseIdentity`：`repository + releaseVersion + tag + commit + protocolVersion + profileId + manifestSha256 + schemaBundleSha256 + vectorsSha256`。任一分量缺失或不同即不是同一契约。
2. `ProtocolVersion` 是线协议破坏性兼容代次，MVP 固定整数 `1` 并精确匹配；`releaseVersion` 使用 SemVer。兼容增加产生同一 ProtocolVersion 的 minor release，纯纠错且不改变任何机器结论产生 patch，破坏性变更同时提升 ProtocolVersion 与 release major。tag 格式固定为 `protocol-v<releaseVersion>`，必须是 annotated tag 且永久指向同一完整 commit。
3. 固定目录为：`manifest/release.json`、`schemas/common/*.schema.json`、`schemas/messages/<messageType>.schema.json`、`schemas/bundle/protocol.schema.json`、`errors/error-codes.json`、`examples/valid/<messageType>/*.json`、`examples/invalid/<messageType>/*.json`、`vectors/<vectorId>/{input.ndjson,expected.json}`、`compatibility/report.json`、`approvals/release-approval.json`、`docs/`。JSON Schema、manifest、错误码 registry、样例和向量是执行权威；Markdown 只能解释，不能增加字段、枚举或处理语义。
4. Schema 使用 JSON Schema Draft 2020-12。每个 messageType 独立引用公共 `$defs`，并固定 envelope 的 `messageType` 常量、方向、交付类别、correlation 规则和 payload。发布 bundle 对本 release 严格拒绝未声明字段；运行时解码器必须忽略未来 release 明确声明的未知可选字段，但不得因此接受未知 messageType、剖面外 messageType 或未知必填语义。
5. JSON 内容哈希统一使用 UTF-8、无 BOM、RFC 8785 JCS 后 SHA-256 小写十六进制；NDJSON 向量逐行对 JSON 对象执行 JCS，再以 LF 连接并以末尾 LF 结束后哈希。二进制或 Markdown 文件按原始 bytes 哈希。manifest 列出除自身外每个发布文件的相对路径、角色、字节数和 SHA-256，并保存其排序后文件表哈希；`manifestSha256` 是最终 `release.json` 原始 bytes 的 SHA-256。
6. 正式 release 必须同时具有 clean-tree 完整 commit、annotated tag、全部哈希、Schema bundle、错误 registry、合法/非法样例、向量、兼容性报告和批准记录。CI 必须从 tag clean checkout 重算全部身份并零差异通过；任何真实凭证、证书 pin、人员认证证明和现场秘密不得进入仓库或普通日志。

### 2. 公共 JSON 契约

下文 `!` 表示 required，`?` 表示字段 required 但值可为 JSON `null`；未标 `!` 的字段为真正 optional，缺失不得改变旧端安全或业务结论。`Id` 均为非空、区分大小写的 UUID 字符串；`Revision`/`Generation` 为 `integer >= 0`；`Instant` 为 UTC RFC 3339 `date-time`；`Sha256` 为 64 位小写十六进制；`SlotNo` 为 `integer 1..8`；所有 Slot 数组必须非空、唯一并按升序编码。

每行 `ProtocolEnvelope` 精确字段为：`protocolVersion:integer! const 1`、`profileId:string! const WIRE_TO_GATE_MVP`、`protocolReleaseVersion:string!`、`protocolReleaseManifestSha256:Sha256!`、`messageType:string!`、`messageId:Id!`、`correlationId:Id?!`、`agvId:string!`、`sessionGeneration:Generation?!`、`sentAt:Instant!`、`payload:object!`。`SessionHello`、`SessionRejected` 可令 sessionGeneration 为 null；`SessionAccepted` 起必须为非 null。响应和 ACK 的 correlationId 必须是原请求/消息 MessageId；无对应请求的可靠事件、遥测和快照必须为 null。

公共对象固定如下：

- `ProtocolReleaseIdentity = {repository:string! const 8005-agv-protocol, releaseVersion:string! pattern ^[0-9]+\\.[0-9]+\\.[0-9]+$, tag:string! pattern ^protocol-v, commit:string! pattern ^[0-9a-f]{40}$, protocolVersion:integer! const 1, profileId:string! const WIRE_TO_GATE_MVP, manifestSha256:Sha256!, schemaBundleSha256:Sha256!, vectorsSha256:Sha256!}`。
- `Problem = {reasonCode:ErrorCode!, fieldPath:string?!, displayMessage:string?!}`，displayMessage 永远非权威。
- `SlotState = {slotNo:SlotNo!, operability:OPERABLE|INOPERABLE|UNKNOWN!, administrativeAvailability:ENABLED|DISABLE_PENDING|DISABLED!, physicalState:EMPTY|OCCUPIED|UNKNOWN!, lockState:LOCKED|UNLOCKED|UNKNOWN!, unlockOutputState:RESET|ACTIVE|UNKNOWN!, reasonCodes:ErrorCode[]!}`。
- `SlotResult = {slotNo:SlotNo!, outcome:COMPLETED|FAILED|NOT_STARTED|UNKNOWN!, finalPhysicalState:EMPTY|OCCUPIED|UNKNOWN!, lockState:LOCKED|UNLOCKED|UNKNOWN!, unlockOutputState:RESET|ACTIVE|UNKNOWN!, reasonCodes:ErrorCode[]!}`。
- `SafetySummary = {departureSafe:boolean!, vehicleStopped:boolean!, allTargetSlotsLocked:boolean!, allUnlockOutputsReset:boolean!, unknownPresent:boolean!, reasonCodes:ErrorCode[]!}`。
- `OperatorContext = {operatorId:string!, verificationMethod:BADGE|SESSION!, verifiedAt:Instant!}`；恢复管理动作另带 `administratorRole:MAINTENANCE_ADMINISTRATOR|SYSTEM_ADMINISTRATOR`，不得携带秘密。
- `PendingResultRef = {messageType:string!, messageId:Id!, businessId:string!, contentSha256:Sha256!}`；`BlockingFact = {reasonCode:ErrorCode!, subjectType:string!, subjectId:string?!}`。

### 3. 每个 messageType 的精确 payload

方向缩写 C=ControlServer、O=OnboardHmi；类别为请求、响应、可靠、快照、遥测、存活。除表内字段外不得增加本 release 的 payload 字段。

| messageType | 方向／类别 | payload 精确字段 |
| --- | --- | --- |
| `SessionHello` | O→C／请求 | `onboardInstanceId:Id!`, `onboardBuildCommit:string!`, `supportedProtocolVersion:integer! const 1`, `profileId:string! const WIRE_TO_GATE_MVP`, `protocolReleaseIdentity:object!`, `credentialProof:string!`（部署期证明，占位样例且禁止日志） |
| `SessionAccepted` | C→O／响应 | `sessionGeneration:Generation!`, `serverInstanceId:Id!`, `serverBuildCommit:string!`, `acceptedProtocolReleaseIdentity:object!`, `acceptedAt:Instant!` |
| `SessionRejected` | C→O／响应 | `problem:Problem!`, `expectedProtocolVersion:integer!`, `expectedProtocolReleaseIdentity:object?!` |
| `Heartbeat` | O→C／存活 | `capabilityVersion:Revision!`, `safetyStateVersion:Revision!` |
| `HeartbeatAck` | C→O／存活响应 | `receivedHeartbeatMessageId:Id!`, `serverTime:Instant!` |
| `CapabilitySnapshotRequested` | C→O／请求 | `requestedCapabilityVersion:Revision?!`, `reason:HANDSHAKE∣VERSION_GAP∣EXPLICIT_RECONCILIATION!` |
| `CapabilitySnapshot` | O→C／快照 | `capabilityVersion:Revision!`, `observedAt:Instant!`, `slotModelVersion:string!`, `activeSlotConfigurationVersion:string!`, `slotStates:SlotState[]!`, `supportsBatchUnlock:boolean!`, `onboardJournalFormatVersion:integer!` |
| `RecoveryStateReport` | O→C／可靠 | `reportId:Id!`, `observedAt:Instant!`, `unsettledSlotOperationAttemptId:Id?!`, `provenRecoveryCheckpoint:NONE∣PREPARED∣ACTIVE_UNLOCK_SET∣SAFE_FINISH_REACHED∣RESULT_RECORDED!`, `activeUnlockSlots:SlotNo[]!`, `forcedRecoveryGeneration:Generation!`, `pendingResults:PendingResultRef[]!`, `journalContentSha256:Sha256!` |
| `SessionReadiness` | C→O／可靠 | `readiness:READY∣RECOVERY_REQUIRED!`, `decidedAt:Instant!`, `reasonCodes:ErrorCode[]!`, `acceptedCapabilityVersion:Revision!`, `acceptedSafetyStateVersion:Revision!`, `vehicleBusinessStateRevision:Revision!` |
| `SafetyStateChanged` | O→C／可靠 | `safetyStateVersion:Revision!`, `observedAt:Instant!`, `safety:SafetySummary!`, `affectedSlots:SlotNo[]!` |
| `SafetyStateSnapshotRequested` | C→O／请求 | `requestedSafetyStateVersion:Revision?!`, `reason:HANDSHAKE∣VERSION_GAP∣PRE_MOVEMENT_RECONCILIATION!` |
| `SafetyStateSnapshot` | O→C／快照 | `safetyStateVersion:Revision!`, `observedAt:Instant!`, `safety:SafetySummary!`, `slotStates:SlotState[]!` |
| `PreDepartureSafetyCheck` | C→O／请求 | `preDepartureSafetyCheckId:Id!`, `demandId:Id!`, `movementLegId:Id!`, `expectedSafetyStateVersion:Revision!`, `targetStationId:string!` |
| `PreDepartureSafetyCheckResult` | O→C／响应 | `preDepartureSafetyCheckId:Id!`, `outcome:SAFE∣UNSAFE∣UNKNOWN!`, `observedAt:Instant!`, `safetyStateVersion:Revision!`, `validUntil:Instant!`, `safety:SafetySummary!` |
| `VehicleBusinessStateSnapshot` | C→O／快照 | `vehicleBusinessStateRevision:Revision!`, `readiness:READY∣RECOVERY_REQUIRED!`, `manualChargingHold:boolean!`, `batteryState:SUFFICIENT∣LOW∣UNKNOWN!`, `blockingFacts:BlockingFact[]!`, `observedAt:Instant!` |
| `CurrentStopWorklistSnapshot` | C→O／快照 | `stationId:string!`, `worklistRevision:Revision!`, `operationSessionId:Id?!`, `items:array maxItems 1!`; item=`{demandId:Id!, transportDemandKey:string!, sublot:string!, workType:string! const WIRE_TO_GATE, stopRole:PICKUP∣GATE!, expectedBasketCount:integer 1..8!}` |
| `UpcomingStopPlanSnapshot` | C→O／快照 | `planRevision:Revision!`, `demandId:Id?!`, `legs:array maxItems 2!`; leg=`{movementLegId:Id!, legType:TO_PICKUP∣TO_GATE!, sequence:integer 1..2!, stationId:string!, mapId:string!, state:PLANNED∣ACTIVE∣ARRIVED∣COMPLETED∣BLOCKED!}`，sequence 唯一升序 |
| `SublotEntryRequested` | C→O／可靠 | `demandId:Id!`, `operationSessionId:Id!`, `stationId:string!`, `worklistRevision:Revision!`, `expectedSublot:string!`, `entryMethods:array! const [SCANNER,KEYBOARD]`, `expiresOnRevisionChange:boolean! const true` |
| `SublotSubmitted` | O→C／请求 | `demandId:Id!`, `operationSessionId:Id!`, `stationId:string!`, `worklistRevision:Revision!`, `sublot:string!`, `entryMethod:SCANNER∣KEYBOARD!`, `operator:OperatorContext!` |
| `SublotRejected` | C→O／响应 | `demandId:Id!`, `operationSessionId:Id!`, `problem:Problem!`, `currentWorklistRevision:Revision!` |
| `SlotOperationCommand` | C→O／可靠 | `demandId:Id!`, `operationSessionId:Id!`, `slotOperationAttemptId:Id!`, `operationType:LOAD∣UNLOAD!`, `slots:SlotNo[]!`, `expectedBasketCount:integer 1..8!`, `expectedFinalPhysicalState:OCCUPIED∣EMPTY!`, `commandContentSha256:Sha256!`; LOAD 必须与 SublotSubmitted correlation，UNLOAD correlationId=null |
| `SlotOperationCommandRejected` | O→C／响应 | `slotOperationAttemptId:Id!`, `problem:Problem!`, `observedCapabilityVersion:Revision!`, `conflictingContentSha256:Sha256?!` |
| `OperationProgress` | O→C／遥测 | `slotOperationAttemptId:Id!`, `phase:PREPARING∣UNLOCKING∣WAITING_OPERATOR∣VERIFYING∣SAFE_FINISH∣PAUSED!`, `activeUnlockSlots:SlotNo[]!`, `completedSlots:SlotNo[]!`, `observedAt:Instant!` |
| `OperationResult` | O→C／可靠 | `demandId:Id!`, `slotOperationAttemptId:Id!`, `operationType:LOAD∣UNLOAD!`, `overallOutcome:COMPLETED∣FAILED∣UNKNOWN!`, `slotResults:SlotResult[]!`, `observedAt:Instant!`, `journalCheckpoint:string!`, `resultContentSha256:Sha256!` |
| `ManualChargingReturnToServiceRequested` | O→C／请求 | `requestId:Id!`, `administrator:OperatorContext!`, `administratorRole:MAINTENANCE_ADMINISTRATOR∣SYSTEM_ADMINISTRATOR!`, `reason:string!`, `observedBatteryPercent:number 0..100?!` |
| `ManualChargingReturnToServiceResult` | C→O／响应 | `requestId:Id!`, `outcome:RETURNED_TO_ELIGIBILITY_EVALUATION∣REJECTED!`, `problem:Problem?!`, `vehicleBusinessStateRevision:Revision!` |
| `LoadCorrectionRequested` | O→C／请求 | `correctionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `slots:SlotNo[]!`, `operator:OperatorContext!`, `reason:string!` |
| `LoadCorrectionRejected` | C→O／响应 | `correctionId:Id!`, `problem:Problem!` |
| `LoadCorrectionCommand` | C→O／可靠 | `correctionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `slots:SlotNo[]!`, `expectedSequence:array! const [EMPTY,OCCUPIED]`, `commandContentSha256:Sha256!` |
| `LoadCorrectionResult` | O→C／可靠 | `correctionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `overallOutcome:COMPLETED∣FAILED∣UNKNOWN!`, `slotResults:SlotResult[]!`, `observedAt:Instant!` |
| `LoadCancellationStartRequested` | O→C／请求 | `cancellationId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id?!`, `operator:OperatorContext!`, `reason:string!` |
| `LoadCancellationAuthorization` | C→O／响应 | `cancellationId:Id!`, `decision:AUTHORIZED∣REJECTED!`, `demandId:Id!`, `slotOperationAttemptId:Id?!`, `slots:SlotNo[]!`, `problem:Problem?!`; AUTHORIZED 时 problem=null 且 slots 非空，REJECTED 时 slots 空且 problem 非 null |
| `LoadCancellationResult` | O→C／可靠 | `cancellationId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id?!`, `overallOutcome:ALL_EMPTY∣FAILED∣UNKNOWN!`, `slotResults:SlotResult[]!`, `observedAt:Instant!` |
| `LoadCompensationRequested` | O→C／请求 | `recoveryActionId:Id!`, `exceptionRecoverySessionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `operator:OperatorContext!` |
| `LoadCompensationRejected` | C→O／响应 | `recoveryActionId:Id!`, `problem:Problem!` |
| `LoadCompensationCommand` | C→O／可靠 | `recoveryActionId:Id!`, `exceptionRecoverySessionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `slots:SlotNo[]!`, `expectedFinalPhysicalState:string! const EMPTY`, `commandContentSha256:Sha256!` |
| `LoadCompensationResult` | O→C／可靠 | `recoveryActionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `overallOutcome:ALL_EMPTY∣FAILED∣UNKNOWN!`, `slotResults:SlotResult[]!`, `observedAt:Instant!` |
| `ExceptionRecoverySessionRequested` | O→C／请求 | `requestId:Id!`, `administrator:OperatorContext!`, `administratorRole:MAINTENANCE_ADMINISTRATOR∣SYSTEM_ADMINISTRATOR!`, `eventId:Id!`, `demandId:Id?!`, `slots:SlotNo[]!`, `reason:string!`, `authenticationProof:string!`（禁止日志） |
| `ExceptionRecoverySessionOpened` | C→O／响应 | `requestId:Id!`, `exceptionRecoverySessionId:Id!`, `openedAt:Instant!`, `eventId:Id!`, `demandId:Id?!`, `slots:SlotNo[]!`, `recoverySessionRevision:Revision!` |
| `ExceptionRecoverySessionRejected` | C→O／响应 | `requestId:Id!`, `problem:Problem!` |
| `ExceptionRecoverySessionSnapshot` | C→O／快照 | `exceptionRecoverySessionId:Id!`, `recoverySessionRevision:Revision!`, `state:OPEN∣ACTION_SELECTED∣EXECUTING∣CLOSED!`, `administratorId:string!`, `administratorRole:MAINTENANCE_ADMINISTRATOR∣SYSTEM_ADMINISTRATOR!`, `eventId:Id!`, `demandId:Id?!`, `slots:SlotNo[]!`, `selectedAction:RESUME_AFTER_REPAIR∣COMPENSATE_LOAD_ALL_EMPTY∣FAULT_CARGO_HANDOFF∣FORCED_MECHANICAL_RECOVERY?!`, `allowedActions:string[]!`, `blockingFacts:BlockingFact[]!` |
| `RecoveryActionSubmitted` | O→C／请求 | `recoveryActionId:Id!`, `exceptionRecoverySessionId:Id!`, `action:RESUME_AFTER_REPAIR∣COMPENSATE_LOAD_ALL_EMPTY∣FAULT_CARGO_HANDOFF∣FORCED_MECHANICAL_RECOVERY!`, `eventId:Id!`, `demandId:Id?!`, `slots:SlotNo[]!`, `operator:OperatorContext!`, `reason:string!` |
| `RecoveryActionAccepted` | C→O／响应 | `recoveryActionId:Id!`, `exceptionRecoverySessionId:Id!`, `acceptedAction:string!`, `recoverySessionRevision:Revision!`, `acceptedAt:Instant!` |
| `RecoveryActionRejected` | C→O／响应 | `recoveryActionId:Id!`, `exceptionRecoverySessionId:Id!`, `problem:Problem!`, `recoverySessionRevision:Revision!` |
| `HardwareRecoveryRecordSubmitted` | O→C／请求 | `recordId:Id!`, `exceptionRecoverySessionId:Id!`, `recoveryActionId:Id!`, `operator:OperatorContext!`, `administratorRole:MAINTENANCE_ADMINISTRATOR∣SYSTEM_ADMINISTRATOR!`, `slots:SlotNo[]!`, `checksPerformed:string[]!`, `actionsPerformed:string[]!`, `observations:string[]!`, `observedAt:Instant!` |
| `HardwareRecoveryRecordResult` | C→O／响应 | `recordId:Id!`, `outcome:RECORDED∣REJECTED!`, `problem:Problem?!`, `recoverySessionRevision:Revision!` |
| `SlotOperationResumeCommand` | C→O／可靠 | `exceptionRecoverySessionId:Id!`, `recoveryActionId:Id!`, `demandId:Id!`, `slotOperationAttemptId:Id!`, `provenRecoveryCheckpoint:PREPARED∣ACTIVE_UNLOCK_SET∣SAFE_FINISH_REACHED!`, `slots:SlotNo[]!`, `commandContentSha256:Sha256!` |
| `FaultCargoRecoveryCommand` | C→O／可靠 | `exceptionRecoverySessionId:Id!`, `recoveryActionId:Id!`, `demandId:Id!`, `slots:SlotNo[]!`, `handoffId:Id!`, `commandContentSha256:Sha256!` |
| `FaultCargoRecoveryResult` | O→C／可靠 | `exceptionRecoverySessionId:Id!`, `recoveryActionId:Id!`, `demandId:Id!`, `handoffId:Id!`, `overallOutcome:HANDED_OFF∣FAILED∣UNKNOWN!`, `slotResults:SlotResult[]!`, `operator:OperatorContext!`, `observedAt:Instant!` |
| `ForcedMechanicalRecoveryCommand` | C→O／可靠 | `exceptionRecoverySessionId:Id!`, `recoveryActionId:Id!`, `demandId:Id?!`, `forcedRecoveryGeneration:Generation!`, `slots:SlotNo[]!`, `commandContentSha256:Sha256!` |
| `ForcedMechanicalRecoveryResult` | O→C／可靠 | `exceptionRecoverySessionId:Id!`, `recoveryActionId:Id!`, `forcedRecoveryGeneration:Generation!`, `outcome:MECHANICALLY_ISOLATED∣FAILED∣UNKNOWN!`, `slots:SlotNo[]!`, `operator:OperatorContext!`, `observedAt:Instant!`, `electronicEmptyProven:boolean! const false`, `vehicleReadyProven:boolean! const false` |
| `DurableAck` | 接收方→发送方／可靠确认 | `acceptedMessageId:Id!`, `acceptedMessageType:string!`, `acceptedContentSha256:Sha256!`, `durablyAcceptedAt:Instant!` |
| `SnapshotAppliedAck` | 接收方→发送方／快照确认 | `snapshotMessageId:Id!`, `snapshotKind:CAPABILITY∣SAFETY_STATE∣VEHICLE_BUSINESS_STATE∣CURRENT_STOP_WORKLIST∣UPCOMING_STOP_PLAN∣EXCEPTION_RECOVERY_SESSION!`, `appliedRevision:Revision!`, `appliedContentSha256:Sha256!` |
| `ProtocolProblem` | 任一方→对端／诊断响应 | `rejectedMessageId:Id!`, `rejectedMessageType:string?!`, `problem:Problem!`, `expectedProtocolVersion:integer!`, `expectedProfileId:string!`, `expectedProtocolReleaseManifestSha256:Sha256!` |

`OperationCancelCommand`、`LoadCancellationCommand`、`LoadFinalConfirmation`、`UnloadCommand`、`SublotAccepted`、`OperationCommandAck`、`OperationResultAck`、`LoadCompensationCommandAck`、`WireToGateExecutionSnapshot`、`DepartureSafetyRevoked` 和 `OnboardCapabilitySnapshot` 必须各有一条 `PROFILE_MESSAGE_NOT_ALLOWED` 非法样例，且绝不能出现在允许 messageType 枚举中。

### 4. 关联、去重与持久承诺的机器规则

1. manifest 为每个 messageType 声明 `sender`、`receiver`、`deliveryClass`、`correlationRule`、`transportDedupKey=messageId`、`businessDedupKeys`、`durableBeforeSend`、`durableBeforeAck` 和 `recoveryRole`。上表外不得由实现自行推导。
2. 所有可靠消息接收方必须先保存完整规范化消息、MessageId、内容 SHA-256 和承担的处理责任，再发 `DurableAck`；所有命令发送方必须先保存意图。所有请求保存首次规范化请求与首次响应，相同 MessageId/同内容返回原响应，相同 MessageId/异内容拒绝。
3. 业务二次键固定为：Demand=`demandId`；同键永久防重=`transportDemandKey`；仓位操作=`slotOperationAttemptId`；发车检查=`preDepartureSafetyCheckId`；纠错=`correctionId`；取消=`cancellationId`；恢复选择=`recoveryActionId`；异常会话=`exceptionRecoverySessionId`；强制处置围栏=`forcedRecoveryGeneration`。同业务键异内容必须 `BUSINESS_ID_CONTENT_CONFLICT`。
4. 快照同 kind 的 revision 只能单调增加；同 revision 同内容幂等确认，同 revision 异内容为 `SNAPSHOT_REVISION_CONTENT_CONFLICT`，回退为 `SNAPSHOT_REVISION_REGRESSION`。Heartbeat 不承诺业务事实；OperationProgress 不补发、不入账。
5. RecoveryHandshake 的向量必须严格证明：SessionHello/Accepted → CapabilitySnapshot → SafetyStateSnapshot（需要时）→ RecoveryStateReport → 原 MessageId 的积压结果补报及 DurableAck → SessionReadiness。中途断线使用新 sessionGeneration 从头开始，但业务 ID 与待补报 MessageId 不变。

### 5. 稳定错误码 registry

最小 registry 必须包含并冻结以下代码；每项记录 `code`、`category`、`meaning`、`allowedMessageTypes`、`retryDisposition` 与 `introducedInRelease`：

- 协议：`PROTOCOL_ENVELOPE_INVALID`、`PROTOCOL_SCHEMA_INVALID`、`UNSUPPORTED_PROTOCOL_VERSION`、`PROTOCOL_RELEASE_IDENTITY_MISMATCH`、`UNKNOWN_MESSAGE_TYPE`、`PROFILE_MESSAGE_NOT_ALLOWED`、`MESSAGE_ID_CONTENT_CONFLICT`、`CORRELATION_INVALID`、`CONTENT_HASH_MISMATCH`。
- 会话/快照：`VEHICLE_CREDENTIAL_INVALID`、`AGV_ID_MISMATCH`、`STALE_SESSION_GENERATION`、`DUPLICATE_ACTIVE_SESSION`、`HANDSHAKE_SEQUENCE_INVALID`、`CAPABILITY_VERSION_GAP`、`SAFETY_STATE_VERSION_GAP`、`SNAPSHOT_REVISION_REGRESSION`、`SNAPSHOT_REVISION_CONTENT_CONFLICT`、`SESSION_RECOVERY_REQUIRED`。
- 业务：`BUSINESS_ID_CONTENT_CONFLICT`、`VEHICLE_NOT_READY`、`DEMAND_NOT_CURRENT`、`OPERATION_SESSION_MISMATCH`、`STATION_MISMATCH`、`WORKLIST_REVISION_STALE`、`SUBLOT_MISMATCH`、`SLOT_SET_INVALID`、`EXPECTED_BASKET_COUNT_MISMATCH`、`SLOT_OPERATION_CONFLICT`、`ACTION_NOT_ALLOWED_IN_STATE`、`MANUAL_CHARGING_HOLD_ACTIVE`。
- 安全/恢复：`CAPABILITY_UNKNOWN`、`SLOT_INOPERABLE`、`SLOT_STATE_UNKNOWN`、`LOCK_NOT_CLOSED`、`UNLOCK_OUTPUT_NOT_RESET`、`DEPARTURE_UNSAFE`、`PREDEPARTURE_CHECK_EXPIRED`、`RECOVERY_SESSION_NOT_OPEN`、`RECOVERY_SCOPE_MISMATCH`、`RECOVERY_CHECKPOINT_NOT_UNIQUE`、`RECOVERY_AUTHENTICATION_FAILED`、`FORCED_RECOVERY_GENERATION_STALE`。

错误码只能追加；删除、改义、换 category 或改变 retryDisposition 属于破坏性变更。文案可本地化但不得参与判断。

### 6. 样例和一致性向量

1. 每个允许 messageType 至少有一个完整合法 envelope 样例 `V-<messageType>-MIN-001`；每个 required、类型、枚举、nullable、数组唯一/排序、关联和跨字段约束至少有一个只破坏该约束的非法样例 `I-<messageType>-<constraint>-NNN`，expected 中必须写唯一错误码和 JSON Pointer。秘密字段只用显式无效占位符。
2. 每个禁止/旧名称消息各有 `I-PROFILE-<name>-001`；未知 messageType、未知 ProtocolVersion、旧 sessionGeneration、release identity/hash 不符各有单独 envelope 向量。
3. 必须发布以下状态轨迹向量：`CV-SESSION-RECOVERY-HAPPY`、`CV-SESSION-RECONNECT-DURING-RECOVERY`、`CV-RELIABLE-RETRY-SAME-CONTENT`、`CV-RELIABLE-RETRY-DIFFERENT-CONTENT`、`CV-REQUEST-FIRST-RESULT-REPLAY`、`CV-SNAPSHOT-REPLACE-AND-ACK`、`CV-SNAPSHOT-SAME-REVISION-CONFLICT`、`CV-PICKUP-SUBLOT-LOAD`、`CV-LOAD-CORRECTION`、`CV-LOAD-CANCELLATION-ALL-EMPTY`、`CV-PREDEPARTURE-SAFETY-EXPIRES`、`CV-GATE-UNLOAD-ALL-EMPTY`、`CV-CONNECTION-LOSS-SAFE-FINISH`、`CV-OPERATION-RESULT-UNKNOWN-RECONCILE`、`CV-EXCEPTION-RESUME`、`CV-EXCEPTION-COMPENSATE`、`CV-FAULT-CARGO-HANDOFF`、`CV-FORCED-MECHANICAL-RECOVERY`、`CV-MANUAL-CHARGING-RETURN`。每个 expected 固定逐步输出消息、持久事实、不可发生的副作用、最终 readiness/业务/物理状态和稳定错误码。
4. 后续《决定双仓库一致性门禁、模拟对端与联调切片》只能决定这些共同向量如何被双 Fake 和 IntegrationSliceId 消费，不得另造字段或改变本票向量结论。

### 7. 变更治理、批准和失败边界

1. 每个变更先形成 `ProtocolChangeProposal`，记录精确 base identity、目标 identity、逐文件/逐字段差异、兼容分类、状态机/安全/持久化/恢复影响、两端迁移和新增/修改向量。只有旧接收方忽略后仍得到相同安全与业务结论、缺失不改变旧行为、且不进入权威或去重判断的新增可选字段，才是同 ProtocolVersion 的兼容增加。
2. 新增/删除 required，收窄或改写类型/枚举/字段含义，改变缺失语义、方向、交付类别、去重、持久承诺、恢复顺序、错误码语义、强制步骤或副作用，全部是破坏性变更，必须提升 ProtocolVersion 和 release major；不进行范围协商或尽量兼容。
3. 每个候选 release 必须由 ControlServer 开发者本人和 OnboardHmi 开发者本人分别确认精确 commit 与 manifest；依地图产品治理，批准记录还必须包含用户与车载端开发同事本人对共同 release 的确认。若用户同时是 ControlServer 开发负责人，可在记录中明确兼任；否则服务端开发负责人仍须本人确认。AI 只能生成候选、差异和检查证据，不能代签、推断沉默同意或复用《验证 OnboardHmi 单场景操作原型》的单票豁免。
4. `approvals/release-approval.json` 只记录批准人真实身份、角色、批准时间、精确 commit、manifestSha256、决定和外部证据指针；不得写虚构确认。本票仅决定治理规则，不构成第一个 release 的外部共同批准。
5. 缺件、哈希不符、未批准、只升级一端、Schema/向量失败或实现声明身份不符，均阻断合并与部署。运行时 ProtocolVersion 不同返回 `SessionRejected/UNSUPPORTED_PROTOCOL_VERSION`；ProtocolVersion 相同但 release identity 不同返回 `SessionRejected/PROTOCOL_RELEASE_IDENTITY_MISMATCH`，不授予 sessionGeneration 或 VehicleBusinessReadiness。
6. 历史 tag、commit、manifest、Schema、样例、向量和批准记录永久保留，不删除、不覆盖、不强推。缺陷只能由新 release supersede；旧 release 可标记 deprecated 或 revoked。revoked release 禁止新部署，已部署实例必须另有显式迁移决定，不能静默继续或自动改写历史证据。

本票没有创建远程仓库、发布 tag 或生成可宣称已批准的协议 release；这些都属于后续实施及真实人员批准边界。
