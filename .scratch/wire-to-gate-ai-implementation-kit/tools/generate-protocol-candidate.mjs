import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const target = process.argv[2];
if (!target) throw new Error("Usage: node generate-protocol-candidate.mjs <protocol-repository>");

const root = path.resolve(target);
const SCHEMA = "https://json-schema.org/draft/2020-12/schema";
const BASE_ID = "https://schemas.8005-agv.local/wire-to-gate/v1";
const candidateVersion = "0.1.0";
const profileId = "WIRE_TO_GATE_MVP";
const protocolVersion = 1;

const writeJson = (relative, value) => {
  const file = path.join(root, relative);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, "utf8");
};
const writeText = (relative, value) => {
  const file = path.join(root, relative);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, value.replace(/\r\n/g, "\n"), "utf8");
};
const clone = (value) => structuredClone(value);
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const canonical = (value) => {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
};

const R = (name) => ({ $ref: `${BASE_ID}/common/types.schema.json#/$defs/${name}` });
const S = (options = {}) => ({ type: "string", minLength: 1, ...options });
const I = (options = {}) => ({ type: "integer", ...options });
const N = (options = {}) => ({ type: "number", ...options });
const B = (options = {}) => ({ type: "boolean", ...options });
const E = (...values) => ({ type: "string", enum: values });
const A = (items, options = {}) => ({ type: "array", items, ...options });
const O = (properties, options = {}) => ({
  type: "object",
  properties,
  required: Object.keys(properties),
  additionalProperties: false,
  ...options,
});
const Nullable = (schema) => ({ anyOf: [schema, { type: "null" }] });
const Slots = () => ({ ...A(R("SlotNo"), { minItems: 1, maxItems: 8, uniqueItems: true }), "x-sortedAscending": true });
const StringArray = (options = {}) => A(S(), { ...options });

const requiredErrorCodes = [
  ["PROTOCOL_ENVELOPE_INVALID", "PROTOCOL", "NEVER"],
  ["PROTOCOL_SCHEMA_INVALID", "PROTOCOL", "NEVER"],
  ["UNSUPPORTED_PROTOCOL_VERSION", "PROTOCOL", "NEVER"],
  ["PROTOCOL_RELEASE_IDENTITY_MISMATCH", "PROTOCOL", "NEVER"],
  ["UNKNOWN_MESSAGE_TYPE", "PROTOCOL", "NEVER"],
  ["PROFILE_MESSAGE_NOT_ALLOWED", "PROTOCOL", "NEVER"],
  ["MESSAGE_ID_CONTENT_CONFLICT", "PROTOCOL", "MANUAL_REVIEW"],
  ["CORRELATION_INVALID", "PROTOCOL", "NEW_MESSAGE_ID"],
  ["CONTENT_HASH_MISMATCH", "PROTOCOL", "NEVER"],
  ["VEHICLE_CREDENTIAL_INVALID", "SESSION", "MANUAL_REVIEW"],
  ["AGV_ID_MISMATCH", "SESSION", "MANUAL_REVIEW"],
  ["STALE_SESSION_GENERATION", "SESSION", "AFTER_RECONNECT"],
  ["DUPLICATE_ACTIVE_SESSION", "SESSION", "AFTER_RECONNECT"],
  ["HANDSHAKE_SEQUENCE_INVALID", "SESSION", "AFTER_RECONNECT"],
  ["CAPABILITY_VERSION_GAP", "SESSION", "AFTER_STATE_CHANGE"],
  ["SAFETY_STATE_VERSION_GAP", "SESSION", "AFTER_STATE_CHANGE"],
  ["SNAPSHOT_REVISION_REGRESSION", "SESSION", "AFTER_STATE_CHANGE"],
  ["SNAPSHOT_REVISION_CONTENT_CONFLICT", "SESSION", "MANUAL_REVIEW"],
  ["SESSION_RECOVERY_REQUIRED", "SESSION", "AFTER_STATE_CHANGE"],
  ["BUSINESS_ID_CONTENT_CONFLICT", "BUSINESS", "MANUAL_REVIEW"],
  ["VEHICLE_NOT_READY", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["DEMAND_NOT_CURRENT", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["OPERATION_SESSION_MISMATCH", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["STATION_MISMATCH", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["WORKLIST_REVISION_STALE", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["SUBLOT_MISMATCH", "BUSINESS", "NEW_MESSAGE_ID"],
  ["SLOT_SET_INVALID", "BUSINESS", "NEW_MESSAGE_ID"],
  ["EXPECTED_BASKET_COUNT_MISMATCH", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["SLOT_OPERATION_CONFLICT", "BUSINESS", "MANUAL_REVIEW"],
  ["ACTION_NOT_ALLOWED_IN_STATE", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["MANUAL_CHARGING_HOLD_ACTIVE", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["CAPABILITY_UNKNOWN", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["SLOT_INOPERABLE", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["SLOT_STATE_UNKNOWN", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["LOCK_NOT_CLOSED", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["UNLOCK_OUTPUT_NOT_RESET", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["DEPARTURE_UNSAFE", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["PREDEPARTURE_CHECK_EXPIRED", "SAFETY_RECOVERY", "NEW_MESSAGE_ID"],
  ["RECOVERY_SESSION_NOT_OPEN", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
  ["RECOVERY_SCOPE_MISMATCH", "SAFETY_RECOVERY", "MANUAL_REVIEW"],
  ["RECOVERY_CHECKPOINT_NOT_UNIQUE", "SAFETY_RECOVERY", "MANUAL_REVIEW"],
  ["RECOVERY_AUTHENTICATION_FAILED", "SAFETY_RECOVERY", "MANUAL_REVIEW"],
  ["FORCED_RECOVERY_GENERATION_STALE", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE"],
];
const errorCodes = requiredErrorCodes.map(([code, category, retryDisposition]) => ({
  code,
  category,
  meaning: `${code} is the stable ${category.toLowerCase()} failure defined by the accepted WIRE_TO_GATE MVP governance decision.`,
  allowedMessageTypes: category === "PROTOCOL" ? ["ProtocolProblem", "SessionRejected"] : ["*"],
  retryDisposition,
  introducedInRelease: candidateVersion,
}));
const errorCodeNames = errorCodes.map((item) => item.code);

const defs = {
  Id: S({ format: "uuid", examples: ["00000000-0000-4000-8000-000000000001"] }),
  Revision: I({ minimum: 0, examples: [1] }),
  Generation: I({ minimum: 0, examples: [1] }),
  Instant: S({ format: "date-time", examples: ["2026-08-25T09:00:00Z"] }),
  Sha256: S({ pattern: "^[0-9a-f]{64}$", examples: ["0".repeat(64)] }),
  CommitSha: S({ pattern: "^[0-9a-f]{40}$", examples: ["0".repeat(40)] }),
  SlotNo: I({ minimum: 1, maximum: 8, examples: [1] }),
  ErrorCode: S({ enum: errorCodeNames, examples: ["ACTION_NOT_ALLOWED_IN_STATE"] }),
};
defs.ProtocolReleaseIdentity = O({
  repository: S({ const: "8005-agv-protocol" }),
  releaseVersion: S({ pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$", examples: [candidateVersion] }),
  tag: S({ pattern: "^protocol-v", examples: [`protocol-v${candidateVersion}`] }),
  commit: R("CommitSha"),
  protocolVersion: I({ const: protocolVersion }),
  profileId: S({ const: profileId }),
  manifestSha256: R("Sha256"),
  schemaBundleSha256: R("Sha256"),
  vectorsSha256: R("Sha256"),
});
defs.Problem = O({ reasonCode: R("ErrorCode"), fieldPath: Nullable(S()), displayMessage: Nullable(S()) });
defs.SlotState = O({
  slotNo: R("SlotNo"),
  operability: E("OPERABLE", "INOPERABLE", "UNKNOWN"),
  administrativeAvailability: E("ENABLED", "DISABLE_PENDING", "DISABLED"),
  physicalState: E("EMPTY", "OCCUPIED", "UNKNOWN"),
  lockState: E("LOCKED", "UNLOCKED", "UNKNOWN"),
  unlockOutputState: E("RESET", "ACTIVE", "UNKNOWN"),
  reasonCodes: A(R("ErrorCode"), { uniqueItems: true }),
});
defs.SlotResult = O({
  slotNo: R("SlotNo"),
  outcome: E("COMPLETED", "FAILED", "NOT_STARTED", "UNKNOWN"),
  finalPhysicalState: E("EMPTY", "OCCUPIED", "UNKNOWN"),
  lockState: E("LOCKED", "UNLOCKED", "UNKNOWN"),
  unlockOutputState: E("RESET", "ACTIVE", "UNKNOWN"),
  reasonCodes: A(R("ErrorCode"), { uniqueItems: true }),
});
defs.SafetySummary = O({
  departureSafe: B(), vehicleStopped: B(), allTargetSlotsLocked: B(), allUnlockOutputsReset: B(), unknownPresent: B(), reasonCodes: A(R("ErrorCode"), { uniqueItems: true }),
});
defs.OperatorContext = O({ operatorId: S(), verificationMethod: E("BADGE", "SESSION"), verifiedAt: R("Instant") });
defs.PendingResultRef = O({ messageType: S(), messageId: R("Id"), businessId: S(), contentSha256: R("Sha256") });
defs.BlockingFact = O({ reasonCode: R("ErrorCode"), subjectType: S(), subjectId: Nullable(S()) });
defs.SlotNoArray = Slots();

const responseNames = new Set([
  "SessionAccepted", "SessionRejected", "HeartbeatAck", "PreDepartureSafetyCheckResult", "SublotRejected", "SlotOperationCommandRejected", "ManualChargingReturnToServiceResult",
  "LoadCorrectionRejected", "LoadCancellationAuthorization", "LoadCompensationRejected", "ExceptionRecoverySessionOpened", "ExceptionRecoverySessionRejected", "RecoveryActionAccepted",
  "RecoveryActionRejected", "HardwareRecoveryRecordResult", "DurableAck", "SnapshotAppliedAck", "ProtocolProblem",
]);
const requestNames = new Set([
  "SessionHello", "CapabilitySnapshotRequested", "SafetyStateSnapshotRequested", "PreDepartureSafetyCheck", "SublotSubmitted", "ManualChargingReturnToServiceRequested",
  "LoadCorrectionRequested", "LoadCancellationStartRequested", "LoadCompensationRequested", "ExceptionRecoverySessionRequested", "RecoveryActionSubmitted", "HardwareRecoveryRecordSubmitted",
]);
const snapshotNames = new Set(["CapabilitySnapshot", "SafetyStateSnapshot", "VehicleBusinessStateSnapshot", "CurrentStopWorklistSnapshot", "UpcomingStopPlanSnapshot", "ExceptionRecoverySessionSnapshot"]);
const telemetryNames = new Set(["OperationProgress"]);
const livenessNames = new Set(["Heartbeat", "HeartbeatAck"]);
const reliableNames = new Set([
  "RecoveryStateReport", "SessionReadiness", "SafetyStateChanged", "SublotEntryRequested", "SlotOperationCommand", "OperationResult", "LoadCorrectionCommand", "LoadCorrectionResult",
  "LoadCancellationResult", "LoadCompensationCommand", "LoadCompensationResult", "SlotOperationResumeCommand", "FaultCargoRecoveryCommand", "FaultCargoRecoveryResult",
  "ForcedMechanicalRecoveryCommand", "ForcedMechanicalRecoveryResult",
]);

const directions = {
  SessionHello: "O_TO_C", SessionAccepted: "C_TO_O", SessionRejected: "C_TO_O", Heartbeat: "O_TO_C", HeartbeatAck: "C_TO_O",
  CapabilitySnapshotRequested: "C_TO_O", CapabilitySnapshot: "O_TO_C", RecoveryStateReport: "O_TO_C", SessionReadiness: "C_TO_O", SafetyStateChanged: "O_TO_C",
  SafetyStateSnapshotRequested: "C_TO_O", SafetyStateSnapshot: "O_TO_C", PreDepartureSafetyCheck: "C_TO_O", PreDepartureSafetyCheckResult: "O_TO_C",
  VehicleBusinessStateSnapshot: "C_TO_O", CurrentStopWorklistSnapshot: "C_TO_O", UpcomingStopPlanSnapshot: "C_TO_O", SublotEntryRequested: "C_TO_O", SublotSubmitted: "O_TO_C",
  SublotRejected: "C_TO_O", SlotOperationCommand: "C_TO_O", SlotOperationCommandRejected: "O_TO_C", OperationProgress: "O_TO_C", OperationResult: "O_TO_C",
  ManualChargingReturnToServiceRequested: "O_TO_C", ManualChargingReturnToServiceResult: "C_TO_O", LoadCorrectionRequested: "O_TO_C", LoadCorrectionRejected: "C_TO_O",
  LoadCorrectionCommand: "C_TO_O", LoadCorrectionResult: "O_TO_C", LoadCancellationStartRequested: "O_TO_C", LoadCancellationAuthorization: "C_TO_O", LoadCancellationResult: "O_TO_C",
  LoadCompensationRequested: "O_TO_C", LoadCompensationRejected: "C_TO_O", LoadCompensationCommand: "C_TO_O", LoadCompensationResult: "O_TO_C",
  ExceptionRecoverySessionRequested: "O_TO_C", ExceptionRecoverySessionOpened: "C_TO_O", ExceptionRecoverySessionRejected: "C_TO_O", ExceptionRecoverySessionSnapshot: "C_TO_O",
  RecoveryActionSubmitted: "O_TO_C", RecoveryActionAccepted: "C_TO_O", RecoveryActionRejected: "C_TO_O", HardwareRecoveryRecordSubmitted: "O_TO_C", HardwareRecoveryRecordResult: "C_TO_O",
  SlotOperationResumeCommand: "C_TO_O", FaultCargoRecoveryCommand: "C_TO_O", FaultCargoRecoveryResult: "O_TO_C", ForcedMechanicalRecoveryCommand: "C_TO_O", ForcedMechanicalRecoveryResult: "O_TO_C",
  DurableAck: "BIDIRECTIONAL", SnapshotAppliedAck: "BIDIRECTIONAL", ProtocolProblem: "BIDIRECTIONAL",
};

const specs = {};
const add = (name, fields, options = {}) => {
  const deliveryClass = requestNames.has(name) ? "REQUEST" : responseNames.has(name) ? "RESPONSE" : snapshotNames.has(name) ? "SNAPSHOT" : telemetryNames.has(name) ? "TELEMETRY" : livenessNames.has(name) ? "LIVENESS" : "RELIABLE";
  specs[name] = { name, fields, direction: directions[name], deliveryClass, businessDedupKeys: options.businessDedupKeys ?? [], recoveryRole: options.recoveryRole ?? "NONE", crossRules: options.crossRules ?? [] };
};

add("SessionHello", { onboardInstanceId: R("Id"), onboardBuildCommit: S(), supportedProtocolVersion: I({ const: 1 }), profileId: S({ const: profileId }), protocolReleaseIdentity: R("ProtocolReleaseIdentity"), credentialProof: S({ examples: ["INVALID-PLACEHOLDER-NOT-A-SECRET"] }) }, { recoveryRole: "HANDSHAKE_START" });
add("SessionAccepted", { sessionGeneration: R("Generation"), serverInstanceId: R("Id"), serverBuildCommit: S(), acceptedProtocolReleaseIdentity: R("ProtocolReleaseIdentity"), acceptedAt: R("Instant") }, { recoveryRole: "SESSION_FENCE" });
add("SessionRejected", { problem: R("Problem"), expectedProtocolVersion: I({ const: 1 }), expectedProtocolReleaseIdentity: Nullable(R("ProtocolReleaseIdentity")) });
add("Heartbeat", { capabilityVersion: R("Revision"), safetyStateVersion: R("Revision") });
add("HeartbeatAck", { receivedHeartbeatMessageId: R("Id"), serverTime: R("Instant") });
add("CapabilitySnapshotRequested", { requestedCapabilityVersion: Nullable(R("Revision")), reason: E("HANDSHAKE", "VERSION_GAP", "EXPLICIT_RECONCILIATION") }, { recoveryRole: "CAPABILITY_RECONCILIATION" });
add("CapabilitySnapshot", { capabilityVersion: R("Revision"), observedAt: R("Instant"), slotModelVersion: S(), activeSlotConfigurationVersion: S(), slotStates: A(R("SlotState"), { minItems: 8, maxItems: 8, uniqueItems: true }), supportsBatchUnlock: B(), onboardJournalFormatVersion: I({ minimum: 1 }) }, { recoveryRole: "CAPABILITY_RECONCILIATION" });
add("RecoveryStateReport", { reportId: R("Id"), observedAt: R("Instant"), unsettledSlotOperationAttemptId: Nullable(R("Id")), provenRecoveryCheckpoint: E("NONE", "PREPARED", "ACTIVE_UNLOCK_SET", "SAFE_FINISH_REACHED", "RESULT_RECORDED"), activeUnlockSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), forcedRecoveryGeneration: R("Generation"), pendingResults: A(R("PendingResultRef"), { uniqueItems: true }), journalContentSha256: R("Sha256") }, { businessDedupKeys: ["reportId"], recoveryRole: "JOURNAL_RECONCILIATION" });
add("SessionReadiness", { readiness: E("READY", "RECOVERY_REQUIRED"), decidedAt: R("Instant"), reasonCodes: A(R("ErrorCode"), { uniqueItems: true }), acceptedCapabilityVersion: R("Revision"), acceptedSafetyStateVersion: R("Revision"), vehicleBusinessStateRevision: R("Revision") }, { recoveryRole: "HANDSHAKE_DECISION" });
add("SafetyStateChanged", { safetyStateVersion: R("Revision"), observedAt: R("Instant"), safety: R("SafetySummary"), affectedSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }) }, { recoveryRole: "SAFETY_RECONCILIATION" });
add("SafetyStateSnapshotRequested", { requestedSafetyStateVersion: Nullable(R("Revision")), reason: E("HANDSHAKE", "VERSION_GAP", "PRE_MOVEMENT_RECONCILIATION") }, { recoveryRole: "SAFETY_RECONCILIATION" });
add("SafetyStateSnapshot", { safetyStateVersion: R("Revision"), observedAt: R("Instant"), safety: R("SafetySummary"), slotStates: A(R("SlotState"), { minItems: 8, maxItems: 8, uniqueItems: true }) }, { recoveryRole: "SAFETY_RECONCILIATION" });
add("PreDepartureSafetyCheck", { preDepartureSafetyCheckId: R("Id"), demandId: R("Id"), movementLegId: R("Id"), expectedSafetyStateVersion: R("Revision"), targetStationId: S() }, { businessDedupKeys: ["preDepartureSafetyCheckId"] });
add("PreDepartureSafetyCheckResult", { preDepartureSafetyCheckId: R("Id"), outcome: E("SAFE", "UNSAFE", "UNKNOWN"), observedAt: R("Instant"), safetyStateVersion: R("Revision"), validUntil: R("Instant"), safety: R("SafetySummary") }, { businessDedupKeys: ["preDepartureSafetyCheckId"] });
add("VehicleBusinessStateSnapshot", { vehicleBusinessStateRevision: R("Revision"), readiness: E("READY", "RECOVERY_REQUIRED"), manualChargingHold: B(), batteryState: E("SUFFICIENT", "LOW", "UNKNOWN"), blockingFacts: A(R("BlockingFact"), { uniqueItems: true }), observedAt: R("Instant") });
add("CurrentStopWorklistSnapshot", { stationId: S(), worklistRevision: R("Revision"), operationSessionId: Nullable(R("Id")), items: A(O({ demandId: R("Id"), transportDemandKey: S(), sublot: S(), workType: S({ const: "WIRE_TO_GATE" }), stopRole: E("PICKUP", "GATE"), expectedBasketCount: I({ minimum: 1, maximum: 8 }) }), { maxItems: 1 }) }, { businessDedupKeys: ["items[].demandId", "items[].transportDemandKey"] });
add("UpcomingStopPlanSnapshot", { planRevision: R("Revision"), demandId: Nullable(R("Id")), legs: A(O({ movementLegId: R("Id"), legType: E("TO_PICKUP", "TO_GATE"), sequence: I({ minimum: 1, maximum: 2 }), stationId: S(), mapId: S(), state: E("PLANNED", "ACTIVE", "ARRIVED", "COMPLETED", "BLOCKED") }), { maxItems: 2, uniqueItems: true, "x-sortedBy": "sequence" }) }, { businessDedupKeys: ["demandId"] });
add("SublotEntryRequested", { demandId: R("Id"), operationSessionId: R("Id"), stationId: S(), worklistRevision: R("Revision"), expectedSublot: S(), entryMethods: A(S(), { const: ["SCANNER", "KEYBOARD"] }), expiresOnRevisionChange: B({ const: true }) }, { businessDedupKeys: ["demandId", "operationSessionId"] });
add("SublotSubmitted", { demandId: R("Id"), operationSessionId: R("Id"), stationId: S(), worklistRevision: R("Revision"), sublot: S(), entryMethod: E("SCANNER", "KEYBOARD"), operator: R("OperatorContext") }, { businessDedupKeys: ["demandId", "operationSessionId"] });
add("SublotRejected", { demandId: R("Id"), operationSessionId: R("Id"), problem: R("Problem"), currentWorklistRevision: R("Revision") }, { businessDedupKeys: ["demandId", "operationSessionId"] });
add("SlotOperationCommand", { demandId: R("Id"), operationSessionId: R("Id"), slotOperationAttemptId: R("Id"), operationType: E("LOAD", "UNLOAD"), slots: Slots(), expectedBasketCount: I({ minimum: 1, maximum: 8 }), expectedFinalPhysicalState: E("OCCUPIED", "EMPTY"), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["demandId", "slotOperationAttemptId"], recoveryRole: "SLOT_OPERATION" });
add("SlotOperationCommandRejected", { slotOperationAttemptId: R("Id"), problem: R("Problem"), observedCapabilityVersion: R("Revision"), conflictingContentSha256: Nullable(R("Sha256")) }, { businessDedupKeys: ["slotOperationAttemptId"] });
add("OperationProgress", { slotOperationAttemptId: R("Id"), phase: E("PREPARING", "UNLOCKING", "WAITING_OPERATOR", "VERIFYING", "SAFE_FINISH", "PAUSED"), activeUnlockSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), completedSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), observedAt: R("Instant") }, { businessDedupKeys: ["slotOperationAttemptId"] });
add("OperationResult", { demandId: R("Id"), slotOperationAttemptId: R("Id"), operationType: E("LOAD", "UNLOAD"), overallOutcome: E("COMPLETED", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant"), journalCheckpoint: S(), resultContentSha256: R("Sha256") }, { businessDedupKeys: ["demandId", "slotOperationAttemptId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("ManualChargingReturnToServiceRequested", { requestId: R("Id"), administrator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), reason: S(), observedBatteryPercent: Nullable(N({ minimum: 0, maximum: 100 })) }, { businessDedupKeys: ["requestId"] });
add("ManualChargingReturnToServiceResult", { requestId: R("Id"), outcome: E("RETURNED_TO_ELIGIBILITY_EVALUATION", "REJECTED"), problem: Nullable(R("Problem")), vehicleBusinessStateRevision: R("Revision") }, { businessDedupKeys: ["requestId"] });
add("LoadCorrectionRequested", { correctionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slots: Slots(), operator: R("OperatorContext"), reason: S() }, { businessDedupKeys: ["correctionId", "demandId", "slotOperationAttemptId"] });
add("LoadCorrectionRejected", { correctionId: R("Id"), problem: R("Problem") }, { businessDedupKeys: ["correctionId"] });
add("LoadCorrectionCommand", { correctionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slots: Slots(), expectedSequence: A(S(), { const: ["EMPTY", "OCCUPIED"] }), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["correctionId", "demandId", "slotOperationAttemptId"], recoveryRole: "LOAD_CORRECTION" });
add("LoadCorrectionResult", { correctionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), overallOutcome: E("COMPLETED", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant") }, { businessDedupKeys: ["correctionId", "demandId", "slotOperationAttemptId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("LoadCancellationStartRequested", { cancellationId: R("Id"), demandId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), operator: R("OperatorContext"), reason: S() }, { businessDedupKeys: ["cancellationId", "demandId"] });
add("LoadCancellationAuthorization", { cancellationId: R("Id"), decision: E("AUTHORIZED", "REJECTED"), demandId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), slots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), problem: Nullable(R("Problem")) }, { businessDedupKeys: ["cancellationId", "demandId"] });
add("LoadCancellationResult", { cancellationId: R("Id"), demandId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), overallOutcome: E("ALL_EMPTY", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant") }, { businessDedupKeys: ["cancellationId", "demandId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("LoadCompensationRequested", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), operator: R("OperatorContext") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId", "demandId", "slotOperationAttemptId"] });
add("LoadCompensationRejected", { recoveryActionId: R("Id"), problem: R("Problem") }, { businessDedupKeys: ["recoveryActionId"] });
add("LoadCompensationCommand", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slots: Slots(), expectedFinalPhysicalState: S({ const: "EMPTY" }), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId", "demandId", "slotOperationAttemptId"], recoveryRole: "LOAD_COMPENSATION" });
add("LoadCompensationResult", { recoveryActionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), overallOutcome: E("ALL_EMPTY", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant") }, { businessDedupKeys: ["recoveryActionId", "demandId", "slotOperationAttemptId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("ExceptionRecoverySessionRequested", { requestId: R("Id"), administrator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), eventId: R("Id"), demandId: Nullable(R("Id")), slots: Slots(), reason: S(), authenticationProof: S({ examples: ["INVALID-PLACEHOLDER-NOT-A-SECRET"] }) }, { businessDedupKeys: ["requestId", "eventId"], recoveryRole: "EXCEPTION_SESSION" });
add("ExceptionRecoverySessionOpened", { requestId: R("Id"), exceptionRecoverySessionId: R("Id"), openedAt: R("Instant"), eventId: R("Id"), demandId: Nullable(R("Id")), slots: Slots(), recoverySessionRevision: R("Revision") }, { businessDedupKeys: ["requestId", "exceptionRecoverySessionId", "eventId"], recoveryRole: "EXCEPTION_SESSION" });
add("ExceptionRecoverySessionRejected", { requestId: R("Id"), problem: R("Problem") }, { businessDedupKeys: ["requestId"] });
add("ExceptionRecoverySessionSnapshot", { exceptionRecoverySessionId: R("Id"), recoverySessionRevision: R("Revision"), state: E("OPEN", "ACTION_SELECTED", "EXECUTING", "CLOSED"), administratorId: S(), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), eventId: R("Id"), demandId: Nullable(R("Id")), slots: Slots(), selectedAction: Nullable(E("RESUME_AFTER_REPAIR", "COMPENSATE_LOAD_ALL_EMPTY", "FAULT_CARGO_HANDOFF", "FORCED_MECHANICAL_RECOVERY")), allowedActions: A(E("RESUME_AFTER_REPAIR", "COMPENSATE_LOAD_ALL_EMPTY", "FAULT_CARGO_HANDOFF", "FORCED_MECHANICAL_RECOVERY"), { uniqueItems: true }), blockingFacts: A(R("BlockingFact"), { uniqueItems: true }) }, { businessDedupKeys: ["exceptionRecoverySessionId", "eventId"], recoveryRole: "EXCEPTION_SESSION" });
add("RecoveryActionSubmitted", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), action: E("RESUME_AFTER_REPAIR", "COMPENSATE_LOAD_ALL_EMPTY", "FAULT_CARGO_HANDOFF", "FORCED_MECHANICAL_RECOVERY"), eventId: R("Id"), demandId: Nullable(R("Id")), slots: Slots(), operator: R("OperatorContext"), reason: S() }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId", "eventId"], recoveryRole: "RECOVERY_ACTION" });
add("RecoveryActionAccepted", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), acceptedAction: E("RESUME_AFTER_REPAIR", "COMPENSATE_LOAD_ALL_EMPTY", "FAULT_CARGO_HANDOFF", "FORCED_MECHANICAL_RECOVERY"), recoverySessionRevision: R("Revision"), acceptedAt: R("Instant") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId"], recoveryRole: "RECOVERY_ACTION" });
add("RecoveryActionRejected", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), problem: R("Problem"), recoverySessionRevision: R("Revision") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId"] });
add("HardwareRecoveryRecordSubmitted", { recordId: R("Id"), exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), operator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), slots: Slots(), checksPerformed: StringArray({ minItems: 1, uniqueItems: true }), actionsPerformed: StringArray({ minItems: 1, uniqueItems: true }), observations: StringArray({ minItems: 1 }), observedAt: R("Instant") }, { businessDedupKeys: ["recordId", "exceptionRecoverySessionId", "recoveryActionId"], recoveryRole: "HARDWARE_RECORD" });
add("HardwareRecoveryRecordResult", { recordId: R("Id"), outcome: E("RECORDED", "REJECTED"), problem: Nullable(R("Problem")), recoverySessionRevision: R("Revision") }, { businessDedupKeys: ["recordId"] });
add("SlotOperationResumeCommand", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), provenRecoveryCheckpoint: E("PREPARED", "ACTIVE_UNLOCK_SET", "SAFE_FINISH_REACHED"), slots: Slots(), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "demandId", "slotOperationAttemptId"], recoveryRole: "RESUME" });
add("FaultCargoRecoveryCommand", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: R("Id"), slots: Slots(), handoffId: R("Id"), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "demandId", "handoffId"], recoveryRole: "FAULT_CARGO_HANDOFF" });
add("FaultCargoRecoveryResult", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: R("Id"), handoffId: R("Id"), overallOutcome: E("HANDED_OFF", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), operator: R("OperatorContext"), observedAt: R("Instant") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "demandId", "handoffId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("ForcedMechanicalRecoveryCommand", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: Nullable(R("Id")), forcedRecoveryGeneration: R("Generation"), slots: Slots(), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "forcedRecoveryGeneration"], recoveryRole: "FORCED_MECHANICAL_RECOVERY" });
add("ForcedMechanicalRecoveryResult", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), forcedRecoveryGeneration: R("Generation"), outcome: E("MECHANICALLY_ISOLATED", "FAILED", "UNKNOWN"), slots: Slots(), operator: R("OperatorContext"), observedAt: R("Instant"), electronicEmptyProven: B({ const: false }), vehicleReadyProven: B({ const: false }) }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "forcedRecoveryGeneration"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("DurableAck", { acceptedMessageId: R("Id"), acceptedMessageType: S(), acceptedContentSha256: R("Sha256"), durablyAcceptedAt: R("Instant") }, { businessDedupKeys: ["acceptedMessageId"], recoveryRole: "DURABLE_ACCEPTANCE" });
add("SnapshotAppliedAck", { snapshotMessageId: R("Id"), snapshotKind: E("CAPABILITY", "SAFETY_STATE", "VEHICLE_BUSINESS_STATE", "CURRENT_STOP_WORKLIST", "UPCOMING_STOP_PLAN", "EXCEPTION_RECOVERY_SESSION"), appliedRevision: R("Revision"), appliedContentSha256: R("Sha256") }, { businessDedupKeys: ["snapshotMessageId"], recoveryRole: "SNAPSHOT_ADOPTION" });
add("ProtocolProblem", { rejectedMessageId: R("Id"), rejectedMessageType: Nullable(S()), problem: R("Problem"), expectedProtocolVersion: I({ const: 1 }), expectedProfileId: S({ const: profileId }), expectedProtocolReleaseManifestSha256: R("Sha256") });

const denylist = ["OperationCancelCommand", "LoadCancellationCommand", "LoadFinalConfirmation", "UnloadCommand", "SublotAccepted", "OperationCommandAck", "OperationResultAck", "LoadCompensationCommandAck", "WireToGateExecutionSnapshot", "DepartureSafetyRevoked", "OnboardCapabilitySnapshot"];

const commonSchema = { $schema: SCHEMA, $id: `${BASE_ID}/common/types.schema.json`, title: "WIRE_TO_GATE MVP common types", $defs: defs };
writeJson("schemas/common/types.schema.json", commonSchema);

const envelopeBase = {
  protocolVersion: I({ const: 1 }),
  profileId: S({ const: profileId }),
  protocolReleaseVersion: S({ pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$", examples: [candidateVersion] }),
  protocolReleaseManifestSha256: R("Sha256"),
  messageType: S(),
  messageId: R("Id"),
  correlationId: Nullable(R("Id")),
  agvId: S({ examples: ["AGV-8005-01"] }),
  sessionGeneration: Nullable(R("Generation")),
  sentAt: R("Instant"),
};
writeJson("schemas/envelope.schema.json", { $schema: SCHEMA, $id: `${BASE_ID}/envelope.schema.json`, title: "ProtocolEnvelope", ...O({ ...envelopeBase, payload: O({}) }) });

const correlationRuleFor = (spec) => {
  if (spec.name === "SlotOperationCommand") return "LOAD_REQUIRES_SUBLOT_CORRELATION_UNLOAD_NULL";
  if (responseNames.has(spec.name)) return "REQUIRED_ORIGINAL_MESSAGE_ID";
  return "MUST_BE_NULL";
};
const senderFor = (direction) => direction === "O_TO_C" ? "ONBOARD_HMI" : direction === "C_TO_O" ? "CONTROL_SERVER" : "EITHER";
const receiverFor = (direction) => direction === "O_TO_C" ? "CONTROL_SERVER" : direction === "C_TO_O" ? "ONBOARD_HMI" : "EITHER";

for (const spec of Object.values(specs)) {
  const correlationRule = correlationRuleFor(spec);
  const properties = {
    ...envelopeBase,
    messageType: S({ const: spec.name }),
    correlationId: correlationRule === "REQUIRED_ORIGINAL_MESSAGE_ID" ? R("Id") : correlationRule === "MUST_BE_NULL" ? { type: "null" } : Nullable(R("Id")),
    sessionGeneration: ["SessionHello", "SessionRejected"].includes(spec.name) ? { type: "null" } : R("Generation"),
    payload: O(spec.fields),
  };
  const schema = { $schema: SCHEMA, $id: `${BASE_ID}/messages/${spec.name}.schema.json`, title: spec.name, ...O(properties) };
  if (spec.name === "SlotOperationCommand") {
    schema.allOf = [
      { if: { properties: { payload: { properties: { operationType: { const: "LOAD" } }, required: ["operationType"] } } }, then: { properties: { correlationId: R("Id") } } },
      { if: { properties: { payload: { properties: { operationType: { const: "UNLOAD" } }, required: ["operationType"] } } }, then: { properties: { correlationId: { type: "null" } } } },
    ];
  }
  writeJson(`schemas/messages/${spec.name}.schema.json`, schema);
}
writeJson("schemas/bundle/protocol.schema.json", {
  $schema: SCHEMA,
  $id: `${BASE_ID}/bundle/protocol.schema.json`,
  title: "WIRE_TO_GATE MVP protocol bundle",
  oneOf: Object.keys(specs).map((name) => ({ $ref: `${BASE_ID}/messages/${name}.schema.json` })),
});

const resolveRef = (schema) => {
  if (!schema?.$ref) return schema;
  const name = schema.$ref.split("/").at(-1);
  return defs[name];
};
let uuidCounter = 1;
const uuid = () => `00000000-0000-4000-8000-${String(uuidCounter++).padStart(12, "0")}`;
const sample = (rawSchema, fieldName = "") => {
  const schema = resolveRef(rawSchema);
  if (schema.examples?.length) return clone(schema.examples[0]);
  if (schema.const !== undefined) return clone(schema.const);
  if (schema.enum?.length) return clone(schema.enum[0]);
  if (schema.anyOf) {
    const nonNull = schema.anyOf.find((item) => item.type !== "null") ?? schema.anyOf[0];
    return sample(nonNull, fieldName);
  }
  if (schema.type === "object") return Object.fromEntries((schema.required ?? Object.keys(schema.properties ?? {})).map((key) => [key, sample(schema.properties[key], key)]));
  if (schema.type === "array") {
    if (schema.const) return clone(schema.const);
    const count = Math.max(schema.minItems ?? 0, 1);
    return Array.from({ length: count }, (_, index) => {
      const value = sample(schema.items, fieldName);
      if (typeof value === "number" && /slot/i.test(fieldName)) return index + 1;
      if (typeof value === "object" && value?.slotNo !== undefined) value.slotNo = index + 1;
      return value;
    });
  }
  if (schema.type === "integer") return schema.minimum ?? 1;
  if (schema.type === "number") return schema.minimum ?? 50;
  if (schema.type === "boolean") return schema.const ?? false;
  if (schema.type === "null") return null;
  if (schema.type === "string") {
    if (schema.format === "uuid") return uuid();
    if (schema.format === "date-time") return "2026-08-25T09:00:00Z";
    if (schema.pattern?.includes("64")) return "0".repeat(64);
    if (schema.pattern?.includes("40")) return "0".repeat(40);
    if (/buildCommit|commit/i.test(fieldName)) return "0".repeat(40);
    if (/credentialProof|authenticationProof/i.test(fieldName)) return "INVALID-PLACEHOLDER-NOT-A-SECRET";
    if (/stationId/i.test(fieldName)) return "STATION-001";
    if (/mapId/i.test(fieldName)) return "25";
    if (/sublot/i.test(fieldName)) return "TEST-SUBLOT-001";
    if (/journalCheckpoint/i.test(fieldName)) return "RESULT_RECORDED";
    if (/contentSha256|manifestSha256/i.test(fieldName)) return "0".repeat(64);
    if (/messageType/i.test(fieldName)) return "OperationResult";
    return `${fieldName || "value"}-test`;
  }
  throw new Error(`Cannot sample ${fieldName}: ${JSON.stringify(schema)}`);
};

const envelopeFor = (spec) => {
  const schema = JSON.parse(fs.readFileSync(path.join(root, `schemas/messages/${spec.name}.schema.json`), "utf8"));
  const value = sample(schema);
  value.messageId = uuid();
  value.protocolReleaseVersion = candidateVersion;
  value.protocolReleaseManifestSha256 = "0".repeat(64);
  value.messageType = spec.name;
  value.agvId = "AGV-8005-01";
  value.sentAt = "2026-08-25T09:00:00Z";
  if (correlationRuleFor(spec) === "REQUIRED_ORIGINAL_MESSAGE_ID") value.correlationId = uuid();
  else if (spec.name === "SlotOperationCommand") value.correlationId = uuid();
  else value.correlationId = null;
  value.sessionGeneration = ["SessionHello", "SessionRejected"].includes(spec.name) ? null : 1;
  if (spec.name === "CapabilitySnapshot" || spec.name === "SafetyStateSnapshot") {
    value.payload.slotStates = Array.from({ length: 8 }, (_, index) => ({ slotNo: index + 1, operability: "OPERABLE", administrativeAvailability: "ENABLED", physicalState: "EMPTY", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: [] }));
  }
  if (spec.name === "SlotOperationCommand") {
    value.payload.operationType = "LOAD";
    value.payload.expectedFinalPhysicalState = "OCCUPIED";
  }
  return value;
};

const invalidTypeValue = (schema) => {
  const resolved = resolveRef(schema);
  if (resolved.anyOf) return { definitely: "invalid" };
  if (resolved.type === "string") return 123;
  if (resolved.type === "integer" || resolved.type === "number") return "not-a-number";
  if (resolved.type === "boolean") return "not-a-boolean";
  if (resolved.type === "array") return {};
  if (resolved.type === "object") return [];
  if (resolved.type === "null") return "not-null";
  return undefined;
};

const invalidWrapper = (vectorId, message, code, fieldPath, rule) => ({ vectorId, message, expected: { code, fieldPath, rule } });
for (const spec of Object.values(specs)) {
  const valid = envelopeFor(spec);
  writeJson(`examples/valid/${spec.name}/V-${spec.name}-MIN-001.json`, valid);
  const schema = JSON.parse(fs.readFileSync(path.join(root, `schemas/messages/${spec.name}.schema.json`), "utf8"));
  for (const field of schema.required) {
    const broken = clone(valid); delete broken[field];
    writeJson(`examples/invalid/${spec.name}/I-${spec.name}-REQUIRED-ENVELOPE-${field}.json`, invalidWrapper(`I-${spec.name}-REQUIRED-ENVELOPE-${field}`, broken, "PROTOCOL_SCHEMA_INVALID", `/${field}`, "required"));
  }
  for (const field of schema.properties.payload.required) {
    const broken = clone(valid); delete broken.payload[field];
    writeJson(`examples/invalid/${spec.name}/I-${spec.name}-REQUIRED-PAYLOAD-${field}.json`, invalidWrapper(`I-${spec.name}-REQUIRED-PAYLOAD-${field}`, broken, "PROTOCOL_SCHEMA_INVALID", `/payload/${field}`, "required"));
  }
  for (const [field, fieldSchema] of Object.entries(schema.properties.payload.properties)) {
    const invalidValue = invalidTypeValue(fieldSchema);
    if (invalidValue === undefined) continue;
    const broken = clone(valid); broken.payload[field] = invalidValue;
    writeJson(`examples/invalid/${spec.name}/I-${spec.name}-TYPE-${field}.json`, invalidWrapper(`I-${spec.name}-TYPE-${field}`, broken, "PROTOCOL_SCHEMA_INVALID", `/payload/${field}`, "type"));
    const resolved = resolveRef(fieldSchema);
    if (resolved.enum || resolved.const !== undefined) {
      const enumBroken = clone(valid); enumBroken.payload[field] = resolved.type === "integer" ? 99999 : "__NOT_ALLOWED__";
      writeJson(`examples/invalid/${spec.name}/I-${spec.name}-ENUM-${field}.json`, invalidWrapper(`I-${spec.name}-ENUM-${field}`, enumBroken, "PROTOCOL_SCHEMA_INVALID", `/payload/${field}`, "enum-or-const"));
    }
    if (resolved.type === "array" && resolved.uniqueItems) {
      const duplicate = sample(resolved.items, field); const arrayBroken = clone(valid); arrayBroken.payload[field] = [duplicate, clone(duplicate)];
      writeJson(`examples/invalid/${spec.name}/I-${spec.name}-UNIQUE-${field}.json`, invalidWrapper(`I-${spec.name}-UNIQUE-${field}`, arrayBroken, "PROTOCOL_SCHEMA_INVALID", `/payload/${field}`, "uniqueItems"));
    }
    if (resolved.type === "array" && (resolved["x-sortedAscending"] || resolved["x-sortedBy"])) {
      const sortedBroken = clone(valid);
      if (resolved["x-sortedBy"]) {
        const first = sample(resolved.items, field); const second = clone(first); first[resolved["x-sortedBy"]] = 2; second[resolved["x-sortedBy"]] = 1; sortedBroken.payload[field] = [first, second];
      } else sortedBroken.payload[field] = [2, 1];
      writeJson(`examples/invalid/${spec.name}/I-${spec.name}-SORT-${field}.json`, invalidWrapper(`I-${spec.name}-SORT-${field}`, sortedBroken, "PROTOCOL_SCHEMA_INVALID", `/payload/${field}`, "x-sorted"));
    }
  }
  if (correlationRuleFor(spec) === "REQUIRED_ORIGINAL_MESSAGE_ID") {
    const broken = clone(valid); broken.correlationId = null;
    writeJson(`examples/invalid/${spec.name}/I-${spec.name}-CORRELATION-001.json`, invalidWrapper(`I-${spec.name}-CORRELATION-001`, broken, "CORRELATION_INVALID", "/correlationId", "semantic-correlation"));
  } else if (correlationRuleFor(spec) === "MUST_BE_NULL") {
    const broken = clone(valid); broken.correlationId = uuid();
    writeJson(`examples/invalid/${spec.name}/I-${spec.name}-CORRELATION-001.json`, invalidWrapper(`I-${spec.name}-CORRELATION-001`, broken, "CORRELATION_INVALID", "/correlationId", "semantic-correlation"));
  }
}

const profileEnvelope = (messageType) => ({ ...envelopeFor(specs.SessionReadiness), messageType, messageId: uuid(), correlationId: null, payload: {} });
for (const name of denylist) writeJson(`examples/invalid/profile/I-PROFILE-${name}-001.json`, invalidWrapper(`I-PROFILE-${name}-001`, profileEnvelope(name), "PROFILE_MESSAGE_NOT_ALLOWED", "/messageType", "profile-denylist"));
writeJson("examples/invalid/profile/I-PROFILE-UNKNOWN-001.json", invalidWrapper("I-PROFILE-UNKNOWN-001", profileEnvelope("UnknownFutureMessage"), "UNKNOWN_MESSAGE_TYPE", "/messageType", "unknown-message-type"));
{
  const broken = envelopeFor(specs.SessionHello); broken.protocolVersion = 999;
  writeJson("examples/invalid/profile/I-ENVELOPE-PROTOCOL-VERSION-001.json", invalidWrapper("I-ENVELOPE-PROTOCOL-VERSION-001", broken, "UNSUPPORTED_PROTOCOL_VERSION", "/protocolVersion", "semantic-protocol-version"));
}
{
  const broken = envelopeFor(specs.SessionReadiness); broken.protocolReleaseManifestSha256 = "f".repeat(64);
  writeJson("examples/invalid/profile/I-ENVELOPE-RELEASE-IDENTITY-001.json", invalidWrapper("I-ENVELOPE-RELEASE-IDENTITY-001", broken, "PROTOCOL_RELEASE_IDENTITY_MISMATCH", "/protocolReleaseManifestSha256", "semantic-release-identity"));
}
{
  const broken = envelopeFor(specs.SessionReadiness); broken.sessionGeneration = 0;
  writeJson("examples/invalid/profile/I-ENVELOPE-STALE-SESSION-001.json", invalidWrapper("I-ENVELOPE-STALE-SESSION-001", broken, "STALE_SESSION_GENERATION", "/sessionGeneration", "semantic-session-generation"));
}

writeJson("errors/error-codes.json", { registryVersion: "1.0.0", appendOnly: true, displayMessageAuthoritative: false, codes: errorCodes });

const trajectories = {
  "CV-SESSION-RECOVERY-HAPPY": ["SessionHello", "SessionAccepted", "CapabilitySnapshot", "SafetyStateSnapshot", "RecoveryStateReport", "SessionReadiness"],
  "CV-SESSION-RECONNECT-DURING-RECOVERY": ["SessionHello", "SessionAccepted", "RecoveryStateReport", "SessionHello", "SessionAccepted", "RecoveryStateReport", "SessionReadiness"],
  "CV-RELIABLE-RETRY-SAME-CONTENT": ["SlotOperationCommand", "SlotOperationCommand", "DurableAck"],
  "CV-RELIABLE-RETRY-DIFFERENT-CONTENT": ["SlotOperationCommand", "SlotOperationCommand", "ProtocolProblem"],
  "CV-REQUEST-FIRST-RESULT-REPLAY": ["SublotSubmitted", "SlotOperationCommand", "SublotSubmitted", "SlotOperationCommand"],
  "CV-SNAPSHOT-REPLACE-AND-ACK": ["VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"],
  "CV-SNAPSHOT-SAME-REVISION-CONFLICT": ["SafetyStateSnapshot", "SnapshotAppliedAck", "SafetyStateSnapshot", "ProtocolProblem"],
  "CV-PICKUP-SUBLOT-LOAD": ["SublotEntryRequested", "SublotSubmitted", "SlotOperationCommand", "OperationResult", "DurableAck"],
  "CV-LOAD-CORRECTION": ["LoadCorrectionRequested", "LoadCorrectionCommand", "LoadCorrectionResult", "DurableAck"],
  "CV-LOAD-CANCELLATION-ALL-EMPTY": ["LoadCancellationStartRequested", "LoadCancellationAuthorization", "LoadCancellationResult", "DurableAck"],
  "CV-PREDEPARTURE-SAFETY-EXPIRES": ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult", "SafetyStateChanged", "ProtocolProblem"],
  "CV-GATE-UNLOAD-ALL-EMPTY": ["SlotOperationCommand", "OperationResult", "DurableAck"],
  "CV-CONNECTION-LOSS-SAFE-FINISH": ["SlotOperationCommand", "OperationProgress", "RecoveryStateReport", "SessionReadiness"],
  "CV-OPERATION-RESULT-UNKNOWN-RECONCILE": ["OperationResult", "DurableAck", "RecoveryStateReport", "OperationResult", "DurableAck"],
  "CV-EXCEPTION-RESUME": ["ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted", "SlotOperationResumeCommand", "OperationResult"],
  "CV-EXCEPTION-COMPENSATE": ["ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted", "LoadCompensationRequested", "LoadCompensationCommand", "LoadCompensationResult"],
  "CV-FAULT-CARGO-HANDOFF": ["RecoveryActionSubmitted", "RecoveryActionAccepted", "FaultCargoRecoveryCommand", "FaultCargoRecoveryResult"],
  "CV-FORCED-MECHANICAL-RECOVERY": ["RecoveryActionSubmitted", "RecoveryActionAccepted", "ForcedMechanicalRecoveryCommand", "ForcedMechanicalRecoveryResult"],
  "CV-MANUAL-CHARGING-RETURN": ["ManualChargingReturnToServiceRequested", "ManualChargingReturnToServiceResult"],
};
for (const [vectorId, messageTypes] of Object.entries(trajectories)) {
  const lines = messageTypes.map((messageType, index) => ({ step: index + 1, atMs: index * 100, action: index === 0 ? "send" : "expect", messageType, virtualTimeOnly: true }));
  writeText(`vectors/${vectorId}/input.ndjson`, `${lines.map(canonical).join("\n")}\n`);
  const stableErrorCode = vectorId.includes("DIFFERENT-CONTENT") ? "MESSAGE_ID_CONTENT_CONFLICT" : vectorId.includes("SAME-REVISION-CONFLICT") ? "SNAPSHOT_REVISION_CONTENT_CONFLICT" : vectorId.includes("EXPIRES") ? "PREDEPARTURE_CHECK_EXPIRED" : null;
  writeJson(`vectors/${vectorId}/expected.json`, {
    vectorId,
    orderedExpectedMessages: messageTypes,
    persistenceCheckpoints: ["durable-before-send", "durable-before-ack", "journal-before-irreversible-io", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"],
    finalState: { readiness: vectorId.includes("RECOVERY") || vectorId.includes("CONNECTION-LOSS") ? "RECOVERY_REQUIRED_OR_UNIQUELY_RECONCILED" : "UNCHANGED_OR_SPECIFIED_BY_VECTOR", business: "NO_DUPLICATE_COMMIT", physical: "NO_UNPROVEN_STATE" },
    stableErrorCode,
  });
}

const slices = [
  ["W2G-IS-00", ["CV-SESSION-RECOVERY-HAPPY", "CV-SESSION-RECONNECT-DURING-RECOVERY", "CV-SNAPSHOT-REPLACE-AND-ACK", "CV-SNAPSHOT-SAME-REVISION-CONFLICT"]],
  ["W2G-IS-01", ["CV-RELIABLE-RETRY-SAME-CONTENT", "CV-REQUEST-FIRST-RESULT-REPLAY"]],
  ["W2G-IS-02", ["CV-PICKUP-SUBLOT-LOAD", "CV-LOAD-CORRECTION", "CV-LOAD-CANCELLATION-ALL-EMPTY"]],
  ["W2G-IS-03", ["CV-PREDEPARTURE-SAFETY-EXPIRES", "CV-OPERATION-RESULT-UNKNOWN-RECONCILE"]],
  ["W2G-IS-04", ["CV-GATE-UNLOAD-ALL-EMPTY"]],
  ["W2G-IS-05", ["CV-CONNECTION-LOSS-SAFE-FINISH", "CV-SESSION-RECONNECT-DURING-RECOVERY"]],
  ["W2G-IS-06", ["CV-RELIABLE-RETRY-SAME-CONTENT", "CV-RELIABLE-RETRY-DIFFERENT-CONTENT", "CV-REQUEST-FIRST-RESULT-REPLAY", "CV-OPERATION-RESULT-UNKNOWN-RECONCILE"]],
  ["W2G-IS-07", ["CV-OPERATION-RESULT-UNKNOWN-RECONCILE", "CV-EXCEPTION-RESUME", "CV-EXCEPTION-COMPENSATE", "CV-FAULT-CARGO-HANDOFF", "CV-FORCED-MECHANICAL-RECOVERY", "CV-MANUAL-CHARGING-RETURN"]],
].map(([integrationSliceId, vectorIds], index) => ({ integrationSliceId, sequence: index, prerequisites: index === 0 ? [] : index <= 4 ? [`W2G-IS-${String(index - 1).padStart(2, "0")}`] : ["W2G-IS-00"], vectorIds, gates: ["G1", "CONTROL_SERVER_G2", "ONBOARD_HMI_G2", "G3"], forbidUnclosedFailOrInconclusive: true }));
writeJson("integration-slices/index.json", { schemaVersion: "1.0.0", slices });

writeJson("runner/runner-contract.schema.json", {
  $schema: SCHEMA, $id: `${BASE_ID}/runner/runner-contract.schema.json`, title: "Language-neutral conformance runner input",
  ...O({ vectorId: S(), integrationSliceId: S({ pattern: "^W2G-IS-0[0-7]$" }), virtualClockStart: I({ minimum: 0 }), steps: A(O({ step: I({ minimum: 1 }), atMs: I({ minimum: 0 }), action: E("send", "expect", "advance", "drop", "delay", "duplicate", "disconnect", "reconnect", "crash", "restart", "adapter-result"), messageType: Nullable(S()), payloadRef: Nullable(S()) }), { minItems: 1 }), initialPersistentFacts: O({}), forbiddenSideEffects: StringArray({ minItems: 1 }) }),
});
writeJson("runner/result.schema.json", {
  $schema: SCHEMA, $id: `${BASE_ID}/runner/result.schema.json`, title: "Conformance result",
  ...O({
    runId: R("Id"),
    integrationSliceId: S({ pattern: "^W2G-IS-0[0-7]$" }),
    runKind: E("G1", "CONTROL_SERVER_G2", "ONBOARD_HMI_G2", "G3"),
    protocolManifestSha256: R("Sha256"),
    controlServerCommit: Nullable(R("CommitSha")),
    onboardHmiCommit: Nullable(R("CommitSha")),
    fakePeerIdentities: A(O({
      repository: S(),
      commit: R("CommitSha"),
      artifactSha256: R("Sha256"),
      harnessContractVersion: S(),
      supportedIntegrationSliceIds: A(S({ pattern: "^W2G-IS-0[0-7]$" }), { minItems: 1, uniqueItems: true }),
    }), { uniqueItems: true }),
    vectorIds: A(S(), { minItems: 1, uniqueItems: true }),
    vectorsSha256: R("Sha256"),
    virtualTimeScriptSha256: R("Sha256"),
    configurationSha256: R("Sha256"),
    startedAt: R("Instant"),
    finishedAt: R("Instant"),
    result: E("PASS", "FAIL", "INCONCLUSIVE"),
    firstDivergence: Nullable(O({ step: I({ minimum: 1 }), expected: S(), actual: S(), stableErrorCode: Nullable(R("ErrorCode")) })),
    evidencePointers: A(S(), { uniqueItems: true }),
  }),
});

writeJson("compatibility/report.json", {
  candidateVersion,
  protocolVersion,
  profileId,
  status: "INITIAL_CANDIDATE_NO_BASE_RELEASE",
  classification: "BREAKING_INITIAL_BASELINE",
  runtimeRule: "Exact ProtocolVersion and exact materialized ProtocolReleaseIdentity required; no negotiation.",
  optionalFieldPolicy: "No optional payload fields exist in this candidate. Future optional fields require proof that omission and ignore preserve safety and business conclusions.",
  historyPolicy: "Published tags, commits, manifests, schemas, vectors and approvals are immutable; defects require a superseding release.",
});
writeJson("approvals/release-approval.json", {
  candidateVersion,
  status: "PENDING",
  approvals: [],
  statement: "This blank record is not approval. AI generated the candidate and must not sign for either human owner.",
});
writeJson("compatibility/implementation-version-matrix.json", {
  status: "CANDIDATE",
  sharedDevelopmentBaseline: {
    dotnetSdk: "8.0.424",
    dotnetRuntime: "8.0.30",
    targetFrameworks: { controlServer: "net8.0", onboardHmi: "net8.0-windows" },
    runtimeIdentifiers: ["win-x64"],
    packageCompatibilityRule: "All Microsoft.Extensions and EF Core packages remain on the 8.x major line and are locked by each implementation repository; protocol wire compatibility is defined only by the materialized ProtocolReleaseIdentity.",
  },
  onboardObservedDevelopmentMachine: { os: "Windows 11 Home zh-CN", version: "10.0.26200", build: "26200", architecture: "x64", installedRuntime: "8.0.29", installedDesktopRuntime: "8.0.29", qualification: "DEVELOPMENT_MACHINE_ONLY" },
  pinnedPackages: [
    { name: "Microsoft.EntityFrameworkCore.Sqlite", version: "8.0.30", consumers: ["ControlServer", "OnboardHmi journal"] },
    { name: "Microsoft.Extensions.Http.Resilience", version: "8.10.0", consumers: ["ControlServer"] },
    { name: "xunit.v3", version: "3.2.2", consumers: ["ControlServer", "OnboardHmi"] },
    { name: "Corvus.Json.Validator", version: "4.6.7", consumers: ["isolated .NET conformance process"] },
    { name: "ajv", version: "8.20.0", consumers: ["protocol G1"] },
    { name: "ajv-formats", version: "3.0.1", consumers: ["protocol G1"] },
  ],
  requiredAction: "Install or pin SDK 8.0.424 before reproducible product builds; do not treat the observed 8.0.29 runtime as equivalent evidence.",
});

writeText("docs/README.md", `# WIRE_TO_GATE MVP protocol candidate\n\nThis repository contains a **candidate**, not an approved ProtocolRelease. Machine-readable JSON Schema, manifests, errors, examples, vectors, runner/result contracts and the integration-slice index are authoritative. Markdown is explanatory only.\n\nRun \`pnpm install --frozen-lockfile\` and \`pnpm g1\`. A PASS proves only candidate-internal consistency. It does not prove human G0 approval, either product implementation, G2/G3, real RIoT, real IO, target hardware or factory qualification.\n`);
writeText("docs/release-governance.md", `# Release governance\n\n- ProtocolVersion is exactly 1 for this candidate; runtime negotiation is forbidden.\n- A formal release requires exact repository, SemVer, annotated tag, full commit, ProtocolVersion, profile, manifest hash, schema bundle hash and vectors hash.\n- Both real product owners must approve the exact commit and manifest before an immutable tag/release is created. AI and CI cannot approve.\n- Required/type/enum/meaning/direction/delivery/dedup/persistence/recovery/error/side-effect changes are breaking and require a ProtocolVersion and release-major increase.\n- Historical red evidence and released identities are immutable.\n`);
writeText("docs/candidate-limitations.md", `# Candidate limitations and release-finalization blocker\n\nThe candidate intentionally uses structurally valid synthetic zero hashes inside envelope examples. Examples are schema fixtures, not evidence of a materialized release identity.\n\nThe accepted governance currently creates a circular finalization dependency: the manifest is required to hash every file except itself, while the approval record is required to contain manifestSha256 and is itself included in the manifest file table. Filling the approval changes the manifest, which changes manifestSha256 again. Formal release must resolve this by an explicit human-approved governance amendment (for example, exclude the external approval attestation from the content manifest while binding it to the immutable candidate commit and manifest hash). G1 may pass the unapproved candidate; no tag/release may be created until the circularity is resolved.\n`);

writeJson("package.json", {
  name: "8005-agv-protocol",
  version: "0.1.0",
  private: true,
  type: "module",
  scripts: { g1: "node tools/g1-validate.mjs", "manifest:finalize": "node tools/finalize-manifest.mjs" },
  devDependencies: { ajv: "8.20.0", "ajv-formats": "3.0.1" },
  engines: { node: ">=20" },
  license: "UNLICENSED",
});

writeText("tools/finalize-manifest.mjs", `import fs from "node:fs";\nimport path from "node:path";\nimport crypto from "node:crypto";\nconst root=path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\\/([A-Za-z]:)/,"$1")),"..");\nconst sha=b=>crypto.createHash("sha256").update(b).digest("hex");\nconst canon=v=>v===null||typeof v!=="object"?JSON.stringify(v):Array.isArray(v)?"["+v.map(canon).join(",")+"]":"{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canon(v[k])).join(",")+"}";\nconst excluded=p=>p==="manifest/release.json"||p.startsWith(".git/")||p.startsWith("node_modules/")||p.startsWith("evidence/");\nconst walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):[p]});\nconst files=walk(root).map(p=>path.relative(root,p).replaceAll("\\\\","/")).filter(p=>!excluded(p)).sort().map(p=>{const b=fs.readFileSync(path.join(root,p));return{path:p,role:p.split("/")[0],bytes:b.length,sha256:sha(b)}});\nconst combine=prefix=>sha(Buffer.from(files.filter(f=>f.path.startsWith(prefix)).map(f=>f.path+":"+f.sha256).join("\\n")+"\\n"));\nconst manifest={status:"CANDIDATE_UNAPPROVED",releaseVersion:"0.1.0",protocolVersion:1,profileId:"WIRE_TO_GATE_MVP",repository:"8005-agv-protocol",generatedAt:"2026-08-25T09:00:00Z",hashAlgorithm:"SHA-256",jsonCanonicalization:"RFC8785-compatible sorted-key JCS for semantic collections; raw bytes for file entries",fileTableSha256:sha(Buffer.from(canon(files))),schemaBundleSha256:combine("schemas/"),examplesSha256:combine("examples/"),vectorsSha256:combine("vectors/"),errorRegistrySha256:combine("errors/"),runnerContractsSha256:combine("runner/"),approvalStatus:"PENDING",files};\nfs.mkdirSync(path.join(root,"manifest"),{recursive:true});fs.writeFileSync(path.join(root,"manifest/release.json"),JSON.stringify(manifest,null,2)+"\\n");console.log(JSON.stringify({manifestSha256:sha(fs.readFileSync(path.join(root,"manifest/release.json"))),files:files.length,...manifest},null,2));\n`);

writeText("tools/g1-validate.mjs", `import fs from "node:fs";\nimport path from "node:path";\nimport crypto from "node:crypto";\nimport Ajv2020 from "ajv/dist/2020.js";\nimport addFormats from "ajv-formats";\nconst root=path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\\/([A-Za-z]:)/,"$1")),"..");\nconst read=p=>JSON.parse(fs.readFileSync(path.join(root,p),"utf8"));\nconst sha=b=>crypto.createHash("sha256").update(b).digest("hex");\nconst walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):[p]});\nconst fail=[];const check=(ok,msg)=>{if(!ok)fail.push(msg)};\nconst ajv=new Ajv2020({allErrors:true,strict:false,validateFormats:true});addFormats(ajv);\nconst schemaFiles=walk(path.join(root,"schemas")).filter(p=>p.endsWith(".json"));const schemas=schemaFiles.map(p=>JSON.parse(fs.readFileSync(p,"utf8")));for(const s of schemas){check(ajv.validateSchema(s),"invalid schema "+s.$id+" "+ajv.errorsText());ajv.addSchema(s)}\nconst messageSchemas=schemas.filter(s=>s.$id?.includes("/messages/"));const names=messageSchemas.map(s=>s.title).sort();const validators=new Map(messageSchemas.map(s=>[s.title,ajv.getSchema(s.$id)]));\nfor(const name of names){const dir=path.join(root,"examples/valid",name);check(fs.existsSync(dir),"missing valid directory "+name);if(!fs.existsSync(dir))continue;const files=walk(dir).filter(p=>p.endsWith(".json"));check(files.length>0,"missing valid example "+name);for(const f of files){const data=JSON.parse(fs.readFileSync(f,"utf8"));const v=validators.get(name);check(v(data),"valid example failed "+path.relative(root,f)+" "+ajv.errorsText(v.errors))}}\nconst semanticRules=new Set(["semantic-correlation","profile-denylist","unknown-message-type","semantic-protocol-version","semantic-release-identity","semantic-session-generation"]);const invalidFiles=walk(path.join(root,"examples/invalid")).filter(p=>p.endsWith(".json"));for(const f of invalidFiles){const x=JSON.parse(fs.readFileSync(f,"utf8"));check(x.vectorId&&x.message&&x.expected?.code&&x.expected?.fieldPath,"invalid wrapper incomplete "+path.relative(root,f));const v=validators.get(x.message.messageType);if(semanticRules.has(x.expected.rule)){if(x.expected.rule==="profile-denylist")check(!names.includes(x.message.messageType),"denylisted name in allowlist "+x.message.messageType);continue}check(v&&!v(x.message),"schema-invalid example unexpectedly valid "+path.relative(root,f))}\nconst manifest=read("manifest/release.json");check(manifest.status==="CANDIDATE_UNAPPROVED","manifest status");check(manifest.approvalStatus==="PENDING","approval status");check(JSON.stringify(names)===JSON.stringify(Object.keys(manifest.messages??{}).sort())||manifest.messages===undefined,"manifest message mismatch");\nconst excluded=p=>p==="manifest/release.json"||p.startsWith(".git/")||p.startsWith("node_modules/")||p.startsWith("evidence/");const actual=walk(root).map(p=>path.relative(root,p).replaceAll("\\\\","/")).filter(p=>!excluded(p)).sort();check(actual.length===manifest.files.length,"manifest file count");const table=new Map(manifest.files.map(f=>[f.path,f]));for(const p of actual){const b=fs.readFileSync(path.join(root,p));const f=table.get(p);check(!!f,"manifest missing "+p);if(f){check(f.bytes===b.length,"byte mismatch "+p);check(f.sha256===sha(b),"hash mismatch "+p)}}\nconst errors=read("errors/error-codes.json").codes;check(new Set(errors.map(e=>e.code)).size===errors.length,"duplicate error codes");for(const e of errors)check(e.category&&e.meaning&&e.allowedMessageTypes?.length&&e.retryDisposition&&e.introducedInRelease,"incomplete error "+e.code);\nconst deny=["OperationCancelCommand","LoadCancellationCommand","LoadFinalConfirmation","UnloadCommand","SublotAccepted","OperationCommandAck","OperationResultAck","LoadCompensationCommandAck","WireToGateExecutionSnapshot","DepartureSafetyRevoked","OnboardCapabilitySnapshot"];for(const n of deny){check(!names.includes(n),"denylisted schema "+n);check(invalidFiles.some(f=>path.basename(f).includes(n)),"missing deny vector "+n)}\nconst requiredVectors=${JSON.stringify(Object.keys(trajectories))};for(const id of requiredVectors){check(fs.existsSync(path.join(root,"vectors",id,"input.ndjson")),"missing vector input "+id);const exp=read("vectors/"+id+"/expected.json");check(exp.orderedExpectedMessages?.length&&exp.persistenceCheckpoints?.length&&exp.forbiddenSideEffects?.length&&exp.finalState,"incomplete vector "+id)}\nconst index=read("integration-slices/index.json");check(index.slices.length===8,"slice count");check(index.slices.map(s=>s.integrationSliceId).join(",")===[0,1,2,3,4,5,6,7].map(i=>"W2G-IS-"+String(i).padStart(2,"0")).join(","),"slice ids");for(const s of index.slices)for(const id of s.vectorIds)check(requiredVectors.includes(id),"unknown slice vector "+id);\nfor(const p of ["runner/runner-contract.schema.json","runner/result.schema.json"]){const s=read(p);check(ajv.validateSchema(s),"invalid runner schema "+p);check(!!ajv.compile(s),"runner compile "+p)}\nconst approval=read("approvals/release-approval.json");check(approval.status==="PENDING"&&approval.approvals.length===0,"candidate must have blank approvals");const matrix=read("compatibility/implementation-version-matrix.json");check(matrix.sharedDevelopmentBaseline.dotnetSdk==="8.0.424"&&matrix.sharedDevelopmentBaseline.dotnetRuntime==="8.0.30","version matrix mismatch");\nconst secretPatterns=[/ghp_[A-Za-z0-9]{20,}/,/github_pat_[A-Za-z0-9_]{20,}/,/-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/];for(const p of actual){const text=fs.readFileSync(path.join(root,p),"utf8");for(const re of secretPatterns)check(!re.test(text),"secret-like content "+p)}\nconst result={gate:"G1",status:fail.length?"FAIL":"PASS",candidateManifestSha256:sha(fs.readFileSync(path.join(root,"manifest/release.json"))),schemaCount:schemas.length,messageTypeCount:names.length,validExampleCount:walk(path.join(root,"examples/valid")).filter(p=>p.endsWith(".json")).length,invalidExampleCount:invalidFiles.length,trajectoryCount:requiredVectors.length,integrationSliceCount:index.slices.length,checkedAt:"2026-08-25T09:00:00Z",failures:fail};fs.mkdirSync(path.join(root,"evidence"),{recursive:true});fs.writeFileSync(path.join(root,"evidence/g1-result.json"),JSON.stringify(result,null,2)+"\\n");console.log(JSON.stringify(result,null,2));if(fail.length)process.exit(1);\n`);

writeJson("manifest/release.json", { status: "CANDIDATE_UNFINALIZED", releaseVersion: candidateVersion, protocolVersion, profileId, repository: "8005-agv-protocol", denylistedMessageTypes: denylist, messages: Object.fromEntries(Object.values(specs).map((spec) => [spec.name, { sender: senderFor(spec.direction), receiver: receiverFor(spec.direction), direction: spec.direction, deliveryClass: spec.deliveryClass, correlationRule: correlationRuleFor(spec), transportDedupKey: "messageId", businessDedupKeys: spec.businessDedupKeys, durableBeforeSend: spec.deliveryClass === "RELIABLE", durableBeforeAck: spec.deliveryClass === "RELIABLE", recoveryRole: spec.recoveryRole, schema: `schemas/messages/${spec.name}.schema.json` }])) });
writeText("tools/finalize-manifest.mjs", `import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\\/([A-Za-z]:)/,"$1")),"..");
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const canon=v=>v===null||typeof v!=="object"?JSON.stringify(v):Array.isArray(v)?"["+v.map(canon).join(",")+"]":"{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canon(v[k])).join(",")+"}";
const excluded=p=>p==="manifest/release.json"||p.startsWith(".git/")||p.startsWith("node_modules/")||p.startsWith("evidence/");
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):[p]});
const files=walk(root).map(p=>path.relative(root,p).replaceAll("\\\\","/")).filter(p=>!excluded(p)).sort().map(p=>{const b=fs.readFileSync(path.join(root,p));return{path:p,role:p.split("/")[0],bytes:b.length,sha256:sha(b)}});
const combine=prefix=>sha(Buffer.from(files.filter(f=>f.path.startsWith(prefix)).map(f=>f.path+":"+f.sha256).join("\\n")+"\\n"));
const seed=JSON.parse(fs.readFileSync(path.join(root,"manifest/release.json"),"utf8"));
const manifest={status:"CANDIDATE_UNAPPROVED",releaseVersion:"0.1.0",protocolVersion:1,profileId:"WIRE_TO_GATE_MVP",repository:"8005-agv-protocol",generatedAt:"2026-08-25T09:00:00Z",hashAlgorithm:"SHA-256",jsonCanonicalization:"RFC8785-compatible sorted-key JCS for semantic collections; raw bytes for file entries",fileTableSha256:sha(Buffer.from(canon(files))),schemaBundleSha256:combine("schemas/"),examplesSha256:combine("examples/"),vectorsSha256:combine("vectors/"),errorRegistrySha256:combine("errors/"),runnerContractsSha256:combine("runner/"),approvalStatus:"PENDING",messages:seed.messages,denylistedMessageTypes:seed.denylistedMessageTypes,files};
fs.mkdirSync(path.join(root,"manifest"),{recursive:true});fs.writeFileSync(path.join(root,"manifest/release.json"),JSON.stringify(manifest,null,2)+"\\n");console.log(JSON.stringify({manifestSha256:sha(fs.readFileSync(path.join(root,"manifest/release.json"))),files:files.length,messageTypeCount:Object.keys(manifest.messages).length,status:manifest.status},null,2));
`);
console.log(JSON.stringify({ generated: true, target: root, messageTypeCount: Object.keys(specs).length, invalidExamplePolicy: "required/type/enum/unique/sort/correlation plus profile and envelope semantics", trajectoryCount: Object.keys(trajectories).length, sliceCount: slices.length }, null, 2));
