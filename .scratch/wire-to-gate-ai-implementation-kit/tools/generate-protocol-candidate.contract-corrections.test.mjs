// Acceptance checks for the five contract corrections of the protocol 3.0.0 candidate (8005-agv-program#150): the onboard
// assertion DISPLAY_ADMISSION_BLOCK_REASON leaves the vector and FP-IS-10, error code ONBOARD_FATAL_FAULT_LATCHED, the
// nullable stopEndedReason on CurrentStopWorklistSnapshot, the description of SublotEntryRequested.expiresOnRevisionChange,
// and CP-0009: ALL_EMPTY_DOOR_UNPROVEN, error code SLOT_DOOR_LOCK_UNPROVEN_AFTER_EMPTY, recovery action HARDWARE_REPAIR_RELEASE,
// PreDepartureSafetyCheck.checkPurpose and vectors CV-LOAD-COMPENSATION-EMPTY-DOOR-UNPROVEN,
// CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN and CV-VEHICLE-HOLD-DOOR-REPAIR-RELEASE.
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.contract-corrections.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written. Expected shapes and
// names come from the ticket, specification 5.3 and 23.5, CP-0009 and the product code read for the ticket (onboard
// w2g/fp-v2-impl@59dd545, control server fp/v2-impl@0c0edfa5), never from the generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
// protocol-v2.0.0 released 58 codes; everything after them is new in 3.0.0.
const RELEASED_CODE_COUNT = 58;
const DEFAULT_SIDE_EFFECTS = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-contract-corrections-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative) => fs.readFileSync(path.join(tree, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const schemaOf = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`);
const payloadSchemaOf = (messageType) => schemaOf(messageType).properties.payload;
const validOf = (messageType) => readJson(`examples/valid/${messageType}/V-${messageType}-MIN-001.json`);
const expectedOf = (vectorId) => readJson(`vectors/${vectorId}/expected.json`);
const sliceOf = (sliceId) => readJson("integration-slices/index.json").slices.find((item) => item.integrationSliceId === sliceId);
const codeOf = (code) => {
  const codes = readJson("errors/error-codes.json").codes;
  const index = codes.findIndex((entry) => entry.code === code);
  return { index, entry: codes[index] };
};

// The subset of JSON Schema 2020-12 the generated message schemas use, as in the recovery-closure test, plus description,
// which is an annotation and constrains nothing. A keyword outside the subset throws rather than being skipped. format is
// not checked (G1 runs ajv-formats), so no test here rests on a malformed date-time or uuid.
const KNOWN_KEYWORDS = new Set(["$ref", "type", "const", "enum", "required", "properties", "additionalProperties", "anyOf", "allOf", "if", "then", "else", "minLength", "pattern", "minimum", "maximum", "items", "minItems", "maxItems", "uniqueItems", "format", "examples", "description", "x-sortedAscending", "x-sortedBy"]);
let commonDefs;
const resolve = (schema) => {
  if (!schema.$ref) return schema;
  commonDefs ??= readJson("schemas/common/types.schema.json").$defs;
  const target = commonDefs[schema.$ref.split("/").at(-1)];
  assert.ok(target, `unresolved ${schema.$ref}`);
  return target;
};
const typeOf = (value) => (value === null ? "null" : Array.isArray(value) ? "array" : Number.isInteger(value) ? "integer" : typeof value);
const typeMatches = (expected, value) => expected === typeOf(value) || (expected === "number" && typeOf(value) === "integer");
const valid = (rawSchema, value) => {
  const schema = resolve(rawSchema);
  const unknown = Object.keys(schema).filter((keyword) => !KNOWN_KEYWORDS.has(keyword));
  if (unknown.length) throw new Error(`the test validator does not implement ${unknown.join(", ")}`);
  if (schema.type !== undefined && !typeMatches(schema.type, value)) return false;
  if ("const" in schema && JSON.stringify(schema.const) !== JSON.stringify(value)) return false;
  if (schema.enum && !schema.enum.includes(value)) return false;
  if (typeof value === "string") {
    if (schema.minLength !== undefined && value.length < schema.minLength) return false;
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) return false;
  }
  if (typeof value === "number") {
    if (schema.minimum !== undefined && value < schema.minimum) return false;
    if (schema.maximum !== undefined && value > schema.maximum) return false;
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) return false;
    if (schema.maxItems !== undefined && value.length > schema.maxItems) return false;
    if (schema.uniqueItems && new Set(value.map((item) => JSON.stringify(item))).size !== value.length) return false;
    if (schema.items && !value.every((item) => valid(schema.items, item))) return false;
  }
  if (typeOf(value) === "object") {
    if (schema.required && !schema.required.every((key) => key in value)) return false;
    for (const [key, child] of Object.entries(value)) {
      if (schema.properties?.[key]) { if (!valid(schema.properties[key], child)) return false; }
      else if (schema.additionalProperties === false) return false;
    }
  }
  if (schema.anyOf && !schema.anyOf.some((option) => valid(option, value))) return false;
  if (schema.allOf && !schema.allOf.every((option) => valid(option, value))) return false;
  if (schema.if) {
    const branch = valid(schema.if, value) ? schema.then : schema.else;
    if (branch && !valid(branch, value)) return false;
  }
  return true;
};
const accepts = (messageType, payload) => valid(payloadSchemaOf(messageType), payload);
const stripConditionals = (schema) => JSON.parse(JSON.stringify(schema, (key, value) => (["if", "then", "else"].includes(key) ? undefined : value)));

// --- item 1: the admission block reason stays on the control server (specification 5.3, program#125) ---

const ADMISSION_VECTOR = "CV-TASK-TYPE-ADMISSION-FAIL-CLOSED";

test(`${ADMISSION_VECTOR} keeps only NEVER_INFER_UNBOUND_TASK_TYPE on the vehicle and its server side verbatim`, () => {
  const { productAssertions } = expectedOf(ADMISSION_VECTOR);
  assert.deepEqual(productAssertions.onboardHmi, ["NEVER_INFER_UNBOUND_TASK_TYPE"]);
  // Deleted, not moved: no dashboard assertion is added to the server side (the ticket's decision).
  assert.deepEqual(productAssertions.controlServer, ["ADMIT_ONLY_BOUND_TASK_TYPES", "FAIL_CLOSED_ON_MISSING_BINDING"]);
});

test("FP-IS-10 keeps only NEVER_INFER_UNBOUND_TASK_TYPE on the vehicle and its server side verbatim", () => {
  const { ownerResponsibilities } = sliceOf("FP-IS-10").definition;
  assert.deepEqual(ownerResponsibilities.onboardHmi, ["NEVER_INFER_UNBOUND_TASK_TYPE"]);
  assert.deepEqual(ownerResponsibilities.controlServer, ["ADMIT_ON_BINDING_ONLY", "BLOCK_ON_MISSING_BINDING"]);
});

test("no vector or slice names DISPLAY_ADMISSION_BLOCK_REASON any more", () => {
  const vectorHits = fs.readdirSync(path.join(tree, "vectors")).filter((id) => read(`vectors/${id}/expected.json`).includes("DISPLAY_ADMISSION_BLOCK_REASON"));
  assert.deepEqual(vectorHits, []);
  assert.doesNotMatch(read("integration-slices/index.json"), /DISPLAY_ADMISSION_BLOCK_REASON/);
});

// --- item 2: the onboard fatal-fault latch gets its own code ---

const LATCH = "ONBOARD_FATAL_FAULT_LATCHED";
// Where the onboard HMI writes the latch today (w2g/fp-v2-impl@59dd545):
// - WireToGateSafetyEvaluator.FatalFaultLatchedReason goes into SafetySummary.reasonCodes, which travels in the three
//   safety messages (onboard-hmi#197);
// - WireToGateSlotOperationExecutor.SettleRefusedByLatchAsync puts it on the refused slot's SlotResult in OperationResult
//   (onboard-hmi#191), for a SlotOperationCommand and a SlotOperationResumeCommand alike;
// - WireToGateRecoveryVectorExecutor.ExecuteExclusiveAsync, shared by correction and clearing, puts it on the refused
//   slot's SlotResult, which SendRecoveryVectorResultAsync sends as LoadCancellationResult, LoadCompensationResult,
//   LoadCorrectionResult or FaultCargoRecoveryResult.
const LATCH_MESSAGES = ["SafetyStateChanged", "SafetyStateSnapshot", "PreDepartureSafetyCheckResult", "OperationResult", "LoadCorrectionResult", "LoadCancellationResult", "LoadCompensationResult", "FaultCargoRecoveryResult"];

test(`${LATCH} is appended after the 2.0.0 codes, introduced in 3.0.0 and allowed where the vehicle writes the latch`, () => {
  const { index, entry } = codeOf(LATCH);
  assert.ok(index >= RELEASED_CODE_COUNT, `${LATCH} at ${index}`);
  assert.equal(entry.introducedInRelease, "3.0.0");
  assert.deepEqual(entry.allowedMessageTypes, LATCH_MESSAGES);
  assert.equal(entry.category, "SAFETY_RECOVERY");
  // Only a person lifts the latch, after reviewing it.
  assert.equal(entry.retryDisposition, "MANUAL_REVIEW");
  assert.ok(readJson("schemas/common/types.schema.json").$defs.ErrorCode.enum.includes(LATCH));
});

test(`${LATCH} says what it is and how it differs from the two codes the latch borrowed`, () => {
  const { meaning } = codeOf(LATCH).entry;
  assert.match(meaning, /^The onboard HMI has latched a fatal safety fault/);
  assert.match(meaning, /until a person reviews and resets the latch/);
  assert.match(meaning, /not VEHICLE_NOT_READY/);
  assert.match(meaning, /not a vehicle that has not come to a stop/);
  assert.match(meaning, /not an unsafe state caused by the slot operation/);
});

test(`${LATCH} passes the closed ErrorCode enum in a safety summary and on a refused slot`, () => {
  const safetyChanged = validOf("SafetyStateChanged").payload;
  assert.equal(accepts("SafetyStateChanged", { ...safetyChanged, safety: { ...safetyChanged.safety, departureSafe: false, reasonCodes: [LATCH] } }), true);
  const result = validOf("OperationResult").payload;
  const refused = { ...result.slotResults[0], outcome: "FAILED", reasonCodes: [LATCH] };
  assert.equal(accepts("OperationResult", { ...result, overallOutcome: "FAILED", slotResults: [refused] }), true);
  assert.equal(accepts("OperationResult", { ...result, overallOutcome: "FAILED", slotResults: [{ ...refused, reasonCodes: ["ONBOARD_FATAL_FAULT_LATCHED_TYPO"] }] }), false);
});

// --- item 3: why the current stop ended ---

const WORKLIST = "CurrentStopWorklistSnapshot";
const REASON = "stopEndedReason";
// One operator-facing reason per way the control server sends an empty worklist (fp/v2-impl@0c0edfa5): JourneyClosure
// and StopEndWorklist are the only two places that build one, and every caller of either names why the stop ended.
const STOP_END_REASONS = ["COMPLETED", "STATION_DEADLINE_EXPIRED", "LOAD_CANCELLED", "LOAD_COMPENSATED", "CARGO_HANDED_OFF", "DEMAND_RELEASED", "TRIP_TERMINATED"];
// The worklist item protocol-v2.0.0 released; G1 compares its required list verbatim (FP-IS-01 worklist Demand representation).
const V2_ITEM_FIELDS = ["demandId", "transportDemandKey", "sublot", "workType", "stopRole", "expectedBasketCount"];
const worklist = (items, reason) => ({ ...validOf(WORKLIST).payload, items, [REASON]: reason });
const oneItem = () => validOf(WORKLIST).payload.items;

test(`${WORKLIST} adds a required nullable ${REASON} after items and leaves the item shape of 2.0.0 alone`, () => {
  const payload = payloadSchemaOf(WORKLIST);
  assert.deepEqual(payload.required, ["stationId", "worklistRevision", "operationSessionId", "stationDepartureDeadlineAt", "items", REASON]);
  assert.deepEqual(Object.keys(payload.properties), payload.required);
  assert.equal(payload.additionalProperties, false);
  assert.deepEqual(payload.properties[REASON], { anyOf: [{ type: "string", enum: STOP_END_REASONS }, { type: "null" }] });
  const items = payload.properties.items;
  assert.equal(items.maxItems, 8);
  assert.equal(items.minItems, undefined, "items gained a lower bound");
  assert.deepEqual(items.items.required, V2_ITEM_FIELDS);
  assert.deepEqual(Object.keys(items.items.properties), V2_ITEM_FIELDS);
});

test(`${REASON} is null while the worklist has items and names a reason once it is empty`, () => {
  assert.equal(accepts(WORKLIST, worklist(oneItem(), null)), true, "items without a reason");
  for (const reason of STOP_END_REASONS) {
    assert.equal(accepts(WORKLIST, worklist(oneItem(), reason)), false, `items with ${reason}`);
    assert.equal(accepts(WORKLIST, worklist([], reason)), true, `empty with ${reason}`);
  }
  assert.equal(accepts(WORKLIST, worklist([], null)), false, "empty without a reason");
  assert.equal(accepts(WORKLIST, worklist([], "NOT_A_STOP_END_REASON")), false, "empty with an unknown reason");
});

test(`the minimal valid ${WORKLIST} satisfies its own schema, conditionals included`, () => {
  const payload = validOf(WORKLIST).payload;
  assert.ok(REASON in payload, `the example lacks ${REASON}`);
  assert.ok(accepts(WORKLIST, payload), `valid example violates its schema: ${JSON.stringify(payload)}`);
});

const worklistNegatives = {
  "IF-THEN-stopEndedReason-ITEMS": (payload) => payload.items.length > 0 && payload[REASON] !== null,
  "IF-THEN-stopEndedReason-EMPTY": (payload) => payload.items.length === 0 && payload[REASON] === null,
};
for (const [suffix, breaks] of Object.entries(worklistNegatives)) {
  test(`if-then negative ${suffix} breaks only the reason correspondence and is rejected by the conditional`, () => {
    const negative = readJson(`examples/invalid/${WORKLIST}/I-${WORKLIST}-${suffix}.json`);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: `/payload/${REASON}`, rule: "if-then" });
    const payload = negative.message.payload;
    assert.ok(breaks(payload), `does not break ${suffix}: ${JSON.stringify({ items: payload.items.length, reason: payload[REASON] })}`);
    assert.equal(accepts(WORKLIST, payload), false, "the schema accepts it");
    assert.equal(valid(stripConditionals(payloadSchemaOf(WORKLIST)), payload), true, "rejected for something other than the conditional");
  });
}

// --- item 4: expiresOnRevisionChange says what a revision change is (specification 23.5) ---

test("expiresOnRevisionChange keeps boolean const true and describes a revision change with both qualifiers of 23.5", () => {
  const field = payloadSchemaOf("SublotEntryRequested").properties.expiresOnRevisionChange;
  assert.deepEqual(Object.keys(field).sort(), ["const", "description", "type"]);
  assert.equal(field.type, "boolean");
  assert.equal(field.const, true);
  assert.match(field.description, /the stop ended/);
  assert.match(field.description, /the operation session or the station changed \(a worklist for another operation session or station with a strictly higher revision\)/);
  assert.match(field.description, /the worklist became empty \(a worklist no older than the entry request with empty `items`\)/);
  assert.match(field.description, /rejected the submission with `WORKLIST_REVISION_STALE`/);
  assert.match(field.description, /A worklist revision advancing within the same operation session at the same station is not a revision change/);
});

test("the wire notes carry the same definition as the schema description, word for word", () => {
  const field = payloadSchemaOf("SublotEntryRequested").properties.expiresOnRevisionChange;
  assert.ok(read("docs/wire-notes.md").includes(field.description), "the wire notes and the description differ");
});

// --- item 5: CP-0009, light curtain proves the slots empty, the door is not proven locked ---

const DOOR_UNPROVEN = "ALL_EMPTY_DOOR_UNPROVEN";
const DOOR_CODE = "SLOT_DOOR_LOCK_UNPROVEN_AFTER_EMPTY";
const DOOR_VECTOR = "CV-LOAD-COMPENSATION-EMPTY-DOOR-UNPROVEN";
const CANCEL_VECTOR = "CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN";
const RELEASE_VECTOR = "CV-VEHICLE-HOLD-DOOR-REPAIR-RELEASE";
// Shared by the two clearing vectors: the same settlement rule, the same hold, the same single way out.
const DOOR_SIDE_EFFECTS = [...DEFAULT_SIDE_EFFECTS, "door-unproven-reported-as-all-empty", "slot-opened-after-door-unproven", "door-unproven-settles-with-a-slot-not-proven-empty", "vehicle-released-without-fresh-lock-proof", "demand-left-blocked-after-door-unproven-empty", "vehicle-held-without-a-repair-release-path"];
// The demand settles the way an all-empty clearing does (SETTLE_DEMAND_AS_ALL_EMPTY_*); the doors do not count as proven locked
// and the vehicle does not become ready (NEVER_TAKE_DOOR_UNPROVEN_FOR_DOORS_PROVEN_LOCKED). Two different things, two names.
const DOOR_SERVER = (settle) => [settle, "SETTLE_DOOR_UNPROVEN_ONLY_ON_THE_EXACT_TARGET_SLOTS_ALL_EMPTY", "HOLD_VEHICLE_UNTIL_HARDWARE_RECORD_AND_FRESH_LOCK_PROOF", "PUBLISH_HOLD_IN_VEHICLE_BUSINESS_STATE", "NEVER_RELEASE_ON_HARDWARE_RECORD_ALONE", "RELEASE_ONLY_THROUGH_HARDWARE_REPAIR_RELEASE", "NEVER_TAKE_DOOR_UNPROVEN_FOR_DOORS_PROVEN_LOCKED"];
// Every new vector keeps the four default persistence checkpoints: the vehicle journals before it sends and before any
// irreversible IO, the control server persists before it acknowledges, and a result is on file before it is replayed.
const DEFAULT_CHECKPOINTS = ["durable-before-send", "durable-before-ack", "journal-before-irreversible-io", "result-before-replay"];
const DOOR_ONBOARD = ["REPORT_LOCK_AND_OUTPUT_STATE_AS_READ", "NEVER_OPEN_ANY_SLOT_AFTER_DOOR_UNPROVEN", "DISPLAY_REPAIR_REQUIRED_NOTICE", "JOURNAL_DOOR_UNPROVEN_RESULT_BEFORE_SENDING", "REPLAY_SAME_DOOR_UNPROVEN_RESULT_AFTER_RESTART"];
const HELD_FINAL_STATE = { readiness: "RECOVERY_REQUIRED", business: "DEMAND_TERMINATED_AS_ALL_EMPTY_VEHICLE_HELD_FOR_REPAIR", physical: "SLOTS_EMPTY_DOOR_UNPROVEN_VEHICLE_HELD" };
// After the result is acknowledged the control server publishes the hold outside any journey, so the vehicle can show it.
const HOLD_PUBLISHED = ["VehicleBusinessStateSnapshot", "SnapshotAppliedAck"];
const unprovenSlot = (slotNo) => ({ slotNo, outcome: "COMPLETED", finalPhysicalState: "EMPTY", lockState: "UNKNOWN", unlockOutputState: "RESET", reasonCodes: [DOOR_CODE] });

for (const message of ["LoadCancellationResult", "LoadCompensationResult"]) {
  test(`${message}.overallOutcome gains exactly ${DOOR_UNPROVEN} after its three released values`, () => {
    assert.deepEqual(payloadSchemaOf(message).properties.overallOutcome, { type: "string", enum: ["ALL_EMPTY", "FAILED", "UNKNOWN", DOOR_UNPROVEN] });
  });

  test(`a ${message} with ${DOOR_UNPROVEN}, an EMPTY slot with an unproven lock and the new code satisfies the schema`, () => {
    const base = validOf(message).payload;
    assert.equal(accepts(message, { ...base, overallOutcome: DOOR_UNPROVEN, slotResults: [unprovenSlot(3)] }), true);
    assert.equal(accepts(message, { ...base, overallOutcome: "ALL_EMPTY_DOOR_UNKNOWN", slotResults: [unprovenSlot(3)] }), false);
  });

  test(`${message} with ${DOOR_UNPROVEN} carries at least one slot and every slot EMPTY, and ALL_EMPTY is not narrowed`, () => {
    const base = validOf(message).payload;
    const occupied = { ...unprovenSlot(4), finalPhysicalState: "OCCUPIED", reasonCodes: [] };
    assert.equal(accepts(message, { ...base, overallOutcome: DOOR_UNPROVEN, slotResults: [] }), false, "no slot");
    assert.equal(accepts(message, { ...base, overallOutcome: DOOR_UNPROVEN, slotResults: [unprovenSlot(3), occupied] }), false, "an occupied slot");
    assert.equal(accepts(message, { ...base, overallOutcome: DOOR_UNPROVEN, slotResults: [unprovenSlot(3), { ...occupied, finalPhysicalState: "UNKNOWN" }] }), false, "an unknown slot");
    // The released values keep exactly the constraints 2.0.0 gave them.
    assert.equal(accepts(message, { ...base, overallOutcome: "FAILED", slotResults: [occupied] }), true, "FAILED with an occupied slot");
  });
}

const doorResultNegatives = {
  LoadCancellationResult: ["IF-THEN-slotResults-ALL_EMPTY_DOOR_UNPROVEN-NO_SLOT", "IF-THEN-slotResults-ALL_EMPTY_DOOR_UNPROVEN-OCCUPIED"],
  // A compensation result already needs one slot, so only the occupied slot is the conditional's own negative.
  LoadCompensationResult: ["IF-THEN-slotResults-ALL_EMPTY_DOOR_UNPROVEN-OCCUPIED"],
};
for (const [message, suffixes] of Object.entries(doorResultNegatives)) {
  for (const suffix of suffixes) {
    test(`if-then negative ${message} ${suffix} is rejected by the conditional alone`, () => {
      const negative = readJson(`examples/invalid/${message}/I-${message}-${suffix}.json`);
      assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/slotResults", rule: "if-then" });
      const payload = negative.message.payload;
      assert.equal(payload.overallOutcome, DOOR_UNPROVEN);
      if (suffix.endsWith("NO_SLOT")) assert.deepEqual(payload.slotResults, []);
      else assert.ok(payload.slotResults.some((slot) => slot.finalPhysicalState !== "EMPTY"));
      assert.equal(accepts(message, payload), false, "the schema accepts it");
      assert.equal(valid(stripConditionals(payloadSchemaOf(message)), payload), true, "rejected for something other than the conditional");
    });
  }
}

test(`${DOOR_CODE} is appended after the 2.0.0 codes, introduced in 3.0.0 and allowed on the two clearing results and the hold`, () => {
  const { index, entry } = codeOf(DOOR_CODE);
  assert.ok(index >= RELEASED_CODE_COUNT, `${DOOR_CODE} at ${index}`);
  assert.equal(entry.introducedInRelease, "3.0.0");
  // The slot's result, and the vehicle's blocking facts for as long as the hold lasts.
  assert.deepEqual(entry.allowedMessageTypes, ["LoadCancellationResult", "LoadCompensationResult", "VehicleBusinessStateSnapshot"]);
  assert.equal(entry.category, "SAFETY_RECOVERY");
  assert.equal(entry.retryDisposition, "MANUAL_REVIEW");
  assert.ok(readJson("schemas/common/types.schema.json").$defs.ErrorCode.enum.includes(DOOR_CODE));
});

test(`${DOOR_CODE} says the cargo settles as empty, the door proof moves to the vehicle's release and ALL_EMPTY keeps its meaning`, () => {
  const { meaning } = codeOf(DOOR_CODE).entry;
  assert.match(meaning, /light curtain reads EMPTY/);
  assert.match(meaning, /cannot prove the door locked or the unlock output reset/);
  assert.match(meaning, /cargo business settles the slot as empty/);
  assert.match(meaning, /overallOutcome ALL_EMPTY_DOOR_UNPROVEN, never ALL_EMPTY, which still means every slot EMPTY, LOCKED and RESET/);
  assert.match(meaning, /no further slot is opened/);
  assert.match(meaning, /a HardwareRecoveryRecord on a HARDWARE_REPAIR_RELEASE recovery action/);
  assert.match(meaning, /LOCKED, RESET and EMPTY readings of the slot that the control server receives after the record/);
  assert.match(meaning, /a SAFE PreDepartureSafetyCheck with checkPurpose HOLD_RELEASE/);
  assert.match(meaning, /blockingFacts of VehicleBusinessStateSnapshot for as long as the vehicle is held/);
  assert.match(meaning, /whether a cancellation or a compensation left it held/);
  assert.match(meaning, /REQ-0364, CP-0009/);
});

test(`a VehicleBusinessStateSnapshot names the held slot with ${DOOR_CODE} in its blocking facts`, () => {
  const base = validOf("VehicleBusinessStateSnapshot").payload;
  const held = { reasonCode: DOOR_CODE, subjectType: "SLOT", subjectId: "3" };
  assert.equal(accepts("VehicleBusinessStateSnapshot", { ...base, readiness: "RECOVERY_REQUIRED", blockingFacts: [held] }), true);
});

// --- the release: one way out of the hold for both clearing paths ---

const RELEASE = "HARDWARE_REPAIR_RELEASE";
const ACTIONS = ["RESUME_AFTER_REPAIR", "COMPENSATE_LOAD_ALL_EMPTY", "FAULT_CARGO_HANDOFF", "FORCED_MECHANICAL_RECOVERY", RELEASE];
const actionSites = [
  ["RecoveryActionSubmitted", (payload) => payload.properties.action],
  ["RecoveryActionAccepted", (payload) => payload.properties.acceptedAction],
  ["ExceptionRecoverySessionSnapshot", (payload) => payload.properties.selectedAction.anyOf[0]],
  ["ExceptionRecoverySessionSnapshot", (payload) => payload.properties.allowedActions.items],
];

test(`the recovery action enum gains ${RELEASE} after its four released values, the same in all four places`, () => {
  for (const [message, site] of actionSites) assert.deepEqual(site(payloadSchemaOf(message)), { type: "string", enum: ACTIONS }, message);
});

test(`${RELEASE} is a recovery action a session may offer, select and accept`, () => {
  const snapshot = validOf("ExceptionRecoverySessionSnapshot").payload;
  assert.equal(accepts("ExceptionRecoverySessionSnapshot", { ...snapshot, state: "OPEN", demandId: null, allowedActions: [RELEASE], selectedAction: null }), true);
  assert.equal(accepts("ExceptionRecoverySessionSnapshot", { ...snapshot, state: "ACTION_SELECTED", demandId: null, allowedActions: [], selectedAction: RELEASE }), true);
  const submitted = validOf("RecoveryActionSubmitted").payload;
  assert.equal(accepts("RecoveryActionSubmitted", { ...submitted, action: RELEASE, demandId: null }), true);
  const acceptedAction = validOf("RecoveryActionAccepted").payload;
  assert.equal(accepts("RecoveryActionAccepted", { ...acceptedAction, acceptedAction: RELEASE, slotOperationAttemptId: null }), true);
});

// The release reuses the hardware recovery record exactly as 2.0.0 released it: both messages are pinned whole, so a field made
// nullable or dropped on either side turns this red.
const TYPES = "https://schemas.8005-agv.local/agv-full-product/v4/common/types.schema.json#/$defs/";
const ref = (name) => ({ $ref: `${TYPES}${name}` });
const nonEmptyStrings = { type: "array", items: { type: "string", minLength: 1 }, minItems: 1 };

test("HardwareRecoveryRecordSubmitted keeps its released shape: both ids required and non-null", () => {
  assert.deepEqual(payloadSchemaOf("HardwareRecoveryRecordSubmitted"), {
    type: "object",
    properties: {
      recordId: ref("Id"),
      exceptionRecoverySessionId: ref("Id"),
      recoveryActionId: ref("Id"),
      operator: ref("OperatorContext"),
      administratorRole: { type: "string", enum: ["MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"] },
      slots: { type: "array", items: ref("SlotNo"), minItems: 1, maxItems: 8, uniqueItems: true, "x-sortedAscending": true },
      checksPerformed: { ...nonEmptyStrings, uniqueItems: true },
      actionsPerformed: { ...nonEmptyStrings, uniqueItems: true },
      observations: nonEmptyStrings,
      observedAt: ref("Instant"),
    },
    required: ["recordId", "exceptionRecoverySessionId", "recoveryActionId", "operator", "administratorRole", "slots", "checksPerformed", "actionsPerformed", "observations", "observedAt"],
    additionalProperties: false,
  });
});

test("HardwareRecoveryRecordResult keeps its released shape: a real session revision, never null", () => {
  const payload = payloadSchemaOf("HardwareRecoveryRecordResult");
  assert.deepEqual(payload, {
    type: "object",
    properties: {
      recordId: ref("Id"),
      outcome: { type: "string", enum: ["RECORDED", "REJECTED"] },
      problem: { anyOf: [ref("Problem"), { type: "null" }] },
      recoverySessionRevision: ref("Revision"),
    },
    required: ["recordId", "outcome", "problem", "recoverySessionRevision"],
    additionalProperties: false,
  });
});

// --- PreDepartureSafetyCheck: a check with or without a demand (ADR-cross-0009, REQ-0364) ---
// ADR-cross-0009 requires a fresh check before every movement request, not only a business one, and REQ-0364 requires a passed
// check before a held vehicle takes work again. Neither an idle return or charging move nor a hold release has a demand, and a
// hold release has no movement leg or target station either.

const CHECK = "PreDepartureSafetyCheck";
const CHECK_RESULT = "PreDepartureSafetyCheckResult";
const PURPOSES = ["DEPARTURE", "NON_BUSINESS_MOVE", "HOLD_RELEASE"];
const CHECK_SCOPE = ["demandId", "movementLegId", "targetStationId"];
// Which of the three a purpose carries: true non-null, false null.
const PURPOSE_SHAPE = {
  DEPARTURE: { demandId: true, movementLegId: true, targetStationId: true },
  NON_BUSINESS_MOVE: { demandId: false, movementLegId: true, targetStationId: true },
  HOLD_RELEASE: { demandId: false, movementLegId: false, targetStationId: false },
};
const scopeValues = { demandId: "00000000-0000-4000-8000-0000000000d1", movementLegId: "00000000-0000-4000-8000-0000000000e1", targetStationId: "STATION-042" };
const check = (checkPurpose, present) => ({ ...validOf(CHECK).payload, checkPurpose, ...Object.fromEntries(CHECK_SCOPE.map((key) => [key, present[key] ? scopeValues[key] : null])) });

test(`${CHECK} gains a required checkPurpose and its demand, leg and station become nullable`, () => {
  const payload = payloadSchemaOf(CHECK);
  assert.deepEqual(payload.required, ["preDepartureSafetyCheckId", "checkPurpose", "demandId", "movementLegId", "expectedSafetyStateVersion", "targetStationId"]);
  assert.deepEqual(Object.keys(payload.properties), payload.required);
  assert.deepEqual(payload.properties.checkPurpose, { type: "string", enum: PURPOSES });
  for (const key of CHECK_SCOPE) assert.deepEqual(payload.properties[key].anyOf?.[1], { type: "null" }, key);
  assert.match(payload.properties.demandId.anyOf[0].$ref, /\$defs\/Id$/);
  assert.match(payload.properties.movementLegId.anyOf[0].$ref, /\$defs\/Id$/);
  assert.deepEqual(payload.properties.targetStationId.anyOf[0], { type: "string", minLength: 1 });
});

test(`${CHECK_RESULT} echoes a required checkPurpose after the check id`, () => {
  const payload = payloadSchemaOf(CHECK_RESULT);
  assert.deepEqual(payload.required.slice(0, 2), ["preDepartureSafetyCheckId", "checkPurpose"]);
  assert.deepEqual(payload.properties.checkPurpose, { type: "string", enum: PURPOSES });
  assert.equal(accepts(CHECK_RESULT, { ...validOf(CHECK_RESULT).payload, checkPurpose: "HOLD_RELEASE" }), true);
});

test(`each checkPurpose accepts exactly its own shape of demand, leg and station`, () => {
  const shapes = [];
  for (const demandId of [true, false]) for (const movementLegId of [true, false]) for (const targetStationId of [true, false]) shapes.push({ demandId, movementLegId, targetStationId });
  for (const purpose of PURPOSES) {
    for (const shape of shapes) {
      const expected = CHECK_SCOPE.every((key) => shape[key] === PURPOSE_SHAPE[purpose][key]);
      assert.equal(accepts(CHECK, check(purpose, shape)), expected, `${purpose} ${JSON.stringify(shape)}`);
    }
  }
});

test(`the minimal valid ${CHECK} is a DEPARTURE check and satisfies its own schema, conditionals included`, () => {
  const payload = validOf(CHECK).payload;
  assert.equal(payload.checkPurpose, "DEPARTURE");
  assert.ok(accepts(CHECK, payload), `valid example violates its schema: ${JSON.stringify(payload)}`);
});

const checkNegatives = [];
for (const purpose of PURPOSES) for (const key of CHECK_SCOPE) checkNegatives.push([purpose, key]);
for (const [purpose, key] of checkNegatives) {
  test(`if-then negative ${CHECK} ${purpose}-${key} breaks only that field's rule for the purpose`, () => {
    const suffix = `IF-THEN-${key}-${purpose}`;
    const negative = readJson(`examples/invalid/${CHECK}/I-${CHECK}-${suffix}.json`);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: `/payload/${key}`, rule: "if-then" });
    const payload = negative.message.payload;
    assert.equal(payload.checkPurpose, purpose);
    for (const other of CHECK_SCOPE) {
      const wantPresent = other === key ? !PURPOSE_SHAPE[purpose][other] : PURPOSE_SHAPE[purpose][other];
      assert.equal(payload[other] !== null, wantPresent, `${other} in ${suffix}`);
    }
    assert.equal(accepts(CHECK, payload), false, "the schema accepts it");
    assert.equal(valid(stripConditionals(payloadSchemaOf(CHECK)), payload), true, "rejected for something other than the conditional");
  });
}

// --- the vectors ---

test(`${DOOR_VECTOR} runs the compensation of CV-EXCEPTION-COMPENSATE, acknowledges the result and publishes the hold`, () => {
  const expected = expectedOf(DOOR_VECTOR);
  const compensate = expectedOf("CV-EXCEPTION-COMPENSATE").orderedExpectedMessages;
  // Every RELIABLE message the vehicle sends gets its own DurableAck.
  assert.deepEqual(expected.orderedExpectedMessages, [...compensate, "DurableAck", ...HOLD_PUBLISHED]);
  assert.equal(compensate.at(-1), "LoadCompensationResult");
  assert.equal(expected.stableErrorCode, DOOR_CODE);
  assert.notEqual(expected.finalState.physical, "NO_UNPROVEN_STATE");
  assert.deepEqual(expected.finalState, HELD_FINAL_STATE);
});

test(`${DOOR_VECTOR} states the product assertions of both sides and a way out that needs no database edit`, () => {
  const expected = expectedOf(DOOR_VECTOR);
  assert.deepEqual(expected.productAssertions, { controlServer: DOOR_SERVER("SETTLE_DEMAND_AS_ALL_EMPTY_COMPENSATION"), onboardHmi: DOOR_ONBOARD });
  assert.deepEqual(expected.forbiddenSideEffects, DOOR_SIDE_EFFECTS);
});

test(`${CANCEL_VECTOR} runs CV-LOAD-CANCELLATION-ALL-EMPTY to a door-unproven result, acknowledged, with the same hold`, () => {
  const expected = expectedOf(CANCEL_VECTOR);
  assert.deepEqual(expected.orderedExpectedMessages, [...expectedOf("CV-LOAD-CANCELLATION-ALL-EMPTY").orderedExpectedMessages, ...HOLD_PUBLISHED]);
  assert.deepEqual(expected.orderedExpectedMessages, ["LoadCancellationStartRequested", "LoadCancellationAuthorization", "LoadCancellationResult", "DurableAck", ...HOLD_PUBLISHED]);
  assert.equal(expected.stableErrorCode, DOOR_CODE);
  assert.deepEqual(expected.finalState, HELD_FINAL_STATE);
  assert.deepEqual(expected.productAssertions, { controlServer: DOOR_SERVER("SETTLE_DEMAND_AS_ALL_EMPTY_CANCELLATION"), onboardHmi: DOOR_ONBOARD });
  assert.deepEqual(expected.forbiddenSideEffects, DOOR_SIDE_EFFECTS);
});

test(`${RELEASE_VECTOR} releases a held vehicle through a session, a repair record, fresh readings and a passed check`, () => {
  const expected = expectedOf(RELEASE_VECTOR);
  assert.deepEqual(expected.orderedExpectedMessages, [
    "ExceptionRecoverySessionRequested", "ExceptionRecoverySessionOpened", "RecoveryActionSubmitted", "RecoveryActionAccepted",
    "HardwareRecoveryRecordSubmitted", "HardwareRecoveryRecordResult", "ExceptionRecoverySessionSnapshot", "SnapshotAppliedAck",
    "SafetyStateSnapshotRequested", "SafetyStateSnapshot", "SnapshotAppliedAck", CHECK, CHECK_RESULT,
    "VehicleBusinessStateSnapshot", "SnapshotAppliedAck",
  ]);
  // The exact list above is what keeps a slot command out of the trace; this line only says so in words, and would miss a
  // door-opening message not named *Command.
  assert.deepEqual(expected.orderedExpectedMessages.filter((type) => /Command$/.test(type)), []);
  // The vector ends READY, so no error code stands at its end: the door code belongs to the two clearing vectors.
  assert.equal(expected.stableErrorCode, null);
  assert.deepEqual(expected.finalState, { readiness: "READY", business: "DOOR_HOLD_LIFTED_RELEASE_SESSION_CLOSED", physical: "HELD_SLOTS_LOCKED_RESET_EMPTY" });
});

for (const vectorId of [DOOR_VECTOR, CANCEL_VECTOR, RELEASE_VECTOR]) {
  test(`${vectorId} keeps the four default persistence checkpoints`, () => {
    assert.deepEqual(expectedOf(vectorId).persistenceCheckpoints, DEFAULT_CHECKPOINTS);
  });
}

test(`${RELEASE_VECTOR} states the product assertions of both sides and forbids a hold with no way out`, () => {
  const expected = expectedOf(RELEASE_VECTOR);
  assert.deepEqual(expected.productAssertions, {
    controlServer: ["OFFER_REPAIR_RELEASE_ONLY_WHILE_HELD_FOR_UNPROVEN_DOOR", "LIFT_DOOR_HOLD_ONLY_ON_A_RECORD_OF_THE_RELEASE_ACTION", "CLOSE_RELEASE_SESSION_ON_RECORDED", "REQUEST_SAFETY_SNAPSHOT_ON_RECORD_AND_AFTER_RECONNECT", "RELEASE_ONLY_ON_READINGS_RECEIVED_AFTER_RECORD_AND_A_SAFE_HOLD_RELEASE_CHECK", "NEVER_RELEASE_ON_HARDWARE_RECORD_ALONE", "VOID_RECORD_AND_ACCEPT_NEW_SESSION_WHEN_FIRST_READINGS_UNPROVEN", "PUBLISH_RELEASE_IN_VEHICLE_BUSINESS_STATE"],
    onboardHmi: ["NEVER_SLOT_IO_FOR_REPAIR_RELEASE", "OPEN_RELEASE_SESSION_OVER_HELD_SLOTS_WITHOUT_DEMAND", "JOURNAL_RELEASE_ACTION_BEFORE_SUBMITTING", "RESTORE_REPAIR_RECORD_FORM_AFTER_RESTART", "SUBMIT_HARDWARE_RECORD_ON_RELEASE_ACTION", "REPORT_FRESH_SLOT_READINGS_ON_REQUEST", "ANSWER_HOLD_RELEASE_CHECK_WITHOUT_DEMAND_OR_LEG", "DISPLAY_HOLD_FROM_BLOCKING_FACTS"],
  });
  assert.deepEqual(expected.forbiddenSideEffects, [...DEFAULT_SIDE_EFFECTS, "slot-opened-for-repair-release", "vehicle-released-on-record-alone", "vehicle-released-on-readings-received-before-record", "repair-release-offered-without-door-hold", "hardware-record-on-a-non-release-action-lifts-door-hold", "release-session-stuck-after-onboard-restart", "vehicle-held-without-a-repair-release-path"]);
});

test(`FP-IS-02 binds ${CANCEL_VECTOR} and names the held vehicle in its outcomes and responsibilities`, () => {
  const slice = sliceOf("FP-IS-02");
  assert.ok(slice.vectorIds.includes(CANCEL_VECTOR));
  assert.ok(slice.definition.requiredOutcomes.includes("EMPTY_SLOTS_SETTLE_WHILE_UNPROVEN_DOOR_HOLDS_VEHICLE"));
  assert.ok(slice.definition.ownerResponsibilities.controlServer.includes("HOLD_VEHICLE_ON_UNPROVEN_DOOR"));
  assert.ok(slice.definition.ownerResponsibilities.onboardHmi.includes("REPORT_UNPROVEN_DOOR_AFTER_EMPTY"));
});

test(`FP-IS-07 binds ${DOOR_VECTOR} and ${RELEASE_VECTOR} and names the hold and the release`, () => {
  const slice = sliceOf("FP-IS-07");
  assert.ok(slice.vectorIds.includes(DOOR_VECTOR));
  assert.ok(slice.vectorIds.includes(RELEASE_VECTOR));
  assert.ok(slice.definition.requiredOutcomes.includes("EMPTY_SLOTS_SETTLE_WHILE_UNPROVEN_DOOR_HOLDS_VEHICLE"));
  assert.ok(slice.definition.requiredOutcomes.includes("HELD_VEHICLE_RELEASED_ONLY_BY_REPAIR_RECORD_AND_FRESH_PROOF"));
  assert.ok(slice.definition.authorityModel.wireMessages.includes("HardwareRecoveryRecordSubmitted"));
  assert.ok(slice.definition.ownerResponsibilities.controlServer.includes("HOLD_VEHICLE_ON_UNPROVEN_DOOR"));
  assert.ok(slice.definition.ownerResponsibilities.controlServer.includes("RELEASE_HELD_VEHICLE_ONLY_ON_FRESH_PROOF"));
  assert.ok(slice.definition.ownerResponsibilities.onboardHmi.includes("REPORT_UNPROVEN_DOOR_AFTER_EMPTY"));
  assert.ok(slice.definition.ownerResponsibilities.onboardHmi.includes("SUBMIT_REPAIR_RECORD_WITHOUT_SLOT_IO"));
});

// --- the compatibility report sentences of this ticket ---

test("compatibility report sentences 5 to 10 state this ticket's changes in their final shape", () => {
  const summary = readJson("compatibility/report.json").changeSummary;
  assert.match(summary[4], /^Vector CV-TASK-TYPE-ADMISSION-FAIL-CLOSED and slice FP-IS-10 drop the onboard assertion DISPLAY_ADMISSION_BLOCK_REASON/);
  // The latch borrowed two codes, not one: DEPARTURE_UNSAFE in the safety summary and VEHICLE_NOT_READY on a refused slot.
  assert.match(summary[5], /ONBOARD_FATAL_FAULT_LATCHED/);
  assert.match(summary[5], /DEPARTURE_UNSAFE/);
  assert.match(summary[5], /VEHICLE_NOT_READY/);
  assert.match(summary[6], /CurrentStopWorklistSnapshot gains a required, nullable stopEndedReason/);
  assert.match(summary[6], /null while the worklist has items/);
  assert.match(summary[7], /SublotEntryRequested\.expiresOnRevisionChange gains a description/);
  assert.match(summary[8], /ALL_EMPTY_DOOR_UNPROVEN/);
  assert.match(summary[8], /ALL_EMPTY keeps its meaning/);
  assert.match(summary[8], /SLOT_DOOR_LOCK_UNPROVEN_AFTER_EMPTY/);
  assert.match(summary[8], /CV-LOAD-COMPENSATION-EMPTY-DOOR-UNPROVEN/);
  assert.match(summary[8], /CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN/);
  assert.match(summary[8], /HARDWARE_REPAIR_RELEASE/);
  assert.match(summary[8], /CV-VEHICLE-HOLD-DOOR-REPAIR-RELEASE/);
  assert.match(summary[8], /checkPurpose HOLD_RELEASE/);
  assert.match(summary[8], /CP-0009/);
  assert.match(summary[9], /^PreDepartureSafetyCheck and PreDepartureSafetyCheckResult gain a required checkPurpose/);
  assert.match(summary[9], /DEPARTURE/);
  assert.match(summary[9], /NON_BUSINESS_MOVE/);
  assert.match(summary[9], /HOLD_RELEASE/);
  assert.match(summary[9], /ADR-cross-0009/);
});
