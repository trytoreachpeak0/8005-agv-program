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
const BASE_ID = "https://schemas.8005-agv.local/agv-full-product/v7";
const candidateVersion = "6.0.0";
const profileId = "AGV_FULL_PRODUCT";
const profileDisplayName = "AGV_FULL_PRODUCT";
const protocolVersion = 7;
const baseReleaseTag = "protocol-v5.0.0";
// Fixed so the candidate tools stay byte-reproducible; it is a candidate stamp, not a build clock.
const candidateTimestamp = "2026-10-21T00:00:00Z";

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
    .replaceAll("__CANDIDATE_TIMESTAMP__", candidateTimestamp)
    // The gate used to keep its own copy of the vector list and its own slice-count and id-pattern
    // literals. Injecting them removes three chances for the gate and the tree to disagree.
    .replaceAll("__REQUIRED_VECTORS_JSON__", JSON.stringify(Object.keys(trajectories)))
    .replaceAll("__SLICE_COUNT__", String(slices.length))
    .replaceAll("__SLICE_ID_PREFIX__", sliceIdPrefix);
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
  // The nine distinctions the ControlServer already emits and the v1 registry never had a code
  // for. Each carries its own allowedMessageTypes, narrowed to the message the implementation
  // actually puts it in: "*" would claim these are legal anywhere a Problem can travel.
  ["RECOVERY_DEMAND_NOT_BLOCKED", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["ExceptionRecoverySessionRejected"],
    meaning: "The demand named by the recovery scope is not blocked, so no exception recovery session may be opened against it.",
  }],
  ["RECOVERY_EVENT_MISMATCH", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["RecoveryActionRejected"],
    meaning: "The eventId carried by the recovery action is not the event the exception recovery session was opened for.",
  }],
  ["RECOVERY_DEMAND_MISMATCH", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["RecoveryActionRejected"],
    meaning: "The demandId carried by the recovery action is not the demand the exception recovery session was opened for.",
  }],
  ["RECOVERY_OPERATOR_MISMATCH", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["RecoveryActionRejected"],
    meaning: "The operator submitting the recovery action is not the administrator who opened the exception recovery session.",
  }],
  ["RECOVERY_ACTION_ALREADY_SELECTED", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["RecoveryActionRejected"],
    meaning: "The exception recovery session has already selected a different recovery action.",
  }],
  ["RECOVERY_OPERATION_NOT_FOUND", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["RecoveryActionRejected"],
    meaning: "The exception recovery session is scoped to a demand, but no station operation exists for that demand.",
  }],
  ["PROVEN_RECOVERY_CHECKPOINT_REQUIRED", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["RecoveryActionRejected"],
    meaning: "RESUME_AFTER_REPAIR requires the vehicle to hold a proven recovery checkpoint for the unsettled slot operation attempt.",
  }],
  // The last two are blocking facts rather than rejections. They state why the session is waiting,
  // so they travel in ExceptionRecoverySessionSnapshot.blockingFacts and never in a Problem.
  ["RECOVERY_ACTION_REQUIRED", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["ExceptionRecoverySessionSnapshot"],
    meaning: "The exception recovery session is open and stays blocked until the operator selects a recovery action.",
  }],
  ["RECOVERY_RESULT_REQUIRED", "SAFETY_RECOVERY", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["ExceptionRecoverySessionSnapshot"],
    meaning: "A recovery action has been selected and the exception recovery session stays blocked until its result arrives.",
  }],
  // Release 2.0.0: why the control server rejects a SUBLOT after entry. ADR-cross-0057 lists four
  // real causes; these three plus the existing EXPECTED_BASKET_COUNT_MISMATCH (revalidated quantity
  // differs from the reservation) cover them. PACKAGE missing, unmatched and conflicting share one
  // code because ErrorCode is closed: finer field detail goes in the non-authoritative displayMessage.
  // introducedInRelease takes effect once the errorCodes mapping reads overrides (program#90).
  ["SUBLOT_NOT_IN_DISPATCH_SCOPE", "BUSINESS", "NEW_MESSAGE_ID", {
    allowedMessageTypes: ["SublotRejected"],
    meaning: "The SUBLOT entered by the operator does not belong to any demand in the current dispatch scope, so the control server rejects the entry (FR-001 AC-4).",
    introducedInRelease: "2.0.0",
  }],
  ["SUBLOT_BOX_COUNT_UNAVAILABLE", "BUSINESS", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["SublotRejected"],
    meaning: "Revalidation after SUBLOT entry found no usable SUBLOT_BOX_COUNT: the lookup failed, returned nothing or returned a non-positive count (BR-013 section 2).",
    introducedInRelease: "2.0.0",
  }],
  ["PACKAGE_CAPACITY_UNRESOLVED", "BUSINESS", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["SublotRejected"],
    meaning: "Revalidation after SUBLOT entry could not resolve basket capacity: PACKAGE is missing, or the approved capacity mapping has no match or conflicting matches (BR-013 section 2).",
    introducedInRelease: "2.0.0",
  }],
  // Release 2.0.0: the reason code of a determinate slot failure after the station deadline
  // (ADR-cross-0058 decision 5). Registered although the v2 onboard HMI never emits it: the control
  // server keeps a defensive determinate-failure settlement that needs a registered code, and another
  // onboard build sending it must still pass the closed enum. The MVP line puts it in exactly one
  // place, SlotResult.reasonCodes of a FAILED slot in OperationResult, hence the narrowing.
  ["OPERATOR_TIMEOUT", "BUSINESS", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["OperationResult"],
    meaning: "The operator did not complete the slot operation before the station departure deadline; the slot door is closed and the unlock output reset, so the slot is settled as a determinate failure rather than an unknown outcome (ADR-cross-0058 decision 5). The WIRE_TO_GATE_MVP line introduced a code of the same name and meaning in protocol-v0.3.0.",
    introducedInRelease: "2.0.0",
  }],
  // Release 3.0.0: the reason code of a slot an administrator declared faulty (CP-0005 section 4.3
  // item 3). It travels in one place, SlotResult.reasonCodes of the declared UNKNOWN slot in
  // OperationResult, so the result itself says it came from a declaration. SAFETY_RECOVERY and
  // MANUAL_REVIEW match RECOVERY_CHECKPOINT_NOT_UNIQUE, the code the restart workaround leaves on the
  // same slot: the slot leaves only through an exception recovery session, never by a retry.
  ["SLOT_FAULT_DECLARED", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["OperationResult"],
    meaning: "An administrator declared the slot faulty on the control server and the onboard HMI applied the declaration, so the slot's SlotResult in OperationResult has outcome UNKNOWN and carries this code in its reasonCodes, and the slot operation leaves only through an exception recovery session (REQ-0359, CP-0005 section 4.3 item 3).",
    introducedInRelease: "3.0.0",
  }],
  // Release 3.0.0: why an exception recovery session closed (control-server#169, #187). Like RECOVERY_ACTION_REQUIRED
  // and RECOVERY_RESULT_REQUIRED it is a state, not a rejection, so it travels in one place only:
  // ExceptionRecoverySessionSnapshot.closedReason of a CLOSED session. MANUAL_REVIEW because the way on is a
  // person's: an administrator looks at what the result left behind and opens a new session.
  ["RECOVERY_ACTION_RESULT_NOT_RECONCILED", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["ExceptionRecoverySessionSnapshot"],
    meaning: "The exception recovery session closed because its recovery action will not reconcile: the result reported FAILED or UNKNOWN, the result reported success that its per-slot results do not bear out, or the vehicle refused the SlotOperationResumeCommand with SlotOperationCommandRejected so no result will come; the demand stays blocked and an administrator opens a new exception recovery session to choose the next action.",
    introducedInRelease: "3.0.0",
  }],
  // Release 3.0.0: the onboard fatal-fault latch (onboard-hmi#191, #197), which until now borrowed DEPARTURE_UNSAFE in the
  // safety summary and VEHICLE_NOT_READY on a refused slot, so a log could not tell a latch from either. The allowed
  // messages are every place the onboard HMI writes the latch today: SafetySummary.reasonCodes in the three safety
  // messages, and the refused slot's SlotResult in OperationResult and in the four results of the shared recovery vector
  // executor. Listing a message permits the code there and obliges nobody to send it. MANUAL_REVIEW because only a person
  // lifts the latch.
  ["ONBOARD_FATAL_FAULT_LATCHED", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["SafetyStateChanged", "SafetyStateSnapshot", "PreDepartureSafetyCheckResult", "OperationResult", "LoadCorrectionResult", "LoadCancellationResult", "LoadCompensationResult", "FaultCargoRecoveryResult"],
    meaning: "The onboard HMI has latched a fatal safety fault: it reports departure unsafe and refuses to open any slot until a person reviews and resets the latch. It is not VEHICLE_NOT_READY, not a vehicle that has not come to a stop, and not an unsafe state caused by the slot operation in progress, so it is never forgiven as operation-induced unsafety.",
    introducedInRelease: "3.0.0",
  }],
  // Release 3.0.0 (CP-0009, REQ-0364, ADR-cross-0063): a cleared slot whose light curtain proves it empty while its door is
  // not proven locked. It travels on that slot's SlotResult in the two clearing results, beside overallOutcome
  // ALL_EMPTY_DOOR_UNPROVEN, and in VehicleBusinessStateSnapshot.blockingFacts for as long as the hold lasts, so the vehicle
  // can say why it is held after a restart. MANUAL_REVIEW because the vehicle leaves the hold only through a repair.
  ["SLOT_DOOR_LOCK_UNPROVEN_AFTER_EMPTY", "SAFETY_RECOVERY", "MANUAL_REVIEW", {
    allowedMessageTypes: ["LoadCancellationResult", "LoadCompensationResult", "VehicleBusinessStateSnapshot"],
    meaning: "The slot's light curtain reads EMPTY but its sensors cannot prove the door locked or the unlock output reset: the cargo business settles the slot as empty and the result carries overallOutcome ALL_EMPTY_DOOR_UNPROVEN, never ALL_EMPTY, which still means every slot EMPTY, LOCKED and RESET; no further slot is opened, and the vehicle stays held, whether a cancellation or a compensation left it held, until a HardwareRecoveryRecord on a HARDWARE_REPAIR_RELEASE recovery action, then LOCKED, RESET and EMPTY readings of the slot that the control server receives after the record, then a SAFE PreDepartureSafetyCheck with checkPurpose HOLD_RELEASE; the code stands in the blockingFacts of VehicleBusinessStateSnapshot for as long as the vehicle is held (REQ-0364, CP-0009).",
    introducedInRelease: "3.0.0",
  }],
  // Release 6.0.0 (CP-0021, REQ-0367, protocol#26): the remaining-baskets skip. The first marks a remaining slot of a skipped
  // load in the one place it travels, the slot's SlotResult in an OperationResult with overallOutcome COMPLETED_REMAINING_SKIPPED;
  // NEVER because the skip is final: the demand completes with the baskets it has, and the slot is not tried again for it.
  ["REMAINING_BASKETS_SKIPPED", "BUSINESS", "NEVER", {
    allowedMessageTypes: ["OperationResult"],
    meaning: "The slot is a remaining slot of a load the control server authorized to end short (REQ-0367, CP-0021): no basket was put in it under this operation, it is EMPTY, LOCKED and RESET, it is not opened again for this demand, and the slot and its reservation are released. It travels only on a NOT_STARTED SlotResult of an OperationResult with overallOutcome COMPLETED_REMAINING_SKIPPED.",
    introducedInRelease: "6.0.0",
  }],
  // A skip asks to end a load short, so a load with nothing in it cannot be skipped: k = 0 is a cancellation under REQ-0211.
  ["REMAINING_BASKETS_SKIP_NOTHING_LOADED", "BUSINESS", "AFTER_STATE_CHANGE", {
    allowedMessageTypes: ["RemainingBasketsSkipResult"],
    meaning: "The control server refuses a remaining-baskets skip because, by its own facts, no target slot of the slot operation attempt has closed safely OCCUPIED (k = 0): with nothing loaded the operator gives the demand up by cancelling it under REQ-0211, not by skipping (REQ-0367, CP-0021). The vehicle keeps loading.",
    introducedInRelease: "6.0.0",
  }],
  // The revised REQ-0211: once a basket is in a target slot the load can no longer be cancelled, only ended short.
  ["LOAD_CANCELLATION_BASKET_LOADED", "BUSINESS", "NEVER", {
    allowedMessageTypes: ["LoadCancellationAuthorization"],
    meaning: "The control server refuses to authorize a load cancellation because a basket has been loaded into a target slot of the demand's load (the revised REQ-0211, CP-0021): a load with a basket in it is never cancelled; to load fewer the operator asks for the remaining-baskets skip (REQ-0367), and a wrong load is corrected. The control server checks a cancellation in the order SLOT_STATE_UNKNOWN, LOAD_CANCELLATION_BASKET_LOADED, LOCK_NOT_CLOSED, UNLOCK_OUTPUT_NOT_RESET, and the first that fails decides: so a load with nothing loaded whose door is not proven locked or whose unlock output is not proven reset is refused with LOCK_NOT_CLOSED or UNLOCK_OUTPUT_NOT_RESET, never with this code.",
    introducedInRelease: "6.0.0",
  }],
];
const errorCodes = requiredErrorCodes.map(([code, category, retryDisposition, overrides = {}]) => ({
  code,
  category,
  meaning: overrides.meaning ?? `${code} is the stable ${category.toLowerCase()} failure defined by the accepted ${profileDisplayName} governance decision.`,
  allowedMessageTypes: overrides.allowedMessageTypes ??
    (category === "PROTOCOL" ? ["ProtocolProblem", "SessionRejected"] : ["*"]),
  retryDisposition,
  // Not candidateVersion: the registry is appendOnly, and a code keeps the release that introduced it.
  // Every code above shipped in protocol-v1.0.0; a code added for a later release names it in overrides.
  introducedInRelease: overrides.introducedInRelease ?? "1.0.0",
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
// MES TASK_TYPE, verbatim: these strings are the hardcoded literals of the UNION ALL branches in the
// factory IT query, one per branch. WIRE_TO_GATE is one of them, not a phase name. Release 5.0.0
// (protocol#21, program#195) appends WIRE_TO_FULL_INSPECTION, wire bonding to the full-inspection
// area; appended, so the released values keep their order. PublicStationFunction gains no matching
// segment: the product no longer maintains it (specification 5.3), and the control server sends a
// value only on a staging pickup leg, WIRE_STAGING (control-server#713), so none would carry it.
defs.TransportTaskType = E("DIE_TO_WIRE_STAGING", "DIE_TO_OVEN", "WIRE_TO_GATE", "WIRE_TO_OPTICAL", "STAGING_TO_WIRE", "WIRE_TO_NITROGEN", "WIRE_TO_FULL_INSPECTION");
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
  "DemandSelectionResult", "UnableToChargeFieldConfirmationResult", "ManualStationClearanceConfirmationResult",
]);
const requestNames = new Set([
  "SessionHello", "CapabilitySnapshotRequested", "SafetyStateSnapshotRequested", "PreDepartureSafetyCheck", "SublotSubmitted", "ManualChargingReturnToServiceRequested",
  "LoadCorrectionRequested", "LoadCancellationStartRequested", "LoadCompensationRequested", "ExceptionRecoverySessionRequested", "RecoveryActionSubmitted", "HardwareRecoveryRecordSubmitted",
  "DemandSelectionRequested", "UnableToChargeFieldConfirmationRequested", "ManualStationClearanceConfirmationRequested",
]);
const snapshotNames = new Set(["CapabilitySnapshot", "SafetyStateSnapshot", "VehicleBusinessStateSnapshot", "CurrentStopWorklistSnapshot", "UpcomingStopPlanSnapshot", "ExceptionRecoverySessionSnapshot", "OnboardAlarmSnapshot"]);
const telemetryNames = new Set(["OperationProgress"]);
const livenessNames = new Set(["Heartbeat", "HeartbeatAck"]);
const reliableNames = new Set([
  "RecoveryStateReport", "SessionReadiness", "SafetyStateChanged", "SublotEntryRequested", "SlotOperationCommand", "OperationResult", "LoadCorrectionCommand", "LoadCorrectionResult",
  "LoadCancellationResult", "LoadCompensationCommand", "LoadCompensationResult", "SlotOperationResumeCommand", "FaultCargoRecoveryCommand", "FaultCargoRecoveryResult",
  "ForcedMechanicalRecoveryCommand", "ForcedMechanicalRecoveryResult",
  "SlotConfigurationActivationCommand", "SlotConfigurationActivationResult",
  "SlotFaultDeclarationCommand", "SlotFaultDeclarationResult",
  "CurrentStopDepartureRequested", "CurrentStopDepartureResult",
  "RemainingBasketsSkipRequested", "RemainingBasketsSkipResult",
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
  DemandSelectionRequested: "O_TO_C", DemandSelectionResult: "C_TO_O",
  UnableToChargeFieldConfirmationRequested: "O_TO_C", UnableToChargeFieldConfirmationResult: "C_TO_O",
  ManualStationClearanceConfirmationRequested: "O_TO_C", ManualStationClearanceConfirmationResult: "C_TO_O",
  SlotConfigurationActivationCommand: "C_TO_O", SlotConfigurationActivationResult: "O_TO_C",
  OnboardAlarmSnapshot: "O_TO_C",
  SlotFaultDeclarationCommand: "C_TO_O", SlotFaultDeclarationResult: "O_TO_C",
  CurrentStopDepartureRequested: "O_TO_C", CurrentStopDepartureResult: "C_TO_O",
  RemainingBasketsSkipRequested: "O_TO_C", RemainingBasketsSkipResult: "C_TO_O",
};

const specs = {};
const checkPurposes = ["DEPARTURE", "NON_BUSINESS_MOVE", "HOLD_RELEASE"];
// Which of demandId, movementLegId and targetStationId each purpose carries (true) or leaves null (false).
const checkPurposeScope = { DEPARTURE: [true, true, true], NON_BUSINESS_MOVE: [false, true, true], HOLD_RELEASE: [false, false, false] };
const checkScopeFields = ["demandId", "movementLegId", "targetStationId"];
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
// 3.0.0 dropped supportsBatchUnlock: with one slot door open at a time (REQ-0357) it was always false,
// it never carried meaning, and neither end decided anything on it. Leaving it out is deliberate.
add("CapabilitySnapshot", { capabilityVersion: R("Revision"), observedAt: R("Instant"), slotModelVersion: S(), activeSlotConfigurationVersion: S(), activeSlotConfigurationFingerprint: R("Sha256"), slotStates: A(R("SlotState"), { minItems: 8, maxItems: 8, uniqueItems: true }), onboardJournalFormatVersion: I({ minimum: 1 }) }, { recoveryRole: "CAPABILITY_RECONCILIATION" });
add("RecoveryStateReport", { reportId: R("Id"), observedAt: R("Instant"), unsettledSlotOperationAttemptId: Nullable(R("Id")), provenRecoveryCheckpoint: E("NONE", "PREPARED", "ACTIVE_UNLOCK_SET", "SAFE_FINISH_REACHED", "RESULT_RECORDED"), activeUnlockSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), forcedRecoveryGeneration: R("Generation"), pendingResults: A(R("PendingResultRef"), { uniqueItems: true }), journalContentSha256: R("Sha256") }, { businessDedupKeys: ["reportId"], recoveryRole: "JOURNAL_RECONCILIATION" });
add("SessionReadiness", { readiness: E("READY", "RECOVERY_REQUIRED"), decidedAt: R("Instant"), reasonCodes: A(R("ErrorCode"), { uniqueItems: true }), acceptedCapabilityVersion: R("Revision"), acceptedSafetyStateVersion: R("Revision"), vehicleBusinessStateRevision: R("Revision") }, { recoveryRole: "HANDSHAKE_DECISION" });
add("SafetyStateChanged", { safetyStateVersion: R("Revision"), observedAt: R("Instant"), safety: R("SafetySummary"), affectedSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }) }, { recoveryRole: "SAFETY_RECONCILIATION" });
add("SafetyStateSnapshotRequested", { requestedSafetyStateVersion: Nullable(R("Revision")), reason: E("HANDSHAKE", "VERSION_GAP", "PRE_MOVEMENT_RECONCILIATION") }, { recoveryRole: "SAFETY_RECONCILIATION" });
add("SafetyStateSnapshot", { safetyStateVersion: R("Revision"), observedAt: R("Instant"), safety: R("SafetySummary"), slotStates: A(R("SlotState"), { minItems: 8, maxItems: 8, uniqueItems: true }) }, { recoveryRole: "SAFETY_RECONCILIATION" });
// Release 3.0.0 (program#150): checkPurpose says what the check is for. ADR-cross-0009 asks for a fresh check before every
// movement request, and REQ-0364 for a passed check before a vehicle held for an unproven door takes work again, yet only a
// business departure has a demand. DEPARTURE carries demand, movement leg and target station as before; NON_BUSINESS_MOVE
// (idle return, charging) carries the leg and the station without a demand; HOLD_RELEASE carries none of the three. The
// result echoes the purpose, so the answer says what it answers.
add("PreDepartureSafetyCheck", { preDepartureSafetyCheckId: R("Id"), checkPurpose: E(...checkPurposes), demandId: Nullable(R("Id")), movementLegId: Nullable(R("Id")), expectedSafetyStateVersion: R("Revision"), targetStationId: Nullable(S()) }, { businessDedupKeys: ["preDepartureSafetyCheckId"] });
add("PreDepartureSafetyCheckResult", { preDepartureSafetyCheckId: R("Id"), checkPurpose: E(...checkPurposes), outcome: E("SAFE", "UNSAFE", "UNKNOWN"), observedAt: R("Instant"), safetyStateVersion: R("Revision"), validUntil: R("Instant"), safety: R("SafetySummary") }, { businessDedupKeys: ["preDepartureSafetyCheckId"] });
// Release 4.0.0 (program#185 CP-0012, protocol#13) appends two ways a loading phase and a stop end, to both closed enums
// alike, so the vehicle tells the operator the same thing in the phase and on the empty worklist: OPERATOR_DEPARTED, the
// operator pressed depart at a STAGING_TO_WIRE staging pickup stop (CurrentStopDepartureRequested); CHARGING_REQUIRED, the
// vehicle fell below the mandatory charge line there and departs to deliver its cargo before it charges (protocol#15,
// program#188 CP-0013).
// Appended, so the released values keep their order.
const loadingClosedReasons = ["VEHICLE_FULL", "CARGO_HOLDING_TIMEOUT", "WAITING_STATION_YIELD", "PLANNED_LOADING_COMPLETE", "OPERATOR_DEPARTED", "CHARGING_REQUIRED"];
const stopEndedReasons = ["COMPLETED", "STATION_DEADLINE_EXPIRED", "LOAD_CANCELLED", "LOAD_COMPENSATED", "CARGO_HANDED_OFF", "DEMAND_RELEASED", "TRIP_TERMINATED", "OPERATOR_DEPARTED", "CHARGING_REQUIRED"];
// Release 2.0.0 (program#94): batteryState and chargingCycleState are orthogonal, per full-product
// ticket 06's B5 table. loadingPhase is null without a transport journey, and carries a closedReason
// exactly when its state is CLOSED.
add("VehicleBusinessStateSnapshot", { vehicleBusinessStateRevision: R("Revision"), readiness: E("READY", "RECOVERY_REQUIRED"), activePurpose: Nullable(E("TRANSPORT", "CHARGING", "CLEARING_MAINTENANCE", "IDLE_RETURN")), manualChargingHold: B(), batteryState: E("SUFFICIENT", "LOW", "UNKNOWN", "MANDATORY_CHARGE"), chargingCycleState: E("NOT_CHARGING", "ALLOCATED", "EN_ROUTE", "CHARGING", "COMPLETE", "UNABLE_TO_CHARGE", "UNKNOWN"), loadingPhase: Nullable(O({ state: E("LOADING", "CARGO_HOLDING_WAIT", "VEHICLE_FULL", "CLOSED"), cargoHoldingDeadlineAt: Nullable(R("Instant")), closedReason: Nullable(E(...loadingClosedReasons)) }, { if: { properties: { state: { const: "CLOSED" } }, required: ["state"] }, then: { properties: { closedReason: { type: "string" } } }, else: { properties: { closedReason: { type: "null" } } } })), blockingFacts: A(R("BlockingFact"), { uniqueItems: true }), observedAt: R("Instant") });
// Release 3.0.0 (program#86, #150): stopEndedReason says why the stop ended, so the vehicle can tell the operator more than
// "nothing pending". Null while the worklist has items; required once it is empty, because the control server sends an
// empty worklist from exactly two places (JourneyClosure, StopEndWorklist) and every caller of either knows why. The
// reasons are the operator's, one per way a stop ends, not the demands' terminal codes. The item shape is 2.0.0's.
add("CurrentStopWorklistSnapshot", { stationId: S(), worklistRevision: R("Revision"), operationSessionId: Nullable(R("Id")), stationDepartureDeadlineAt: Nullable(R("Instant")), items: A(O({ demandId: R("Id"), transportDemandKey: S(), sublot: S(), workType: R("TransportTaskType"), stopRole: E("PICKUP", "DROPOFF"), expectedBasketCount: I({ minimum: 1, maximum: 8 }) }), { maxItems: 8 }), stopEndedReason: Nullable(E(...stopEndedReasons)) }, { businessDedupKeys: ["worklistRevision"] });
add("UpcomingStopPlanSnapshot", { planRevision: R("Revision"), legs: A(O({ movementLegId: R("Id"), legType: Nullable(E("TO_PICKUP", "TO_DROPOFF")), stopPurposeCategory: R("StopPurposeCategory"), demandId: Nullable(R("Id")), publicStationFunction: Nullable(R("PublicStationFunction")), sequence: I({ minimum: 1, maximum: 9 }), stationId: S(), mapId: S(), state: E("PLANNED", "ACTIVE", "ARRIVED", "COMPLETED", "BLOCKED") }), { maxItems: 9, uniqueItems: true, "x-sortedBy": "sequence" }) }, { businessDedupKeys: ["planRevision"] });
// Release 2.0.0: sublot entry is scoped to the dispatch. The control server offers every SUBLOT in
// scope, the vehicle reports only what was scanned, and the control server resolves the demand
// (FP-IS-01 NEVER_DISCOVER_SELECT_OR_BIND_DEMAND). One worklistRevision offers one scope, so the
// request is identified by it. A submission and its rejection carry no business identity: a rescan
// of the same SUBLOT may differ in entryMethod, operator and revalidated reason, so any key short of
// the whole payload would call it a conflict. Each entry is its own messageId, and SublotRejected
// points back at it through correlationId.
// expiresOnRevisionChange stays const true (program#150): both ends implement specification 23.5, and the literal name read
// alone suggests any revision advance withdraws the request. Its description is the definition the wire notes carry, the
// same string, so the two cannot drift apart.
const revisionChangeDefinition = "`true` means the entry request expires on a revision change, and a revision change is: the stop ended, the operation session or the station changed (a worklist for another operation session or station with a strictly higher revision), the worklist became empty (a worklist no older than the entry request with empty `items`), or the control server rejected the submission with `WORKLIST_REVISION_STALE`. A worklist revision advancing within the same operation session at the same station is not a revision change, and the entry request stays open.";
add("SublotEntryRequested", { operationSessionId: R("Id"), stationId: S(), worklistRevision: R("Revision"), expectedSublots: StringArray({ minItems: 1, maxItems: 8, uniqueItems: true }), entryMethods: A(S(), { const: ["SCANNER", "KEYBOARD"] }), expiresOnRevisionChange: B({ const: true, description: revisionChangeDefinition }) }, { businessDedupKeys: ["operationSessionId", "worklistRevision"] });
add("SublotSubmitted", { operationSessionId: R("Id"), stationId: S(), worklistRevision: R("Revision"), sublot: S(), entryMethod: E("SCANNER", "KEYBOARD"), operator: R("OperatorContext") });
add("SublotRejected", { demandId: Nullable(R("Id")), operationSessionId: R("Id"), problem: R("Problem"), currentWorklistRevision: R("Revision"), rejectedSublot: S() });
add("SlotOperationCommand", { demandId: R("Id"), operationSessionId: R("Id"), slotOperationAttemptId: R("Id"), operationType: E("LOAD", "UNLOAD"), slots: Slots(), expectedBasketCount: I({ minimum: 1, maximum: 8 }), expectedFinalPhysicalState: E("OCCUPIED", "EMPTY"), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["demandId", "slotOperationAttemptId"], recoveryRole: "SLOT_OPERATION" });
add("SlotOperationCommandRejected", { slotOperationAttemptId: R("Id"), problem: R("Problem"), observedCapabilityVersion: R("Revision"), conflictingContentSha256: Nullable(R("Sha256")) }, { businessDedupKeys: ["slotOperationAttemptId"] });
add("OperationProgress", { slotOperationAttemptId: R("Id"), phase: E("PREPARING", "UNLOCKING", "WAITING_OPERATOR", "VERIFYING", "SAFE_FINISH", "PAUSED"), activeUnlockSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), completedSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), observedAt: R("Instant") }, { businessDedupKeys: ["slotOperationAttemptId"] });
// Release 6.0.0 (CP-0021, REQ-0367, protocol#26) appends COMPLETED_REMAINING_SKIPPED: a load the control server authorized to
// end short, its k loaded slots COMPLETED and the rest NOT_STARTED with REMAINING_BASKETS_SKIPPED. An end that reads only
// overallOutcome never takes it for a load of every target slot. No field names the authorization: an attempt is authorized at
// most once, so the control server finds it by (demandId, slotOperationAttemptId), and every other OperationResult either end
// builds keeps the 5.0.0 fields (review M2).
add("OperationResult", { demandId: R("Id"), slotOperationAttemptId: R("Id"), operationType: E("LOAD", "UNLOAD"), overallOutcome: E("COMPLETED", "FAILED", "UNKNOWN", "COMPLETED_REMAINING_SKIPPED"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant"), journalCheckpoint: S(), resultContentSha256: R("Sha256") }, { businessDedupKeys: ["demandId", "slotOperationAttemptId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("ManualChargingReturnToServiceRequested", { requestId: R("Id"), administrator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), reason: S(), observedBatteryPercent: Nullable(N({ minimum: 0, maximum: 100 })) }, { businessDedupKeys: ["requestId"] });
add("ManualChargingReturnToServiceResult", { requestId: R("Id"), outcome: E("RETURNED_TO_ELIGIBILITY_EVALUATION", "REJECTED"), problem: Nullable(R("Problem")), vehicleBusinessStateRevision: R("Revision") }, { businessDedupKeys: ["requestId"] });
add("LoadCorrectionRequested", { correctionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slots: Slots(), operator: R("OperatorContext"), reason: S() }, { businessDedupKeys: ["correctionId", "demandId", "slotOperationAttemptId"] });
add("LoadCorrectionRejected", { correctionId: R("Id"), problem: R("Problem") }, { businessDedupKeys: ["correctionId"] });
add("LoadCorrectionCommand", { correctionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slots: Slots(), expectedSequence: A(S(), { const: ["EMPTY", "OCCUPIED"] }), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["correctionId", "demandId", "slotOperationAttemptId"], recoveryRole: "LOAD_CORRECTION" });
add("LoadCorrectionResult", { correctionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), overallOutcome: E("COMPLETED", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant") }, { businessDedupKeys: ["correctionId", "demandId", "slotOperationAttemptId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("LoadCancellationStartRequested", { cancellationId: R("Id"), demandId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), operator: R("OperatorContext"), reason: S() }, { businessDedupKeys: ["cancellationId", "demandId"] });
add("LoadCancellationAuthorization", { cancellationId: R("Id"), decision: E("AUTHORIZED", "REJECTED"), demandId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), slots: A(R("SlotNo"), { maxItems: 8, "x-sortedAscending": true }), problem: Nullable(R("Problem")) }, { businessDedupKeys: ["cancellationId", "demandId"] });
add("LoadCancellationResult", { cancellationId: R("Id"), demandId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), overallOutcome: E("ALL_EMPTY", "FAILED", "UNKNOWN", "ALL_EMPTY_DOOR_UNPROVEN"), slotResults: A(R("SlotResult"), { minItems: 0, maxItems: 8, uniqueItems: true }), observedAt: R("Instant") }, { businessDedupKeys: ["cancellationId", "demandId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("LoadCompensationRequested", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), operator: R("OperatorContext") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId", "demandId", "slotOperationAttemptId"] });
add("LoadCompensationRejected", { recoveryActionId: R("Id"), problem: R("Problem") }, { businessDedupKeys: ["recoveryActionId"] });
add("LoadCompensationCommand", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slots: Slots(), expectedFinalPhysicalState: S({ const: "EMPTY" }), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId", "demandId", "slotOperationAttemptId"], recoveryRole: "LOAD_COMPENSATION" });
// Release 3.0.0 (CP-0009): ALL_EMPTY_DOOR_UNPROVEN on both clearing results -- every slot EMPTY by its light curtain, some
// door not proven locked or its output not proven reset. ALL_EMPTY keeps meaning EMPTY, LOCKED and RESET on every slot, so an
// end that reads only overallOutcome never takes an unproven door for a closed operation and lets the vehicle go.
add("LoadCompensationResult", { recoveryActionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), overallOutcome: E("ALL_EMPTY", "FAILED", "UNKNOWN", "ALL_EMPTY_DOOR_UNPROVEN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), observedAt: R("Instant") }, { businessDedupKeys: ["recoveryActionId", "demandId", "slotOperationAttemptId"], recoveryRole: "PENDING_RESULT_REPLAY" });
// The recovery actions, written once for the four places that carry them. Release 3.0.0 (CP-0009, program#150) appends
// HARDWARE_REPAIR_RELEASE: the way out of the hold an unproven door leaves after a clearing proved the slots empty. It commands
// no slot IO; its only effect is that a HardwareRecoveryRecord can be bound to it, and the control server offers it only while
// the vehicle is held for an unproven door. Appended, so the released four keep their order.
const recoveryActions = ["RESUME_AFTER_REPAIR", "COMPENSATE_LOAD_ALL_EMPTY", "FAULT_CARGO_HANDOFF", "FORCED_MECHANICAL_RECOVERY", "HARDWARE_REPAIR_RELEASE"];
add("ExceptionRecoverySessionRequested", { requestId: R("Id"), administrator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), eventId: R("Id"), demandId: Nullable(R("Id")), slots: Slots(), reason: S(), authenticationProof: S({ examples: ["INVALID-PLACEHOLDER-NOT-A-SECRET"] }) }, { businessDedupKeys: ["requestId", "eventId"], recoveryRole: "EXCEPTION_SESSION" });
add("ExceptionRecoverySessionOpened", { requestId: R("Id"), exceptionRecoverySessionId: R("Id"), openedAt: R("Instant"), eventId: R("Id"), demandId: Nullable(R("Id")), slotOperationAttemptId: Nullable(R("Id")), slots: Slots(), recoverySessionRevision: R("Revision") }, { businessDedupKeys: ["requestId", "exceptionRecoverySessionId", "eventId"], recoveryRole: "EXCEPTION_SESSION" });
add("ExceptionRecoverySessionRejected", { requestId: R("Id"), problem: R("Problem") }, { businessDedupKeys: ["requestId"] });
// Release 3.0.0 (control-server#169): closedReason says why a CLOSED session closed, null on a normal close and on every
// state before CLOSED. blockingFacts cannot carry it: they are empty once the session is CLOSED.
add("ExceptionRecoverySessionSnapshot", { exceptionRecoverySessionId: R("Id"), recoverySessionRevision: R("Revision"), state: E("OPEN", "ACTION_SELECTED", "EXECUTING", "CLOSED"), administratorId: S(), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), eventId: R("Id"), demandId: Nullable(R("Id")), slotOperationAttemptId: Nullable(R("Id")), slots: Slots(), selectedAction: Nullable(E(...recoveryActions)), allowedActions: A(E(...recoveryActions), { uniqueItems: true }), blockingFacts: A(R("BlockingFact"), { uniqueItems: true }), closedReason: Nullable(R("ErrorCode")) }, { businessDedupKeys: ["exceptionRecoverySessionId", "eventId"], recoveryRole: "EXCEPTION_SESSION" });
add("RecoveryActionSubmitted", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), action: E(...recoveryActions), eventId: R("Id"), demandId: Nullable(R("Id")), slots: Slots(), operator: R("OperatorContext"), reason: S() }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId", "eventId"], recoveryRole: "RECOVERY_ACTION" });
add("RecoveryActionAccepted", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), slotOperationAttemptId: Nullable(R("Id")), acceptedAction: E(...recoveryActions), recoverySessionRevision: R("Revision"), acceptedAt: R("Instant") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId"], recoveryRole: "RECOVERY_ACTION" });
add("RecoveryActionRejected", { recoveryActionId: R("Id"), exceptionRecoverySessionId: R("Id"), problem: R("Problem"), recoverySessionRevision: R("Revision") }, { businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId"] });
add("HardwareRecoveryRecordSubmitted", { recordId: R("Id"), exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), operator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), slots: Slots(), checksPerformed: StringArray({ minItems: 1, uniqueItems: true }), actionsPerformed: StringArray({ minItems: 1, uniqueItems: true }), observations: StringArray({ minItems: 1 }), observedAt: R("Instant") }, { businessDedupKeys: ["recordId", "exceptionRecoverySessionId", "recoveryActionId"], recoveryRole: "HARDWARE_RECORD" });
add("HardwareRecoveryRecordResult", { recordId: R("Id"), outcome: E("RECORDED", "REJECTED"), problem: Nullable(R("Problem")), recoverySessionRevision: R("Revision") }, { businessDedupKeys: ["recordId"] });
add("SlotOperationResumeCommand", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), provenRecoveryCheckpoint: E("PREPARED", "ACTIVE_UNLOCK_SET", "SAFE_FINISH_REACHED"), slots: Slots(), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "demandId", "slotOperationAttemptId"], recoveryRole: "RESUME" });
add("FaultCargoRecoveryCommand", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: R("Id"), slots: Slots(), handoffId: R("Id"), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "demandId", "handoffId"], recoveryRole: "FAULT_CARGO_HANDOFF" });
add("FaultCargoRecoveryResult", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: R("Id"), handoffId: R("Id"), overallOutcome: E("HANDED_OFF", "FAILED", "UNKNOWN"), slotResults: A(R("SlotResult"), { minItems: 1, maxItems: 8, uniqueItems: true }), operator: R("OperatorContext"), observedAt: R("Instant") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "demandId", "handoffId"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("ForcedMechanicalRecoveryCommand", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), demandId: Nullable(R("Id")), forcedRecoveryGeneration: R("Generation"), slots: Slots(), commandContentSha256: R("Sha256") }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "forcedRecoveryGeneration"], recoveryRole: "FORCED_MECHANICAL_RECOVERY" });
// Release 3.0.0 (REQ-0242, control-server#137): cargoHandoff is the forced-removal cargo handoff record: the product
// identified by its SUBLOT, the named person it was handed to and when. demandId copies ForcedMechanicalRecoveryCommand.demandId.
// The record is non-null exactly when the vehicle was MECHANICALLY_ISOLATED on a session with a demand: once that result is
// acknowledged the vehicle drops its recovery context for the demand, so the record is the only thing the control server can
// settle the demand on, and without it the demand could never leave RecoveryRequired. There is no unidentified branch: by the
// user's site fact of 2026-09-29 staff always identify what they take out. The receiver is a name, not an OperatorContext:
// the person taking the cargo need not have been verified on the vehicle. The two proofs stay false.
add("ForcedMechanicalRecoveryResult", { exceptionRecoverySessionId: R("Id"), recoveryActionId: R("Id"), forcedRecoveryGeneration: R("Generation"), outcome: E("MECHANICALLY_ISOLATED", "FAILED", "UNKNOWN"), slots: Slots(), operator: R("OperatorContext"), observedAt: R("Instant"), electronicEmptyProven: B({ const: false }), vehicleReadyProven: B({ const: false }), demandId: Nullable(R("Id")), cargoHandoff: Nullable(O({ sublot: S(), receiverName: S(), handedOverAt: R("Instant") })) }, { businessDedupKeys: ["exceptionRecoverySessionId", "recoveryActionId", "forcedRecoveryGeneration"], recoveryRole: "PENDING_RESULT_REPLAY" });
add("DurableAck", { acceptedMessageId: R("Id"), acceptedMessageType: S(), acceptedContentSha256: R("Sha256"), durablyAcceptedAt: R("Instant") }, { businessDedupKeys: ["acceptedMessageId"], recoveryRole: "DURABLE_ACCEPTANCE" });
add("SnapshotAppliedAck", { snapshotMessageId: R("Id"), snapshotKind: E("CAPABILITY", "SAFETY_STATE", "VEHICLE_BUSINESS_STATE", "CURRENT_STOP_WORKLIST", "UPCOMING_STOP_PLAN", "EXCEPTION_RECOVERY_SESSION", "ONBOARD_ALARM"), appliedRevision: R("Revision"), appliedContentSha256: R("Sha256") }, { businessDedupKeys: ["snapshotMessageId"], recoveryRole: "SNAPSHOT_ADOPTION" });
add("ProtocolProblem", { rejectedMessageId: R("Id"), rejectedMessageType: Nullable(S()), problem: R("Problem"), expectedProtocolVersion: I({ const: protocolVersion }), expectedProfileId: S({ const: profileId }), expectedProtocolReleaseManifestSha256: R("Sha256") });
// --- v2 additions. All nine take the single-Result shape: one outcome enum plus a nullable
// problem, never an Accepted/Rejected pair. The pair form would cost four more schemas and about
// a hundred more examples and buy no expressiveness. ---

// The onboard side picks which committed worklist item to work next. It never discovers, selects
// or binds a Demand: the list it picks from is the one the control server committed.
add("DemandSelectionRequested", { selectionRequestId: R("Id"), stationId: S(), worklistRevision: R("Revision"), selectedDemandId: R("Id"), operator: R("OperatorContext"), requestedAt: R("Instant") }, { businessDedupKeys: ["selectionRequestId"] });
add("DemandSelectionResult", { selectionRequestId: R("Id"), outcome: E("SELECTED", "REJECTED"), problem: Nullable(R("Problem")), operationSessionId: Nullable(R("Id")), currentWorklistRevision: R("Revision") }, { businessDedupKeys: ["selectionRequestId"] });

// Charging failure is a field observation before it is a policy decision: the vehicle reports what
// it saw at the charger, the control server decides what that means for the charging cycle.
add("UnableToChargeFieldConfirmationRequested", { confirmationRequestId: R("Id"), chargerStationId: S(), observedCondition: E("CHARGER_UNREACHABLE", "CHARGER_OCCUPIED", "CONNECTION_FAILED", "CHARGER_FAULT"), operator: R("OperatorContext"), observedAt: R("Instant") }, { businessDedupKeys: ["confirmationRequestId"] });
add("UnableToChargeFieldConfirmationResult", { confirmationRequestId: R("Id"), outcome: E("CONFIRMED", "REJECTED"), problem: Nullable(R("Problem")), chargingPolicyDecision: Nullable(E("RETRY_LATER", "MANUAL_CHARGING_HOLD", "REASSIGN_CHARGER")) }, { businessDedupKeys: ["confirmationRequestId"] });

// Clearing a blocked public station is a human act; the wire only carries who confirmed it and
// whether the control server released the station's occupancy as a result.
add("ManualStationClearanceConfirmationRequested", { confirmationRequestId: R("Id"), stationId: S(), publicStationFunction: Nullable(R("PublicStationFunction")), clearedCondition: E("STATION_EMPTY", "OBSTRUCTION_REMOVED", "CARGO_RELOCATED"), operator: R("OperatorContext"), observedAt: R("Instant") }, { businessDedupKeys: ["confirmationRequestId"] });
add("ManualStationClearanceConfirmationResult", { confirmationRequestId: R("Id"), outcome: E("CONFIRMED", "REJECTED"), problem: Nullable(R("Problem")), stationReleased: B() }, { businessDedupKeys: ["confirmationRequestId"] });

// RELIABLE rather than REQUEST/RESPONSE: activating a slot configuration must not be guessed
// successful, which is exactly what PENDING_RESULT_REPLAY exists for. A RESPONSE has no re-report
// semantics, so a disconnect would simply lose the answer.
add("SlotConfigurationActivationCommand", { activationId: R("Id"), targetSlotConfigurationVersion: S(), targetSlotConfigurationFingerprint: R("Sha256"), expectedActiveSlotConfigurationVersion: Nullable(S()), administrator: R("OperatorContext"), issuedAt: R("Instant") }, { businessDedupKeys: ["activationId"], recoveryRole: "SLOT_CONFIGURATION" });
add("SlotConfigurationActivationResult", { activationId: R("Id"), outcome: E("ACTIVATED", "REJECTED", "UNKNOWN"), problem: Nullable(R("Problem")), activeSlotConfigurationVersion: S(), activeSlotConfigurationFingerprint: R("Sha256"), verifiedAt: R("Instant") }, { businessDedupKeys: ["activationId"], recoveryRole: "PENDING_RESULT_REPLAY" });

// Alarms are a snapshot, not an event stream: an event stream's reconnect gap is precisely the
// "stale" display state the rules forbid. AlarmEntry.code is an open set, deliberately not
// ErrorCode.
add("OnboardAlarmSnapshot", { alarmSnapshotRevision: R("Revision"), observedAt: R("Instant"), alarms: A(R("AlarmEntry"), { uniqueItems: true }) }, { recoveryRole: "SNAPSHOT_ADOPTION" });

// Release 3.0.0 (REQ-0359, CP-0005 section 4.3 items 1-2): an administrator declares on the control
// server that the slot an operation is waiting on is faulty. Both messages are RELIABLE, so a
// declaration survives a disconnect and its result is replayed; neither is a response, so
// correlationId stays null and declarationId alone ties the result to the declaration. The result
// comes first and OperationResult (UNKNOWN for the declared slot) follows, as CV-SLOT-FAULT-DECLARATION-APPLIED
// fixes. NOT_APPLICABLE carries ACTION_NOT_ALLOWED_IN_STATE and changes no business state.
add("SlotFaultDeclarationCommand", { declarationId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), slotNo: R("SlotNo"), administrator: R("OperatorContext"), administratorRole: E("MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"), faultCategory: E("LOCK", "LIGHT_CURTAIN", "DOOR_MECHANISM", "IO_MODULE"), note: S(), declaredAt: R("Instant") }, { businessDedupKeys: ["declarationId"], recoveryRole: "SLOT_FAULT_DECLARATION" });
add("SlotFaultDeclarationResult", { declarationId: R("Id"), slotOperationAttemptId: R("Id"), outcome: E("APPLIED", "NOT_APPLICABLE"), problem: Nullable(R("Problem")) }, { businessDedupKeys: ["declarationId"], recoveryRole: "PENDING_RESULT_REPLAY" });

// Release 4.0.0 (program#185 CP-0012, protocol#13): the operator asks to leave the current stop now. Both messages are RELIABLE,
// the SlotFaultDeclaration shape: the press is journaled before it is sent and survives a disconnect, and the control
// server's answer is durable and replayed, so a refusal is never lost behind a DurableAck that only says "received".
// correlationId stays null and departureRequestId alone ties the result to the request; the same departureRequestId again is
// answered with the same result and no second effect. The request echoes the worklist the vehicle shows: operationSessionId
// is null whenever that worklist carries none, which an empty worklist always does -- and a vehicle holding cargo at the
// staging station, where depart is pressed most, shows an empty one. ACCEPTED is followed by the snapshots that carry the
// departure (loadingPhase CLOSED with OPERATOR_DEPARTED, the worklist, the plan); REJECTED carries why and changes nothing.
add("CurrentStopDepartureRequested", { departureRequestId: R("Id"), operationSessionId: Nullable(R("Id")), stationId: S(), worklistRevision: R("Revision"), operator: R("OperatorContext") }, { businessDedupKeys: ["departureRequestId"], recoveryRole: "CURRENT_STOP_DEPARTURE" });
add("CurrentStopDepartureResult", { departureRequestId: R("Id"), outcome: E("ACCEPTED", "REJECTED"), problem: Nullable(R("Problem")), currentWorklistRevision: R("Revision") }, { businessDedupKeys: ["departureRequestId"], recoveryRole: "PENDING_RESULT_REPLAY" });

// Release 6.0.0 (CP-0021, REQ-0367, protocol#26): the operator asks to leave the remaining baskets of a multi-basket load, and
// only the control server's authorization lets the vehicle end the load short. A message pair rather than a new OperationResult
// outcome alone: an outcome alone would let the vehicle end the load first and tell the control server afterwards. Both RELIABLE,
// the CurrentStopDeparture shape: the press is journaled before it is sent and survives a disconnect or a restart, and the answer
// is durable and replayed. loadedSlots are the k target slots the vehicle has closed safely OCCUPIED; at least one, so k = 0 --
// a cancellation under REQ-0211 -- cannot be asked for. The operator is recorded when known and is never a condition (CP-0021
// new item 1 note 8). An authorization names exactly the slots the vehicle then reports COMPLETED; a refusal names none.
add("RemainingBasketsSkipRequested", { skipRequestId: R("Id"), demandId: R("Id"), operationSessionId: R("Id"), slotOperationAttemptId: R("Id"), loadedSlots: Slots(), operator: Nullable(R("OperatorContext")) }, { businessDedupKeys: ["skipRequestId"], recoveryRole: "REMAINING_BASKETS_SKIP" });
add("RemainingBasketsSkipResult", { skipRequestId: R("Id"), demandId: R("Id"), slotOperationAttemptId: R("Id"), outcome: E("AUTHORIZED", "REJECTED"), loadedSlots: A(R("SlotNo"), { maxItems: 8, uniqueItems: true, "x-sortedAscending": true }), problem: Nullable(R("Problem")) }, { businessDedupKeys: ["skipRequestId"], recoveryRole: "PENDING_RESULT_REPLAY" });

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

const resultsRefusingSkipMarker = ["LoadCorrectionResult", "LoadCancellationResult", "LoadCompensationResult", "FaultCargoRecoveryResult"];
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
  // A declaration the vehicle refused says why; an applied one has nothing to explain. Same if/then/else
  // form as loadingPhase's closedReason, on the payload object itself.
  if (spec.name === "SlotFaultDeclarationResult") {
    Object.assign(schema.properties.payload, {
      if: { properties: { outcome: { const: "NOT_APPLICABLE" } }, required: ["outcome"] },
      then: { properties: { problem: { type: "object" } } },
      else: { properties: { problem: { type: "null" } } },
    });
  }
  // A refused departure says why; an accepted one has nothing to explain.
  if (spec.name === "CurrentStopDepartureResult") {
    Object.assign(schema.properties.payload, {
      if: { properties: { outcome: { const: "REJECTED" } }, required: ["outcome"] },
      then: { properties: { problem: { type: "object" } } },
      else: { properties: { problem: { type: "null" } } },
    });
  }
  // A refused skip says why and authorizes no slot; an authorized one names the slots it authorizes and has nothing to explain.
  if (spec.name === "RemainingBasketsSkipResult") {
    Object.assign(schema.properties.payload, {
      if: { properties: { outcome: { const: "REJECTED" } }, required: ["outcome"] },
      then: { properties: { problem: { type: "object" }, loadedSlots: { maxItems: 0 } } },
      else: { properties: { problem: { type: "null" }, loadedSlots: { minItems: 1 } } },
    });
  }
  // A skipped load is a LOAD whose every slot is closed and proven -- LOCKED and RESET, no UNKNOWN -- because the skip is
  // authorized only so (REQ-0367); the loaded slots are COMPLETED and OCCUPIED, the remaining ones NOT_STARTED, EMPTY and
  // REMAINING_BASKETS_SKIPPED; at least one of each, so 1 <= k < N. The marker travels on remaining slots of a skipped load and
  // nowhere else: not on its loaded slots, and on no slot of any other result (review L5).
  if (spec.name === "OperationResult") {
    const withoutSkipCode = { reasonCodes: { not: { contains: { const: "REMAINING_BASKETS_SKIPPED" } } } };
    Object.assign(schema.properties.payload, {
      allOf: [{
        if: { properties: { overallOutcome: { const: "COMPLETED_REMAINING_SKIPPED" } }, required: ["overallOutcome"] },
        then: {
          properties: {
            operationType: { const: "LOAD" },
            slotResults: {
              items: {
                properties: { outcome: { enum: ["COMPLETED", "NOT_STARTED"] }, lockState: { const: "LOCKED" }, unlockOutputState: { const: "RESET" } },
                allOf: [
                  { if: { properties: { outcome: { const: "COMPLETED" } }, required: ["outcome"] }, then: { properties: { finalPhysicalState: { const: "OCCUPIED" }, ...withoutSkipCode } } },
                  { if: { properties: { outcome: { const: "NOT_STARTED" } }, required: ["outcome"] }, then: { properties: { finalPhysicalState: { const: "EMPTY" }, reasonCodes: { contains: { const: "REMAINING_BASKETS_SKIPPED" } } } } },
                ],
              },
              allOf: [
                { contains: { properties: { outcome: { const: "COMPLETED" } } }, minContains: 1 },
                { contains: { properties: { outcome: { const: "NOT_STARTED" } } }, minContains: 1 },
              ],
            },
          },
        },
        else: { properties: { slotResults: { items: { properties: withoutSkipCode } } } },
      }],
    });
  }
  // Release 6.0.0 (the revised REQ-0211, review M3 and L-c): a cancellation is authorized only over an empty scope, so no door
  // is opened for it, and carries no problem; a refusal says why and names no slot either. slots is therefore always empty; it
  // stays a field so the message keeps its released shape.
  if (spec.name === "LoadCancellationAuthorization") {
    Object.assign(schema.properties.payload, {
      if: { properties: { decision: { const: "REJECTED" } }, required: ["decision"] },
      then: { properties: { problem: { type: "object" }, slots: { maxItems: 0 } } },
      else: { properties: { problem: { type: "null" }, slots: { maxItems: 0 } } },
    });
  }
  // The skip marker belongs to a skipped OperationResult only (review L-a): the other four results that carry SlotResult refuse
  // it on every slot. SlotResult itself stays shared and unchanged.
  if (resultsRefusingSkipMarker.includes(spec.name)) {
    schema.properties.payload.allOf = [...(schema.properties.payload.allOf ?? []), { properties: { slotResults: { items: { properties: { reasonCodes: { not: { contains: { const: "REMAINING_BASKETS_SKIPPED" } } } } } } } }];
  }
  // A handoff record exactly when the vehicle was isolated on a session with a demand: that result settles the demand. A
  // FAILED or UNKNOWN result and an isolation without a demand settle nothing and carry none.
  if (spec.name === "ForcedMechanicalRecoveryResult") {
    Object.assign(schema.properties.payload, {
      if: { properties: { outcome: { const: "MECHANICALLY_ISOLATED" }, demandId: { type: "string" } }, required: ["outcome", "demandId"] },
      then: { properties: { cargoHandoff: { type: "object" } } },
      else: { properties: { cargoHandoff: { type: "null" } } },
    });
  }
  // A worklist with items has not ended its stop, so it carries no reason; an empty one always says why the stop ended.
  if (spec.name === "CurrentStopWorklistSnapshot") {
    Object.assign(schema.properties.payload, {
      if: { properties: { items: { minItems: 1 } }, required: ["items"] },
      then: { properties: { stopEndedReason: { type: "null" } } },
      else: { properties: { stopEndedReason: { type: "string" } } },
    });
  }
  // Each check purpose carries exactly its own scope: a missing demand or leg is never a departure.
  if (spec.name === "PreDepartureSafetyCheck") {
    Object.assign(schema.properties.payload, {
      allOf: checkPurposes.map((purpose) => ({
        if: { properties: { checkPurpose: { const: purpose } }, required: ["checkPurpose"] },
        then: { properties: Object.fromEntries(checkScopeFields.map((field, index) => [field, { type: checkPurposeScope[purpose][index] ? "string" : "null" }])) },
      })),
    });
  }
  // A door-unproven clearing names at least one slot and proves every slot it names EMPTY: the light curtains are what let it
  // settle. ALL_EMPTY keeps the constraints 2.0.0 gave it.
  if (spec.name === "LoadCancellationResult" || spec.name === "LoadCompensationResult") {
    Object.assign(schema.properties.payload, {
      if: { properties: { overallOutcome: { const: "ALL_EMPTY_DOOR_UNPROVEN" } }, required: ["overallOutcome"] },
      then: { properties: { slotResults: { minItems: 1, items: { properties: { finalPhysicalState: { const: "EMPTY" } } } } } },
    });
  }
  // A session states why it closed only once it has: every earlier state carries null. A CLOSED session carries null on a
  // normal close, so there is no then-branch.
  if (spec.name === "ExceptionRecoverySessionSnapshot") {
    Object.assign(schema.properties.payload, {
      if: { properties: { state: { const: "CLOSED" } }, required: ["state"] },
      else: { properties: { closedReason: { type: "null" } } },
    });
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
  // The sampler takes the first enum value for closedReason, but loadingPhase allows a reason only
  // once the phase is CLOSED.
  if (spec.name === "VehicleBusinessStateSnapshot") value.payload.loadingPhase.closedReason = null;
  // The sampler takes APPLIED and a Problem object, but an applied declaration carries no problem.
  if (spec.name === "SlotFaultDeclarationResult") value.payload.problem = null;
  // The sampler takes ACCEPTED and a Problem object, but an accepted departure carries no problem.
  if (spec.name === "CurrentStopDepartureResult") value.payload.problem = null;
  // The sampler takes AUTHORIZED and a Problem object, but an authorized skip carries no problem.
  if (spec.name === "RemainingBasketsSkipResult") value.payload.problem = null;
  // The sampler takes AUTHORIZED with a slot and a Problem object, but an authorized cancellation has an empty scope and no problem.
  if (spec.name === "LoadCancellationAuthorization") Object.assign(value.payload, { slots: [], problem: null });
  // The sampler takes OPEN and an ErrorCode, but only a CLOSED session states why it closed.
  if (spec.name === "ExceptionRecoverySessionSnapshot") value.payload.closedReason = null;
  // The sampler takes one item and a reason, but a worklist with items has not ended its stop.
  if (spec.name === "CurrentStopWorklistSnapshot") value.payload.stopEndedReason = null;
  return value;
};

const invalidTypeValue = (schema) => {
  const resolved = resolveRef(schema);
  // A nullable inline object needs a value that is neither branch: an object with unknown keys is
  // rejected for its required and additionalProperties, which is not the type failure it claims.
  if (resolved.anyOf?.some((option) => option.type === "object")) return "not-an-object";
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
  const payloadNegative = (suffix, fieldPath, rule, mutate) => {
    const vectorId = `I-${spec.name}-${suffix}`;
    const broken = clone(valid); mutate(broken.payload);
    writeJson(`examples/invalid/${spec.name}/${vectorId}.json`, invalidWrapper(vectorId, broken, "PROTOCOL_SCHEMA_INVALID", fieldPath, rule));
  };
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
    // An inline object field, as opposed to a shared $ref type, gets the same negatives one level
    // down, plus one for a property the object does not declare.
    const inline = fieldSchema.type === "object" ? fieldSchema : fieldSchema.anyOf?.find((option) => option.type === "object");
    if (inline) {
      for (const key of inline.required) payloadNegative(`REQUIRED-PAYLOAD-${field}-${key}`, `/payload/${field}/${key}`, "required", (payload) => { delete payload[field][key]; });
      for (const [key, keySchema] of Object.entries(inline.properties)) {
        const invalidValue = invalidTypeValue(keySchema);
        if (invalidValue !== undefined) payloadNegative(`TYPE-${field}-${key}`, `/payload/${field}/${key}`, "type", (payload) => { payload[field][key] = invalidValue; });
        if ([resolveRef(keySchema), ...(keySchema.anyOf ?? [])].some((option) => option.enum)) payloadNegative(`ENUM-${field}-${key}`, `/payload/${field}/${key}`, "enum-or-const", (payload) => { payload[field][key] = "__NOT_ALLOWED__"; });
      }
      payloadNegative(`ADDITIONAL-${field}`, `/payload/${field}`, "additionalProperties", (payload) => { payload[field].undeclaredProperty = "not-in-schema"; });
    }
  }
  // Both sides of loadingPhase's CLOSED correspondence: a closed phase without a reason, an open one with a reason.
  if (spec.name === "VehicleBusinessStateSnapshot") {
    payloadNegative("IF-THEN-loadingPhase-closedReason-CLOSED", "/payload/loadingPhase/closedReason", "if-then", (payload) => { payload.loadingPhase.state = "CLOSED"; });
    payloadNegative("IF-THEN-loadingPhase-closedReason-OPEN", "/payload/loadingPhase/closedReason", "if-then", (payload) => { payload.loadingPhase.closedReason = "PLANNED_LOADING_COMPLETE"; });
  }
  // Both sides of the declaration result's correspondence: a refusal without a reason, an applied one with a problem.
  if (spec.name === "SlotFaultDeclarationResult") {
    payloadNegative("IF-THEN-problem-NOT_APPLICABLE", "/payload/problem", "if-then", (payload) => { payload.outcome = "NOT_APPLICABLE"; });
    payloadNegative("IF-THEN-problem-APPLIED", "/payload/problem", "if-then", (payload) => { payload.problem = { reasonCode: "ACTION_NOT_ALLOWED_IN_STATE", fieldPath: null, displayMessage: null }; });
  }
  // Both sides of the departure result's correspondence: a refusal without a reason, an accepted one with a problem.
  if (spec.name === "CurrentStopDepartureResult") {
    payloadNegative("IF-THEN-problem-REJECTED", "/payload/problem", "if-then", (payload) => { payload.outcome = "REJECTED"; });
    payloadNegative("IF-THEN-problem-ACCEPTED", "/payload/problem", "if-then", (payload) => { payload.problem = { reasonCode: "WORKLIST_REVISION_STALE", fieldPath: null, displayMessage: null }; });
  }
  // Release 6.0.0 (protocol#26): a skip asked for with no loaded slot, k = 0, cannot be written.
  if (spec.name === "RemainingBasketsSkipRequested") {
    payloadNegative("MIN-ITEMS-loadedSlots", "/payload/loadedSlots", "minItems", (payload) => { payload.loadedSlots = []; });
  }
  // A refusal, with its reason and no slot; then both sides of both correspondences.
  if (spec.name === "RemainingBasketsSkipResult") {
    const rejected = clone(valid);
    Object.assign(rejected.payload, { outcome: "REJECTED", loadedSlots: [], problem: { reasonCode: "LOCK_NOT_CLOSED", fieldPath: null, displayMessage: null } });
    writeJson(`examples/valid/${spec.name}/V-${spec.name}-REJECTED-001.json`, rejected);
    const rejectedNegative = (suffix, fieldPath, mutate) => {
      const vectorId = `I-${spec.name}-${suffix}`;
      const broken = clone(rejected); mutate(broken.payload);
      writeJson(`examples/invalid/${spec.name}/${vectorId}.json`, invalidWrapper(vectorId, broken, "PROTOCOL_SCHEMA_INVALID", fieldPath, "if-then"));
    };
    rejectedNegative("IF-THEN-problem-REJECTED", "/payload/problem", (payload) => { payload.problem = null; });
    rejectedNegative("IF-THEN-loadedSlots-REJECTED", "/payload/loadedSlots", (payload) => { payload.loadedSlots = [1]; });
    payloadNegative("IF-THEN-problem-AUTHORIZED", "/payload/problem", "if-then", (payload) => { payload.problem = { reasonCode: "LOCK_NOT_CLOSED", fieldPath: null, displayMessage: null }; });
    payloadNegative("IF-THEN-loadedSlots-AUTHORIZED", "/payload/loadedSlots", "if-then", (payload) => { payload.loadedSlots = []; });
  }
  // A skipped load of two slots, one loaded and one left, and one example per way its shape can break.
  if (spec.name === "OperationResult") {
    const skipped = clone(valid);
    Object.assign(skipped.payload, {
      operationType: "LOAD",
      overallOutcome: "COMPLETED_REMAINING_SKIPPED",
      slotResults: [
        { slotNo: 1, outcome: "COMPLETED", finalPhysicalState: "OCCUPIED", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: [] },
        { slotNo: 2, outcome: "NOT_STARTED", finalPhysicalState: "EMPTY", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: ["REMAINING_BASKETS_SKIPPED"] },
      ],
    });
    writeJson(`examples/valid/${spec.name}/V-${spec.name}-REMAINING-BASKETS-SKIPPED-001.json`, skipped);
    const skippedNegative = (suffix, fieldPath, mutate) => {
      const vectorId = `I-${spec.name}-${suffix}`;
      const broken = clone(skipped); mutate(broken.payload);
      writeJson(`examples/invalid/${spec.name}/${vectorId}.json`, invalidWrapper(vectorId, broken, "PROTOCOL_SCHEMA_INVALID", fieldPath, "if-then"));
    };
    skippedNegative("IF-THEN-operationType-SKIPPED-UNLOAD", "/payload/operationType", (payload) => { payload.operationType = "UNLOAD"; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-NOTHING-LOADED", "/payload/slotResults", (payload) => { payload.slotResults[0] = { ...payload.slotResults[1], slotNo: 1 }; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-NOTHING-REMAINING", "/payload/slotResults", (payload) => { payload.slotResults[1] = { ...payload.slotResults[0], slotNo: 2 }; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-UNKNOWN", "/payload/slotResults", (payload) => { Object.assign(payload.slotResults[1], { outcome: "UNKNOWN", finalPhysicalState: "UNKNOWN" }); });
    // A third slot that passes every other constraint, so the outcome enum alone refuses it (review L1).
    skippedNegative("IF-THEN-slotResults-SKIPPED-FAILED", "/payload/slotResults", (payload) => { payload.slotResults.push({ slotNo: 3, outcome: "FAILED", finalPhysicalState: "EMPTY", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: [] }); });
    skippedNegative("IF-THEN-slotResults-SKIPPED-UNLOCKED", "/payload/slotResults", (payload) => { payload.slotResults[1].lockState = "UNLOCKED"; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-OUTPUT-ACTIVE", "/payload/slotResults", (payload) => { payload.slotResults[0].unlockOutputState = "ACTIVE"; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-REMAINING-OCCUPIED", "/payload/slotResults", (payload) => { payload.slotResults[1].finalPhysicalState = "OCCUPIED"; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-REMAINING-WITHOUT-CODE", "/payload/slotResults", (payload) => { payload.slotResults[1].reasonCodes = []; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-LOADED-EMPTY", "/payload/slotResults", (payload) => { payload.slotResults[0].finalPhysicalState = "EMPTY"; });
    skippedNegative("IF-THEN-slotResults-SKIPPED-LOADED-WITH-CODE", "/payload/slotResults", (payload) => { payload.slotResults[0].reasonCodes = ["REMAINING_BASKETS_SKIPPED"]; });
    payloadNegative("IF-THEN-slotResults-COMPLETED-WITH-CODE", "/payload/slotResults", "if-then", (payload) => { payload.slotResults[0].reasonCodes = ["REMAINING_BASKETS_SKIPPED"]; });
  }
  // A cancellation refused once a basket is loaded; an authorization naming a slot, and a refusal without a reason.
  if (spec.name === "LoadCancellationAuthorization") {
    const rejected = clone(valid);
    Object.assign(rejected.payload, { decision: "REJECTED", problem: { reasonCode: "LOAD_CANCELLATION_BASKET_LOADED", fieldPath: null, displayMessage: null } });
    writeJson(`examples/valid/${spec.name}/V-${spec.name}-REJECTED-001.json`, rejected);
    payloadNegative("IF-THEN-slots-AUTHORIZED", "/payload/slots", "if-then", (payload) => { payload.slots = [1]; });
    payloadNegative("IF-THEN-problem-REJECTED", "/payload/problem", "if-then", (payload) => { payload.decision = "REJECTED"; });
    payloadNegative("IF-THEN-problem-AUTHORIZED", "/payload/problem", "if-then", (payload) => { payload.problem = { reasonCode: "LOAD_CANCELLATION_BASKET_LOADED", fieldPath: null, displayMessage: null }; });
    payloadNegative("IF-THEN-slots-REJECTED", "/payload/slots", "if-then", (payload) => { Object.assign(payload, { decision: "REJECTED", slots: [1], problem: { reasonCode: "LOAD_CANCELLATION_BASKET_LOADED", fieldPath: null, displayMessage: null } }); });
  }
  // L-a: the skip marker on a slot of any other result.
  if (resultsRefusingSkipMarker.includes(spec.name)) {
    payloadNegative("NOT-slotResults-REMAINING_BASKETS_SKIPPED", "/payload/slotResults", "not", (payload) => { payload.slotResults[0].reasonCodes = ["REMAINING_BASKETS_SKIPPED"]; });
  }
  // Both sides of the record correspondence: isolated on a demand without a record, a record without a demand, and a record
  // on a FAILED and on an UNKNOWN result.
  if (spec.name === "ForcedMechanicalRecoveryResult") {
    payloadNegative("IF-THEN-cargoHandoff-MECHANICALLY_ISOLATED", "/payload/cargoHandoff", "if-then", (payload) => { payload.cargoHandoff = null; });
    payloadNegative("IF-THEN-cargoHandoff-NO_DEMAND", "/payload/cargoHandoff", "if-then", (payload) => { payload.demandId = null; });
    for (const outcome of ["FAILED", "UNKNOWN"]) payloadNegative(`IF-THEN-cargoHandoff-${outcome}`, "/payload/cargoHandoff", "if-then", (payload) => { payload.outcome = outcome; });
  }
  // A reason on each state before CLOSED.
  if (spec.name === "ExceptionRecoverySessionSnapshot") {
    for (const state of ["OPEN", "ACTION_SELECTED", "EXECUTING"]) payloadNegative(`IF-THEN-closedReason-${state}`, "/payload/closedReason", "if-then", (payload) => { payload.state = state; payload.closedReason = "RECOVERY_ACTION_RESULT_NOT_RECONCILED"; });
  }
  // Each purpose with one of its three fields on the wrong side of null.
  if (spec.name === "PreDepartureSafetyCheck") {
    for (const purpose of checkPurposes) {
      checkScopeFields.forEach((field, index) => payloadNegative(`IF-THEN-${field}-${purpose}`, `/payload/${field}`, "if-then", (payload) => {
        payload.checkPurpose = purpose;
        checkScopeFields.forEach((other, otherIndex) => { if (checkPurposeScope[purpose][otherIndex] === (otherIndex === index)) payload[other] = null; });
      }));
    }
  }
  // A door-unproven result without a slot, and one naming a slot that is not EMPTY. A compensation result needs a slot anyway.
  if (spec.name === "LoadCancellationResult") {
    payloadNegative("IF-THEN-slotResults-ALL_EMPTY_DOOR_UNPROVEN-NO_SLOT", "/payload/slotResults", "if-then", (payload) => { payload.overallOutcome = "ALL_EMPTY_DOOR_UNPROVEN"; payload.slotResults = []; });
  }
  if (spec.name === "LoadCancellationResult" || spec.name === "LoadCompensationResult") {
    payloadNegative("IF-THEN-slotResults-ALL_EMPTY_DOOR_UNPROVEN-OCCUPIED", "/payload/slotResults", "if-then", (payload) => { payload.overallOutcome = "ALL_EMPTY_DOOR_UNPROVEN"; payload.slotResults[0].finalPhysicalState = "OCCUPIED"; });
  }
  // Both sides of the stop-end correspondence: a reason on a worklist with items, an empty worklist without one.
  if (spec.name === "CurrentStopWorklistSnapshot") {
    payloadNegative("IF-THEN-stopEndedReason-ITEMS", "/payload/stopEndedReason", "if-then", (payload) => { payload.stopEndedReason = "STATION_DEADLINE_EXPIRED"; });
    payloadNegative("IF-THEN-stopEndedReason-EMPTY", "/payload/stopEndedReason", "if-then", (payload) => { payload.items = []; });
    // Release 5.0.0 (protocol#21, program#195): the minimal example takes the first TransportTaskType, so the value 5.0.0
    // appends gets a valid example of its own, and a misspelled and a lowercase spelling of it are refused. TransportTaskType
    // is a closed enum: near misses are the spellings an implementation that pattern-matched would wrongly let through.
    const fullInspection = clone(valid); fullInspection.payload.items[0].workType = "WIRE_TO_FULL_INSPECTION";
    writeJson(`examples/valid/${spec.name}/V-${spec.name}-WIRE-TO-FULL-INSPECTION-001.json`, fullInspection);
    for (const [suffix, value] of [["MISSPELLED", "WIRE_TO_FULL_INSPECTON"], ["LOWERCASE", "wire_to_full_inspection"]]) {
      const vectorId = `I-${spec.name}-ENUM-items-workType-${suffix}`;
      const broken = clone(fullInspection); broken.payload.items[0].workType = value;
      writeJson(`examples/invalid/${spec.name}/${vectorId}.json`, invalidWrapper(vectorId, broken, "PROTOCOL_SCHEMA_INVALID", "/payload/items/0/workType", "enum-or-const"));
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

writeJson("errors/error-codes.json", { registryVersion: "1.3.0", appendOnly: true, displayMessageAuthoritative: false, codes: errorCodes });

// Every vector carries productAssertions: what each side must be able to prove when the wire
// trace matches. That was FP-IS-01's special case in v1; here it is mandatory for every vector, because
// a trace alone never distinguishes "did the right thing" from "emitted the right bytes".
const wire = (...messages) => messages;
const trajectories = {
  "CV-SESSION-RECOVERY-HAPPY": {
    messages: wire("SessionHello", "SessionAccepted", "CapabilitySnapshot", "SafetyStateSnapshot", "RecoveryStateReport", "SessionReadiness"),
    productAssertions: { controlServer: ["SESSION_ACCEPTED_ONCE", "CAPABILITY_AND_SAFETY_ADOPTED", "READINESS_DECIDED_FROM_REPORTED_STATE"], onboardHmi: ["REPORT_UNSETTLED_STATE_BEFORE_READY", "ADOPT_SERVER_READINESS_DECISION"] },
  },
  "CV-SESSION-RECONNECT-DURING-RECOVERY": {
    messages: wire("SessionHello", "SessionAccepted", "RecoveryStateReport", "SessionHello", "SessionAccepted", "RecoveryStateReport", "SessionReadiness"),
    productAssertions: { controlServer: ["SUPERSEDE_STALE_SESSION_GENERATION", "NEVER_TWO_ACTIVE_SESSIONS"], onboardHmi: ["RESUBMIT_RECOVERY_STATE_AFTER_RECONNECT", "NEVER_ASSUME_PREVIOUS_SESSION_SURVIVED"] },
  },
  "CV-RELIABLE-RETRY-SAME-CONTENT": {
    messages: wire("SlotOperationCommand", "SlotOperationCommand", "DurableAck"),
    productAssertions: { controlServer: ["ACK_RETRY_WITHOUT_DUPLICATE_EFFECT", "IDEMPOTENT_ON_BUSINESS_KEY"], onboardHmi: ["RETRY_WITH_IDENTICAL_CONTENT", "NEVER_MUTATE_MESSAGE_ID_CONTENT_PAIR"] },
  },
  "CV-RELIABLE-RETRY-DIFFERENT-CONTENT": {
    messages: wire("SlotOperationCommand", "SlotOperationCommand", "ProtocolProblem"),
    productAssertions: { controlServer: ["REJECT_MESSAGE_ID_CONTENT_CONFLICT", "NEVER_APPLY_CONFLICTING_RETRY"], onboardHmi: ["SURFACE_PROTOCOL_PROBLEM", "NEVER_SILENTLY_REPLACE_CONTENT"] },
  },
  "CV-REQUEST-FIRST-RESULT-REPLAY": {
    messages: wire("SublotSubmitted", "SlotOperationCommand", "SublotSubmitted", "SlotOperationCommand", "OperationResult"),
    productAssertions: { controlServer: ["REPLAY_PENDING_RESULT_ON_REQUEST", "NEVER_RECOMPUTE_SETTLED_RESULT"], onboardHmi: ["REQUEST_BEFORE_ASSUMING_LOSS", "ADOPT_REPLAYED_RESULT"] },
  },
  "CV-SNAPSHOT-REPLACE-AND-ACK": {
    messages: wire("VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["ADVANCE_REVISION_MONOTONICALLY"], onboardHmi: ["REPLACE_NOT_MERGE_SNAPSHOT", "ACK_APPLIED_REVISION"] },
  },
  "CV-SNAPSHOT-SAME-REVISION-CONFLICT": {
    messages: wire("SafetyStateSnapshot", "SnapshotAppliedAck", "SafetyStateSnapshot", "ProtocolProblem"),
    productAssertions: { controlServer: ["REJECT_SAME_REVISION_DIFFERENT_CONTENT"], onboardHmi: ["NEVER_APPLY_CONFLICTING_SAME_REVISION"] },
  },
  "CV-PICKUP-SUBLOT-LOAD": {
    messages: wire("SublotEntryRequested", "SublotSubmitted", "SlotOperationCommand", "OperationResult", "DurableAck"),
    productAssertions: { controlServer: ["BIND_SUBLOT_TO_OPERATION_SESSION", "AUTHORIZE_SLOT_SET_ONCE"], onboardHmi: ["SUBMIT_SCANNED_SUBLOT", "LOAD_ONLY_AUTHORIZED_SLOTS"] },
  },
  "CV-LOAD-CORRECTION": {
    messages: wire("LoadCorrectionRequested", "LoadCorrectionCommand", "LoadCorrectionResult", "DurableAck"),
    productAssertions: { controlServer: ["AUTHORIZE_CORRECTION_AGAINST_COMMITTED_SET"], onboardHmi: ["REPORT_CORRECTED_SLOT_OUTCOME", "NEVER_CORRECT_WITHOUT_AUTHORIZATION"] },
  },
  // Rewritten in 6.0.0 (the revised REQ-0211, review M4): once loading has started a cancellation is authorized only with every
  // target slot EMPTY, every door proven locked and every output reset, and over an empty scope, so the vehicle opens no slot
  // for it and reports ALL_EMPTY without slot IO. Until 5.0.0 this vector cleared the loaded slots after authorization.
  "CV-LOAD-CANCELLATION-ALL-EMPTY": {
    messages: wire("LoadCancellationStartRequested", "LoadCancellationAuthorization", "LoadCancellationResult", "DurableAck"),
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "business-cancellation-opened-a-slot", "cancellation-authorized-after-a-basket-is-loaded"],
    productAssertions: { controlServer: ["AUTHORIZE_CANCELLATION_EXPLICITLY", "AUTHORIZE_ONLY_WITH_EVERY_TARGET_SLOT_EMPTY_LOCKED_AND_RESET", "AUTHORIZE_WITH_AN_EMPTY_SLOT_SCOPE", "RECONCILE_EMPTY_FINAL_STATE"], onboardHmi: ["NEVER_OPEN_A_SLOT_FOR_A_CANCELLATION", "REPORT_ALL_EMPTY_WITHOUT_SLOT_IO", "NEVER_CANCEL_UNILATERALLY"] },
  },
  // Cancelled at the pickup station before any SlotOperationCommand: no slot was opened, so the
  // result carries an empty slotResults. Four steps, not the MVP's two (protocol-v0.3.0 db064d2):
  // ADR-cross-0046 ends this case with LoadCancellationResult as well, and the demand terminates
  // only once that result is durably accepted.
  "CV-LOAD-CANCELLATION-BEFORE-LOAD": {
    messages: wire("LoadCancellationStartRequested", "LoadCancellationAuthorization", "LoadCancellationResult", "DurableAck"),
    productAssertions: { controlServer: ["AUTHORIZE_CANCELLATION_WITHOUT_SLOT_OPERATION", "TERMINATE_ONLY_ON_ALL_EMPTY_RESULT"], onboardHmi: ["REPORT_ALL_EMPTY_WITHOUT_SLOT_IO", "NEVER_CANCEL_UNILATERALLY"] },
  },
  // BR-013 revalidates after entry; a failure comes back to the vehicle as SublotRejected with its
  // real reason code instead of the SUBLOT silently missing from the worklist.
  "CV-SUBLOT-REJECTED-AFTER-ENTRY": {
    messages: wire("SublotEntryRequested", "SublotSubmitted", "SublotRejected"),
    stableErrorCode: "PACKAGE_CAPACITY_UNRESOLVED",
    productAssertions: { controlServer: ["REVALIDATE_SUBLOT_AFTER_ENTRY", "NEVER_UNLOCK_ON_REJECTED_ENTRY"], onboardHmi: ["DISPLAY_SERVER_REJECTION_REASON", "KEEP_ENTRY_OPEN_FOR_RESCAN"] },
  },
  "CV-PREDEPARTURE-SAFETY-EXPIRES": {
    messages: wire("PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult", "SafetyStateChanged", "ProtocolProblem"),
    productAssertions: { controlServer: ["EXPIRE_CHECK_ON_SAFETY_STATE_CHANGE", "NEVER_DEPART_ON_EXPIRED_CHECK"], onboardHmi: ["REPORT_SAFETY_STATE_CHANGE_PROMPTLY", "REREQUEST_CHECK_AFTER_EXPIRY"] },
  },
  // Renamed from CV-GATE-UNLOAD-ALL-EMPTY: the gate is one of five public station functions, not
  // the destination of every task. Same correction as stopRole's GATE -> DROPOFF.
  "CV-DESTINATION-UNLOAD-ALL-EMPTY": {
    messages: wire("SlotOperationCommand", "OperationResult", "DurableAck"),
    productAssertions: { controlServer: ["COMMIT_UNLOAD_ONCE", "RECONCILE_EMPTY_FINAL_STATE"], onboardHmi: ["UNLOAD_AUTHORIZED_SLOTS_ONLY", "REPORT_FINAL_PHYSICAL_STATE"] },
  },
  "CV-CONNECTION-LOSS-SAFE-FINISH": {
    messages: wire("SlotOperationCommand", "OperationProgress", "RecoveryStateReport", "SessionReadiness"),
    productAssertions: { controlServer: ["NEVER_READY_BEFORE_RECONCILIATION"], onboardHmi: ["FINISH_IN_PROGRESS_OPERATION_SAFELY", "JOURNAL_BEFORE_IRREVERSIBLE_IO"] },
  },
  "CV-OPERATION-RESULT-UNKNOWN-RECONCILE": {
    messages: wire("OperationResult", "DurableAck", "RecoveryStateReport", "OperationResult", "DurableAck"),
    productAssertions: { controlServer: ["NEVER_TREAT_UNKNOWN_AS_SUCCESS", "RECONCILE_FROM_REPORTED_JOURNAL"], onboardHmi: ["REPORT_UNKNOWN_AS_UNKNOWN", "REPLAY_RESULT_ON_RECONNECT"] },
  },
  "CV-EXCEPTION-RESUME": {
    messages: wire("ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted", "SlotOperationResumeCommand", "OperationResult"),
    productAssertions: { controlServer: ["OPEN_RECOVERY_SESSION_FOR_VERIFIED_ADMINISTRATOR", "AUTHORIZE_RESUME_SCOPE"], onboardHmi: ["RESUME_ONLY_AUTHORIZED_SCOPE", "REPORT_RESUMED_OUTCOME"] },
  },
  "CV-EXCEPTION-COMPENSATE": {
    messages: wire("ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted", "LoadCompensationRequested", "LoadCompensationCommand", "LoadCompensationResult"),
    productAssertions: { controlServer: ["AUTHORIZE_COMPENSATION_AGAINST_RECOVERY_SESSION"], onboardHmi: ["EXECUTE_COMPENSATION_ONCE", "REPORT_COMPENSATED_SLOT_STATE"] },
  },
  "CV-FAULT-CARGO-HANDOFF": {
    messages: wire("RecoveryActionSubmitted", "RecoveryActionAccepted", "FaultCargoRecoveryCommand", "FaultCargoRecoveryResult"),
    productAssertions: { controlServer: ["RECORD_FAULT_CARGO_HANDOFF"], onboardHmi: ["HANDOFF_ONLY_ON_AUTHORIZED_COMMAND", "REPORT_HANDOFF_OUTCOME"] },
  },
  // Revised in 3.0.0 (REQ-0242): the result carries the cargo handoff record, and every outcome has a way out that needs
  // no database edit. Isolated on a demand: the record is required and the control server settles the demand on it, never
  // refusing the result over what the record says -- the vehicle drops its recovery context once the result is
  // acknowledged, so a refused settlement would leave the demand nothing to recover through. That covers the content of
  // cargoHandoff only: a demandId other than the session's is a business identity conflict and is refused as today.
  // FAILED: the vehicle keeps its context, the session closes and the blocked demand takes a new session. A command with
  // no demand is answered too, or the session would stay EXECUTING. The messages and the final state are the released ones.
  "CV-FORCED-MECHANICAL-RECOVERY": {
    messages: wire("RecoveryActionSubmitted", "RecoveryActionAccepted", "ForcedMechanicalRecoveryCommand", "ForcedMechanicalRecoveryResult"),
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "isolation-on-a-demand-without-handoff-record", "handoff-record-proves-empty-slot-or-ready-vehicle", "demand-left-blocked-after-acknowledged-isolation", "recovery-context-cleared-on-failed-or-unknown-forced-recovery"],
    productAssertions: {
      controlServer: ["FENCE_FORCED_RECOVERY_BY_GENERATION", "SETTLE_DEMAND_ONLY_ON_NAMED_HANDOFF", "NEVER_REFUSE_AN_ISOLATION_RESULT_OVER_ITS_RECORD", "KEEP_DEMAND_BLOCKED_AND_ACCEPT_NEW_SESSION_ON_FAILED_OR_UNKNOWN", "NEVER_TREAT_HANDOFF_AS_EMPTY_SLOT_OR_READY_VEHICLE"],
      // demandId is copied from the command, never left null on a demand, or the record requirement would not apply. The
      // SUBLOT is checked against the demand before the result goes out, because the control server will not refuse it
      // afterwards; a mismatch warns and asks the operator to confirm again, then sends -- the slot is already physically
      // isolated, so the check never holds the result back for good. The record is part of the durable result, so a result
      // replayed after a restart carries the same record. A command without a demand is answered like any other.
      onboardHmi: ["REFUSE_STALE_FORCED_RECOVERY_GENERATION", "REPORT_FORCED_RECOVERY_OUTCOME", "REPORT_CARGO_HANDOFF_RECORD_IN_RESULT", "COPY_COMMAND_DEMAND_INTO_RESULT", "CONFIRM_SUBLOT_AGAINST_DEMAND_BEFORE_SENDING", "REPLAY_SAME_HANDOFF_RECORD_AFTER_RESTART", "KEEP_RECOVERY_CONTEXT_UNLESS_ISOLATION_ACKNOWLEDGED", "ANSWER_FORCED_RECOVERY_COMMAND_WITHOUT_DEMAND"],
    },
  },
  "CV-MANUAL-CHARGING-RETURN": {
    messages: wire("ManualChargingReturnToServiceRequested", "ManualChargingReturnToServiceResult"),
    productAssertions: { controlServer: ["REEVALUATE_ELIGIBILITY_AFTER_RETURN", "REQUIRE_VERIFIED_ADMINISTRATOR"], onboardHmi: ["REQUEST_RETURN_WITH_OPERATOR_CONTEXT", "NEVER_CLEAR_HOLD_LOCALLY"] },
  },
  // A trajectory may also spell its steps out in full when they are not a plain send/expect chain.
  // FP-IS-01's adapter results are what that slice is about, and they are not wire messages.
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

  // --- v2 additions ---
  "CV-MULTI-STOP-PLAN-NINE-LEGS": {
    messages: wire("UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "CurrentStopWorklistSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["PLAN_UP_TO_NINE_LEGS", "ORDER_LEGS_BY_SEQUENCE", "CATEGORISE_EVERY_STOP_PURPOSE"], onboardHmi: ["DISPLAY_REMAINING_JOURNEY_PLAN", "NEVER_REORDER_LEGS_LOCALLY"] },
  },
  "CV-WORKLIST-SELECTION-ACCEPTED": {
    messages: wire("CurrentStopWorklistSnapshot", "SnapshotAppliedAck", "DemandSelectionRequested", "DemandSelectionResult"),
    productAssertions: { controlServer: ["SELECT_ONLY_FROM_COMMITTED_WORKLIST", "OPEN_OPERATION_SESSION_FOR_SELECTED_DEMAND"], onboardHmi: ["SELECT_FROM_COMMITTED_WORKLIST_ONLY", "CARRY_WORKLIST_REVISION_IN_REQUEST"] },
  },
  "CV-WORKLIST-SELECTION-STALE-REVISION": {
    messages: wire("DemandSelectionRequested", "DemandSelectionResult", "CurrentStopWorklistSnapshot", "SnapshotAppliedAck"),
    stableErrorCode: "WORKLIST_REVISION_STALE",
    productAssertions: { controlServer: ["REJECT_STALE_WORKLIST_REVISION", "RETURN_CURRENT_WORKLIST_REVISION"], onboardHmi: ["ADOPT_RETURNED_WORKLIST_REVISION", "NEVER_PROCEED_ON_REJECTED_SELECTION"] },
  },
  // 3.0.0 dropped the onboard DISPLAY_ADMISSION_BLOCK_REASON (program#125): an admission block reason stays on the control
  // server and its dashboard and is never sent to the vehicle (specification 5.3), so no implementation could produce it.
  "CV-TASK-TYPE-ADMISSION-FAIL-CLOSED": {
    messages: wire("UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    stableErrorCode: "ACTION_NOT_ALLOWED_IN_STATE",
    productAssertions: { controlServer: ["ADMIT_ONLY_BOUND_TASK_TYPES", "FAIL_CLOSED_ON_MISSING_BINDING"], onboardHmi: ["NEVER_INFER_UNBOUND_TASK_TYPE"] },
  },
  "CV-REVERSED-DIRECTION-JOURNEY": {
    messages: wire("UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "CurrentStopWorklistSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["DERIVE_DIRECTION_FROM_TASK_TYPE_RULE", "NEVER_SWAP_ORIGIN_AND_DESTINATION"], onboardHmi: ["DISPLAY_DIRECTION_AS_PLANNED"] },
  },
  "CV-WAITING-POINT-IDLE-RETURN": {
    messages: wire("UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["CLAIM_WAITING_POINT_EXCLUSIVELY", "RELEASE_ON_DEPARTURE_EVIDENCE"], onboardHmi: ["TREAT_WAITING_POINT_AS_NON_BUSINESS_STOP", "NEVER_LOAD_AT_WAITING_POINT"] },
  },
  "CV-AUTOMATIC-CHARGING-CYCLE": {
    messages: wire("UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["CLAIM_VEHICLE_FOR_CHARGING_PURPOSE", "NEVER_DISPATCH_DURING_CHARGING"], onboardHmi: ["DISPLAY_CHARGING_PURPOSE", "NEVER_LOAD_AT_CHARGER"] },
  },
  "CV-UNABLE-TO-CHARGE-FIELD-CONFIRMATION": {
    messages: wire("UnableToChargeFieldConfirmationRequested", "UnableToChargeFieldConfirmationResult", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["DECIDE_CHARGING_POLICY_CENTRALLY", "RECORD_FIELD_OBSERVATION"], onboardHmi: ["REPORT_OBSERVED_CONDITION_WITH_OPERATOR", "NEVER_DECIDE_CHARGING_POLICY_LOCALLY"] },
  },
  "CV-MANUAL-STATION-CLEARANCE": {
    messages: wire("ManualStationClearanceConfirmationRequested", "ManualStationClearanceConfirmationResult"),
    productAssertions: { controlServer: ["RELEASE_STATION_ONLY_ON_CONFIRMED_CLEARANCE"], onboardHmi: ["CONFIRM_CLEARANCE_WITH_OPERATOR", "NEVER_RELEASE_STATION_LOCALLY"] },
  },
  "CV-SLOT-CONFIGURATION-ACTIVATION": {
    messages: wire("SlotConfigurationActivationCommand", "SlotConfigurationActivationResult", "CapabilitySnapshot", "SnapshotAppliedAck"),
    stableErrorCode: "SLOT_CONFIGURATION_FINGERPRINT_MISMATCH",
    productAssertions: { controlServer: ["VERIFY_FINGERPRINT_BEFORE_ACTIVATION", "NEVER_GUESS_ACTIVATION_SUCCESS"], onboardHmi: ["REPORT_ACTIVATION_OUTCOME_INCLUDING_UNKNOWN", "REPLAY_PENDING_ACTIVATION_RESULT"] },
  },
  "CV-ONBOARD-ALARM-SNAPSHOT": {
    messages: wire("OnboardAlarmSnapshot", "SnapshotAppliedAck", "OnboardAlarmSnapshot", "SnapshotAppliedAck"),
    productAssertions: { controlServer: ["ADOPT_ALARM_SNAPSHOT_BY_REVISION"], onboardHmi: ["PUBLISH_COMPLETE_ALARM_SET", "NEVER_PUBLISH_STALE_ALARM_STATE"] },
  },

  // --- 3.0.0 additions ---
  // REQ-0359. The vehicle journals the declaration, then writes and sends its APPLIED result at the
  // moment it decides to abort, then settles the operation, so SlotFaultDeclarationResult precedes
  // OperationResult and each RELIABLE message gets its own DurableAck. Both implementations follow
  // this order. The side effects list the six defaults and the three a declaration must never have.
  "CV-SLOT-FAULT-DECLARATION-APPLIED": {
    messages: wire("SlotFaultDeclarationCommand", "SlotFaultDeclarationResult", "DurableAck", "OperationResult", "DurableAck"),
    stableErrorCode: "SLOT_FAULT_DECLARED",
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "unlock-after-declaration", "declaration-settles-business-or-cancels-demand", "declaration-marks-slot-inoperable"],
    productAssertions: {
      controlServer: ["DECLARE_ONLY_ON_OVERDUE_SLOT_AWAITING_OPERATOR", "AUDIT_DECLARATION_AND_VEHICLE_RESULT", "BLOCK_JOURNEY_ON_DECLARED_UNKNOWN"],
      // A crash between the APPLIED result and the settlement must not let the restart's live-reading
      // settlement report the declared slot COMPLETED: the declaration is journaled first and survives.
      onboardHmi: ["APPLY_ONLY_TO_SAME_ATTEMPT_AND_SLOT_STILL_AWAITING", "JOURNAL_DECLARATION_BEFORE_APPLIED_RESULT", "KEEP_DECLARED_SLOT_UNKNOWN_ACROSS_RESTART", "NEVER_UNLOCK_AFTER_DECLARATION_APPLIED", "REPORT_DECLARED_SLOT_UNKNOWN_LATER_SLOTS_NOT_STARTED", "REPORT_COMPLETED_SLOTS_FROM_LIVE_READINGS", "SEND_DECLARATION_RESULT_BEFORE_OPERATION_RESULT"],
    },
    finalState: { readiness: "RECOVERY_REQUIRED", business: "JOURNEY_BLOCKED_DEMAND_NOT_SETTLED", physical: "DECLARED_SLOT_UNKNOWN_LATER_SLOTS_NOT_STARTED" },
  },
  // The declaration lost a race: the slot had closed, was already UNKNOWN, or the attempt had been
  // superseded (CP-0005 new item two note 5). The vehicle refuses, the control server withdraws it.
  // An attempt the vehicle does not know is refused the same way: a ProtocolProblem would leave the
  // RELIABLE command without a result for ever. A pending declaration never stops the control server
  // from settling the operation result that closed the slot.
  "CV-SLOT-FAULT-DECLARATION-NOT-APPLICABLE": {
    messages: wire("SlotFaultDeclarationCommand", "SlotFaultDeclarationResult", "DurableAck"),
    stableErrorCode: "ACTION_NOT_ALLOWED_IN_STATE",
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "unlock-after-declaration", "declaration-settles-business-or-cancels-demand", "declaration-marks-slot-inoperable", "business-state-changed-by-rejected-declaration"],
    productAssertions: {
      controlServer: ["DECLARE_ONLY_ON_OVERDUE_SLOT_AWAITING_OPERATOR", "AUDIT_DECLARATION_AND_VEHICLE_RESULT", "WITHDRAW_DECLARATION_WITHOUT_BUSINESS_CHANGE", "SETTLE_OPERATION_RESULT_NORMALLY_WHILE_DECLARATION_PENDING"],
      onboardHmi: ["REJECT_DECLARATION_ON_SETTLED_UNKNOWN_OR_SUPERSEDED_ATTEMPT", "ANSWER_UNKNOWN_ATTEMPT_WITH_NOT_APPLICABLE", "NEVER_APPLY_DECLARATION_TO_ANOTHER_ATTEMPT_OR_SLOT"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_DECLARATION_WITHDRAWN", physical: "UNCHANGED" },
  },
  // control-server#169: a recovery result that does not reconcile -- here a compensation reporting FAILED -- closes the
  // session with RECOVERY_ACTION_RESULT_NOT_RECONCILED, so the vehicle sees why. The session closes rather than staying
  // EXECUTING, which refused a second action and a new session; the demand stays blocked and a new session is accepted,
  // so the close is never a state only a database edit can leave. The result gets its DurableAck, the snapshot its ack.
  "CV-RECOVERY-SESSION-CLOSED-RESULT-NOT-RECONCILED": {
    messages: wire("RecoveryActionSubmitted", "RecoveryActionAccepted", "LoadCompensationRequested", "LoadCompensationCommand", "LoadCompensationResult", "DurableAck", "ExceptionRecoverySessionSnapshot", "SnapshotAppliedAck"),
    stableErrorCode: "RECOVERY_ACTION_RESULT_NOT_RECONCILED",
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "unreconciled-result-settles-demand", "session-left-open-after-final-result", "new-session-refused-after-unreconciled-close"],
    productAssertions: {
      // The reason is part of the session, not of one message: a CLOSED snapshot sent again after a reconnect carries it too.
      controlServer: ["CLOSE_SESSION_WITH_REASON_ON_UNRECONCILED_RESULT", "KEEP_DEMAND_BLOCKED_AFTER_UNRECONCILED_CLOSE", "ACCEPT_NEW_SESSION_AFTER_UNRECONCILED_CLOSE", "RESEND_CLOSED_REASON_AFTER_RECONNECT"],
      onboardHmi: ["DISPLAY_SESSION_CLOSED_REASON", "ALLOW_REOPENING_AFTER_SESSION_CLOSED", "NEVER_TREAT_UNRECONCILED_CLOSE_AS_RECOVERED"],
    },
    finalState: { readiness: "RECOVERY_REQUIRED", business: "DEMAND_BLOCKED_SESSION_CLOSED_NEW_SESSION_ALLOWED", physical: "AS_REPORTED_BY_UNRECONCILED_RESULT" },
  },
  // CP-0009 (REQ-0364): a compensation whose light curtains prove every slot empty while a door is not proven locked. The
  // demand ends as a compensation proven all empty does, with the same suppression; the door proof moves to the vehicle's
  // release. The control server settles on the new value only when the result names exactly the target slots and every one
  // of them EMPTY; anything else stays unreconciled and the demand stays blocked for a new session. The result gets its
  // DurableAck, and the control server then publishes the hold in VehicleBusinessStateSnapshot outside any journey. The way out
  // needs no database edit and is the same for a cancellation: CV-VEHICLE-HOLD-DOOR-REPAIR-RELEASE.
  // The demand settles the way an all-empty compensation does (SETTLE_DEMAND_AS_ALL_EMPTY_COMPENSATION); the doors never count
  // as proven locked and the vehicle never becomes ready on this result (NEVER_TAKE_DOOR_UNPROVEN_FOR_DOORS_PROVEN_LOCKED).
  "CV-LOAD-COMPENSATION-EMPTY-DOOR-UNPROVEN": {
    messages: wire("ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted", "LoadCompensationRequested", "LoadCompensationCommand", "LoadCompensationResult", "DurableAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    stableErrorCode: "SLOT_DOOR_LOCK_UNPROVEN_AFTER_EMPTY",
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "door-unproven-reported-as-all-empty", "slot-opened-after-door-unproven", "door-unproven-settles-with-a-slot-not-proven-empty", "vehicle-released-without-fresh-lock-proof", "demand-left-blocked-after-door-unproven-empty", "vehicle-held-without-a-repair-release-path"],
    productAssertions: {
      controlServer: ["SETTLE_DEMAND_AS_ALL_EMPTY_COMPENSATION", "SETTLE_DOOR_UNPROVEN_ONLY_ON_THE_EXACT_TARGET_SLOTS_ALL_EMPTY", "HOLD_VEHICLE_UNTIL_HARDWARE_RECORD_AND_FRESH_LOCK_PROOF", "PUBLISH_HOLD_IN_VEHICLE_BUSINESS_STATE", "NEVER_RELEASE_ON_HARDWARE_RECORD_ALONE", "RELEASE_ONLY_THROUGH_HARDWARE_REPAIR_RELEASE", "NEVER_TAKE_DOOR_UNPROVEN_FOR_DOORS_PROVEN_LOCKED"],
      // The result is journaled before it is sent, so a result replayed after a restart is the same DOOR_UNPROVEN one and
      // never a live re-reading that might now say ALL_EMPTY or UNKNOWN.
      onboardHmi: ["REPORT_LOCK_AND_OUTPUT_STATE_AS_READ", "NEVER_OPEN_ANY_SLOT_AFTER_DOOR_UNPROVEN", "DISPLAY_REPAIR_REQUIRED_NOTICE", "JOURNAL_DOOR_UNPROVEN_RESULT_BEFORE_SENDING", "REPLAY_SAME_DOOR_UNPROVEN_RESULT_AFTER_RESTART"],
    },
    finalState: { readiness: "RECOVERY_REQUIRED", business: "DEMAND_TERMINATED_AS_ALL_EMPTY_VEHICLE_HELD_FOR_REPAIR", physical: "SLOTS_EMPTY_DOOR_UNPROVEN_VEHICLE_HELD" },
  },
  // Kept in 6.0.0 as a defence only (review M4, L-d): under the revised REQ-0211 a cancellation opens no slot, so this path is
  // no longer reached; should a result still report a door unproven, the outcome is not taken as ALL_EMPTY, the demand ends as
  // this vector sets it (as an all-empty cancellation) and the vehicle is held for repair. To be removed in the next major version.
  // CP-0009 on the cancellation path: the lock fails during a cancellation already authorized, so no exception recovery
  // session is open. The demand ends as a cancellation proven all empty does (CANCELLED_BY_OPERATOR, same suppression) and the
  // vehicle is held exactly as after the compensation, with the same way out. Same messages as CV-LOAD-CANCELLATION-ALL-EMPTY.
  "CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN": {
    messages: wire("LoadCancellationStartRequested", "LoadCancellationAuthorization", "LoadCancellationResult", "DurableAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    stableErrorCode: "SLOT_DOOR_LOCK_UNPROVEN_AFTER_EMPTY",
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "door-unproven-reported-as-all-empty", "slot-opened-after-door-unproven", "door-unproven-settles-with-a-slot-not-proven-empty", "vehicle-released-without-fresh-lock-proof", "demand-left-blocked-after-door-unproven-empty", "vehicle-held-without-a-repair-release-path"],
    productAssertions: {
      controlServer: ["SETTLE_DEMAND_AS_ALL_EMPTY_CANCELLATION", "SETTLE_DOOR_UNPROVEN_ONLY_ON_THE_EXACT_TARGET_SLOTS_ALL_EMPTY", "HOLD_VEHICLE_UNTIL_HARDWARE_RECORD_AND_FRESH_LOCK_PROOF", "PUBLISH_HOLD_IN_VEHICLE_BUSINESS_STATE", "NEVER_RELEASE_ON_HARDWARE_RECORD_ALONE", "RELEASE_ONLY_THROUGH_HARDWARE_REPAIR_RELEASE", "NEVER_TAKE_DOOR_UNPROVEN_FOR_DOORS_PROVEN_LOCKED"],
      onboardHmi: ["REPORT_LOCK_AND_OUTPUT_STATE_AS_READ", "NEVER_OPEN_ANY_SLOT_AFTER_DOOR_UNPROVEN", "DISPLAY_REPAIR_REQUIRED_NOTICE", "JOURNAL_DOOR_UNPROVEN_RESULT_BEFORE_SENDING", "REPLAY_SAME_DOOR_UNPROVEN_RESULT_AFTER_RESTART"],
    },
    finalState: { readiness: "RECOVERY_REQUIRED", business: "DEMAND_TERMINATED_AS_ALL_EMPTY_VEHICLE_HELD_FOR_REPAIR", physical: "SLOTS_EMPTY_DOOR_UNPROVEN_VEHICLE_HELD" },
  },
  // CP-0009 (REQ-0364): the one way out of the hold, after a cancellation or a compensation alike. The administrator opens a
  // session without a demand over the held slots (taken from the SLOT blocking facts), selects HARDWARE_REPAIR_RELEASE --
  // offered only while the vehicle is held for an unproven door -- and submits the repair record against that action; the
  // vehicle journals the action before submitting it so a restart reopens the record form instead of leaving the session
  // executing. RECORDED closes the session, and on persisting the record the control server asks for a safety snapshot
  // (reason PRE_MOVEMENT_RECONCILIATION, asked again after a reconnect). "Fresh" is by the control server's receipt: the first
  // safety readings it receives after the record must show every held slot LOCKED, RESET and EMPTY, then a SAFE
  // PreDepartureSafetyCheck with checkPurpose HOLD_RELEASE lifts the hold and the vehicle's business state is published. If those
  // readings still do not prove the door, the record is spent and a new session is accepted, so no step needs a database edit.
  // Only a record on a release action lifts this hold; nothing in the trace commands slot IO.
  "CV-VEHICLE-HOLD-DOOR-REPAIR-RELEASE": {
    messages: wire("ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted", "HardwareRecoveryRecordSubmitted", "HardwareRecoveryRecordResult", "ExceptionRecoverySessionSnapshot", "SnapshotAppliedAck", "SafetyStateSnapshotRequested", "SafetyStateSnapshot", "SnapshotAppliedAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    // No stable error code: the vector ends READY, and the door code belongs to the two clearing vectors that hold the vehicle.
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "slot-opened-for-repair-release", "vehicle-released-on-record-alone", "vehicle-released-on-readings-received-before-record", "repair-release-offered-without-door-hold", "hardware-record-on-a-non-release-action-lifts-door-hold", "release-session-stuck-after-onboard-restart", "vehicle-held-without-a-repair-release-path"],
    productAssertions: {
      controlServer: ["OFFER_REPAIR_RELEASE_ONLY_WHILE_HELD_FOR_UNPROVEN_DOOR", "LIFT_DOOR_HOLD_ONLY_ON_A_RECORD_OF_THE_RELEASE_ACTION", "CLOSE_RELEASE_SESSION_ON_RECORDED", "REQUEST_SAFETY_SNAPSHOT_ON_RECORD_AND_AFTER_RECONNECT", "RELEASE_ONLY_ON_READINGS_RECEIVED_AFTER_RECORD_AND_A_SAFE_HOLD_RELEASE_CHECK", "NEVER_RELEASE_ON_HARDWARE_RECORD_ALONE", "VOID_RECORD_AND_ACCEPT_NEW_SESSION_WHEN_FIRST_READINGS_UNPROVEN", "PUBLISH_RELEASE_IN_VEHICLE_BUSINESS_STATE"],
      onboardHmi: ["NEVER_SLOT_IO_FOR_REPAIR_RELEASE", "OPEN_RELEASE_SESSION_OVER_HELD_SLOTS_WITHOUT_DEMAND", "JOURNAL_RELEASE_ACTION_BEFORE_SUBMITTING", "RESTORE_REPAIR_RECORD_FORM_AFTER_RESTART", "SUBMIT_HARDWARE_RECORD_ON_RELEASE_ACTION", "REPORT_FRESH_SLOT_READINGS_ON_REQUEST", "ANSWER_HOLD_RELEASE_CHECK_WITHOUT_DEMAND_OR_LEG", "DISPLAY_HOLD_FROM_BLOCKING_FACTS"],
    },
    finalState: { readiness: "READY", business: "DOOR_HOLD_LIFTED_RELEASE_SESSION_CLOSED", physical: "HELD_SLOTS_LOCKED_RESET_EMPTY" },
  },

  // --- 4.0.0 additions (program#185 CP-0012, protocol#13; program#191 CP-0014, protocol#17) ---
  // The operator presses depart at a STAGING_TO_WIRE staging pickup stop (a machine pickup stop has its own vectors below). The request is journaled and acknowledged, the
  // control server answers ACCEPTED, then publishes the departure: loadingPhase CLOSED with OPERATOR_DEPARTED, the worklist
  // (empty with stopEndedReason OPERATOR_DEPARTED when the stop ends with demands not loaded), the plan, and the normal
  // departure check. Demands not loaded are released back to dispatch -- not cancelled, not suppressed, not counted against
  // the station-timeout release limit -- and loaded ones stay on the journey. With nothing loaded the journey closes and the
  // vehicle stays where it is. The correction gate and the departure safety check hold the vehicle exactly as before.
  "CV-CURRENT-STOP-DEPARTURE-ACCEPTED": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "CurrentStopWorklistSnapshot", "SnapshotAppliedAck", "UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"),
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "departure-decision-and-releases-durable-before-result", "result-before-replay", "snapshot-before-ack"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-cancels-or-suppresses-unloaded-demand", "departure-counts-against-station-timeout-release-limit", "departure-bypasses-correction-gate-or-safety-check", "vehicle-moved-after-departure-with-nothing-loaded"],
    productAssertions: {
      controlServer: ["ACCEPT_DEPARTURE_AT_STAGING_PICKUP_STOP", "RELEASE_UNLOADED_DEMANDS_WITHOUT_CANCEL_OR_SUPPRESSION", "KEEP_LOADED_DEMANDS_ON_JOURNEY", "CLOSE_LOADING_PHASE_WITH_OPERATOR_DEPARTED", "CLOSE_JOURNEY_IN_PLACE_WHEN_NOTHING_LOADED", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK", "AUDIT_DEPARTURE_OPERATOR"],
      onboardHmi: ["OFFER_DEPART_AT_STAGING_PICKUP_STOP", "NEVER_OFFER_DEPART_DURING_SLOT_OPERATION_OR_CORRECTION", "JOURNAL_DEPARTURE_REQUEST_BEFORE_SENDING", "ECHO_DISPLAYED_WORKLIST_IN_REQUEST", "DISPLAY_DEPARTURE_FROM_SNAPSHOTS", "NEVER_DEPART_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "LOADING_PHASE_CLOSED_OPERATOR_DEPARTED_UNLOADED_DEMANDS_RELEASED", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },
  // The worklist moved on while the operator decided -- typically a demand appended at the same stop. The control server
  // refuses with WORKLIST_REVISION_STALE and the current revision, so the operator sees the new item before departing again.
  // Since protocol#23 only a material change is refused; CV-CURRENT-STOP-DEPARTURE-STALE-REVISION-ACCEPTED is the exception.
  "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck"),
    stableErrorCode: "WORKLIST_REVISION_STALE",
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-on-stale-worklist-revision-with-material-change", "business-state-changed-by-rejected-departure"],
    productAssertions: {
      controlServer: ["REJECT_DEPARTURE_ON_STALE_WORKLIST_REVISION_WITH_MATERIAL_CHANGE", "RETURN_CURRENT_WORKLIST_REVISION", "CHANGE_NOTHING_ON_REJECTED_DEPARTURE"],
      onboardHmi: ["DISPLAY_DEPARTURE_REJECTION_REASON", "ADOPT_RETURNED_WORKLIST_REVISION", "NEVER_RESEND_REJECTED_DEPARTURE_UNCHANGED"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_DEPARTURE_REJECTED", physical: "UNCHANGED" },
  },
  // The same press at a machine pickup stop, but the revisions differ in nothing material (protocol#23, program#201 CP-0015,
  // control-server#742): the requested revision is lower, belongs to this stop at this station, the operation session matches
  // when one is echoed, every worklist from it to the current one has empty items, and since it no load settled, no loaded
  // basket left and no correction opened (by the control server's receipt). The request is then decided by the remaining
  // checks; this trace shows them passing with only the station departure wait left. Not at a staging pickup stop.
  "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION-ACCEPTED": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"),
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "departure-decision-durable-before-result", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-refused-on-stale-revision-without-material-change", "stale-revision-exception-skips-remaining-checks", "stale-revision-exception-at-staging-pickup-stop", "departure-bypasses-correction-gate-or-safety-check"],
    productAssertions: {
      controlServer: ["ACCEPT_STALE_REVISION_WITHOUT_MATERIAL_CHANGE_AT_MACHINE_PICKUP_STOP", "DECIDE_STALE_REVISION_WITHOUT_MATERIAL_CHANGE_BY_REMAINING_CHECKS", "REQUIRE_REQUESTED_REVISION_LOWER_WITHIN_CURRENT_STOP_AT_CURRENT_STATION", "REQUIRE_OPERATION_SESSION_MATCH_WHEN_REQUEST_CARRIES_ONE", "REQUIRE_EMPTY_ITEMS_IN_EVERY_WORKLIST_FROM_REQUESTED_TO_CURRENT_REVISION", "REQUIRE_NO_LOAD_SETTLED_NO_LOADED_BASKET_LEFT_AND_NO_CORRECTION_SINCE_REQUESTED_REVISION", "TIME_LOAD_SETTLEMENT_AND_CORRECTION_BY_SERVER_RECEIPT", "NEVER_APPLY_STALE_REVISION_EXCEPTION_AT_STAGING_PICKUP_STOP", "RETURN_CURRENT_WORKLIST_REVISION", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK", "AUDIT_DEPARTURE_OPERATOR"],
      onboardHmi: ["ECHO_DISPLAYED_WORKLIST_IN_REQUEST", "JOURNAL_DEPARTURE_REQUEST_BEFORE_SENDING", "ADOPT_ACCEPTED_DEPARTURE_ON_STALE_REVISION", "NEVER_DEPART_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "STALE_REVISION_WITHOUT_MATERIAL_CHANGE_DEPARTURE_ACCEPTED_EN_ROUTE_TO_DROPOFF", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },
  // The request names a station that is not the vehicle's current stop -- typically a request journaled at the previous
  // stop and resubmitted after the vehicle moved on. STATION_MISMATCH is checked first, before the worklist revision, so the
  // answer says the request is for another stop rather than that its revision is old.
  "CV-CURRENT-STOP-DEPARTURE-STATION-MISMATCH": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck"),
    stableErrorCode: "STATION_MISMATCH",
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-applied-to-another-stop", "business-state-changed-by-rejected-departure"],
    productAssertions: {
      controlServer: ["REJECT_DEPARTURE_FOR_ANOTHER_STOP", "CHECK_STATION_BEFORE_WORKLIST_REVISION", "CHANGE_NOTHING_ON_REJECTED_DEPARTURE"],
      onboardHmi: ["DISPLAY_DEPARTURE_REJECTION_REASON", "DISCARD_DEPARTURE_REQUEST_OF_A_PREVIOUS_STOP"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_DEPARTURE_REJECTED", physical: "UNCHANGED" },
  },
  // Depart pressed where it does not apply: a stop that is not a pickup stop, or while a slot operation runs or a load
  // correction is open (a stop that is not the vehicle's current one is CV-CURRENT-STOP-DEPARTURE-STATION-MISMATCH, a
  // machine pickup stop whose loads are not complete is CV-CURRENT-STOP-DEPARTURE-MACHINE-LOADING-INCOMPLETE). Refused with ACTION_NOT_ALLOWED_IN_STATE;
  // nothing changes and the operator may press again once the state allows it.
  "CV-CURRENT-STOP-DEPARTURE-NOT-ALLOWED": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck"),
    stableErrorCode: "ACTION_NOT_ALLOWED_IN_STATE",
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-accepted-at-a-stop-that-is-not-a-pickup-stop", "departure-during-slot-operation-or-correction", "business-state-changed-by-rejected-departure"],
    productAssertions: {
      controlServer: ["REJECT_DEPARTURE_AT_A_STOP_THAT_IS_NOT_A_PICKUP_STOP", "REJECT_DEPARTURE_DURING_SLOT_OPERATION_OR_CORRECTION", "CHANGE_NOTHING_ON_REJECTED_DEPARTURE"],
      onboardHmi: ["DISPLAY_DEPARTURE_REJECTION_REASON", "ALLOW_NEW_DEPARTURE_REQUEST_AFTER_REJECTION"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_DEPARTURE_REJECTED", physical: "UNCHANGED" },
  },
  // The same departureRequestId arrives again under a new messageId -- a restart resubmitting from the journal, or a double
  // press that reuses the pending request. The control server replays the result it gave and departs once. The same
  // departureRequestId with different content is a BUSINESS_ID_CONTENT_CONFLICT and is never applied.
  "CV-CURRENT-STOP-DEPARTURE-DUPLICATE-REQUEST": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck", "CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck"),
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "second-departure-on-duplicate-request", "demands-released-twice", "conflicting-duplicate-departure-applied"],
    productAssertions: {
      controlServer: ["DEDUPLICATE_DEPARTURE_ON_REQUEST_ID", "REPLAY_SAME_DEPARTURE_RESULT", "REJECT_SAME_REQUEST_ID_WITH_DIFFERENT_CONTENT"],
      onboardHmi: ["REUSE_PENDING_DEPARTURE_REQUEST_ID", "ADOPT_REPLAYED_DEPARTURE_RESULT", "NEVER_MINT_NEW_REQUEST_ID_FOR_SAME_PRESS"],
    },
    finalState: { readiness: "UNCHANGED_OR_SPECIFIED_BY_VECTOR", business: "AT_MOST_ONE_DEPARTURE_PER_REQUEST_ID", physical: "NO_UNPROVEN_STATE" },
  },
  // Low battery with cargo on board at the staging station (protocol#15, program#188 CP-0013, which replaced the charging
  // stop CP-0012 gave this candidate): deliver first, charge afterwards. The control server departs the vehicle as for an
  // accepted departure -- loadingPhase closes with CHARGING_REQUIRED, the loaded demands stay on the journey, the demands
  // not yet loaded are released back to dispatch, and the vehicle leaves through the correction gate and the DEPARTURE
  // check. The journey carries no CHARGER stop, activePurpose stays TRANSPORT, and the existing charging allocation takes
  // the vehicle once the journey ends. Without cargo the journey closes in place instead (no CHARGING_REQUIRED phase).
  "CV-STAGING-CHARGING-REQUIRED-DEPARTURE-WITH-CARGO": {
    messages: wire("VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "CurrentStopWorklistSnapshot", "SnapshotAppliedAck", "UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"),
    persistenceCheckpoints: ["charging-required-decision-and-releases-durable-before-snapshot", "projection-revision-before-send", "snapshot-before-ack"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "charger-stop-in-transport-journey", "transport-purpose-replaced-by-charging", "loaded-demand-released-for-charging", "departure-cancels-or-suppresses-unloaded-demand", "departure-counts-against-station-timeout-release-limit", "departure-bypasses-correction-gate-or-safety-check", "return-to-staging-before-dropoff", "charging-required-departure-at-a-machine-pickup-stop"],
    productAssertions: {
      controlServer: ["DEPART_WITH_CARGO_WHEN_CHARGING_REQUIRED_AT_STAGING", "CLOSE_LOADING_PHASE_WITH_CHARGING_REQUIRED", "RELEASE_UNLOADED_DEMANDS_WITHOUT_CANCEL_OR_SUPPRESSION", "KEEP_LOADED_DEMANDS_ON_JOURNEY", "INSERT_NO_CHARGER_STOP_IN_TRANSPORT_JOURNEY", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK", "CHARGE_THROUGH_CHARGING_ALLOCATION_AFTER_JOURNEY_ENDS"],
      onboardHmi: ["DISPLAY_CHARGING_REQUIRED_DEPARTURE_FROM_SNAPSHOTS", "NEVER_DEPART_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "LOADING_PHASE_CLOSED_CHARGING_REQUIRED_EN_ROUTE_TO_DROPOFF", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },
  // --- 4.0.0, program#191 CP-0014 section 3 item 4, protocol#17 ---
  // A machine pickup stop accepts depart once every load committed to the stop is complete with a basket on board. Here the
  // vehicle is still in CARGO_HOLDING_WAIT: the departure counts as the cargo-holding deadline expiring now, so loadingPhase
  // closes with OPERATOR_DEPARTED (not CARGO_HOLDING_TIMEOUT -- the floor must tell a press from an expiry), the appended
  // stops not yet loaded go back to dispatch exactly as on a cargo-holding timeout and leave the plan, and the vehicle
  // leaves at once: the stop does not wait out the rest of its station departure deadline and keeps no correction grace.
  "CV-CURRENT-STOP-DEPARTURE-MACHINE-CARGO-HOLDING": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"),
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "departure-decision-and-releases-durable-before-result", "result-before-replay", "snapshot-before-ack"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-cancels-or-suppresses-unloaded-demand", "departure-counts-against-station-timeout-release-limit", "loaded-demand-released-on-departure", "departure-waits-out-station-departure-deadline", "departure-bypasses-correction-gate-or-safety-check"],
    productAssertions: {
      controlServer: ["ACCEPT_DEPARTURE_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE", "TREAT_DEPARTURE_AS_CARGO_HOLDING_DEADLINE_EXPIRING_NOW", "CLOSE_LOADING_PHASE_WITH_OPERATOR_DEPARTED", "RELEASE_UNLOADED_APPENDED_STOPS_AS_ON_CARGO_HOLDING_TIMEOUT", "KEEP_LOADED_DEMANDS_ON_JOURNEY", "END_STOP_WITHOUT_WAITING_OUT_STATION_DEPARTURE_DEADLINE", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK", "AUDIT_DEPARTURE_OPERATOR"],
      onboardHmi: ["OFFER_DEPART_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE", "NEVER_OFFER_DEPART_DURING_SLOT_OPERATION_OR_CORRECTION", "JOURNAL_DEPARTURE_REQUEST_BEFORE_SENDING", "DISPLAY_DEPARTURE_FROM_SNAPSHOTS", "NEVER_DEPART_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "LOADING_PHASE_CLOSED_OPERATOR_DEPARTED_APPENDED_STOPS_RELEASED_EN_ROUTE_TO_DROPOFF", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },
  // The same press after the loading phase has already ended -- the vehicle is full, every zone it serves forbids en-route
  // appends so it never held, or the cargo-holding deadline has expired -- and only the station departure wait is left.
  // loadingPhase and its closedReason stay as they were; the departure only ends that wait and the vehicle leaves at once.
  "CV-CURRENT-STOP-DEPARTURE-MACHINE-STATION-WAIT": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"),
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "departure-decision-durable-before-result", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "closed-reason-rewritten-by-departure", "departure-waits-out-station-departure-deadline", "departure-bypasses-correction-gate-or-safety-check"],
    productAssertions: {
      controlServer: ["ACCEPT_DEPARTURE_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE", "KEEP_LOADING_PHASE_AND_CLOSED_REASON_ON_DEPARTURE", "END_STOP_WITHOUT_WAITING_OUT_STATION_DEPARTURE_DEADLINE", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK", "AUDIT_DEPARTURE_OPERATOR"],
      onboardHmi: ["OFFER_DEPART_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE", "OFFER_DEPART_WHILE_ONLY_STATION_DEPARTURE_WAIT_REMAINS", "JOURNAL_DEPARTURE_REQUEST_BEFORE_SENDING", "NEVER_DEPART_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "STATION_DEPARTURE_WAIT_ENDED_CLOSED_REASON_UNCHANGED_EN_ROUTE_TO_DROPOFF", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },
  // Depart pressed at a machine pickup stop before every committed load is complete -- the operator is still entering or
  // loading -- or with nothing loaded at all. Refused with ACTION_NOT_ALLOWED_IN_STATE; nothing changes.
  "CV-CURRENT-STOP-DEPARTURE-MACHINE-LOADING-INCOMPLETE": {
    messages: wire("CurrentStopDepartureRequested", "DurableAck", "CurrentStopDepartureResult", "DurableAck"),
    stableErrorCode: "ACTION_NOT_ALLOWED_IN_STATE",
    persistenceCheckpoints: ["departure-request-journaled-before-send", "departure-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "departure-accepted-before-committed-loads-complete", "departure-accepted-with-nothing-loaded-at-a-machine-pickup-stop", "business-state-changed-by-rejected-departure"],
    productAssertions: {
      controlServer: ["REJECT_DEPARTURE_AT_MACHINE_PICKUP_STOP_BEFORE_COMMITTED_LOADS_COMPLETE", "REJECT_DEPARTURE_AT_MACHINE_PICKUP_STOP_WITH_NOTHING_LOADED", "CHANGE_NOTHING_ON_REJECTED_DEPARTURE"],
      onboardHmi: ["NEVER_OFFER_DEPART_AT_MACHINE_PICKUP_STOP_BEFORE_COMMITTED_LOADS_COMPLETE", "DISPLAY_DEPARTURE_REJECTION_REASON"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_DEPARTURE_REJECTED", physical: "UNCHANGED" },
  },
  // A staging pickup stop has no cargo-holding deadline while nothing is loaded. The load batch that puts cargo on board sets
  // it, with the machine duration; each demand for this station appended to the vehicle afterwards moves it to the append
  // plus that duration. Releases, cancellations and other worklist changes do not move it, and it clears again if the cargo
  // is undone back to none. The append opens a new stop at the same station (EnRouteAppendPlanner), so it travels in the
  // plan, not in the current worklist. The first business snapshot is CARGO_HOLDING_WAIT with the deadline (nothing left to
  // load); the second is LOADING with the moved deadline, because the appended demand is still to be loaded -- the control
  // server sends LOADING whenever loads remain (LoadingPhaseMachine, protocol#19), so the HMI keys the countdown on the
  // deadline, not on the state.
  "CV-STAGING-CARGO-HOLDING-DEADLINE-MOVED": {
    messages: wire("VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"),
    persistenceCheckpoints: ["cargo-holding-deadline-durable-before-snapshot", "projection-revision-before-send", "snapshot-before-ack"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "cargo-holding-deadline-set-with-nothing-loaded", "cargo-holding-deadline-not-moved-on-append", "cargo-holding-deadline-moved-by-release-cancellation-or-other-worklist-change", "cargo-holding-wait-sent-while-a-demand-remains-to-load", "station-departure-deadline-at-staging-pickup-stop"],
    productAssertions: {
      controlServer: ["SET_STAGING_CARGO_HOLDING_DEADLINE_ON_FIRST_LOADED_BASKET", "MOVE_STAGING_CARGO_HOLDING_DEADLINE_ON_DEMAND_APPENDED_FOR_THE_STATION", "KEEP_STAGING_CARGO_HOLDING_DEADLINE_ON_RELEASE_CANCELLATION_OR_OTHER_WORKLIST_CHANGE", "CLEAR_STAGING_CARGO_HOLDING_DEADLINE_WHEN_NO_CARGO_REMAINS", "SEND_LOADING_WHILE_A_DEMAND_REMAINS_TO_LOAD_AT_THE_STATION", "SEND_CARGO_HOLDING_DEADLINE_IN_LOADING_AND_CARGO_HOLDING_WAIT"],
      onboardHmi: ["DISPLAY_CARGO_HOLDING_COUNTDOWN_AT_STAGING_PICKUP_STOP", "ADOPT_MOVED_CARGO_HOLDING_DEADLINE", "DISPLAY_CARGO_HOLDING_COUNTDOWN_FROM_DEADLINE_NOT_FROM_STATE", "NEVER_RUN_COUNTDOWN_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "STAGING_LOADING_WITH_CARGO_HOLDING_DEADLINE_MOVED_TO_APPEND", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },
  // The staging cargo-holding deadline expires. The loading phase ends as at a machine pickup stop: CARGO_HOLDING_TIMEOUT,
  // the loaded demands stay on the journey, those not yet loaded go back to dispatch -- not cancelled, not suppressed, not
  // counted against the station-timeout release limit -- and the empty worklist says DEMAND_RELEASED. A running slot
  // operation, correction or cancellation settles first. The vehicle leaves through the correction gate and DEPARTURE check.
  "CV-STAGING-CARGO-HOLDING-TIMEOUT": {
    messages: wire("VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "CurrentStopWorklistSnapshot", "SnapshotAppliedAck", "UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"),
    persistenceCheckpoints: ["cargo-holding-timeout-decision-and-releases-durable-before-snapshot", "projection-revision-before-send", "snapshot-before-ack"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "operator-departed-reason-on-cargo-holding-timeout", "cargo-holding-timeout-cancels-or-suppresses-unloaded-demand", "cargo-holding-timeout-counts-against-station-timeout-release-limit", "cargo-holding-timeout-interrupts-slot-operation-or-correction", "loaded-demand-released-on-cargo-holding-timeout", "departure-bypasses-correction-gate-or-safety-check"],
    productAssertions: {
      controlServer: ["CLOSE_STAGING_LOADING_PHASE_WITH_CARGO_HOLDING_TIMEOUT", "END_EMPTY_WORKLIST_WITH_DEMAND_RELEASED", "RELEASE_UNLOADED_DEMANDS_WITHOUT_CANCEL_OR_SUPPRESSION", "KEEP_LOADED_DEMANDS_ON_JOURNEY", "LET_SLOT_OPERATION_OR_CORRECTION_SETTLE_BEFORE_EXPIRY", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK"],
      onboardHmi: ["DISPLAY_CARGO_HOLDING_TIMEOUT_FROM_SNAPSHOTS", "NEVER_DEPART_LOCALLY"],
    },
    finalState: { readiness: "READY", business: "LOADING_PHASE_CLOSED_CARGO_HOLDING_TIMEOUT_UNLOADED_DEMANDS_RELEASED", physical: "LOADED_SLOTS_OCCUPIED_LOCKED_RESET" },
  },

  // --- 6.0.0 additions (program#213 CP-0021, REQ-0367 and the revised REQ-0211, REQ-0352; protocol#26) ---
  // A multi-basket load with k of N slots closed safely OCCUPIED, every door proven locked and every output reset, no UNKNOWN
  // slot and no manual recovery: the operator asks to leave the rest. The request is journaled and acknowledged, the control
  // server authorizes it naming the k slots, and only then does the vehicle end the operation, opening no further slot, and
  // report COMPLETED_REMAINING_SKIPPED. The control server commits the k baskets as one LoadBatch,
  // releases the remaining slots and their reservation, later unloads only the k, and completes the demand as a normal
  // delivery: not cancelled, not suppressed, no manual transport alarm.
  "CV-REMAINING-BASKETS-SKIP-AUTHORIZED": {
    messages: wire("RemainingBasketsSkipRequested", "DurableAck", "RemainingBasketsSkipResult", "DurableAck", "OperationResult", "DurableAck"),
    stableErrorCode: "REMAINING_BASKETS_SKIPPED",
    persistenceCheckpoints: ["skip-request-journaled-before-send", "skip-request-durable-before-ack", "skip-decision-durable-before-result", "skip-result-journaled-before-ending-the-operation", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "remaining-baskets-skipped-without-authorization", "slot-opened-while-skip-pending", "skip-settled-as-cancellation-or-suppression", "manual-transport-alarm-on-skip", "skipped-slots-kept-reserved", "loaded-slot-cleared-on-skip"],
    productAssertions: {
      controlServer: ["AUTHORIZE_SKIP_ONLY_WITH_AT_LEAST_ONE_LOADED_AND_ONE_REMAINING_SLOT", "AUTHORIZE_SKIP_ONLY_WITH_ALL_DOORS_LOCKED_OUTPUTS_RESET_AND_NO_UNKNOWN", "COMMIT_AUTHORIZED_LOADED_SLOTS_AS_ONE_LOAD_BATCH", "RELEASE_REMAINING_SLOTS_AND_RESERVATION_ON_SETTLEMENT", "UNLOAD_ONLY_THE_AUTHORIZED_LOADED_SLOTS", "COMPLETE_DEMAND_AS_NORMAL_DELIVERY_WITHOUT_SUPPRESSION_OR_ALARM", "AUDIT_SKIP_N_TO_K_WITH_OPERATOR_WHEN_KNOWN"],
      onboardHmi: ["OFFER_SKIP_ONLY_WHILE_ITS_CONDITIONS_HOLD", "JOURNAL_SKIP_REQUEST_BEFORE_SENDING", "NEVER_OPEN_A_SLOT_WHILE_SKIP_PENDING", "END_OPERATION_ONLY_ON_AUTHORIZED_SKIP", "REPORT_AUTHORIZED_SLOTS_COMPLETED_AND_REMAINING_SLOTS_SKIPPED", "NEVER_ACT_ON_AN_AUTHORIZATION_AFTER_THE_OPERATION_ENDED_ANOTHER_WAY"],
    },
    finalState: { readiness: "READY", business: "DEMAND_LOADED_WITH_AUTHORIZED_BASKETS_REMAINING_SLOTS_RELEASED", physical: "LOADED_SLOTS_OCCUPIED_REMAINING_SLOTS_EMPTY_ALL_LOCKED_RESET" },
  },
  // Refused, here because a door is not proven locked; an unproven output, an UNKNOWN slot, a manual recovery, a correction or
  // cancellation in progress or a load already ended are refused the same way with their own codes. Nothing changes: the
  // operation goes on, the vehicle says why, and the operator may load on or ask again.
  "CV-REMAINING-BASKETS-SKIP-REJECTED": {
    messages: wire("RemainingBasketsSkipRequested", "DurableAck", "RemainingBasketsSkipResult", "DurableAck"),
    stableErrorCode: "LOCK_NOT_CLOSED",
    persistenceCheckpoints: ["skip-request-journaled-before-send", "skip-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "remaining-baskets-skipped-without-authorization", "business-state-changed-by-rejected-skip", "slot-operation-ended-by-rejected-skip"],
    productAssertions: {
      controlServer: ["REJECT_SKIP_WITH_A_DOOR_NOT_PROVEN_LOCKED_OR_OUTPUT_NOT_RESET", "REJECT_SKIP_WITH_AN_UNKNOWN_SLOT_OR_MANUAL_RECOVERY", "REJECT_SKIP_DURING_CORRECTION_OR_CANCELLATION_OR_AFTER_LOADING_ENDED", "CHANGE_NOTHING_ON_REJECTED_SKIP"],
      onboardHmi: ["DISPLAY_SKIP_REJECTION_REASON", "CONTINUE_LOADING_AFTER_REJECTED_SKIP", "ALLOW_NEW_SKIP_REQUEST_AFTER_REJECTION"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_SKIP_REJECTED_LOADING_CONTINUES", physical: "UNCHANGED" },
  },
  // k = 0 by the control server's facts: no target slot has closed safely OCCUPIED. Giving the whole demand up is a
  // cancellation (REQ-0211), so the skip is refused and nothing changes. A request naming no slot cannot be written at all
  // (I-RemainingBasketsSkipRequested-MIN-ITEMS-loadedSlots); this is the request whose claim the control server cannot bear out.
  "CV-REMAINING-BASKETS-SKIP-NOTHING-LOADED": {
    messages: wire("RemainingBasketsSkipRequested", "DurableAck", "RemainingBasketsSkipResult", "DurableAck"),
    stableErrorCode: "REMAINING_BASKETS_SKIP_NOTHING_LOADED",
    persistenceCheckpoints: ["skip-request-journaled-before-send", "skip-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "remaining-baskets-skipped-without-authorization", "skip-authorized-with-nothing-loaded", "business-state-changed-by-rejected-skip"],
    productAssertions: {
      controlServer: ["REJECT_SKIP_WHEN_NO_TARGET_SLOT_CLOSED_OCCUPIED", "CHANGE_NOTHING_ON_REJECTED_SKIP"],
      onboardHmi: ["NEVER_OFFER_SKIP_BEFORE_A_BASKET_IS_LOADED", "DISPLAY_SKIP_REJECTION_REASON", "CONTINUE_LOADING_AFTER_REJECTED_SKIP"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_SKIP_REJECTED_LOADING_CONTINUES", physical: "UNCHANGED" },
  },
  // The same skipRequestId again under a new messageId -- a restart resubmitting from the journal, a reconnect, or a double press
  // reusing the pending request. The control server replays the result it gave and skips once. The same skipRequestId with
  // different content is a BUSINESS_ID_CONTENT_CONFLICT and is never applied.
  "CV-REMAINING-BASKETS-SKIP-DUPLICATE-REQUEST": {
    messages: wire("RemainingBasketsSkipRequested", "DurableAck", "RemainingBasketsSkipResult", "DurableAck", "RemainingBasketsSkipRequested", "DurableAck", "RemainingBasketsSkipResult", "DurableAck"),
    persistenceCheckpoints: ["skip-request-journaled-before-send", "skip-request-durable-before-ack", "result-before-replay"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "second-skip-effect-on-duplicate-request", "conflicting-duplicate-skip-applied", "remaining-baskets-skipped-without-authorization"],
    productAssertions: {
      controlServer: ["DEDUPLICATE_SKIP_ON_REQUEST_ID", "REPLAY_SAME_SKIP_RESULT", "REJECT_SAME_REQUEST_ID_WITH_DIFFERENT_CONTENT"],
      onboardHmi: ["REUSE_PENDING_SKIP_REQUEST_ID_AFTER_RECONNECT_OR_RESTART", "ADOPT_REPLAYED_SKIP_RESULT", "NEVER_MINT_NEW_REQUEST_ID_FOR_SAME_PRESS"],
    },
    finalState: { readiness: "UNCHANGED_OR_SPECIFIED_BY_VECTOR", business: "AT_MOST_ONE_SKIP_PER_REQUEST_ID", physical: "NO_UNPROVEN_STATE" },
  },
  // What protocol#26 must make impossible: a vehicle reporting COMPLETED_REMAINING_SKIPPED that no AUTHORIZED
  // RemainingBasketsSkipResult of the same demand and attempt bears out -- none sent, only a REJECTED one, or other COMPLETED
  // slots than it authorized. The result is acknowledged as received, never settled: no LoadBatch, no released slot,
  // and the demand stays unsettled behind a blocked journey, as for any result that does not reconcile.
  "CV-REMAINING-BASKETS-SKIP-UNAUTHORIZED-RESULT": {
    messages: wire("OperationResult", "DurableAck"),
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "remaining-baskets-skipped-without-authorization", "unauthorized-skip-result-settled-as-completed", "skipped-slots-released-without-authorization"],
    productAssertions: {
      controlServer: ["NEVER_SETTLE_SKIPPED_RESULT_WITHOUT_MATCHING_AUTHORIZATION", "FIND_THE_AUTHORIZATION_BY_DEMAND_AND_ATTEMPT", "SETTLE_SKIPPED_RESULT_ONLY_ON_THE_AUTHORIZED_LOADED_SLOTS", "BLOCK_JOURNEY_ON_UNRECONCILED_SKIPPED_RESULT"],
      onboardHmi: ["NEVER_REPORT_SKIPPED_RESULT_WITHOUT_AUTHORIZATION"],
    },
    finalState: { readiness: "RECOVERY_REQUIRED", business: "JOURNEY_BLOCKED_DEMAND_NOT_SETTLED", physical: "AS_REPORTED_BY_UNRECONCILED_RESULT" },
  },
  // The revised REQ-0211: once a basket is in a target slot the load is no longer cancelled. The control server refuses with
  // LOAD_CANCELLATION_BASKET_LOADED (a door not proven locked or an output not reset with LOCK_NOT_CLOSED or
  // UNLOCK_OUTPUT_NOT_RESET), and nothing changes; to load fewer the operator asks for the remaining-baskets skip.
  "CV-LOAD-CANCELLATION-BASKET-LOADED": {
    messages: wire("LoadCancellationStartRequested", "LoadCancellationAuthorization"),
    stableErrorCode: "LOAD_CANCELLATION_BASKET_LOADED",
    persistenceCheckpoints: ["cancellation-decision-durable-before-authorization"],
    forbiddenSideEffects: ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success", "cancellation-authorized-after-a-basket-is-loaded", "loaded-slot-cleared-by-business-cancellation", "business-state-changed-by-rejected-cancellation"],
    productAssertions: {
      controlServer: ["REJECT_CANCELLATION_ONCE_A_BASKET_IS_LOADED", "REJECT_CANCELLATION_WITH_A_DOOR_NOT_PROVEN_LOCKED_OR_OUTPUT_NOT_RESET", "CHANGE_NOTHING_ON_REJECTED_CANCELLATION"],
      onboardHmi: ["NEVER_OFFER_CANCELLATION_ONCE_A_BASKET_IS_LOADED", "DISPLAY_CANCELLATION_REJECTION_REASON", "OFFER_REMAINING_BASKETS_SKIP_INSTEAD"],
    },
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_CANCELLATION_REJECTED", physical: "UNCHANGED" },
  },
};
for (const [vectorId, trajectory] of Object.entries(trajectories)) {
  const steps = trajectory.steps
    ?? trajectory.messages.map((messageType, index) => ({ step: index + 1, atMs: index * 100, action: index === 0 ? "send" : "expect", messageType, virtualTimeOnly: true }));
  if (!trajectory.productAssertions?.controlServer?.length || !trajectory.productAssertions?.onboardHmi?.length) throw new Error(`${vectorId}: productAssertions are mandatory for every vector`);
  writeText(`vectors/${vectorId}/input.ndjson`, `${steps.map(canonical).join("\n")}\n`);
  const stableErrorCode = trajectory.stableErrorCode ?? (vectorId.includes("DIFFERENT-CONTENT") ? "MESSAGE_ID_CONTENT_CONFLICT" : vectorId.includes("SAME-REVISION-CONFLICT") ? "SNAPSHOT_REVISION_CONTENT_CONFLICT" : vectorId.includes("EXPIRES") ? "PREDEPARTURE_CHECK_EXPIRED" : null);
  if (stableErrorCode) noteErrorCodeAsset(stableErrorCode);
  const expected = {
    vectorId,
    orderedExpectedMessages: steps.filter((step) => step.messageType).map((step) => step.messageType),
    persistenceCheckpoints: trajectory.persistenceCheckpoints ?? ["durable-before-send", "durable-before-ack", "journal-before-irreversible-io", "result-before-replay"],
    forbiddenSideEffects: trajectory.forbiddenSideEffects ?? ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"],
  };
  expected.productAssertions = trajectory.productAssertions;
  expected.finalState = trajectory.finalState ?? { readiness: vectorId.includes("RECOVERY") || vectorId.includes("CONNECTION-LOSS") ? "RECOVERY_REQUIRED_OR_UNIQUELY_RECONCILED" : "UNCHANGED_OR_SPECIFIED_BY_VECTOR", business: "NO_DUPLICATE_COMMIT", physical: "NO_UNPROVEN_STATE" };
  expected.stableErrorCode = stableErrorCode;
  writeJson(`vectors/${vectorId}/expected.json`, expected);
}

// The slice family's shape lives here once: the index, its governance schema and the gate read
// these rather than repeating the count / the id pattern / the gate list in three places.
// Four onboard authority modes. The single const of v1 could only say "read-only projection",
// which is false for a slice where the vehicle is the physical authority or the operator's voice.
const onboardModes = ["READ_ONLY_COMMITTED_PROJECTION", "SELECTION_WITHIN_COMMITTED_SET", "OPERATOR_CONFIRMATION_SOURCE", "PHYSICAL_EXECUTION_AUTHORITY"];
const sliceIndexSchemaVersion = "2.0.0";
const attestationSchemaVersion = "1.0.0";
const sliceIdPrefix = "FP-IS-";
const sliceIdPattern = `^${sliceIdPrefix}[0-9]{2}$`;
const gateModel = ["G1", "CONTROL_SERVER_G2", "ONBOARD_HMI_G2", "G3"];
// Neither the batch nor the business cluster goes into the id. The batch is a circular dependency
// (it is decided by a later decision that this one blocks) and cluster membership has been
// rejudged five times, while an id lives in 161 test traits and in immutable evidence directories.
// The business face is carried by definition.scope instead. Batch and face stay in the
// specification: writing "FP-IS-13 belongs to batch 8" into the protocol repository would turn a
// re-plan into a protocol change, and a protocol change voids both sides' gate evidence.
const slices = [
  ["FP-IS-00", 0, [], ["CV-SESSION-RECOVERY-HAPPY", "CV-SESSION-RECONNECT-DURING-RECOVERY", "CV-SNAPSHOT-REPLACE-AND-ACK", "CV-SNAPSHOT-SAME-REVISION-CONFLICT"], {
    scope: "SESSION_HANDSHAKE_RECOVERY_AND_SNAPSHOT",
    requiredOutcomes: ["EXACTLY_ONE_ACTIVE_SESSION", "READINESS_DECIDED_BY_CONTROL_SERVER", "SNAPSHOTS_REPLACED_NOT_MERGED"],
    authorityModel: { controlServerFact: "SessionGeneration", wireMessages: ["SessionHello", "SessionAccepted", "SessionReadiness"], onboardMode: ["READ_ONLY_COMMITTED_PROJECTION", "PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["FENCE_STALE_GENERATIONS", "DECIDE_READINESS"], onboardHmi: ["REPORT_UNSETTLED_STATE", "ADOPT_READINESS_DECISION"] },
  }],
  ["FP-IS-01", 1, ["FP-IS-00"], ["CV-DEMAND-ACCEPT-TO-PICKUP"], {
    scope: "DEMAND_ACCEPTANCE_AND_TO_PICKUP",
    requiredOutcomes: ["EXACTLY_ONE_ACCEPTED_DEMAND_SNAPSHOT", "EXACTLY_ONE_TO_PICKUP_INTENT", "EXACTLY_ONE_RIOT_ORDER", "TRUSTED_PICKUP_ARRIVAL", "COMMITTED_DEMAND_JOURNEY_PROJECTED"],
    authorityModel: { controlServerFact: "AcceptedDemandSnapshot", wireMessages: ["UpcomingStopPlanSnapshot", "CurrentStopWorklistSnapshot"], onboardMode: ["READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["MESINGEST_FINAL_REREAD", "ATOMIC_DEMAND_ACCEPTANCE", "DEDUPLICATED_TO_PICKUP_INTENT", "RIOT_ORDER_RECONCILIATION", "TRUSTED_PICKUP_ARRIVAL_ADOPTION"], onboardHmi: ["DISPLAY_COMMITTED_DEMAND_JOURNEY", "DISPLAY_CURRENT_STOP", "NEVER_DISCOVER_SELECT_OR_BIND_DEMAND"] },
  }],
  ["FP-IS-02", 2, ["FP-IS-01"], ["CV-PICKUP-SUBLOT-LOAD", "CV-LOAD-CORRECTION", "CV-LOAD-CANCELLATION-ALL-EMPTY", "CV-LOAD-CANCELLATION-BEFORE-LOAD", "CV-SUBLOT-REJECTED-AFTER-ENTRY", "CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN", "CV-CURRENT-STOP-DEPARTURE-ACCEPTED", "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION", "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION-ACCEPTED", "CV-CURRENT-STOP-DEPARTURE-NOT-ALLOWED", "CV-CURRENT-STOP-DEPARTURE-STATION-MISMATCH", "CV-CURRENT-STOP-DEPARTURE-DUPLICATE-REQUEST", "CV-CURRENT-STOP-DEPARTURE-MACHINE-CARGO-HOLDING", "CV-CURRENT-STOP-DEPARTURE-MACHINE-STATION-WAIT", "CV-CURRENT-STOP-DEPARTURE-MACHINE-LOADING-INCOMPLETE", "CV-STAGING-CARGO-HOLDING-DEADLINE-MOVED", "CV-STAGING-CARGO-HOLDING-TIMEOUT", "CV-REMAINING-BASKETS-SKIP-AUTHORIZED", "CV-REMAINING-BASKETS-SKIP-REJECTED", "CV-REMAINING-BASKETS-SKIP-NOTHING-LOADED", "CV-REMAINING-BASKETS-SKIP-DUPLICATE-REQUEST", "CV-REMAINING-BASKETS-SKIP-UNAUTHORIZED-RESULT", "CV-LOAD-CANCELLATION-BASKET-LOADED"], {
    scope: "STATION_PICKUP_AND_MULTI_SLOT_LOAD",
    requiredOutcomes: ["SUBLOT_BOUND_TO_OPERATION_SESSION", "SLOT_SET_AUTHORIZED_ONCE", "CORRECTION_AND_CANCELLATION_AUTHORIZED", "EMPTY_SLOTS_SETTLE_WHILE_UNPROVEN_DOOR_HOLDS_VEHICLE", "PICKUP_DEPARTURE_ON_OPERATOR_REQUEST_RELEASES_UNLOADED_DEMANDS", "STAGING_CARGO_HOLDING_DEADLINE_RUNS_WITH_CARGO_ON_BOARD", "REMAINING_BASKETS_SKIPPED_ONLY_ON_SERVER_AUTHORIZATION", "LOAD_CANCELLATION_REFUSED_ONCE_A_BASKET_IS_LOADED"],
    authorityModel: { controlServerFact: "OperationSession", wireMessages: ["SublotEntryRequested", "SlotOperationCommand", "OperationResult", "CurrentStopDepartureRequested", "CurrentStopDepartureResult", "RemainingBasketsSkipRequested", "RemainingBasketsSkipResult"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY", "OPERATOR_CONFIRMATION_SOURCE"] },
    ownerResponsibilities: { controlServer: ["AUTHORIZE_SLOT_SET", "RECONCILE_LOAD_OUTCOME", "HOLD_VEHICLE_ON_UNPROVEN_DOOR", "DECIDE_PICKUP_DEPARTURE_ON_REQUEST", "RUN_STAGING_CARGO_HOLDING_DEADLINE", "AUTHORIZE_REMAINING_BASKETS_SKIP"], onboardHmi: ["SUBMIT_SCANNED_SUBLOT", "LOAD_ONLY_AUTHORIZED_SLOTS", "REPORT_UNPROVEN_DOOR_AFTER_EMPTY", "REQUEST_PICKUP_DEPARTURE_WITH_OPERATOR", "REQUEST_REMAINING_BASKETS_SKIP_NEVER_SKIP_LOCALLY"] },
  }],
  ["FP-IS-03", 3, ["FP-IS-02"], ["CV-PREDEPARTURE-SAFETY-EXPIRES", "CV-OPERATION-RESULT-UNKNOWN-RECONCILE"], {
    scope: "PREDEPARTURE_SAFETY_AND_RESULT_RECONCILE",
    requiredOutcomes: ["NEVER_DEPART_ON_EXPIRED_CHECK", "UNKNOWN_NEVER_TREATED_AS_SUCCESS"],
    authorityModel: { controlServerFact: "PreDepartureSafetyCheck", wireMessages: ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult", "SafetyStateChanged"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["EXPIRE_CHECK_ON_STATE_CHANGE", "RECONCILE_FROM_REPORTED_JOURNAL"], onboardHmi: ["REPORT_SAFETY_STATE_PROMPTLY", "REPORT_UNKNOWN_AS_UNKNOWN"] },
  }],
  ["FP-IS-04", 4, ["FP-IS-03"], ["CV-DESTINATION-UNLOAD-ALL-EMPTY"], {
    scope: "DESTINATION_UNLOAD",
    requiredOutcomes: ["UNLOAD_COMMITTED_ONCE", "FINAL_PHYSICAL_STATE_PROVEN_EMPTY"],
    authorityModel: { controlServerFact: "OperationSession", wireMessages: ["SlotOperationCommand", "OperationResult"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["COMMIT_UNLOAD_ONCE"], onboardHmi: ["UNLOAD_AUTHORIZED_SLOTS_ONLY", "REPORT_FINAL_PHYSICAL_STATE"] },
  }],
  ["FP-IS-05", 5, ["FP-IS-00"], ["CV-CONNECTION-LOSS-SAFE-FINISH", "CV-SESSION-RECONNECT-DURING-RECOVERY", "CV-REMAINING-BASKETS-SKIP-DUPLICATE-REQUEST"], {
    scope: "CONNECTION_LOSS_SAFE_FINISH",
    requiredOutcomes: ["IN_PROGRESS_OPERATION_FINISHED_SAFELY", "NEVER_READY_BEFORE_RECONCILIATION"],
    authorityModel: { controlServerFact: "SessionGeneration", wireMessages: ["RecoveryStateReport", "SessionReadiness"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["WITHHOLD_READINESS_UNTIL_RECONCILED"], onboardHmi: ["FINISH_SAFELY_OFFLINE", "JOURNAL_BEFORE_IRREVERSIBLE_IO"] },
  }],
  ["FP-IS-06", 6, ["FP-IS-00"], ["CV-RELIABLE-RETRY-SAME-CONTENT", "CV-RELIABLE-RETRY-DIFFERENT-CONTENT", "CV-REQUEST-FIRST-RESULT-REPLAY"], {
    scope: "RELIABLE_DELIVERY_AND_RESULT_REPLAY",
    requiredOutcomes: ["RETRY_IS_IDEMPOTENT", "CONFLICTING_RETRY_REJECTED", "PENDING_RESULT_REPLAYED"],
    authorityModel: { controlServerFact: "DurableAcceptance", wireMessages: ["DurableAck", "ProtocolProblem"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["ACK_WITHOUT_DUPLICATE_EFFECT", "REPLAY_NOT_RECOMPUTE"], onboardHmi: ["RETRY_WITH_IDENTICAL_CONTENT", "ADOPT_REPLAYED_RESULT"] },
  }],
  ["FP-IS-07", 7, ["FP-IS-00"], ["CV-OPERATION-RESULT-UNKNOWN-RECONCILE", "CV-EXCEPTION-RESUME", "CV-EXCEPTION-COMPENSATE", "CV-FAULT-CARGO-HANDOFF", "CV-FORCED-MECHANICAL-RECOVERY", "CV-MANUAL-CHARGING-RETURN", "CV-SLOT-FAULT-DECLARATION-APPLIED", "CV-SLOT-FAULT-DECLARATION-NOT-APPLICABLE", "CV-RECOVERY-SESSION-CLOSED-RESULT-NOT-RECONCILED", "CV-LOAD-COMPENSATION-EMPTY-DOOR-UNPROVEN", "CV-VEHICLE-HOLD-DOOR-REPAIR-RELEASE"], {
    scope: "EXCEPTION_RECOVERY_AND_MANUAL_RETURN",
    requiredOutcomes: ["RECOVERY_SESSION_REQUIRES_VERIFIED_ADMINISTRATOR", "EVERY_RECOVERY_ACTION_AUTHORIZED", "FORCED_RECOVERY_FENCED_BY_GENERATION", "SLOT_FAULT_DECLARATION_APPLIED_ONLY_TO_AWAITING_SLOT", "FORCED_ISOLATION_ON_A_DEMAND_SETTLES_ON_A_NAMED_HANDOFF", "UNRECONCILED_SESSION_CLOSE_STATES_ITS_REASON", "EMPTY_SLOTS_SETTLE_WHILE_UNPROVEN_DOOR_HOLDS_VEHICLE", "HELD_VEHICLE_RELEASED_ONLY_BY_REPAIR_RECORD_AND_FRESH_PROOF"],
    authorityModel: { controlServerFact: "SlotFaultDeclarationAndExceptionRecoverySession", wireMessages: ["ExceptionRecoverySessionOpened", "RecoveryActionAccepted", "ForcedMechanicalRecoveryCommand", "SlotFaultDeclarationCommand", "ExceptionRecoverySessionSnapshot", "HardwareRecoveryRecordSubmitted"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY", "OPERATOR_CONFIRMATION_SOURCE"] },
    ownerResponsibilities: { controlServer: ["AUTHORIZE_EVERY_RECOVERY_ACTION", "FENCE_BY_GENERATION", "DECLARE_SLOT_FAULT_ONLY_ON_OVERDUE_SLOT", "CLOSE_UNRECONCILED_SESSION_WITH_REASON", "HOLD_VEHICLE_ON_UNPROVEN_DOOR", "RELEASE_HELD_VEHICLE_ONLY_ON_FRESH_PROOF"], onboardHmi: ["ACT_ONLY_ON_AUTHORIZED_SCOPE", "REPORT_RECOVERY_OUTCOME", "VERIFY_DECLARATION_BEFORE_ABORTING", "RECORD_FORCED_REMOVAL_HANDOFF", "REPORT_UNPROVEN_DOOR_AFTER_EMPTY", "SUBMIT_REPAIR_RECORD_WITHOUT_SLOT_IO"] },
  }],
  ["FP-IS-08", 8, ["FP-IS-04"], ["CV-MULTI-STOP-PLAN-NINE-LEGS"], {
    scope: "MULTI_STOP_JOURNEY_PLAN",
    requiredOutcomes: ["UP_TO_NINE_REMAINING_LEGS_PLANNED", "EVERY_STOP_HAS_PURPOSE_CATEGORY", "LEGS_ORDERED_BY_SEQUENCE"],
    authorityModel: { controlServerFact: "JourneyPlan", wireMessages: ["UpcomingStopPlanSnapshot"], onboardMode: ["READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["PLAN_AND_REVISE_JOURNEY"], onboardHmi: ["DISPLAY_REMAINING_JOURNEY_PLAN", "NEVER_REORDER_LEGS_LOCALLY"] },
  }],
  ["FP-IS-09", 9, ["FP-IS-08"], ["CV-WORKLIST-SELECTION-ACCEPTED", "CV-WORKLIST-SELECTION-STALE-REVISION"], {
    scope: "ONBOARD_WORKLIST_SELECTION",
    requiredOutcomes: ["SELECTION_CONFINED_TO_COMMITTED_WORKLIST", "STALE_REVISION_REJECTED"],
    authorityModel: { controlServerFact: "CommittedWorklist", wireMessages: ["CurrentStopWorklistSnapshot", "DemandSelectionRequested", "DemandSelectionResult"], onboardMode: ["SELECTION_WITHIN_COMMITTED_SET", "READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["COMMIT_THE_WORKLIST", "REJECT_STALE_SELECTION"], onboardHmi: ["SELECT_WITHIN_COMMITTED_SET", "CARRY_WORKLIST_REVISION"] },
  }],
  ["FP-IS-10", 10, ["FP-IS-01"], ["CV-TASK-TYPE-ADMISSION-FAIL-CLOSED"], {
    scope: "TASK_TYPE_ADMISSION_FAIL_CLOSED",
    requiredOutcomes: ["ONLY_BOUND_TASK_TYPES_ADMITTED", "MISSING_BINDING_FAILS_CLOSED"],
    authorityModel: { controlServerFact: "TaskTypePublicStationRuleVersion", wireMessages: ["VehicleBusinessStateSnapshot"], onboardMode: ["READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["ADMIT_ON_BINDING_ONLY", "BLOCK_ON_MISSING_BINDING"], onboardHmi: ["NEVER_INFER_UNBOUND_TASK_TYPE"] },
  }],
  ["FP-IS-11", 11, ["FP-IS-10"], ["CV-REVERSED-DIRECTION-JOURNEY"], {
    scope: "REVERSED_DIRECTION_JOURNEY",
    requiredOutcomes: ["DIRECTION_DERIVED_FROM_RULE", "ORIGIN_AND_DESTINATION_NEVER_SWAPPED"],
    authorityModel: { controlServerFact: "TaskTypePublicStationRuleVersion", wireMessages: ["UpcomingStopPlanSnapshot"], onboardMode: ["READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["DERIVE_DIRECTION_FROM_RULE"], onboardHmi: ["DISPLAY_DIRECTION_AS_PLANNED"] },
  }],
  ["FP-IS-12", 12, ["FP-IS-04"], ["CV-WAITING-POINT-IDLE-RETURN"], {
    scope: "WAITING_POINT_IDLE_RETURN",
    requiredOutcomes: ["WAITING_POINT_CLAIMED_EXCLUSIVELY", "RELEASED_ON_DEPARTURE_EVIDENCE"],
    authorityModel: { controlServerFact: "VehiclePurposeClaim", wireMessages: ["UpcomingStopPlanSnapshot", "VehicleBusinessStateSnapshot"], onboardMode: ["READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["CLAIM_AND_RELEASE_WAITING_POINT"], onboardHmi: ["TREAT_WAITING_POINT_AS_NON_BUSINESS_STOP"] },
  }],
  ["FP-IS-13", 13, ["FP-IS-12"], ["CV-AUTOMATIC-CHARGING-CYCLE", "CV-UNABLE-TO-CHARGE-FIELD-CONFIRMATION", "CV-MANUAL-STATION-CLEARANCE", "CV-MANUAL-CHARGING-RETURN", "CV-STAGING-CHARGING-REQUIRED-DEPARTURE-WITH-CARGO"], {
    scope: "AUTOMATIC_CHARGING_CYCLE_AND_CLEARANCE",
    requiredOutcomes: ["CHARGING_CLAIMS_THE_VEHICLE", "CHARGING_POLICY_DECIDED_CENTRALLY", "STATION_RELEASED_ONLY_ON_CONFIRMED_CLEARANCE", "STAGING_CARGO_DELIVERED_BEFORE_CHARGING"],
    authorityModel: { controlServerFact: "VehiclePurposeClaim", wireMessages: ["UnableToChargeFieldConfirmationRequested", "ManualStationClearanceConfirmationRequested", "VehicleBusinessStateSnapshot"], onboardMode: ["OPERATOR_CONFIRMATION_SOURCE", "READ_ONLY_COMMITTED_PROJECTION"] },
    ownerResponsibilities: { controlServer: ["DECIDE_CHARGING_POLICY", "RELEASE_STATION_ON_CONFIRMATION", "DELIVER_STAGING_CARGO_BEFORE_CHARGING"], onboardHmi: ["REPORT_FIELD_OBSERVATION_WITH_OPERATOR", "NEVER_DECIDE_POLICY_LOCALLY"] },
  }],
  ["FP-IS-14", 14, ["FP-IS-00"], ["CV-SLOT-CONFIGURATION-ACTIVATION"], {
    scope: "SLOT_CONFIGURATION_ACTIVATION",
    requiredOutcomes: ["FINGERPRINT_VERIFIED_BEFORE_ACTIVATION", "ACTIVATION_NEVER_GUESSED_SUCCESSFUL"],
    authorityModel: { controlServerFact: "SlotConfigurationVersion", wireMessages: ["SlotConfigurationActivationCommand", "SlotConfigurationActivationResult", "CapabilitySnapshot"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["ISSUE_AND_VERIFY_ACTIVATION"], onboardHmi: ["REPORT_ACTIVATION_OUTCOME_INCLUDING_UNKNOWN", "REPLAY_PENDING_RESULT"] },
  }],
  ["FP-IS-15", 15, ["FP-IS-00"], ["CV-ONBOARD-ALARM-SNAPSHOT"], {
    scope: "ONBOARD_ALARM_SNAPSHOT",
    requiredOutcomes: ["ALARM_SET_PUBLISHED_COMPLETE", "STALE_ALARM_STATE_NEVER_DISPLAYED"],
    authorityModel: { controlServerFact: "AlarmSnapshotRevision", wireMessages: ["OnboardAlarmSnapshot", "SnapshotAppliedAck"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["ADOPT_ALARM_SNAPSHOT_BY_REVISION"], onboardHmi: ["PUBLISH_COMPLETE_ALARM_SET", "NEVER_PUBLISH_STALE_ALARM_STATE"] },
  }],
].map(([integrationSliceId, sequence, prerequisites, vectorIds, definition]) => ({ integrationSliceId, sequence, prerequisites, vectorIds, gates: gateModel, definition, forbidUnclosedFailOrInconclusive: true }));
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
        required: ["integrationSliceId", "sequence", "prerequisites", "vectorIds", "gates", "definition", "forbidUnclosedFailOrInconclusive"],
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
      required: ["scope", "requiredOutcomes", "authorityModel", "ownerResponsibilities"],
      properties: {
        scope: { type: "string", pattern: "^[A-Z][A-Z0-9_]+$" },
        requiredOutcomes: { $ref: "#/$defs/tokenArray" },
        // Replaces demandRepresentation, whose three fields were all const and therefore fit
        // exactly one slice: charging, activation and alarms could not fill in any of them.
        authorityModel: {
          type: "object",
          additionalProperties: false,
          required: ["controlServerFact", "wireMessages", "onboardMode"],
          properties: {
            controlServerFact: { type: "string", pattern: "^[A-Za-z][A-Za-z0-9]+$" },
            wireMessages: { type: "array", minItems: 1, items: { type: "string", pattern: "^[A-Z][A-Za-z0-9]+$" }, uniqueItems: true },
            onboardMode: { type: "array", minItems: 1, items: { enum: onboardModes }, uniqueItems: true },
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
        required: ["ownerId", "approverKind", "decidedAt", "decision", "statement"],
        properties: {
          ownerId: { type: "string", minLength: 1 },
          approverKind: { enum: ["PRODUCT_OWNER", "AI_AGENT"] },
          authorizedBy: { type: "string", minLength: 1 },
          decidedAt: { type: "string", format: "date-time" },
          decision: { const: "APPROVED" },
          statement: { type: "string", minLength: 1 },
        },
        if: { properties: { approverKind: { const: "AI_AGENT" } }, required: ["approverKind"] },
        then: { required: ["authorizedBy"] },
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
      then: { properties: { protocolCommit: { type: "string", pattern: "^[0-9a-f]{40}$" }, contentManifestSha256: { type: "string", pattern: sha256Pattern }, approvals: { minItems: 1, maxItems: 1 } } },
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
  // One sentence per change against baseRelease. The 5.0.0 sentences (protocol#21, #23) are released history in
  // protocol-v5.0.0; 6.0.0 has the change of protocol#26 (program#210, CP-0021). The ticket that changes a shape rewrites its own sentence.
  changeSummary: [
    "RemainingBasketsSkipRequested and RemainingBasketsSkipResult, a new RELIABLE pair, let the operator ask to leave the remaining baskets of a multi-basket load and let only the control server's authorization end the load short, OperationResult gains the overallOutcome COMPLETED_REMAINING_SKIPPED and no field, LoadCancellationAuthorization authorizes only an empty scope and refuses only with a reason, the error registry appends REMAINING_BASKETS_SKIPPED, REMAINING_BASKETS_SKIP_NOTHING_LOADED and LOAD_CANCELLATION_BASKET_LOADED, the last refusing a load cancellation once a basket is loaded under the revised REQ-0211, six vectors are added, and a 5.0.0 implementation rejects the new messages and the new outcome as schema-invalid, so both implementations move to 6.0.0 together.",
  ],
  runtimeRule: "Exact ProtocolVersion and exact materialized ProtocolReleaseIdentity required; no negotiation.",
  optionalFieldPolicy: "No optional payload fields exist in this candidate. Future optional fields require proof that omission and ignore preserve safety and business conclusions.",
  historyPolicy: "Published tags, commits, manifests, schemas, vectors and approvals are immutable; defects require a superseding release.",
});
writeJson("compatibility/implementation-version-matrix.json", {
  status: "CANDIDATE",
  sharedDevelopmentBaseline: {
    dotnetSdk: "8.0.425",
    dotnetRuntime: "8.0.31",
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
  requiredAction: "Install or pin SDK 8.0.425 before reproducible product builds; do not treat the observed 8.0.29 runtime as equivalent evidence.",
});

writeText("docs/README.md", `# ${profileDisplayName} protocol candidate\n\nThis repository contains an approval-neutral **content snapshot**, not an approved ProtocolRelease. Machine-readable JSON Schema, the content manifest, the external approval attestation, errors, examples, vectors, the governance schemas and the integration-slice index are authoritative. Markdown is explanatory only; \`docs/wire-notes.md\` explains wire semantics the Schema cannot express.\n\nRun \`pnpm install --frozen-lockfile\`, \`pnpm manifest:finalize\` and \`pnpm g1\`. A PASS proves content and attestation consistency and reports their independent hashes. It does not turn a \`PENDING\` attestation into human G0 approval or prove either product implementation, G2/G3, real RIoT, real IO, target hardware or factory qualification.\n`);
// The ProtocolVersion collisions and release history named below are facts about released identities,
// so they stay literal: moving the candidate constants must not rewrite them. The 6.0.0 sentence names this
// candidate before its release; it is literal so that the next candidate keeps it as history instead of rewriting it.
writeText("docs/release-governance.md", `# Release governance\n\n- ProtocolVersion is exactly ${protocolVersion} for this candidate; runtime negotiation is forbidden.\n- ProtocolVersion is scoped to a \`profileId\`: the integer increases monotonically only within one \`profileId\`, and two profiles can carry the same integer. \`WIRE_TO_GATE_MVP\` 0.2.0 and \`AGV_FULL_PRODUCT\` 1.0.0 are both ProtocolVersion 2; \`WIRE_TO_GATE_MVP\` 0.3.0 and \`AGV_FULL_PRODUCT\` 2.0.0 are both ProtocolVersion 3. \`AGV_FULL_PRODUCT\` 3.0.0 is ProtocolVersion 4, \`AGV_FULL_PRODUCT\` 4.0.0 is ProtocolVersion 5, \`AGV_FULL_PRODUCT\` 5.0.0 is ProtocolVersion 6, and \`AGV_FULL_PRODUCT\` 6.0.0 is ProtocolVersion 7. Identity is therefore compared only as the complete \`ProtocolReleaseIdentity\`, never by the integer alone, and evidence and logs always write the pair \`(profileId, ProtocolVersion)\`.\n- \`manifest/release.json\` is an approval-neutral content snapshot. It hashes all governed protocol content except itself, \`attestations/\`, \`.git/\`, \`node_modules/\`, generated \`evidence/\` and \`.github/\`.\n- \`attestations/release-approval.template.json\` is a tracked, blank template governed by its JSON Schema and excluded from the content manifest. A completed \`release-approval.json\` must remain external to Git and be uploaded as a GitHub Release Asset. This prevents the approval record from changing either the manifest hash or the commit it approves.\n- A formal release requires exact repository, SemVer, annotated tag, full commit, ProtocolVersion, profile, content manifest hash, approval-attestation hash, schema bundle hash and vectors hash.\n- Exactly one approval of the exact commit and content manifest hash must be recorded in the attestation before an immutable tag/release is created. The approver is the product owner or, since 2026-09-12, an AI agent the product owner has authorized for that release; the attestation records which (\`approverKind\`) and, for an AI agent, who authorized it (\`authorizedBy\`). CI cannot approve.\n- This required **two** distinct product owners until 2026-09-08. The second signature was the counterpart maintainer of the onboard HMI and simulator repositories; that role ended when the project was taken over, and a rule demanding a signature nobody can give is a rule that gets worked around. \`WIRE_TO_GATE_MVP\` releases from 0.2.0 onward and every \`AGV_FULL_PRODUCT\` release carry exactly one approval. On 2026-09-12 the product owner also allowed an AI agent to approve: requiring the owner to perform every release by hand added a step without adding a decision. What still holds: CI cannot approve, and the attestation records who approved — the product owner by name, or an AI agent together with the owner who authorized it — at a stated time.\n- G1 validates the content manifest and attestation independently, verifies an approved attestation points at the current content manifest, requires exactly one approval, and reports both hashes. Candidate G1 uses the tracked blank template. Release G1 sets \`PROTOCOL_APPROVAL_ATTESTATION\` to the external completed asset. The annotated tag message and GitHub release metadata must record both reported hashes.\n- The attestation never contains its own hash. Its SHA-256 is computed from its final bytes and bound externally by the annotated tag and release metadata, avoiding another self-reference.\n- Release order is fixed: freeze and push the content commit; generate the external attestation against that commit and manifest; run G1 with \`PROTOCOL_APPROVAL_ATTESTATION\`; create annotated \`protocol-v<SemVer>\` tag pointing at the frozen content commit with both hashes in its message; then publish the same attestation as a release asset.\n- Required/type/enum/meaning/direction/delivery/dedup/persistence/recovery/error/side-effect changes are breaking and require a ProtocolVersion and release-major increase.\n- A conformance-index or trajectory correction may use a patch release only when it restores an already approved responsibility boundary, changes no message Schema or wire semantics, and the release approver approves that compatibility classification. It still changes the manifest/vector identity and invalidates affected G1/G2/G3 evidence.\n- Historical red evidence and released identities are immutable.\n`);
// Wire semantics JSON Schema cannot carry. Each section is fixed by its source (CP-0005 section 4.1,
// specification 23.5); a later description keyword on the same field must say the same thing.
writeText("docs/wire-notes.md", `# Wire notes\n\nExplanatory notes on wire semantics that JSON Schema cannot carry. Machine-readable JSON Schema, errors, examples and vectors remain authoritative: where a note and a Schema disagree, the Schema wins and the note is a defect.\n\n## Alarm code \`SLOT_EXPECTED_ACTION_OVERDUE\`\n\nSource: CP-0005 section 4.1 (REQ-0358).\n\n- \`AlarmEntry.code\` is an open set of strings, not an enum, so registering this code changes no schema.\n- The onboard HMI raises it in \`OnboardAlarmSnapshot\` when the current slot of a slot operation has waited for the operator beyond the configured threshold.\n- \`subjectType\` is \`SLOT\` and \`subjectId\` is the slot number.\n- \`raisedAt\` is the instant the wait crossed the threshold.\n- \`displayMessage\` is the action the vehicle expects.\n- The time already waited is derived from \`raisedAt\` and the threshold. \`OperationProgress\` (\`phase\` \`WAITING_OPERATOR\`, \`activeUnlockSlots\`) may help, but it is \`TELEMETRY\` and can be lost, so it is never the basis.\n- The slot readings (\`lockState\`, \`physicalState\`, \`unlockOutputState\`) are taken from \`SafetyStateSnapshot\`.\n- This alarm is the precondition of \`SlotFaultDeclarationCommand\`: an administrator can declare a fault only on a current slot that has reported it (REQ-0359).\n\n## \`SublotEntryRequested.expiresOnRevisionChange\`\n\nSource: specification 23.5.\n\n- The field stays \`const: true\`; neither its value nor its type changes.\n- ${revisionChangeDefinition}\n- Separately from expiry, a \`LOAD\` \`SlotOperationCommand\` of the same operation session answers the entry request and so ends it.\n\n## Staging pickup stops\n\nSource: CP-0012 (program#185) section 3, protocol#13; CP-0014 (program#191) section 3 item 4, protocol#17.\n\n- A staging pickup stop is a pickup stop at the fixed origin station of \`STAGING_TO_WIRE\`, the staging station. Pickup stops at machine stations keep every rule below unchanged.\n- \`CurrentStopWorklistSnapshot.stationDepartureDeadlineAt\` is always \`null\` at a staging pickup stop: the stop has no station departure deadline and no countdown.\n- At a staging pickup stop, as at a machine pickup stop, \`VehicleBusinessStateSnapshot.loadingPhase.state\` is \`LOADING\` while a demand of this stop remains to be loaded, and \`CARGO_HOLDING_WAIT\` once none remains and at least one basket is loaded. \`cargoHoldingDeadlineAt\` is \`null\` until a basket is loaded, as the program#94 table gives \`null\` before the first load batch closes safely.\n- Once a basket is loaded \`cargoHoldingDeadlineAt\` is set, counted from the safe closure of the load batch that put cargo on board, with the same duration as at a machine pickup stop. Each demand with this station as its pickup station appended to the vehicle afterwards moves it to the time of the append plus that duration; a release, a cancellation or any other worklist change does not move it. This is the one difference from a machine pickup stop, whose \`cargoHoldingDeadlineAt\` never moves once given. If the cargo is undone until no basket is loaded, the deadline returns to \`null\`, and the next loaded basket sets it afresh.\n- \`cargoHoldingDeadlineAt\` may be non-null in either state, \`LOADING\` or \`CARGO_HOLDING_WAIT\`: the onboard HMI shows the cargo-holding countdown from \`cargoHoldingDeadlineAt\` alone, never from \`state\`. A demand appended for this station opens a new stop at it, so \`state\` returns to \`LOADING\`, carrying the moved deadline, until that demand is loaded. At a machine pickup stop likewise, once the first load batch closes safely while loads committed to the stop remain, \`state\` is \`LOADING\` with \`cargoHoldingDeadlineAt\` already set (ADR-cross-0057).\n- When the cargo-holding deadline expires at a staging pickup stop, the loading phase ends as at a machine pickup stop: \`loadingPhase\` is \`CLOSED\` with \`closedReason\` \`CARGO_HOLDING_TIMEOUT\`, the loaded demands stay on the journey, and demands not yet loaded are released back to dispatch, never cancelled or suppressed and never counted against the station-timeout release limit; if an empty worklist is sent because of the release, it carries \`stopEndedReason\` \`DEMAND_RELEASED\`, as at a machine pickup stop. The expiry does not interrupt a running slot operation, load correction or cancellation; the phase ends once it settles. The vehicle leaves through the correction gate and the \`DEPARTURE\` safety check as before, with no further correction grace.\n- When a staging pickup stop ends because the operator departed or because the vehicle must charge, and demands not yet loaded are released back to dispatch, the empty worklist carries \`stopEndedReason\` \`OPERATOR_DEPARTED\` or \`CHARGING_REQUIRED\`, never \`DEMAND_RELEASED\` and never a timeout reason: those two belong to the expiry above. When every demand of the stop is loaded the vehicle leaves as before and no empty worklist is sent. A vehicle holding cargo already shows an empty worklist; if the control server sends another one after a departure, it carries \`OPERATOR_DEPARTED\`.\n\n## \`CurrentStopDepartureRequested\` and \`CurrentStopDepartureResult\`\n\nSource: CP-0012 (program#185) section 3, protocol#13; CP-0014 (program#191) section 3 item 4, protocol#17; CP-0015 (program#201) and control-server#742, protocol#23.\n\n- The control server accepts a departure request at a staging pickup stop, and at a machine pickup stop once every load committed to that stop is complete, at least one basket is loaded and the vehicle has not yet asked to leave, whether the vehicle is still in cargo-holding wait or its loading phase has already ended and only the station departure wait remains. The \`loadingPhase\` the vehicle shows does not decide this: on a journey that does not hold cargo, because every zone the vehicle serves forbids en-route appends, it still reads the last \`LOADING\` sent. The message itself is not scoped to a task type, and the request is refused elsewhere.\n- The onboard HMI journals the request before it sends it. Each press mints one \`departureRequestId\`; a resubmission of the same press, including after a restart, reuses it.\n- The request echoes the worklist the vehicle shows: its \`stationId\`, \`worklistRevision\` and \`operationSessionId\`. The control server identifies the stop by \`stationId\` and \`worklistRevision\`. \`operationSessionId\` is \`null\` when that worklist carries none, as every empty worklist does, so a vehicle holding cargo at the staging station with an empty worklist can still depart.\n- The control server answers every request with \`CurrentStopDepartureResult\`. It checks in this order and the first check that fails decides: \`STATION_MISMATCH\` when \`stationId\` is not the vehicle's current stop; \`WORKLIST_REVISION_STALE\` when \`worklistRevision\` is not the current worklist revision of that stop (\`currentWorklistRevision\` names it) and the exception for a stale revision without material change below does not apply; \`ACTION_NOT_ALLOWED_IN_STATE\` when the stop accepts no departure in its present state: a machine pickup stop whose committed loads are not all complete or that has no basket loaded, a stop that is not a pickup stop, a vehicle that has already asked to leave, a running slot operation, an open load correction or a cancellation in progress. A \`REJECTED\` result carries that \`Problem\` and changes no business state. \`ACCEPTED\` carries no \`Problem\`.\n- At a machine pickup stop, when the \`worklistRevision\` of a departure request is not the current one, the two revisions differ in nothing material only when all of the following hold: (1) the requested revision is lower than the current one, lies within the worklist revisions of the current stop itself, and the worklist of that revision has the current station as its \`stationId\`; (2) when the request carries an \`operationSessionId\`, it equals the current stop's; a \`null\` one is not compared; (3) every worklist sent for this stop, from the requested revision up to and including the current one, has empty \`items\`; (4) since the requested revision no load has settled at this stop, none of the baskets already loaded has left it (terminated or removed), and no load correction has been opened at it; when a load settled and when a correction was opened are taken at the control server's receipt. If any of them fails the answer is still \`WORKLIST_REVISION_STALE\`. If all hold, the request is decided by the remaining checks, and answered \`ACCEPTED\` when they pass. The exception does not apply at a staging pickup stop. A control server that does not record when a basket left the stop may treat every basket loaded at this stop that is no longer loaded as having left it since the requested revision, and so fail (4); that is only more conservative: the worst outcome is a \`WORKLIST_REVISION_STALE\` where an \`ACCEPTED\` was possible, and the operator presses again.\n- After \`ACCEPTED\` the departure travels in the existing snapshots. At a staging pickup stop it goes as follows. With at least one basket loaded, \`loadingPhase\` is \`CLOSED\` with \`closedReason\` \`OPERATOR_DEPARTED\`, the loaded demands stay on the journey, and the vehicle leaves through the correction gate and the \`DEPARTURE\` safety check as before. With nothing loaded the journey closes, \`loadingPhase\` is \`null\`, and the vehicle stays where it is. Either way demands not yet loaded are released back to dispatch, never cancelled or suppressed and never counted against the station-timeout release limit.\n- At a machine pickup stop accepted in \`CARGO_HOLDING_WAIT\`, the departure counts as the cargo-holding deadline expiring now: \`loadingPhase\` is \`CLOSED\` with \`closedReason\` \`OPERATOR_DEPARTED\`, not \`CARGO_HOLDING_TIMEOUT\`, so the vehicle tells a press from an expiry; the loaded demands stay on the journey, and appended stops not yet loaded are released back to dispatch as on a cargo-holding timeout, never cancelled or suppressed and never counted against the station-timeout release limit. Accepted after \`loadingPhase\` has ended, \`loadingPhase\` stays as it was, \`closedReason\` included. Either way the stop ends at once: the vehicle does not wait out the rest of the station departure deadline (\`stationDepartureDeadlineAt\`), keeps no correction grace, and leaves through the correction gate and the \`DEPARTURE\` safety check; an empty worklist sent for it carries \`stopEndedReason\` \`OPERATOR_DEPARTED\`.\n- The same \`departureRequestId\` with the same content is answered by replaying the stored result exactly as it was first decided, \`currentWorklistRevision\` included, never recomputed, and has no second effect.\n- The same \`departureRequestId\` with different content is answered with \`ProtocolProblem\` carrying \`BUSINESS_ID_CONTENT_CONFLICT\`. No \`CurrentStopDepartureResult\` is sent for it and it is not applied.\n\n## Charging required at a staging pickup stop\n\nSource: CP-0013 (program#188) section 3, protocol#15. It replaces the charging stop CP-0012 section 3 gave this candidate: the vehicle delivers its cargo first and charges afterwards. No schema changes; the Schemas already allow these values.\n\n- At a staging pickup stop with at least one basket loaded and no slot operation running, a vehicle below the mandatory charge line departs as for an accepted departure, decided by the control server and not by an operator. \`loadingPhase\` is \`CLOSED\` with \`closedReason\` \`CHARGING_REQUIRED\`, the loaded demands stay on the journey, and demands not yet loaded are released back to dispatch, never cancelled or suppressed and never counted against the station-timeout release limit. The vehicle leaves through the correction gate and the \`DEPARTURE\` safety check as before.\n- The journey goes on to its existing dropoff stops and carries no charging stop: \`UpcomingStopPlanSnapshot\` gains no \`CHARGER\` leg, \`activePurpose\` stays \`TRANSPORT\` and \`chargingCycleState\` stays \`NOT_CHARGING\` while the journey lasts. \`batteryState\` may read \`MANDATORY_CHARGE\` meanwhile; the journey is not interrupted to charge. Every departure on it is a \`PreDepartureSafetyCheck\` with \`checkPurpose\` \`DEPARTURE\`, as on any transport journey.\n- Once the journey ends the existing charging allocation takes the vehicle, as it takes any vehicle without a purpose below the mandatory charge line: \`activePurpose\` becomes \`CHARGING\`, its moves are \`NON_BUSINESS_MOVE\` checks, and \`chargingCycleState\` runs from there. The vehicle does not return to the staging station before it charges.\n- Without cargo the journey closes instead, \`loadingPhase\` is \`null\`, and the existing charging allocation takes the vehicle, so \`closedReason\` \`CHARGING_REQUIRED\` appears only with cargo on board.\n\n## \`TransportTaskType\` \`WIRE_TO_FULL_INSPECTION\`\n\nSource: the user's decisions 6 and 7 of 2026-10-16 in program#195, protocol#21.\n\n- \`WIRE_TO_FULL_INSPECTION\` is the seventh transport task type: lots go from wire bonding machines to the full-inspection area. Its destination is the area, a public station, not a machine in it. The full-inspection area is a different place from the \`WIRE_TO_GATE\` quality gate.\n- It is appended to \`TransportTaskType\`, the closed enum of \`CurrentStopWorklistSnapshot.items[].workType\`, the one message field that carries a task type. The six released values keep their order and meaning.\n- Appending a value to a closed enum is breaking (\`docs/release-governance.md\`): a 4.0.0 implementation rejects a message carrying \`WIRE_TO_FULL_INSPECTION\` as \`PROTOCOL_SCHEMA_INVALID\`, so both implementations move to 5.0.0 together, in one package, and no 4.0.0 peer is ever connected to a 5.0.0 one. The exact \`ProtocolReleaseIdentity\` check already refuses such a pair at the handshake.\n- \`PublicStationFunction\` is unchanged: it gains no \`FULL_INSPECTION\`. Specification 5.3 no longer maintains that field: the control server sends \`publicStationFunction\` as \`null\` on every leg except a staging pickup leg, where it sends \`WIRE_STAGING\` (control-server#713), and nothing sends \`FULL_INSPECTION\`. The user decided on 2026-10-16 not to add it.\n- The value is spelled exactly \`WIRE_TO_FULL_INSPECTION\`, as the MES \`TASK_TYPE\` literal; a misspelled or lowercase spelling is schema-invalid, like any value outside the enum.\n\n## \`UpcomingStopPlanSnapshot\` carries the remaining plan\n\nSource: the user's decision of 2026-10-17, CP-0015 (program#201) revision of REQ-0196, protocol#23. No schema changes.\n\n- The plan holds the vehicle's current stop and the stops after it that are not yet complete. Stops already passed are not sent, and the onboard HMI shows none. This holds for every plan except one, the clearance move below.\n- The one exception is a clearance move off a charger, the plan sent while \`activePurpose\` is \`CLEARING_MAINTENANCE\`: while the vehicle drives from the suspended charger to a waiting point, the plan keeps the \`CHARGER\` leg it left, as \`COMPLETED\`, ahead of the waiting point leg. The onboard HMI names the charger of the clearance from that leg (control-server#406), and the clearance goes on after the vehicle has left the charger. No other plan sends a stop already passed.\n- At most nine legs remain, as \`legs\` \`maxItems\` 9 has always allowed.\n\n## \`RemainingBasketsSkipRequested\` and \`RemainingBasketsSkipResult\`\n\nSource: CP-0021 (program#213) new item 1 (REQ-0367) and the revised REQ-0211 and REQ-0352, requirements-baseline-v1.20.0; protocol#26.\n\n- At a pickup stop, machine or staging alike, a \`LOAD\` slot operation of a demand whose expected basket count N is greater than 1 may end short. Once k of its target slots, 1 <= k < N, have closed safely \`OCCUPIED\` (a basket in, the door proven locked, the unlock output proven reset), the operator may ask to leave the remaining baskets, and the demand then completes with the k baskets as a normal delivery. This is not a cancellation: the demand is not terminated with \`CANCELLED_BY_OPERATOR\`, nothing is suppressed, no loaded slot is cleared, and no manual transport alarm is raised. With nothing loaded, giving the demand up is a cancellation under REQ-0211.\n- The onboard HMI never ends a load short on its own: only a \`RemainingBasketsSkipResult\` with \`outcome\` \`AUTHORIZED\` lets it. It offers the skip only while at least one target slot has closed safely \`OCCUPIED\`, at least one has not, every target door is proven locked, every unlock output is proven reset, no slot is \`UNKNOWN\` and the operation has not gone to manual recovery. Each press mints one \`skipRequestId\`; the onboard HMI journals the request before it sends it. A transport retry of the same message keeps its \`messageId\`; a resubmission of the same press, after a reconnect or a restart, is a new \`messageId\` with the same \`skipRequestId\` and the same payload. It opens no further slot while the request is pending, and it has at most one request of a demand pending. After \`REJECTED\` it goes on loading, shows why, and a later press is a new request with a new \`skipRequestId\`.\n- A pending request ends without effect, and the vehicle drops it, goes on as the operation now stands and lets the operator press again while the operation still runs, in these cases: the request is answered with \`ProtocolProblem\` (for example \`BUSINESS_ID_CONTENT_CONFLICT\`), which no \`RemainingBasketsSkipResult\` follows, so the vehicle drops the request; or the operation ends another way before an answer arrives: it has gone to manual recovery (an exception recovery session, a slot fault declaration), the station departure deadline has settled it, or an \`OperationResult\` of the attempt has been written for any other reason. Without an answer and without any of these, the request stays pending and is resent. An \`AUTHORIZED\` result that arrives after the operation has ended another way is journaled and not acted on: no slot is reported skipped because of it.\n- \`loadedSlots\` are the k target slots of \`slotOperationAttemptId\` that have closed safely \`OCCUPIED\`, at least one, so a request for k = 0 cannot be written. \`operator\` is the operator when the vehicle knows one and \`null\` otherwise; it is recorded and is never a reason to refuse.\n- The control server answers every request with \`RemainingBasketsSkipResult\`. It checks in this order and the first check that fails decides: \`DEMAND_NOT_CURRENT\` when the demand is not a demand of the vehicle's current pickup stop or \`slotOperationAttemptId\` is not its current \`LOAD\` attempt; \`OPERATION_SESSION_MISMATCH\` when \`operationSessionId\` is not the current stop's; \`ACTION_NOT_ALLOWED_IN_STATE\` when the load accepts no skip in its present state: the demand's expected basket count is 1, the attempt already has an \`OperationResult\` (the load has ended), the operation has gone to manual recovery (an exception recovery session or a slot fault declaration), a load correction or cancellation of the demand is in progress, or another skip of the attempt has been authorized, so an attempt is authorized at most once; \`SLOT_STATE_UNKNOWN\` when a target slot is \`UNKNOWN\`; \`LOCK_NOT_CLOSED\` when a target door is not proven locked; \`UNLOCK_OUTPUT_NOT_RESET\` when a target unlock output is not proven reset; \`REMAINING_BASKETS_SKIP_NOTHING_LOADED\` when by its facts no target slot has closed safely \`OCCUPIED\`; \`SLOT_SET_INVALID\` when \`loadedSlots\` are not exactly the target slots that by its facts have closed safely \`OCCUPIED\`, or name every target slot so that none remains. Its slot facts are the readings it holds from the vehicle (\`SafetyStateChanged\`, \`SafetyStateSnapshot\`); it may ask for a \`SafetyStateSnapshot\` before it decides. A \`REJECTED\` result carries that \`Problem\` and empty \`loadedSlots\`, and changes no business state.\n- \`AUTHORIZED\` carries no \`Problem\` and names in \`loadedSlots\` exactly the k slots of the request. The onboard HMI journals it, opens no further slot, ends the operation and reports \`OperationResult\` with \`overallOutcome\` \`COMPLETED_REMAINING_SKIPPED\`: every authorized slot \`COMPLETED\`, \`OCCUPIED\`, \`LOCKED\` and \`RESET\`; every other target slot of the command \`NOT_STARTED\`, \`EMPTY\`, \`LOCKED\` and \`RESET\` with \`REMAINING_BASKETS_SKIPPED\` in its \`reasonCodes\`, a slot opened earlier and closed empty included. \`REMAINING_BASKETS_SKIPPED\` appears on no other slot of any result. If the slots no longer read so when the operation ends, the vehicle reports the result as it would without the skip, \`FAILED\` or \`UNKNOWN\`.\n- To settle a \`COMPLETED_REMAINING_SKIPPED\` result the control server finds the one \`RemainingBasketsSkipResult\` with \`outcome\` \`AUTHORIZED\` it sent for the result's \`demandId\` and \`slotOperationAttemptId\`; it settles the result only when that authorization exists, its \`COMPLETED\` slots are exactly the authorization's \`loadedSlots\`, and its \`NOT_STARTED\` slots are exactly the rest of the command's target slots. It then commits the k baskets as one LoadBatch. The remaining slots and their reservation are released when the control server settles the result (REQ-0352); in the normal flow the result follows the authorization at once, so this is the same moment as the immediate release REQ-0367 asks for, and releasing at settlement rather than at authorization is the conservative reading: a slot is never offered to another demand while the vehicle may still report it. The demand goes on as a load of k baskets: its later \`UNLOAD\` \`SlotOperationCommand\` names only the k slots, with \`expectedBasketCount\` k, while its \`CurrentStopWorklistSnapshot\` item keeps the demand's \`expectedBasketCount\` N, which does not change; once unloaded the demand completes as a normal delivery. Any other skipped result -- no authorization for the demand and attempt, only a \`REJECTED\` one, or other slots -- is acknowledged with \`DurableAck\`, and the control server never settles it as completed: it stays unreconciled and the journey is blocked for recovery, as for any result that does not reconcile.\n- When an attempt with an authorization settles with any result other than \`COMPLETED_REMAINING_SKIPPED\`, the authorization is spent: the control server settles that result by the rules for it, releases slots and reservation as those rules say, and never applies the authorization afterwards.\n- A pending request never stops the control server from settling an \`OperationResult\` of the attempt that arrives first; the request is then refused with \`ACTION_NOT_ALLOWED_IN_STATE\`. A cancellation asked for while a skip is pending or authorized is refused, as every cancellation is once a basket is loaded (below).\n- The same \`skipRequestId\` with the same content is answered by replaying the stored result exactly as it was first decided, never recomputed, and has no second effect. The same \`skipRequestId\` with different content is answered with \`ProtocolProblem\` carrying \`BUSINESS_ID_CONTENT_CONFLICT\`; no \`RemainingBasketsSkipResult\` is sent for it and it is not applied.\n- The control server records each skip with N and k, when it was asked for and decided, and the operator when known, on its dashboard and in its audit (REQ-0367).\n- Under the revised REQ-0211 a load with a basket in any target slot is never cancelled. The control server checks a cancellation in the order \`SLOT_STATE_UNKNOWN\`, then \`LOAD_CANCELLATION_BASKET_LOADED\`, then \`LOCK_NOT_CLOSED\`, then \`UNLOCK_OUTPUT_NOT_RESET\`, and the first that fails decides; \`LoadCancellationAuthorization\` is then \`REJECTED\` and carries that \`Problem\`, which the Schema requires. Once loading has started a cancellation is authorized only with every target slot \`EMPTY\`, every door proven locked and every output reset, and always with empty \`slots\`, which the Schema requires of every \`AUTHORIZED\` decision: no door is opened to clear it, as \`CV-LOAD-CANCELLATION-ALL-EMPTY\` shows. \`CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN\` is kept as a defence: the path is no longer reached; should a cancellation result still report \`ALL_EMPTY_DOOR_UNPROVEN\`, this outcome is not settled as \`ALL_EMPTY\`: the demand ends as that vector sets it, as an all-empty cancellation, and the vehicle is held for repair. It goes in the next major version.\n- Upgrading: both implementations bind the exact \`ProtocolReleaseIdentity\` (\`INCOMPATIBLE_EXACT_IDENTITY_REQUIRED\`), so there is no rollout of one side first. With both outboxes drained -- no unacknowledged RELIABLE message on either side -- both services are stopped and both are replaced together.\n`);
writeText("docs/candidate-limitations.md", `# Candidate limitations and release finalization\n\nThe candidate intentionally uses structurally valid synthetic zero hashes inside envelope examples. Examples are schema fixtures, not evidence of a materialized release identity.\n\nThe manifest/approval circularity is resolved by the owner-approved governance separation recorded on 2026-08-25. \`manifest/release.json\` is an approval-neutral content snapshot and excludes \`attestations/\`; a completed external \`release-approval.json\` GitHub Release Asset binds the final immutable candidate commit and content manifest hash. The repository tracks only its blank Schema-governed template. G1 validates both artifacts and reports both hashes for the annotated tag and GitHub release metadata.\n\n**Conformance vectors are a weak binding.** No assertion executor has ever read \`input.ndjson\` or \`expected.json\`: all five were searched and every \`vectorId\` reference is a label written by a human. The \`runner/\` contracts were dropped in 1.0.0 rather than keeping a promise of an executor that does not exist. What replaces them is an architecture test in each implementation repository asserting that every \`vectorId\` has an identically named test. G2's "the vector is the criterion" is consequently a permanent weak binding: what is mechanically guaranteed is that a vector has a corresponding test, not that its bytes were executed.\n\n\`${baseReleaseTag}\` remains immutable. The current \`${candidateVersion}\` candidate is a breaking ProtocolVersion increase to ${protocolVersion} under profile \`${profileId}\`: for the remaining-baskets skip of CP-0021 (protocol#26) it adds the RELIABLE pair \`RemainingBasketsSkipRequested\` and \`RemainingBasketsSkipResult\`, \`OperationResult\` gains the outcome \`COMPLETED_REMAINING_SKIPPED\`, and \`LoadCancellationAuthorization\` authorizes only an empty scope; the identity fields move with it, and a 5.0.0 implementation refuses every 6.0.0 message because its identity and ProtocolVersion differ, so both implementations change together; the error registry appends three error codes after the 62 that 5.0.0 released, the common \`ErrorCode\` enum grows with it, \`LoadCorrectionResult\`, \`LoadCancellationResult\`, \`LoadCompensationResult\` and \`FaultCargoRecoveryResult\` refuse the new slot marker, and every other schema stays as 5.0.0 released it; six vectors are added, carried by integration slices FP-IS-02 and FP-IS-05; no negotiation or downgrade path exists. Its attestation remains \`PENDING\`; its release approval — by the product owner or an AI agent the product owner authorized — must cover the new exact commit, content manifest hash, vectors hash and breaking classification before \`protocol-v${candidateVersion}\` can be created.\n`);

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
