// Acceptance checks for the remaining-baskets skip in the protocol 6.0.0 candidate (8005-agv-protocol#26, tracking
// 8005-agv-program#210; CP-0021, REQ-0367, the revised REQ-0211 and REQ-0352 in requirements-baseline-v1.20.0).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.remaining-baskets-skip.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written. Whether each example
// really passes or fails its schema is G1's to prove on the regenerated tree; these checks pin the shapes and the examples.
// Expected values come from the ticket and CP-0021 section 3 item 4, never from the generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const COMMON = "https://schemas.8005-agv.local/agv-full-product/v7/common/types.schema.json#/$defs/";
const REQUEST = "RemainingBasketsSkipRequested";
const RESULT = "RemainingBasketsSkipResult";
const OPERATION_RESULT = "OperationResult";
// protocol-v5.0.0 released 62 codes; everything after them is new in 6.0.0.
const V5_RELEASED_CODE_COUNT = 62;
const SKIPPED_CODE = "REMAINING_BASKETS_SKIPPED";
const NOTHING_LOADED_CODE = "REMAINING_BASKETS_SKIP_NOTHING_LOADED";
const CANCELLATION_CODE = "LOAD_CANCELLATION_BASKET_LOADED";
const DEFAULT_FORBIDDEN = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-remaining-baskets-skip-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative) => fs.readFileSync(path.join(tree, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const schemaOf = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`);
const payloadOf = (messageType) => schemaOf(messageType).properties.payload;
const validOf = (messageType, suffix = "MIN-001") => readJson(`examples/valid/${messageType}/V-${messageType}-${suffix}.json`);
const invalidOf = (messageType, suffix) => readJson(`examples/invalid/${messageType}/I-${messageType}-${suffix}.json`);
const ref = (name) => ({ $ref: `${COMMON}${name}` });
const nullable = (schema) => ({ anyOf: [schema, { type: "null" }] });
const slotArray = (options) => ({ type: "array", items: ref("SlotNo"), ...options, "x-sortedAscending": true });
const section = (heading) => {
  const notes = read("docs/wire-notes.md");
  const start = notes.indexOf(`## ${heading}`);
  assert.ok(start >= 0, `wire-notes section ${heading} not found`);
  const next = notes.indexOf("\n## ", start + 1);
  return notes.slice(start, next < 0 ? undefined : next);
};

// --- the two new messages ---

// Both RELIABLE, the CurrentStopDeparture shape: the press is journaled before it is sent and survives a disconnect or a
// restart, and the control server's answer is durable and replayed, so a refusal is never lost behind a DurableAck.
for (const [messageType, direction, recoveryRole] of [
  [REQUEST, "O_TO_C", "REMAINING_BASKETS_SKIP"],
  [RESULT, "C_TO_O", "PENDING_RESULT_REPLAY"],
]) {
  test(`${messageType} is ${direction}, RELIABLE, durable on both ends, deduplicated by skipRequestId, with a null correlationId`, () => {
    const entry = readJson("manifest/release.json").messages[messageType];
    assert.ok(entry, `${messageType} missing from the manifest`);
    assert.equal(entry.direction, direction);
    assert.equal(entry.deliveryClass, "RELIABLE");
    assert.equal(entry.durableBeforeSend, true);
    assert.equal(entry.durableBeforeAck, true);
    assert.deepEqual(entry.businessDedupKeys, ["skipRequestId"]);
    assert.equal(entry.correlationRule, "MUST_BE_NULL");
    assert.equal(entry.recoveryRole, recoveryRole);
    assert.deepEqual(schemaOf(messageType).properties.correlationId, { type: "null" });
    assert.equal(validOf(messageType).correlationId, null);
  });
}

test(`${REQUEST} names the demand, the operation session, the attempt, the k loaded slots and the operator if known`, () => {
  const payload = payloadOf(REQUEST);
  assert.deepEqual(payload.required, ["skipRequestId", "demandId", "operationSessionId", "slotOperationAttemptId", "loadedSlots", "operator"]);
  assert.equal(payload.additionalProperties, false);
  assert.deepEqual(payload.properties.skipRequestId, ref("Id"));
  assert.deepEqual(payload.properties.demandId, ref("Id"));
  assert.deepEqual(payload.properties.operationSessionId, ref("Id"));
  assert.deepEqual(payload.properties.slotOperationAttemptId, ref("Id"));
  // k >= 1 is part of the shape: a request naming no loaded slot cannot be written at all (REQ-0367: k = 0 is a cancellation).
  assert.deepEqual(payload.properties.loadedSlots, slotArray({ minItems: 1, maxItems: 8, uniqueItems: true }));
  // CP-0021 new item 1 note 8: no badge is required, so the operator is recorded when known and is never a condition.
  assert.deepEqual(payload.properties.operator, nullable(ref("OperatorContext")));
});

test(`a ${REQUEST} naming no loaded slot (k = 0) is a schema-invalid example`, () => {
  const wrapper = invalidOf(REQUEST, "MIN-ITEMS-loadedSlots");
  assert.deepEqual(wrapper.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/loadedSlots", rule: "minItems" });
  assert.deepEqual(wrapper.message.payload.loadedSlots, []);
  const restored = structuredClone(wrapper.message);
  restored.payload.loadedSlots = validOf(REQUEST).payload.loadedSlots;
  assert.deepEqual(restored, validOf(REQUEST));
});

test(`${RESULT} authorizes or rejects one request and names the k slots it authorizes`, () => {
  const payload = payloadOf(RESULT);
  assert.deepEqual(payload.required, ["skipRequestId", "demandId", "slotOperationAttemptId", "outcome", "loadedSlots", "problem"]);
  assert.equal(payload.additionalProperties, false);
  assert.deepEqual(payload.properties.outcome, { type: "string", enum: ["AUTHORIZED", "REJECTED"] });
  assert.deepEqual(payload.properties.loadedSlots, slotArray({ maxItems: 8, uniqueItems: true }));
  assert.deepEqual(payload.properties.problem, nullable(ref("Problem")));
  // A refusal says why and authorizes no slot; an authorization names at least one slot and carries no problem.
  assert.deepEqual(payload.if, { properties: { outcome: { const: "REJECTED" } }, required: ["outcome"] });
  assert.deepEqual(payload.then, { properties: { problem: { type: "object" }, loadedSlots: { maxItems: 0 } } });
  assert.deepEqual(payload.else, { properties: { problem: { type: "null" }, loadedSlots: { minItems: 1 } } });
});

test(`${RESULT} has a valid example of each outcome and an invalid one on each side of each correspondence`, () => {
  const authorized = validOf(RESULT);
  assert.equal(authorized.payload.outcome, "AUTHORIZED");
  assert.equal(authorized.payload.problem, null);
  assert.ok(authorized.payload.loadedSlots.length >= 1);
  const rejected = validOf(RESULT, "REJECTED-001");
  assert.equal(rejected.payload.outcome, "REJECTED");
  assert.equal(rejected.payload.problem.reasonCode, "LOCK_NOT_CLOSED");
  assert.deepEqual(rejected.payload.loadedSlots, []);
  for (const [suffix, fieldPath] of [
    ["IF-THEN-problem-REJECTED", "/payload/problem"],
    ["IF-THEN-problem-AUTHORIZED", "/payload/problem"],
    ["IF-THEN-loadedSlots-REJECTED", "/payload/loadedSlots"],
    ["IF-THEN-loadedSlots-AUTHORIZED", "/payload/loadedSlots"],
  ]) assert.deepEqual(invalidOf(RESULT, suffix).expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath, rule: "if-then" }, suffix);
  assert.equal(invalidOf(RESULT, "IF-THEN-problem-REJECTED").message.payload.problem, null);
  assert.deepEqual(invalidOf(RESULT, "IF-THEN-loadedSlots-AUTHORIZED").message.payload.loadedSlots, []);
});

// --- the operation result of a skipped load ---

test(`${OPERATION_RESULT} appends COMPLETED_REMAINING_SKIPPED and adds no field`, () => {
  const payload = payloadOf(OPERATION_RESULT);
  // Appended, so the released three keep their order; an end that reads only overallOutcome never takes a skipped load for a
  // load of every target slot.
  assert.deepEqual(payload.properties.overallOutcome.enum, ["COMPLETED", "FAILED", "UNKNOWN", "COMPLETED_REMAINING_SKIPPED"]);
  // Review M2: the control server finds the one authorization by (demandId, slotOperationAttemptId), so the result names no
  // skip request, and an OperationResult built anywhere else on either end keeps the 5.0.0 fields.
  assert.deepEqual(payload.required, ["demandId", "slotOperationAttemptId", "operationType", "overallOutcome", "slotResults", "observedAt", "journalCheckpoint", "resultContentSha256"]);
  assert.equal(Object.hasOwn(payload.properties, "remainingBasketsSkipRequestId"), false);
});

test(`a skipped load reports its k slots COMPLETED and OCCUPIED and every remaining slot NOT_STARTED, EMPTY and ${SKIPPED_CODE}`, () => {
  const { payload } = validOf(OPERATION_RESULT, "REMAINING-BASKETS-SKIPPED-001");
  assert.equal(payload.operationType, "LOAD");
  assert.equal(payload.overallOutcome, "COMPLETED_REMAINING_SKIPPED");
  assert.deepEqual(payload.slotResults, [
    { slotNo: 1, outcome: "COMPLETED", finalPhysicalState: "OCCUPIED", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: [] },
    { slotNo: 2, outcome: "NOT_STARTED", finalPhysicalState: "EMPTY", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: [SKIPPED_CODE] },
  ]);
});

test(`the skipped outcome is a LOAD whose every slot is closed and proven, and only its remaining slots carry ${SKIPPED_CODE}`, () => {
  const branches = payloadOf(OPERATION_RESULT).allOf;
  assert.ok(Array.isArray(branches), "OperationResult payload has no allOf");
  const skipped = branches.find((branch) => branch.if?.properties?.overallOutcome?.const === "COMPLETED_REMAINING_SKIPPED");
  assert.ok(skipped, "no branch for COMPLETED_REMAINING_SKIPPED");
  const withoutCode = { reasonCodes: { not: { contains: { const: SKIPPED_CODE } } } };
  // Review L5: every other result -- COMPLETED, FAILED, UNKNOWN, LOAD or UNLOAD -- never carries the code on any slot.
  assert.deepEqual(skipped.else, { properties: { slotResults: { items: { properties: withoutCode } } } });
  const then = skipped.then.properties;
  assert.deepEqual(Object.keys(then).sort(), ["operationType", "slotResults"]);
  assert.deepEqual(then.operationType, { const: "LOAD" });
  const items = then.slotResults.items;
  assert.deepEqual(items.properties.outcome, { enum: ["COMPLETED", "NOT_STARTED"] });
  assert.deepEqual(items.properties.lockState, { const: "LOCKED" });
  assert.deepEqual(items.properties.unlockOutputState, { const: "RESET" });
  assert.deepEqual(items.allOf, [
    { if: { properties: { outcome: { const: "COMPLETED" } }, required: ["outcome"] }, then: { properties: { finalPhysicalState: { const: "OCCUPIED" }, ...withoutCode } } },
    { if: { properties: { outcome: { const: "NOT_STARTED" } }, required: ["outcome"] }, then: { properties: { finalPhysicalState: { const: "EMPTY" }, reasonCodes: { contains: { const: SKIPPED_CODE } } } } },
  ]);
  // At least one loaded slot (k >= 1) and at least one remaining slot (k < N).
  assert.deepEqual(then.slotResults.allOf, [
    { contains: { properties: { outcome: { const: "COMPLETED" } } }, minContains: 1 },
    { contains: { properties: { outcome: { const: "NOT_STARTED" } } }, minContains: 1 },
  ]);
});

test("each way a skipped result can break its shape has its own invalid example", () => {
  const cases = {
    "IF-THEN-operationType-SKIPPED-UNLOAD": "/payload/operationType",
    "IF-THEN-slotResults-SKIPPED-NOTHING-LOADED": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-NOTHING-REMAINING": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-UNKNOWN": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-FAILED": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-UNLOCKED": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-OUTPUT-ACTIVE": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-REMAINING-OCCUPIED": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-REMAINING-WITHOUT-CODE": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-LOADED-EMPTY": "/payload/slotResults",
    "IF-THEN-slotResults-SKIPPED-LOADED-WITH-CODE": "/payload/slotResults",
    "IF-THEN-slotResults-COMPLETED-WITH-CODE": "/payload/slotResults",
  };
  for (const [suffix, fieldPath] of Object.entries(cases)) {
    const wrapper = invalidOf(OPERATION_RESULT, suffix);
    assert.deepEqual(wrapper.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath, rule: "if-then" }, suffix);
  }
  // Review L1: a third slot FAILED, EMPTY, LOCKED and RESET passes every other constraint, so only the outcome enum refuses it.
  assert.deepEqual(invalidOf(OPERATION_RESULT, "IF-THEN-slotResults-SKIPPED-FAILED").message.payload.slotResults.map((slot) => slot.outcome), ["COMPLETED", "NOT_STARTED", "FAILED"]);
  assert.deepEqual(invalidOf(OPERATION_RESULT, "IF-THEN-slotResults-SKIPPED-FAILED").message.payload.slotResults[2], { slotNo: 3, outcome: "FAILED", finalPhysicalState: "EMPTY", lockState: "LOCKED", unlockOutputState: "RESET", reasonCodes: [] });
  const completed = invalidOf(OPERATION_RESULT, "IF-THEN-slotResults-COMPLETED-WITH-CODE").message.payload;
  assert.equal(completed.overallOutcome, "COMPLETED");
  assert.deepEqual(completed.slotResults[0].reasonCodes, [SKIPPED_CODE]);
});

// --- the load cancellation authorization (review M3) ---

test("LoadCancellationAuthorization authorizes only an empty scope and refuses only with a reason", () => {
  const payload = payloadOf("LoadCancellationAuthorization");
  assert.deepEqual(payload.if, { properties: { decision: { const: "REJECTED" } }, required: ["decision"] });
  assert.deepEqual(payload.then, { properties: { problem: { type: "object" }, slots: { maxItems: 0 } } });
  assert.deepEqual(payload.else, { properties: { problem: { type: "null" }, slots: { maxItems: 0 } } });
  // Review L-b: both decisions carry empty slots, so uniqueItems has no shape left to test; it goes, and its negative with it.
  assert.equal(Object.hasOwn(payload.properties.slots, "uniqueItems"), false);
  assert.equal(fs.existsSync(path.join(tree, "examples/invalid/LoadCancellationAuthorization/I-LoadCancellationAuthorization-UNIQUE-slots.json")), false);
  const authorized = validOf("LoadCancellationAuthorization");
  assert.equal(authorized.payload.decision, "AUTHORIZED");
  assert.deepEqual(authorized.payload.slots, []);
  const rejected = validOf("LoadCancellationAuthorization", "REJECTED-001");
  assert.equal(rejected.payload.decision, "REJECTED");
  assert.equal(rejected.payload.problem.reasonCode, CANCELLATION_CODE);
  assert.deepEqual(invalidOf("LoadCancellationAuthorization", "IF-THEN-slots-AUTHORIZED").expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/slots", rule: "if-then" });
  assert.deepEqual(invalidOf("LoadCancellationAuthorization", "IF-THEN-slots-AUTHORIZED").message.payload.slots, [1]);
  assert.deepEqual(invalidOf("LoadCancellationAuthorization", "IF-THEN-problem-REJECTED").expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/problem", rule: "if-then" });
  assert.equal(invalidOf("LoadCancellationAuthorization", "IF-THEN-problem-REJECTED").message.payload.problem, null);
  // Review L-c: an authorization with a problem, and a refusal naming a slot.
  assert.deepEqual(invalidOf("LoadCancellationAuthorization", "IF-THEN-problem-AUTHORIZED").expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/problem", rule: "if-then" });
  assert.equal(invalidOf("LoadCancellationAuthorization", "IF-THEN-problem-AUTHORIZED").message.payload.decision, "AUTHORIZED");
  assert.equal(typeof invalidOf("LoadCancellationAuthorization", "IF-THEN-problem-AUTHORIZED").message.payload.problem, "object");
  assert.deepEqual(invalidOf("LoadCancellationAuthorization", "IF-THEN-slots-REJECTED").expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/slots", rule: "if-then" });
  assert.equal(invalidOf("LoadCancellationAuthorization", "IF-THEN-slots-REJECTED").message.payload.decision, "REJECTED");
  assert.deepEqual(invalidOf("LoadCancellationAuthorization", "IF-THEN-slots-REJECTED").message.payload.slots, [1]);
});

// --- review L-a: the four other results that carry SlotResult refuse the skip marker ---

for (const messageType of ["LoadCorrectionResult", "LoadCancellationResult", "LoadCompensationResult", "FaultCargoRecoveryResult"]) {
  test(`${messageType} refuses ${SKIPPED_CODE} on any slot`, () => {
    const payload = payloadOf(messageType);
    assert.ok(Array.isArray(payload.allOf), `${messageType} payload has no allOf`);
    assert.ok(payload.allOf.some((branch) => JSON.stringify(branch) === JSON.stringify({ properties: { slotResults: { items: { properties: { reasonCodes: { not: { contains: { const: SKIPPED_CODE } } } } } } } })), messageType);
    const wrapper = invalidOf(messageType, "NOT-slotResults-REMAINING_BASKETS_SKIPPED");
    assert.deepEqual(wrapper.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/slotResults", rule: "not" });
    assert.deepEqual(wrapper.message.payload.slotResults[0].reasonCodes, [SKIPPED_CODE]);
  });
}

// --- error codes ---

test("6.0.0 appends three codes, each narrowed to the one message that carries it", () => {
  const codes = readJson("errors/error-codes.json").codes;
  const appended = codes.slice(V5_RELEASED_CODE_COUNT);
  assert.deepEqual(appended.map((entry) => entry.code), [SKIPPED_CODE, NOTHING_LOADED_CODE, CANCELLATION_CODE]);
  const byCode = Object.fromEntries(appended.map((entry) => [entry.code, entry]));
  assert.deepEqual(byCode[SKIPPED_CODE].allowedMessageTypes, [OPERATION_RESULT]);
  assert.deepEqual(byCode[NOTHING_LOADED_CODE].allowedMessageTypes, [RESULT]);
  assert.deepEqual(byCode[CANCELLATION_CODE].allowedMessageTypes, ["LoadCancellationAuthorization"]);
  for (const entry of appended) {
    assert.equal(entry.category, "BUSINESS", entry.code);
    assert.equal(entry.introducedInRelease, "6.0.0", entry.code);
    assert.match(entry.meaning, /CP-0021/, entry.code);
  }
  assert.match(byCode[SKIPPED_CODE].meaning, /REQ-0367/);
  assert.match(byCode[SKIPPED_CODE].meaning, /COMPLETED_REMAINING_SKIPPED/);
  assert.match(byCode[NOTHING_LOADED_CODE].meaning, /REQ-0211/);
  assert.match(byCode[CANCELLATION_CODE].meaning, /REQ-0211/);
  assert.match(byCode[CANCELLATION_CODE].meaning, /REQ-0367/);
});

// --- vectors and slices ---

const vectors = {
  "CV-REMAINING-BASKETS-SKIP-AUTHORIZED": {
    messages: [REQUEST, "DurableAck", RESULT, "DurableAck", OPERATION_RESULT, "DurableAck"],
    stableErrorCode: SKIPPED_CODE,
    forbidden: ["remaining-baskets-skipped-without-authorization", "slot-opened-while-skip-pending", "skip-settled-as-cancellation-or-suppression", "manual-transport-alarm-on-skip", "skipped-slots-kept-reserved", "loaded-slot-cleared-on-skip"],
    controlServer: ["AUTHORIZE_SKIP_ONLY_WITH_AT_LEAST_ONE_LOADED_AND_ONE_REMAINING_SLOT", "AUTHORIZE_SKIP_ONLY_WITH_ALL_DOORS_LOCKED_OUTPUTS_RESET_AND_NO_UNKNOWN", "COMMIT_AUTHORIZED_LOADED_SLOTS_AS_ONE_LOAD_BATCH", "RELEASE_REMAINING_SLOTS_AND_RESERVATION_ON_SETTLEMENT", "UNLOAD_ONLY_THE_AUTHORIZED_LOADED_SLOTS", "COMPLETE_DEMAND_AS_NORMAL_DELIVERY_WITHOUT_SUPPRESSION_OR_ALARM", "AUDIT_SKIP_N_TO_K_WITH_OPERATOR_WHEN_KNOWN"],
    onboardHmi: ["OFFER_SKIP_ONLY_WHILE_ITS_CONDITIONS_HOLD", "JOURNAL_SKIP_REQUEST_BEFORE_SENDING", "NEVER_OPEN_A_SLOT_WHILE_SKIP_PENDING", "END_OPERATION_ONLY_ON_AUTHORIZED_SKIP", "REPORT_AUTHORIZED_SLOTS_COMPLETED_AND_REMAINING_SLOTS_SKIPPED", "NEVER_ACT_ON_AN_AUTHORIZATION_AFTER_THE_OPERATION_ENDED_ANOTHER_WAY"],
    finalState: { readiness: "READY", business: "DEMAND_LOADED_WITH_AUTHORIZED_BASKETS_REMAINING_SLOTS_RELEASED", physical: "LOADED_SLOTS_OCCUPIED_REMAINING_SLOTS_EMPTY_ALL_LOCKED_RESET" },
  },
  "CV-REMAINING-BASKETS-SKIP-REJECTED": {
    messages: [REQUEST, "DurableAck", RESULT, "DurableAck"],
    stableErrorCode: "LOCK_NOT_CLOSED",
    forbidden: ["remaining-baskets-skipped-without-authorization", "business-state-changed-by-rejected-skip", "slot-operation-ended-by-rejected-skip"],
    controlServer: ["REJECT_SKIP_WITH_A_DOOR_NOT_PROVEN_LOCKED_OR_OUTPUT_NOT_RESET", "REJECT_SKIP_WITH_AN_UNKNOWN_SLOT_OR_MANUAL_RECOVERY", "REJECT_SKIP_DURING_CORRECTION_OR_CANCELLATION_OR_AFTER_LOADING_ENDED", "CHANGE_NOTHING_ON_REJECTED_SKIP"],
    onboardHmi: ["DISPLAY_SKIP_REJECTION_REASON", "CONTINUE_LOADING_AFTER_REJECTED_SKIP", "ALLOW_NEW_SKIP_REQUEST_AFTER_REJECTION"],
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_SKIP_REJECTED_LOADING_CONTINUES", physical: "UNCHANGED" },
  },
  "CV-REMAINING-BASKETS-SKIP-NOTHING-LOADED": {
    messages: [REQUEST, "DurableAck", RESULT, "DurableAck"],
    stableErrorCode: NOTHING_LOADED_CODE,
    forbidden: ["remaining-baskets-skipped-without-authorization", "skip-authorized-with-nothing-loaded", "business-state-changed-by-rejected-skip"],
    controlServer: ["REJECT_SKIP_WHEN_NO_TARGET_SLOT_CLOSED_OCCUPIED", "CHANGE_NOTHING_ON_REJECTED_SKIP"],
    onboardHmi: ["NEVER_OFFER_SKIP_BEFORE_A_BASKET_IS_LOADED", "DISPLAY_SKIP_REJECTION_REASON", "CONTINUE_LOADING_AFTER_REJECTED_SKIP"],
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_SKIP_REJECTED_LOADING_CONTINUES", physical: "UNCHANGED" },
  },
  "CV-REMAINING-BASKETS-SKIP-DUPLICATE-REQUEST": {
    messages: [REQUEST, "DurableAck", RESULT, "DurableAck", REQUEST, "DurableAck", RESULT, "DurableAck"],
    stableErrorCode: null,
    forbidden: ["second-skip-effect-on-duplicate-request", "conflicting-duplicate-skip-applied", "remaining-baskets-skipped-without-authorization"],
    controlServer: ["DEDUPLICATE_SKIP_ON_REQUEST_ID", "REPLAY_SAME_SKIP_RESULT", "REJECT_SAME_REQUEST_ID_WITH_DIFFERENT_CONTENT"],
    onboardHmi: ["REUSE_PENDING_SKIP_REQUEST_ID_AFTER_RECONNECT_OR_RESTART", "ADOPT_REPLAYED_SKIP_RESULT", "NEVER_MINT_NEW_REQUEST_ID_FOR_SAME_PRESS"],
    finalState: { readiness: "UNCHANGED_OR_SPECIFIED_BY_VECTOR", business: "AT_MOST_ONE_SKIP_PER_REQUEST_ID", physical: "NO_UNPROVEN_STATE" },
  },
  // The ticket's failure condition: the vehicle must not be able to skip without the control server's authorization.
  "CV-REMAINING-BASKETS-SKIP-UNAUTHORIZED-RESULT": {
    messages: [OPERATION_RESULT, "DurableAck"],
    stableErrorCode: null,
    forbidden: ["remaining-baskets-skipped-without-authorization", "unauthorized-skip-result-settled-as-completed", "skipped-slots-released-without-authorization"],
    controlServer: ["NEVER_SETTLE_SKIPPED_RESULT_WITHOUT_MATCHING_AUTHORIZATION", "FIND_THE_AUTHORIZATION_BY_DEMAND_AND_ATTEMPT", "SETTLE_SKIPPED_RESULT_ONLY_ON_THE_AUTHORIZED_LOADED_SLOTS", "BLOCK_JOURNEY_ON_UNRECONCILED_SKIPPED_RESULT"],
    onboardHmi: ["NEVER_REPORT_SKIPPED_RESULT_WITHOUT_AUTHORIZATION"],
    finalState: { readiness: "RECOVERY_REQUIRED", business: "JOURNEY_BLOCKED_DEMAND_NOT_SETTLED", physical: "AS_REPORTED_BY_UNRECONCILED_RESULT" },
  },
  "CV-LOAD-CANCELLATION-BASKET-LOADED": {
    messages: ["LoadCancellationStartRequested", "LoadCancellationAuthorization"],
    stableErrorCode: CANCELLATION_CODE,
    forbidden: ["cancellation-authorized-after-a-basket-is-loaded", "loaded-slot-cleared-by-business-cancellation", "business-state-changed-by-rejected-cancellation"],
    controlServer: ["REJECT_CANCELLATION_ONCE_A_BASKET_IS_LOADED", "REJECT_CANCELLATION_WITH_A_DOOR_NOT_PROVEN_LOCKED_OR_OUTPUT_NOT_RESET", "CHANGE_NOTHING_ON_REJECTED_CANCELLATION"],
    onboardHmi: ["NEVER_OFFER_CANCELLATION_ONCE_A_BASKET_IS_LOADED", "DISPLAY_CANCELLATION_REJECTION_REASON", "OFFER_REMAINING_BASKETS_SKIP_INSTEAD"],
    finalState: { readiness: "UNCHANGED", business: "UNCHANGED_CANCELLATION_REJECTED", physical: "UNCHANGED" },
  },
};

for (const [vectorId, want] of Object.entries(vectors)) {
  test(`${vectorId} carries its trace, its error code, its forbidden side effects and its product assertions`, () => {
    const expected = readJson(`vectors/${vectorId}/expected.json`);
    assert.equal(expected.vectorId, vectorId);
    assert.deepEqual(expected.orderedExpectedMessages, want.messages);
    assert.equal(expected.stableErrorCode, want.stableErrorCode);
    assert.deepEqual(expected.forbiddenSideEffects, [...DEFAULT_FORBIDDEN, ...want.forbidden]);
    assert.deepEqual(expected.productAssertions, { controlServer: want.controlServer, onboardHmi: want.onboardHmi });
    assert.deepEqual(expected.finalState, want.finalState);
    const steps = read(`vectors/${vectorId}/input.ndjson`).trim().split("\n").map((line) => JSON.parse(line));
    assert.deepEqual(steps.map((step) => step.messageType), want.messages);
  });
}

test("CV-LOAD-CANCELLATION-ALL-EMPTY authorizes an empty scope and opens no slot for the cancellation (review M4)", () => {
  const expected = readJson("vectors/CV-LOAD-CANCELLATION-ALL-EMPTY/expected.json");
  assert.deepEqual(expected.orderedExpectedMessages, ["LoadCancellationStartRequested", "LoadCancellationAuthorization", "LoadCancellationResult", "DurableAck"]);
  assert.deepEqual(expected.forbiddenSideEffects, [...DEFAULT_FORBIDDEN, "business-cancellation-opened-a-slot", "cancellation-authorized-after-a-basket-is-loaded"]);
  assert.deepEqual(expected.productAssertions, {
    controlServer: ["AUTHORIZE_CANCELLATION_EXPLICITLY", "AUTHORIZE_ONLY_WITH_EVERY_TARGET_SLOT_EMPTY_LOCKED_AND_RESET", "AUTHORIZE_WITH_AN_EMPTY_SLOT_SCOPE", "RECONCILE_EMPTY_FINAL_STATE"],
    onboardHmi: ["NEVER_OPEN_A_SLOT_FOR_A_CANCELLATION", "REPORT_ALL_EMPTY_WITHOUT_SLOT_IO", "NEVER_CANCEL_UNILATERALLY"],
  });
  // CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN is kept as a defence, unchanged.
  assert.ok(readJson("integration-slices/index.json").slices.find((slice) => slice.integrationSliceId === "FP-IS-02").vectorIds.includes("CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN"));
});

test("the authorization reaches the vehicle before the skipped operation result in the authorized trace", () => {
  const messages = readJson("vectors/CV-REMAINING-BASKETS-SKIP-AUTHORIZED/expected.json").orderedExpectedMessages;
  assert.ok(messages.indexOf(RESULT) < messages.indexOf(OPERATION_RESULT));
});

test("FP-IS-02 carries every new vector and both new messages; FP-IS-05 carries the duplicate request", () => {
  const slices = readJson("integration-slices/index.json").slices;
  const is02 = slices.find((slice) => slice.integrationSliceId === "FP-IS-02");
  for (const vectorId of Object.keys(vectors)) assert.ok(is02.vectorIds.includes(vectorId), vectorId);
  assert.ok(is02.definition.authorityModel.wireMessages.includes(REQUEST));
  assert.ok(is02.definition.authorityModel.wireMessages.includes(RESULT));
  assert.ok(is02.definition.requiredOutcomes.includes("REMAINING_BASKETS_SKIPPED_ONLY_ON_SERVER_AUTHORIZATION"));
  assert.ok(is02.definition.requiredOutcomes.includes("LOAD_CANCELLATION_REFUSED_ONCE_A_BASKET_IS_LOADED"));
  assert.ok(is02.definition.ownerResponsibilities.controlServer.includes("AUTHORIZE_REMAINING_BASKETS_SKIP"));
  assert.ok(is02.definition.ownerResponsibilities.onboardHmi.includes("REQUEST_REMAINING_BASKETS_SKIP_NEVER_SKIP_LOCALLY"));
  const is05 = slices.find((slice) => slice.integrationSliceId === "FP-IS-05");
  assert.ok(is05.vectorIds.includes("CV-REMAINING-BASKETS-SKIP-DUPLICATE-REQUEST"));
});

test("G1 refuses a tree whose authorized skip trace lets the operation result come before the authorization", () => {
  const g1 = read("tools/g1-validate.mjs");
  assert.match(g1, /CV-REMAINING-BASKETS-SKIP-AUTHORIZED/);
  assert.match(g1, /a remaining-baskets skip settles only after its authorization/);
  assert.match(g1, /an unauthorized skipped result is never settled/);
});

// --- prose ---

test("the wire notes define the skip, the checks in order, the settlement and the refusal of a late cancellation", () => {
  const body = section("`RemainingBasketsSkipRequested` and `RemainingBasketsSkipResult`");
  assert.match(body, /CP-0021/);
  assert.match(body, /REQ-0367/);
  assert.match(body, /protocol#26/);
  // The vehicle asks, the control server decides; the vehicle never skips on its own.
  assert.match(body, /The onboard HMI never ends a load short on its own/);
  assert.match(body, /journals the request before it sends it/);
  assert.match(body, /opens no further slot while the request is pending/);
  // The checks, in order, first failing decides.
  for (const code of ["DEMAND_NOT_CURRENT", "OPERATION_SESSION_MISMATCH", "ACTION_NOT_ALLOWED_IN_STATE", "SLOT_STATE_UNKNOWN", "LOCK_NOT_CLOSED", "UNLOCK_OUTPUT_NOT_RESET", NOTHING_LOADED_CODE, "SLOT_SET_INVALID"]) {
    assert.match(body, new RegExp(`\`${code}\``), code);
  }
  assert.match(body, /first check that fails decides/);
  // Settlement only on a matching authorization.
  assert.match(body, /`COMPLETED_REMAINING_SKIPPED`/);
  assert.match(body, /finds the one `RemainingBasketsSkipResult` with `outcome` `AUTHORIZED` it sent for the result's `demandId` and `slotOperationAttemptId`/);
  assert.doesNotMatch(body, /remainingBasketsSkipRequestId/);
  // Review M1: every way out of a pending request, a late authorization, and an authorization spent by another result.
  assert.match(body, /answered with `ProtocolProblem`.*drops the request/s);
  assert.match(body, /gone to manual recovery.*station departure deadline.*`OperationResult` of the attempt/s);
  assert.match(body, /An `AUTHORIZED` result that arrives after the operation has ended another way is journaled and not acted on/);
  assert.match(body, /settles with any result other than `COMPLETED_REMAINING_SKIPPED`, the authorization is spent/);
  // Review L6: the release happens at settlement.
  assert.match(body, /released when the control server settles the result/);
  assert.match(body, /same moment as the immediate release REQ-0367 asks for/);
  // Review L7: a resubmission is a new message of the same request.
  assert.match(body, /new `messageId` with the same `skipRequestId` and the same payload/);
  // Review L2: the order of the cancellation refusals.
  assert.match(body, /`SLOT_STATE_UNKNOWN`, then `LOAD_CANCELLATION_BASKET_LOADED`, then `LOCK_NOT_CLOSED`, then `UNLOCK_OUTPUT_NOT_RESET`/);
  // Review M4: the door-unproven cancellation vector is kept only as a defence.
  assert.match(body, /`CV-LOAD-CANCELLATION-EMPTY-DOOR-UNPROVEN` is kept as a defence/);
  assert.match(body, /this outcome is not settled as `ALL_EMPTY`: the demand ends as that vector sets it, as an all-empty cancellation, and the vehicle is held for repair/);
  assert.doesNotMatch(body, /never settled as `ALL_EMPTY`/);
  // Review M2: the upgrade order.
  assert.match(body, /no rollout of one side first/);
  assert.match(body, /both outboxes drained/);
  assert.match(body, /never settles it as completed/);
  // Duplicates and conflicts.
  assert.match(body, /same `skipRequestId` with the same content is answered by replaying the stored result/);
  assert.match(body, /`BUSINESS_ID_CONTENT_CONFLICT`/);
  // What happens next: k baskets go, the rest is released, unload opens only k.
  assert.match(body, /not a cancellation/);
  assert.match(body, /`expectedBasketCount` k/);
  // The revised REQ-0211.
  assert.match(body, new RegExp(`\`${CANCELLATION_CODE}\``));
});

test("the compatibility report states the one 6.0.0 change in one sentence", () => {
  const [sentence, ...rest] = readJson("compatibility/report.json").changeSummary;
  assert.deepEqual(rest, []);
  assert.match(sentence, /RemainingBasketsSkipRequested.*RemainingBasketsSkipResult/);
  assert.match(sentence, /COMPLETED_REMAINING_SKIPPED/);
  assert.doesNotMatch(sentence, /remainingBasketsSkipRequestId/);
  assert.match(sentence, /LoadCancellationAuthorization/);
  assert.match(sentence, new RegExp(CANCELLATION_CODE));
  assert.match(sentence, /5\.0\.0 implementation/);
});

test("candidate limitations describe what 6.0.0 changes and what it carries over", () => {
  const lastParagraph = read("docs/candidate-limitations.md").trim().split("\n\n").at(-1);
  assert.match(lastParagraph, /RemainingBasketsSkipRequested/);
  assert.match(lastParagraph, /COMPLETED_REMAINING_SKIPPED/);
  assert.match(lastParagraph, /LoadCancellationAuthorization/);
  assert.doesNotMatch(lastParagraph, /remainingBasketsSkipRequestId/);
  assert.match(lastParagraph, /three error codes/);
  assert.match(lastParagraph, /every other schema stays as 5\.0\.0 released it/);
  // Review L-d: a 5.0.0 implementation refuses a 6.0.0 message for its identity, not for an empty scope.
  assert.doesNotMatch(lastParagraph, /authorizes only an empty scope, which a 5\.0\.0 implementation rejects/);
  assert.match(lastParagraph, /refuses every 6\.0\.0 message because its identity and ProtocolVersion differ/);
  assert.match(lastParagraph, /LoadCorrectionResult.*FaultCargoRecoveryResult.*refuse the new slot marker/);
});
