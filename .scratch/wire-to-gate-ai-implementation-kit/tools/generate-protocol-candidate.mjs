import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import os from "node:os";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const selfPath = fileURLToPath(import.meta.url);
const argv = process.argv.slice(2);
const verifyDeterminism = argv.includes("--verify-determinism");
const target = argv.find((value) => !value.startsWith("--"));
if (!target && !verifyDeterminism) throw new Error("Usage: node generate-protocol-candidate.mjs <protocol-repository> [--verify-determinism]");

const digestTree = (directory) => {
  const walkTree = (current) => fs.readdirSync(current, { withFileTypes: true }).flatMap((entry) => {
    const child = path.join(current, entry.name);
    return entry.isDirectory() ? walkTree(child) : [child];
  });
  return new Map(walkTree(directory).map((file) => [
    path.relative(directory, file).replaceAll("\\", "/"),
    crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"),
  ]));
};

// Same input, two generations, byte-identical output. Each generation runs in its own process:
// the generator carries module-level counters that a second in-process run would continue rather
// than restart, so an in-process repeat would report a false divergence.
if (verifyDeterminism) {
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-candidate-determinism-"));
  try {
    const [first, second] = ["run-a", "run-b"].map((label) => {
      const directory = path.join(scratch, label);
      const run = spawnSync(process.execPath, [selfPath, directory], { encoding: "utf8" });
      if (run.status !== 0) throw new Error(`determinism ${label} exited ${run.status}: ${run.stderr}`);
      return digestTree(directory);
    });
    const paths = [...new Set([...first.keys(), ...second.keys()])].sort();
    const divergent = paths.filter((relative) => first.get(relative) !== second.get(relative));
    console.log(JSON.stringify({
      deterministic: divergent.length === 0,
      fileCount: first.size,
      divergentFileCount: divergent.length,
      divergent: divergent.slice(0, 20),
    }, null, 2));
    process.exit(divergent.length ? 1 : 0);
  } finally {
    fs.rmSync(scratch, { recursive: true, force: true });
  }
}

const root = path.resolve(target);
const SCHEMA = "https://json-schema.org/draft/2020-12/schema";

// Candidate identity. Everything written below derives from these constants, so moving the
// candidate to another protocol version, profile or release version is an edit of this block
// alone. Never reintroduce these values as literals in the write-out region.
const BASE_ID = "https://schemas.8005-agv.local/agv-full-product/v2";
const candidateVersion = "1.0.0";
const profileId = "AGV_FULL_PRODUCT";
const profileDisplayName = "AGV_FULL_PRODUCT";
const protocolVersion = 2;
const baseReleaseTag = "protocol-v0.1.1";
// Fixed so the candidate tools stay byte-reproducible; it is a candidate stamp, not a build clock.
const candidateTimestamp = "2026-09-04T00:00:00Z";

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
const templateDirectory = path.join(path.dirname(selfPath), "templates");
// The two candidate tools live as real .mjs files under tools/templates/. Lines opening with the
// template marker are stripped on write; double-underscore placeholders take the constants above.
const renderTemplate = (name) => {
  const raw = fs.readFileSync(path.join(templateDirectory, name), "utf8").replace(/\r\n/g, "\n");
  const rendered = raw
    .split("\n")
    .filter((line) => !line.startsWith("//!"))
    .join("\n")
    .replaceAll("__BASE_ID__", BASE_ID)
    .replaceAll("__PROFILE_ID__", profileId)
    .replaceAll("__PROFILE_DISPLAY_NAME__", profileDisplayName)
    .replaceAll("__CANDIDATE_VERSION__", candidateVersion)
    .replaceAll("__PROTOCOL_VERSION__", String(protocolVersion))
    .replaceAll("__CANDIDATE_TIMESTAMP__", candidateTimestamp);
  const unresolved = rendered.match(/__[A-Z0-9_]+__/);
  if (unresolved) throw new Error(`${name}: unresolved template placeholder ${unresolved[0]}`);
  return rendered;
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
  // Appended for the v2 candidate. The registry is appendOnly, so new codes go at the end rather
  // than beside their category peers.
  ["SLOT_CONFIGURATION_VERIFICATION_FAILED", "BUSINESS", "AFTER_STATE_CHANGE"],
  ["SLOT_CONFIGURATION_FINGERPRINT_MISMATCH", "BUSINESS", "MANUAL_REVIEW"],
];
const errorCodes = requiredErrorCodes.map(([code, category, retryDisposition]) => ({
  code,
  category,
  meaning: `${code} is the stable ${category.toLowerCase()} failure defined by the accepted ${profileDisplayName} governance decision.`,
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
// A stop's third orthogonal dimension: what the vehicle is there for. Business stops load or
// unload, waiting points and chargers do neither.
defs.StopPurposeCategory = E("BUSINESS", "WAITING_POINT", "CHARGER");
// The five fixed public station functions. The segment names line up with TransportTaskType, so
// DIE_TO_OVEN visibly ends at OVEN and STAGING_TO_WIRE visibly starts at WIRE_STAGING.
defs.PublicStationFunction = E("WIRE_STAGING", "OVEN", "GATE", "OPTICAL", "NITROGEN");
// MES TASK_TYPE, verbatim: these six strings are the hardcoded literals of the six UNION ALL
// branches in the factory IT query. WIRE_TO_GATE is one of them, not a phase name.
defs.TransportTaskType = E("DIE_TO_WIRE_STAGING", "DIE_TO_OVEN", "WIRE_TO_GATE", "WIRE_TO_OPTICAL", "STAGING_TO_WIRE", "WIRE_TO_NITROGEN");
// Alarm codes are an open set and deliberately not ErrorCode: folding an open set into a closed
// enum would make every new fault code a breaking protocol change.
defs.AlarmEntry = O({
  alarmId: R("Id"),
  code: S(),
  severity: E("INFO", "WARNING", "CRITICAL"),
  raisedAt: R("Instant"),
  subjectType: S(),
  subjectId: Nullable(S()),
  displayMessage: Nullable(S()),
});

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

add("SessionHello", { onboardInstanceId: R("Id"), onboardBuildCommit: S(), supportedProtocolVersion: I({ const: protocolVersion }), profileId: S({ const: profileId }), protocolReleaseIdentity: R("ProtocolReleaseIdentity"), credentialProof: S({ examples: ["INVALID-PLACEHOLDER-NOT-A-SECRET"] }) }, { recoveryRole: "HANDSHAKE_START" });
add("SessionAccepted", { sessionGeneration: R("Generation"), serverInstanceId: R("Id"), serverBuildCommit: S(), acceptedProtocolReleaseIdentity: R("ProtocolReleaseIdentity"), acceptedAt: R("Instant") }, { recoveryRole: "SESSION_FENCE" });
add("SessionRejected", { problem: R("Problem"), expectedProtocolVersion: I({ const: protocolVersion }), expectedProtocolReleaseIdentity: Nullable(R("ProtocolReleaseIdentity")) });
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
add("ProtocolProblem", { rejectedMessageId: R("Id"), rejectedMessageType: Nullable(S()), problem: R("Problem"), expectedProtocolVersion: I({ const: protocolVersion }), expectedProfileId: S({ const: profileId }), expectedProtocolReleaseManifestSha256: R("Sha256") });

const denylist = ["OperationCancelCommand", "LoadCancellationCommand", "LoadFinalConfirmation", "UnloadCommand", "SublotAccepted", "OperationCommandAck", "OperationResultAck", "LoadCompensationCommandAck", "WireToGateExecutionSnapshot", "DepartureSafetyRevoked", "OnboardCapabilitySnapshot"];

const commonSchema = { $schema: SCHEMA, $id: `${BASE_ID}/common/types.schema.json`, title: `${profileDisplayName} common types`, $defs: defs };
writeJson("schemas/common/types.schema.json", commonSchema);

const envelopeBase = {
  protocolVersion: I({ const: protocolVersion }),
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
  title: `${profileDisplayName} protocol bundle`,
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

// Coverage is judged against what the implementations can emit, not against the registry: a
// vector per registry entry would manufacture assets for codes nobody sends. This counter reports
// which codes the generated tree actually backs, so the gap is a number rather than a guess.
const errorCodeAssets = new Map(errorCodeNames.map((code) => [code, 0]));
const noteErrorCodeAsset = (code) => {
  if (errorCodeAssets.has(code)) errorCodeAssets.set(code, errorCodeAssets.get(code) + 1);
};
const invalidWrapper = (vectorId, message, code, fieldPath, rule) => {
  noteErrorCodeAsset(code);
  return { vectorId, message, expected: { code, fieldPath, rule } };
};
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
  // A trajectory may also be spelled out in full when its steps are not a plain send/expect chain
  // or when it carries product assertions. FP-IS-01's demand acceptance is the first such vector:
  // its adapter results are what the slice is about, and they are not wire messages.
  "CV-DEMAND-ACCEPT-TO-PICKUP": {
    steps: [
      { step: 1, atMs: 0, action: "adapter-result", adapter: "MES_INGEST", result: "FINAL_REREAD_ONE_EXTERNALLY_READABLE_DEMAND", virtualTimeOnly: true },
      { step: 2, atMs: 100, action: "adapter-result", adapter: "RIOT", result: "TO_PICKUP_ORDER_CREATED", virtualTimeOnly: true },
      { step: 3, atMs: 200, action: "expect", messageType: "UpcomingStopPlanSnapshot", virtualTimeOnly: true },
      { step: 4, atMs: 300, action: "expect", messageType: "SnapshotAppliedAck", virtualTimeOnly: true },
      { step: 5, atMs: 400, action: "adapter-result", adapter: "RIOT", result: "PICKUP_ARRIVED", virtualTimeOnly: true },
      { step: 6, atMs: 500, action: "expect", messageType: "CurrentStopWorklistSnapshot", virtualTimeOnly: true },
      { step: 7, atMs: 600, action: "expect", messageType: "SnapshotAppliedAck", virtualTimeOnly: true },
      { step: 8, atMs: 700, action: "expect", messageType: "UpcomingStopPlanSnapshot", virtualTimeOnly: true },
      { step: 9, atMs: 800, action: "expect", messageType: "SnapshotAppliedAck", virtualTimeOnly: true },
    ],
    persistenceCheckpoints: ["accepted-demand-snapshot-before-to-pickup-intent", "to-pickup-intent-before-riot-call", "projection-revision-before-send", "snapshot-before-ack"],
    forbiddenSideEffects: ["duplicate-demand-acceptance", "duplicate-riot-order", "onboard-mesingest-read", "onboard-demand-selection", "onboard-demand-binding", "uncommitted-demand-projection", "slot-operation-before-pickup-arrival"],
    productAssertions: {
      controlServer: ["EXACTLY_ONE_ACCEPTED_DEMAND_SNAPSHOT", "EXACTLY_ONE_TO_PICKUP_INTENT", "EXACTLY_ONE_RIOT_ORDER", "TRUSTED_PICKUP_ARRIVAL"],
      onboardHmi: ["DISPLAY_COMMITTED_DEMAND_JOURNEY", "DISPLAY_CURRENT_STOP", "NEVER_DISCOVER_SELECT_OR_BIND_DEMAND"],
    },
    finalState: { readiness: "READY", business: "ONE_ACCEPTED_DEMAND_ONE_TO_PICKUP_ORDER_AT_PICKUP", physical: "NO_SLOT_OPERATION_STARTED" },
  },
};
for (const [vectorId, trajectory] of Object.entries(trajectories)) {
  const explicit = !Array.isArray(trajectory);
  const steps = explicit
    ? trajectory.steps
    : trajectory.map((messageType, index) => ({ step: index + 1, atMs: index * 100, action: index === 0 ? "send" : "expect", messageType, virtualTimeOnly: true }));
  writeText(`vectors/${vectorId}/input.ndjson`, `${steps.map(canonical).join("\n")}\n`);
  const stableErrorCode = vectorId.includes("DIFFERENT-CONTENT") ? "MESSAGE_ID_CONTENT_CONFLICT" : vectorId.includes("SAME-REVISION-CONFLICT") ? "SNAPSHOT_REVISION_CONTENT_CONFLICT" : vectorId.includes("EXPIRES") ? "PREDEPARTURE_CHECK_EXPIRED" : null;
  if (stableErrorCode) noteErrorCodeAsset(stableErrorCode);
  const expected = {
    vectorId,
    orderedExpectedMessages: steps.filter((step) => step.messageType).map((step) => step.messageType),
    persistenceCheckpoints: trajectory.persistenceCheckpoints ?? ["durable-before-send", "durable-before-ack", "journal-before-irreversible-io", "result-before-replay"],
    forbiddenSideEffects: trajectory.forbiddenSideEffects ?? ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"],
  };
  if (trajectory.productAssertions) expected.productAssertions = trajectory.productAssertions;
  expected.finalState = trajectory.finalState ?? { readiness: vectorId.includes("RECOVERY") || vectorId.includes("CONNECTION-LOSS") ? "RECOVERY_REQUIRED_OR_UNIQUELY_RECONCILED" : "UNCHANGED_OR_SPECIFIED_BY_VECTOR", business: "NO_DUPLICATE_COMMIT", physical: "NO_UNPROVEN_STATE" };
  expected.stableErrorCode = stableErrorCode;
  writeJson(`vectors/${vectorId}/expected.json`, expected);
}

// The slice family's shape lives here once: the index, its governance schema and the gate read
// these rather than repeating 8 / ^W2G-IS-0[0-7]$ / the gate list in three places.
const sliceIndexSchemaVersion = "1.1.0";
const attestationSchemaVersion = "1.0.0";
const sliceIdPattern = "^W2G-IS-0[0-7]$";
const gateModel = ["G1", "CONTROL_SERVER_G2", "ONBOARD_HMI_G2", "G3"];
const slices = [
  ["W2G-IS-00", ["CV-SESSION-RECOVERY-HAPPY", "CV-SESSION-RECONNECT-DURING-RECOVERY", "CV-SNAPSHOT-REPLACE-AND-ACK", "CV-SNAPSHOT-SAME-REVISION-CONFLICT"]],
  ["W2G-IS-01", ["CV-DEMAND-ACCEPT-TO-PICKUP"], {
    scope: "DEMAND_ACCEPTANCE_AND_TO_PICKUP",
    requiredOutcomes: ["EXACTLY_ONE_ACCEPTED_DEMAND_SNAPSHOT", "EXACTLY_ONE_TO_PICKUP_INTENT", "EXACTLY_ONE_RIOT_ORDER", "TRUSTED_PICKUP_ARRIVAL", "COMMITTED_DEMAND_JOURNEY_PROJECTED"],
    demandRepresentation: { controlServerFact: "AcceptedDemandSnapshot", wireMessages: ["UpcomingStopPlanSnapshot", "CurrentStopWorklistSnapshot"], onboardMode: "READ_ONLY_COMMITTED_PROJECTION" },
    ownerResponsibilities: {
      controlServer: ["MESINGEST_FINAL_REREAD", "ATOMIC_DEMAND_ACCEPTANCE", "DEDUPLICATED_TO_PICKUP_INTENT", "RIOT_ORDER_RECONCILIATION", "TRUSTED_PICKUP_ARRIVAL_ADOPTION"],
      onboardHmi: ["DISPLAY_COMMITTED_DEMAND_JOURNEY", "DISPLAY_CURRENT_STOP", "NEVER_DISCOVER_SELECT_OR_BIND_DEMAND"],
    },
  }],
  ["W2G-IS-02", ["CV-PICKUP-SUBLOT-LOAD", "CV-LOAD-CORRECTION", "CV-LOAD-CANCELLATION-ALL-EMPTY"]],
  ["W2G-IS-03", ["CV-PREDEPARTURE-SAFETY-EXPIRES", "CV-OPERATION-RESULT-UNKNOWN-RECONCILE"]],
  ["W2G-IS-04", ["CV-GATE-UNLOAD-ALL-EMPTY"]],
  ["W2G-IS-05", ["CV-CONNECTION-LOSS-SAFE-FINISH", "CV-SESSION-RECONNECT-DURING-RECOVERY"]],
  ["W2G-IS-06", ["CV-RELIABLE-RETRY-SAME-CONTENT", "CV-RELIABLE-RETRY-DIFFERENT-CONTENT", "CV-REQUEST-FIRST-RESULT-REPLAY", "CV-OPERATION-RESULT-UNKNOWN-RECONCILE"]],
  ["W2G-IS-07", ["CV-OPERATION-RESULT-UNKNOWN-RECONCILE", "CV-EXCEPTION-RESUME", "CV-EXCEPTION-COMPENSATE", "CV-FAULT-CARGO-HANDOFF", "CV-FORCED-MECHANICAL-RECOVERY", "CV-MANUAL-CHARGING-RETURN"]],
].map(([integrationSliceId, vectorIds, definition], index) => {
  const slice = { integrationSliceId, sequence: index, prerequisites: index === 0 ? [] : index <= 4 ? [`W2G-IS-${String(index - 1).padStart(2, "0")}`] : ["W2G-IS-00"], vectorIds, gates: gateModel };
  if (definition) slice.definition = definition;
  slice.forbidUnclosedFailOrInconclusive = true;
  return slice;
});
writeJson("integration-slices/index.json", { schemaVersion: sliceIndexSchemaVersion, slices });

// Governance schemas. They are not part of the three frozen surfaces — they govern the manifest,
// the slice index and the external approval attestation — but G1 compiles and applies all three,
// so the generator owns them rather than leaving them as files nobody can regenerate.
const sha256Pattern = "^[0-9a-f]{64}$";
writeJson("schemas/governance/content-manifest.schema.json", {
  $schema: SCHEMA,
  $id: `${BASE_ID}/governance/content-manifest.schema.json`,
  title: "ProtocolContentManifest",
  type: "object",
  additionalProperties: false,
  required: ["status", "releaseVersion", "protocolVersion", "profileId", "repository", "generatedAt", "hashAlgorithm", "jsonCanonicalization", "fileTableSha256", "schemaBundleSha256", "examplesSha256", "vectorsSha256", "errorRegistrySha256", "messages", "denylistedMessageTypes", "files"],
  properties: {
    status: { const: "CONTENT_SNAPSHOT" },
    releaseVersion: { type: "string", pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    protocolVersion: { type: "integer", minimum: 1 },
    profileId: { type: "string", minLength: 1 },
    repository: { const: "8005-agv-protocol" },
    generatedAt: { type: "string", format: "date-time" },
    hashAlgorithm: { const: "SHA-256" },
    jsonCanonicalization: { type: "string", minLength: 1 },
    fileTableSha256: { $ref: "#/$defs/sha256" },
    schemaBundleSha256: { $ref: "#/$defs/sha256" },
    examplesSha256: { $ref: "#/$defs/sha256" },
    vectorsSha256: { $ref: "#/$defs/sha256" },
    errorRegistrySha256: { $ref: "#/$defs/sha256" },
    messages: { type: "object", minProperties: 1 },
    denylistedMessageTypes: { type: "array", items: { type: "string" }, uniqueItems: true },
    files: {
      type: "array",
      minItems: 1,
      items: {
        type: "object",
        additionalProperties: false,
        required: ["path", "role", "bytes", "sha256"],
        properties: {
          path: { type: "string", minLength: 1 },
          role: { type: "string", minLength: 1 },
          bytes: { type: "integer", minimum: 0 },
          sha256: { $ref: "#/$defs/sha256" },
        },
      },
    },
  },
  $defs: { sha256: { type: "string", pattern: sha256Pattern } },
});
writeJson("schemas/governance/integration-slice-index.schema.json", {
  $schema: SCHEMA,
  $id: `${BASE_ID}/governance/integration-slice-index.schema.json`,
  title: "IntegrationSliceIndex",
  type: "object",
  additionalProperties: false,
  required: ["schemaVersion", "slices"],
  properties: {
    schemaVersion: { const: sliceIndexSchemaVersion },
    slices: {
      type: "array",
      minItems: slices.length,
      maxItems: slices.length,
      items: {
        type: "object",
        additionalProperties: false,
        required: ["integrationSliceId", "sequence", "prerequisites", "vectorIds", "gates", "forbidUnclosedFailOrInconclusive"],
        properties: {
          integrationSliceId: { type: "string", pattern: sliceIdPattern },
          sequence: { type: "integer", minimum: 0, maximum: slices.length - 1 },
          prerequisites: { type: "array", items: { type: "string", pattern: sliceIdPattern }, uniqueItems: true },
          vectorIds: { type: "array", minItems: 1, items: { type: "string", pattern: "^CV-[A-Z0-9-]+$" }, uniqueItems: true },
          gates: { type: "array", const: gateModel },
          forbidUnclosedFailOrInconclusive: { const: true },
          definition: { $ref: "#/$defs/definition" },
        },
      },
    },
  },
  $defs: {
    tokenArray: { type: "array", minItems: 1, items: { type: "string", pattern: "^[A-Z][A-Z0-9_]+$" }, uniqueItems: true },
    definition: {
      type: "object",
      additionalProperties: false,
      required: ["scope", "requiredOutcomes", "demandRepresentation", "ownerResponsibilities"],
      properties: {
        scope: { type: "string", pattern: "^[A-Z][A-Z0-9_]+$" },
        requiredOutcomes: { $ref: "#/$defs/tokenArray" },
        demandRepresentation: {
          type: "object",
          additionalProperties: false,
          required: ["controlServerFact", "wireMessages", "onboardMode"],
          properties: {
            controlServerFact: { const: "AcceptedDemandSnapshot" },
            wireMessages: { type: "array", const: ["UpcomingStopPlanSnapshot", "CurrentStopWorklistSnapshot"] },
            onboardMode: { const: "READ_ONLY_COMMITTED_PROJECTION" },
          },
        },
        ownerResponsibilities: {
          type: "object",
          additionalProperties: false,
          required: ["controlServer", "onboardHmi"],
          properties: { controlServer: { $ref: "#/$defs/tokenArray" }, onboardHmi: { $ref: "#/$defs/tokenArray" } },
        },
      },
    },
  },
});
writeJson("schemas/governance/release-approval-attestation.schema.json", {
  $schema: SCHEMA,
  $id: `${BASE_ID}/governance/release-approval-attestation.schema.json`,
  title: "ProtocolReleaseApprovalAttestation",
  type: "object",
  additionalProperties: false,
  required: ["schemaVersion", "candidateVersion", "status", "protocolCommit", "contentManifestSha256", "approvals", "statement"],
  properties: {
    schemaVersion: { const: attestationSchemaVersion },
    candidateVersion: { type: "string", pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    status: { enum: ["PENDING", "APPROVED"] },
    protocolCommit: { type: ["string", "null"], pattern: "^[0-9a-f]{40}$" },
    contentManifestSha256: { type: ["string", "null"], pattern: sha256Pattern },
    approvals: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["ownerId", "decidedAt", "decision", "statement"],
        properties: {
          ownerId: { type: "string", minLength: 1 },
          decidedAt: { type: "string", format: "date-time" },
          decision: { const: "APPROVED" },
          statement: { type: "string", minLength: 1 },
        },
      },
    },
    statement: { type: "string", minLength: 1 },
  },
  allOf: [
    {
      if: { properties: { status: { const: "PENDING" } }, required: ["status"] },
      then: { properties: { protocolCommit: { type: "null" }, contentManifestSha256: { type: "null" }, approvals: { maxItems: 0 } } },
    },
    {
      if: { properties: { status: { const: "APPROVED" } }, required: ["status"] },
      then: { properties: { protocolCommit: { type: "string", pattern: "^[0-9a-f]{40}$" }, contentManifestSha256: { type: "string", pattern: sha256Pattern }, approvals: { minItems: 2, maxItems: 2 } } },
    },
  ],
});
// The tracked template is blank by construction and excluded from the content manifest, so filling
// in an approval cannot change the manifest hash that the approval is about. The completed copy
// stays outside Git as a GitHub Release Asset.
writeJson("attestations/release-approval.template.json", {
  schemaVersion: attestationSchemaVersion,
  candidateVersion,
  status: "PENDING",
  protocolCommit: null,
  contentManifestSha256: null,
  approvals: [],
  statement: "This tracked approval template is excluded from the content manifest. PENDING is not a ProtocolRelease approval. A completed copy must remain external and be uploaded as a GitHub Release Asset.",
});

writeJson("compatibility/report.json", {
  candidateVersion,
  protocolVersion,
  profileId,
  status: "SUPERSEDING_CANDIDATE",
  baseRelease: baseReleaseTag,
  classification: "BREAKING_PROTOCOL_VERSION_INCREASE",
  wireCompatibility: "INCOMPATIBLE_EXACT_IDENTITY_REQUIRED",
  changeSummary: `Freeze the ${profileDisplayName} protocol surface: ProtocolVersion ${protocolVersion}, profile ${profileId}, release ${candidateVersion}. Payload, delivery-class, error-registry and conformance-index changes against ${baseReleaseTag} are breaking; no negotiation and no downgrade path exist.`,
  runtimeRule: "Exact ProtocolVersion and exact materialized ProtocolReleaseIdentity required; no negotiation.",
  optionalFieldPolicy: "No optional payload fields exist in this candidate. Future optional fields require proof that omission and ignore preserve safety and business conclusions.",
  historyPolicy: "Published tags, commits, manifests, schemas, vectors and approvals are immutable; defects require a superseding release.",
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
    { name: "xunit.runner.visualstudio", version: "3.1.5", consumers: ["ControlServer test projects", "OnboardHmi test projects"] },
    { name: "Corvus.Json.Validator", version: "4.6.7", consumers: ["isolated .NET conformance process"] },
    { name: "ajv", version: "8.20.0", consumers: ["protocol G1"] },
    { name: "ajv-formats", version: "3.0.1", consumers: ["protocol G1"] },
  ],
  requiredAction: "Install or pin SDK 8.0.424 before reproducible product builds; do not treat the observed 8.0.29 runtime as equivalent evidence.",
});

writeText("docs/README.md", `# ${profileDisplayName} protocol candidate\n\nThis repository contains an approval-neutral **content snapshot**, not an approved ProtocolRelease. Machine-readable JSON Schema, the content manifest, the external approval attestation, errors, examples, vectors, the governance schemas and the integration-slice index are authoritative. Markdown is explanatory only.\n\nRun \`pnpm install --frozen-lockfile\`, \`pnpm manifest:finalize\` and \`pnpm g1\`. A PASS proves content and attestation consistency and reports their independent hashes. It does not turn a \`PENDING\` attestation into human G0 approval or prove either product implementation, G2/G3, real RIoT, real IO, target hardware or factory qualification.\n`);
writeText("docs/release-governance.md", `# Release governance\n\n- ProtocolVersion is exactly ${protocolVersion} for this candidate; runtime negotiation is forbidden.\n- \`manifest/release.json\` is an approval-neutral content snapshot. It hashes all governed protocol content except itself, \`attestations/\`, \`.git/\`, \`node_modules/\`, generated \`evidence/\` and \`.github/\`.\n- \`attestations/release-approval.template.json\` is a tracked, blank template governed by its JSON Schema and excluded from the content manifest. A completed \`release-approval.json\` must remain external to Git and be uploaded as a GitHub Release Asset. This prevents the approval record from changing either the manifest hash or the commit it approves.\n- A formal release requires exact repository, SemVer, annotated tag, full commit, ProtocolVersion, profile, content manifest hash, approval-attestation hash, schema bundle hash and vectors hash.\n- Both real product owners must approve the exact commit and content manifest hash in the attestation before an immutable tag/release is created. AI and CI cannot approve.\n- G1 validates the content manifest and attestation independently, verifies an approved attestation points at the current content manifest, requires two distinct owners, and reports both hashes. Candidate G1 uses the tracked blank template. Release G1 sets \`PROTOCOL_APPROVAL_ATTESTATION\` to the external completed asset. The annotated tag message and GitHub release metadata must record both reported hashes.\n- The attestation never contains its own hash. Its SHA-256 is computed from its final bytes and bound externally by the annotated tag and release metadata, avoiding another self-reference.\n- Release order is fixed: freeze and push the content commit; generate the external attestation against that commit and manifest; run G1 with \`PROTOCOL_APPROVAL_ATTESTATION\`; create annotated \`protocol-v<SemVer>\` tag pointing at the frozen content commit with both hashes in its message; then publish the same attestation as a release asset.\n- Required/type/enum/meaning/direction/delivery/dedup/persistence/recovery/error/side-effect changes are breaking and require a ProtocolVersion and release-major increase.\n- A conformance-index or trajectory correction may use a patch release only when it restores an already approved responsibility boundary, changes no message Schema or wire semantics, and both product owners approve that compatibility classification. It still changes the manifest/vector identity and invalidates affected G1/G2/G3 evidence.\n- Historical red evidence and released identities are immutable.\n`);
writeText("docs/candidate-limitations.md", `# Candidate limitations and release finalization\n\nThe candidate intentionally uses structurally valid synthetic zero hashes inside envelope examples. Examples are schema fixtures, not evidence of a materialized release identity.\n\nThe manifest/approval circularity is resolved by the owner-approved governance separation recorded on 2026-08-25. \`manifest/release.json\` is an approval-neutral content snapshot and excludes \`attestations/\`; a completed external \`release-approval.json\` GitHub Release Asset binds the final immutable candidate commit and content manifest hash. The repository tracks only its blank Schema-governed template. G1 validates both artifacts and reports both hashes for the annotated tag and GitHub release metadata.\n\n**Conformance vectors are a weak binding, and this candidate makes that explicit.** No assertion executor has ever read \`input.ndjson\` or \`expected.json\`: all five were searched and every \`vectorId\` reference is a label written by a human. This candidate therefore drops the \`runner/\` contracts rather than keeping a promise of an executor that does not exist. What replaces them is an architecture test in each implementation repository asserting that every \`vectorId\` has an identically named test. G2's "the vector is the criterion" is consequently a permanent weak binding: what is mechanically guaranteed is that a vector has a corresponding test, not that its bytes were executed.\n\n\`${baseReleaseTag}\` remains immutable. The current \`${candidateVersion}\` candidate is a breaking ProtocolVersion increase to ${protocolVersion} under profile \`${profileId}\`: message payloads, the error registry and the conformance index all change, and no negotiation or downgrade path exists. Its attestation remains \`PENDING\`; both product owners must approve the new exact commit, content manifest hash, vectors hash and breaking classification before \`protocol-v${candidateVersion}\` can be created.\n`);

writeJson("package.json", {
  name: "8005-agv-protocol",
  version: candidateVersion,
  private: true,
  type: "module",
  scripts: { g1: "node tools/g1-validate.mjs", "manifest:finalize": "node tools/finalize-manifest.mjs" },
  devDependencies: { ajv: "8.20.0", "ajv-formats": "3.0.1" },
  engines: { node: ">=20" },
  license: "UNLICENSED",
});

writeText("tools/finalize-manifest.mjs", renderTemplate("finalize-manifest.mjs"));

writeText("tools/g1-validate.mjs", renderTemplate("g1-validate.mjs"));

writeJson("manifest/release.json", { status: "CANDIDATE_UNFINALIZED", releaseVersion: candidateVersion, protocolVersion, profileId, repository: "8005-agv-protocol", denylistedMessageTypes: denylist, messages: Object.fromEntries(Object.values(specs).map((spec) => [spec.name, { sender: senderFor(spec.direction), receiver: receiverFor(spec.direction), direction: spec.direction, deliveryClass: spec.deliveryClass, correlationRule: correlationRuleFor(spec), transportDedupKey: "messageId", businessDedupKeys: spec.businessDedupKeys, durableBeforeSend: spec.deliveryClass === "RELIABLE", durableBeforeAck: spec.deliveryClass === "RELIABLE", recoveryRole: spec.recoveryRole, schema: `schemas/messages/${spec.name}.schema.json` }])) });
console.log(JSON.stringify({ generated: true, target: root, messageTypeCount: Object.keys(specs).length, invalidExamplePolicy: "required/type/enum/unique/sort/correlation plus profile and envelope semantics", trajectoryCount: Object.keys(trajectories).length, sliceCount: slices.length, errorCodeCount: errorCodeNames.length, errorCodesWithAsset: [...errorCodeAssets.values()].filter((count) => count > 0).length, errorCodesWithoutAsset: [...errorCodeAssets].filter(([, count]) => count === 0).map(([code]) => code) }, null, 2));
