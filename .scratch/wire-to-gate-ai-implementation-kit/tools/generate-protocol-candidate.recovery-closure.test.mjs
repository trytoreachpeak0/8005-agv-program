// Acceptance checks for the recovery surface of the protocol 3.0.0 candidate (8005-agv-program#149): the forced-removal
// cargo handoff record on ForcedMechanicalRecoveryResult, the close reason on ExceptionRecoverySessionSnapshot, error code
// RECOVERY_ACTION_RESULT_NOT_RECONCILED and vector CV-RECOVERY-SESSION-CLOSED-RESULT-NOT-RECONCILED.
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.recovery-closure.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written. Expected shapes,
// names and payloads come from the ticket and REQ-0242, never from the generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const RESULT = "ForcedMechanicalRecoveryResult";
const SNAPSHOT = "ExceptionRecoverySessionSnapshot";
const CODE = "RECOVERY_ACTION_RESULT_NOT_RECONCILED";
const FORCED_VECTOR = "CV-FORCED-MECHANICAL-RECOVERY";
const CLOSED_VECTOR = "CV-RECOVERY-SESSION-CLOSED-RESULT-NOT-RECONCILED";
// protocol-v2.0.0 released 58 codes; everything after them is new in 3.0.0.
const RELEASED_CODE_COUNT = 58;
// The six forbidden side effects every vector carries unless it names its own.
const DEFAULT_SIDE_EFFECTS = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-recovery-closure-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));
const schemaOf = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`);
const validOf = (messageType) => readJson(`examples/valid/${messageType}/V-${messageType}-MIN-001.json`);
const expectedOf = (vectorId) => readJson(`vectors/${vectorId}/expected.json`);

// G1's ajv runs only in a protocol clone, and this repository carries no ajv. This evaluates the subset of JSON Schema
// 2020-12 the generated message schemas use -- $ref into the common types, type, const, enum, required, properties,
// additionalProperties false, anyOf, allOf, if/then/else, minLength, pattern, minimum/maximum and the array keywords -- so
// a payload the tests build by hand is judged by the schema actually written, conditionals included. It is looser than
// G1 in one place: format is not checked (G1 runs ajv-formats), so no test here may rest on a date-time or uuid being
// malformed. A keyword outside that subset throws rather than being skipped, so a schema that grows one cannot be judged
// valid by silence.
const KNOWN_KEYWORDS = new Set(["$ref", "type", "const", "enum", "required", "properties", "additionalProperties", "anyOf", "allOf", "if", "then", "else", "minLength", "pattern", "minimum", "maximum", "items", "minItems", "maxItems", "uniqueItems", "format", "examples", "x-sortedAscending", "x-sortedBy"]);
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
const payloadSchemaOf = (messageType) => schemaOf(messageType).properties.payload;
const accepts = (messageType, payload) => valid(payloadSchemaOf(messageType), payload);

// --- ForcedMechanicalRecoveryResult: the forced-removal cargo handoff record (REQ-0242) ---
// The user's site fact of 2026-09-29: staff always identify the cargo they take out, so there is no unidentified branch.
// A record exists exactly when the vehicle was mechanically isolated on a session with a demand, because that is the one
// case where the vehicle, once the result is acknowledged, drops its recovery context for the demand: without a record the
// control server would have nothing to settle the demand on and the demand could never leave RecoveryRequired.

const HANDOFF_KEYS = ["sublot", "receiverName", "handedOverAt"];
const DEMAND_ID = "00000000-0000-4000-8000-00000000d001";
const resultPayload = (outcome, demandId, cargoHandoff) => ({ ...validOf(RESULT).payload, outcome, demandId, cargoHandoff });
// Handed over by name to a person who is not the forced-removal operator, with the product identified by its SUBLOT.
const handoff = () => ({ sublot: "SUBLOT-2026-0929-017", receiverName: "Wang Receiving Clerk", handedOverAt: "2026-09-29T08:15:00Z" });

test("ForcedMechanicalRecoveryResult adds a nullable demandId and a nullable cargoHandoff after its released fields", () => {
  const payload = payloadSchemaOf(RESULT);
  const released = ["exceptionRecoverySessionId", "recoveryActionId", "forcedRecoveryGeneration", "outcome", "slots", "operator", "observedAt", "electronicEmptyProven", "vehicleReadyProven"];
  assert.deepEqual(payload.required, [...released, "demandId", "cargoHandoff"]);
  assert.deepEqual(Object.keys(payload.properties), payload.required);
  assert.equal(payload.additionalProperties, false);
  assert.deepEqual(payload.properties.outcome, { type: "string", enum: ["MECHANICALLY_ISOLATED", "FAILED", "UNKNOWN"] });
  // The same nullable Id as ForcedMechanicalRecoveryCommand.demandId, which the vehicle copies back.
  assert.deepEqual(payload.properties.demandId, payloadSchemaOf("ForcedMechanicalRecoveryCommand").properties.demandId);
  const { anyOf } = payload.properties.cargoHandoff;
  assert.equal(anyOf?.length, 2, "cargoHandoff is not a two-way union");
  assert.deepEqual(anyOf[1], { type: "null" });
  const record = anyOf[0];
  assert.equal(record.type, "object");
  assert.deepEqual(record.required, HANDOFF_KEYS);
  assert.deepEqual(Object.keys(record.properties), HANDOFF_KEYS);
  assert.equal(record.additionalProperties, false);
  // Every field of the record is required and non-null: an identified product, a named receiver, a time.
  assert.deepEqual(record.properties.sublot, { type: "string", minLength: 1 });
  // The receiver is a named string, not an OperatorContext: the person taking the cargo may never have been verified
  // on the vehicle, and an OperatorContext would claim a badge or session verification that did not happen.
  assert.deepEqual(record.properties.receiverName, { type: "string", minLength: 1 });
  assert.match(record.properties.handedOverAt.$ref ?? "", /\/common\/types\.schema\.json#\/\$defs\/Instant$/);
});

test("a handoff record never proves an empty slot or a ready vehicle: both proofs stay const false", () => {
  const payload = payloadSchemaOf(RESULT);
  assert.deepEqual(payload.properties.electronicEmptyProven, { type: "boolean", const: false });
  assert.deepEqual(payload.properties.vehicleReadyProven, { type: "boolean", const: false });
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, handoff())), true, "the baseline record is refused");
  assert.equal(accepts(RESULT, { ...resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, handoff()), electronicEmptyProven: true }), false);
  assert.equal(accepts(RESULT, { ...resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, handoff()), vehicleReadyProven: true }), false);
});

test("every forced-recovery outcome has exactly one accepted shape, with or without a demand", () => {
  // Isolated on a demand: the record is required, and it is what the control server settles the demand on.
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, handoff())), true, "isolated on a demand with a record");
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, null)), false, "isolated on a demand without a record");
  // Isolated without a demand: nothing to settle, so no record.
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", null, null)), true, "isolated without a demand, no record");
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", null, handoff())), false, "isolated without a demand, with a record");
  // FAILED or UNKNOWN: the vehicle keeps its recovery context and nothing is handed over, with a demand or without.
  for (const outcome of ["FAILED", "UNKNOWN"]) {
    for (const demandId of [DEMAND_ID, null]) {
      assert.equal(accepts(RESULT, resultPayload(outcome, demandId, null)), true, `${outcome} demand=${demandId} without a record`);
      assert.equal(accepts(RESULT, resultPayload(outcome, demandId, handoff())), false, `${outcome} demand=${demandId} with a record`);
    }
  }
});

test("a handoff record requires an identified product, a named receiver and a handover time, and nothing else", () => {
  const record = handoff();
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, record)), true, "the baseline record is refused");
  for (const key of HANDOFF_KEYS) {
    assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, { ...record, [key]: null })), false, `${key} null`);
    const { [key]: _, ...without } = record;
    assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, without)), false, `${key} missing`);
  }
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, { ...record, sublot: "" })), false, "empty sublot");
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, { ...record, receiverName: "" })), false, "empty receiver");
  assert.equal(accepts(RESULT, resultPayload("MECHANICALLY_ISOLATED", DEMAND_ID, { ...record, physicalDescription: "one basket" })), false, "an undeclared field");
});

test("the minimal valid ForcedMechanicalRecoveryResult satisfies its own schema, conditionals included", () => {
  const payload = validOf(RESULT).payload;
  assert.ok("cargoHandoff" in payload && "demandId" in payload, "the example lacks the new fields");
  assert.ok(accepts(RESULT, payload), `valid example violates its schema: ${JSON.stringify(payload)}`);
});

// Each negative breaks only the record correspondence: with the conditional removed from the schema the payload would be
// valid, so a rejection can only come from the conditional.
const stripConditionals = (schema) => JSON.parse(JSON.stringify(schema, (key, value) => (["if", "then", "else"].includes(key) ? undefined : value)));
const resultNegatives = {
  "IF-THEN-cargoHandoff-MECHANICALLY_ISOLATED": (payload) => payload.outcome === "MECHANICALLY_ISOLATED" && typeof payload.demandId === "string" && payload.cargoHandoff === null,
  "IF-THEN-cargoHandoff-NO_DEMAND": (payload) => payload.outcome === "MECHANICALLY_ISOLATED" && payload.demandId === null && payload.cargoHandoff !== null,
  "IF-THEN-cargoHandoff-FAILED": (payload) => payload.outcome === "FAILED" && typeof payload.demandId === "string" && payload.cargoHandoff !== null,
  "IF-THEN-cargoHandoff-UNKNOWN": (payload) => payload.outcome === "UNKNOWN" && typeof payload.demandId === "string" && payload.cargoHandoff !== null,
};
for (const [suffix, breaks] of Object.entries(resultNegatives)) {
  test(`if-then negative ${suffix} breaks only the record correspondence and is rejected by the conditional`, () => {
    const negative = readJson(`examples/invalid/${RESULT}/I-${RESULT}-${suffix}.json`);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/cargoHandoff", rule: "if-then" });
    const payload = negative.message.payload;
    assert.ok(breaks(payload), `does not break ${suffix}: ${JSON.stringify({ outcome: payload.outcome, demandId: payload.demandId, cargoHandoff: payload.cargoHandoff })}`);
    assert.equal(accepts(RESULT, payload), false, "the schema accepts it");
    assert.equal(valid(stripConditionals(payloadSchemaOf(RESULT)), payload), true, "rejected for something other than the conditional");
  });
}

// --- ExceptionRecoverySessionSnapshot: why the session closed ---

const snapshotPayload = (state, closedReason) => ({ ...validOf(SNAPSHOT).payload, state, closedReason });

test("ExceptionRecoverySessionSnapshot adds a required nullable closedReason typed ErrorCode, last", () => {
  const payload = payloadSchemaOf(SNAPSHOT);
  assert.equal(payload.required.at(-1), "closedReason");
  assert.equal(payload.required.at(-2), "blockingFacts");
  assert.deepEqual(Object.keys(payload.properties), payload.required);
  assert.equal(payload.additionalProperties, false);
  const { anyOf } = payload.properties.closedReason;
  assert.equal(anyOf?.length, 2);
  assert.match(anyOf[0].$ref ?? "", /\/common\/types\.schema\.json#\/\$defs\/ErrorCode$/);
  assert.deepEqual(anyOf[1], { type: "null" });
  // The four states and the four actions are unchanged.
  assert.deepEqual(payload.properties.state, { type: "string", enum: ["OPEN", "ACTION_SELECTED", "EXECUTING", "CLOSED"] });
});

test("closedReason is null unless the session is CLOSED, and a CLOSED session may carry the code or null", () => {
  for (const state of ["OPEN", "ACTION_SELECTED", "EXECUTING"]) {
    assert.equal(accepts(SNAPSHOT, snapshotPayload(state, CODE)), false, `${state} with a reason`);
    assert.equal(accepts(SNAPSHOT, snapshotPayload(state, null)), true, `${state} without a reason`);
  }
  assert.equal(accepts(SNAPSHOT, snapshotPayload("CLOSED", CODE)), true, "CLOSED on an unreconciled result");
  assert.equal(accepts(SNAPSHOT, snapshotPayload("CLOSED", null)), true, "CLOSED normally");
  assert.equal(accepts(SNAPSHOT, snapshotPayload("CLOSED", "NOT_A_REGISTERED_CODE")), false, "CLOSED with an unregistered code");
});

test("the minimal valid ExceptionRecoverySessionSnapshot satisfies its own schema, conditionals included", () => {
  const payload = validOf(SNAPSHOT).payload;
  assert.ok("closedReason" in payload, "the example lacks closedReason");
  assert.ok(accepts(SNAPSHOT, payload), `valid example violates its schema: ${JSON.stringify(payload)}`);
});

for (const state of ["OPEN", "ACTION_SELECTED", "EXECUTING"]) {
  test(`if-then negative IF-THEN-closedReason-${state} carries a reason on a ${state} session and is rejected by the conditional`, () => {
    const negative = readJson(`examples/invalid/${SNAPSHOT}/I-${SNAPSHOT}-IF-THEN-closedReason-${state}.json`);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/closedReason", rule: "if-then" });
    const payload = negative.message.payload;
    assert.equal(payload.state, state);
    assert.equal(payload.closedReason, CODE);
    assert.equal(accepts(SNAPSHOT, payload), false, "the schema accepts it");
    assert.equal(valid(stripConditionals(payloadSchemaOf(SNAPSHOT)), payload), true, "rejected for something other than the conditional");
  });
}

// --- the error code ---

test("RECOVERY_ACTION_RESULT_NOT_RECONCILED is appended after the 2.0.0 codes, introduced in 3.0.0 and narrowed to the snapshot", () => {
  const codes = readJson("errors/error-codes.json").codes;
  const index = codes.findIndex((entry) => entry.code === CODE);
  assert.ok(index >= RELEASED_CODE_COUNT, `${CODE} at ${index}`);
  const entry = codes[index];
  assert.equal(entry.introducedInRelease, "3.0.0");
  assert.deepEqual(entry.allowedMessageTypes, [SNAPSHOT]);
  assert.equal(entry.category, "SAFETY_RECOVERY");
  assert.equal(entry.retryDisposition, "MANUAL_REVIEW");
  // A self-contained sentence: what closed, on which results, and what is left for the administrator.
  assert.match(entry.meaning, /^The exception recovery session closed because/);
  assert.match(entry.meaning, /FAILED or UNKNOWN/);
  // The third source (control-server#187): the vehicle refused the command that would have produced a result.
  assert.match(entry.meaning, /vehicle refused the SlotOperationResumeCommand with SlotOperationCommandRejected so no result will come/);
  assert.match(entry.meaning, /demand stays blocked/);
  assert.match(entry.meaning, /new exception recovery session/);
  assert.ok(readJson("schemas/common/types.schema.json").$defs.ErrorCode.enum.includes(CODE));
});

// --- vectors and the slice ---

test(`${CLOSED_VECTOR} runs an unreconciled compensation to a CLOSED snapshot and its ack, with the new stable code`, () => {
  const expected = expectedOf(CLOSED_VECTOR);
  // Every RELIABLE message the vehicle sends gets its own DurableAck; the snapshot gets its SnapshotAppliedAck.
  assert.deepEqual(expected.orderedExpectedMessages, ["RecoveryActionSubmitted", "RecoveryActionAccepted", "LoadCompensationRequested", "LoadCompensationCommand", "LoadCompensationResult", "DurableAck", SNAPSHOT, "SnapshotAppliedAck"]);
  assert.equal(expected.stableErrorCode, CODE);
  assert.deepEqual(expected.finalState, { readiness: "RECOVERY_REQUIRED", business: "DEMAND_BLOCKED_SESSION_CLOSED_NEW_SESSION_ALLOWED", physical: "AS_REPORTED_BY_UNRECONCILED_RESULT" });
});

test(`${CLOSED_VECTOR} states the product assertions of both sides and forbids an unreconciled close that nothing can leave`, () => {
  const expected = expectedOf(CLOSED_VECTOR);
  assert.deepEqual(expected.productAssertions, {
    controlServer: ["CLOSE_SESSION_WITH_REASON_ON_UNRECONCILED_RESULT", "KEEP_DEMAND_BLOCKED_AFTER_UNRECONCILED_CLOSE", "ACCEPT_NEW_SESSION_AFTER_UNRECONCILED_CLOSE", "RESEND_CLOSED_REASON_AFTER_RECONNECT"],
    onboardHmi: ["DISPLAY_SESSION_CLOSED_REASON", "ALLOW_REOPENING_AFTER_SESSION_CLOSED", "NEVER_TREAT_UNRECONCILED_CLOSE_AS_RECOVERED"],
  });
  assert.deepEqual(expected.forbiddenSideEffects, [...DEFAULT_SIDE_EFFECTS, "unreconciled-result-settles-demand", "session-left-open-after-final-result", "new-session-refused-after-unreconciled-close"]);
});

test(`${FORCED_VECTOR} keeps its messages and asserts the named handoff and a way out for every outcome`, () => {
  const expected = expectedOf(FORCED_VECTOR);
  assert.deepEqual(expected.orderedExpectedMessages, ["RecoveryActionSubmitted", "RecoveryActionAccepted", "ForcedMechanicalRecoveryCommand", RESULT]);
  assert.deepEqual(expected.productAssertions, {
    controlServer: ["FENCE_FORCED_RECOVERY_BY_GENERATION", "SETTLE_DEMAND_ONLY_ON_NAMED_HANDOFF", "NEVER_REFUSE_AN_ISOLATION_RESULT_OVER_ITS_RECORD", "KEEP_DEMAND_BLOCKED_AND_ACCEPT_NEW_SESSION_ON_FAILED_OR_UNKNOWN", "NEVER_TREAT_HANDOFF_AS_EMPTY_SLOT_OR_READY_VEHICLE"],
    onboardHmi: ["REFUSE_STALE_FORCED_RECOVERY_GENERATION", "REPORT_FORCED_RECOVERY_OUTCOME", "REPORT_CARGO_HANDOFF_RECORD_IN_RESULT", "COPY_COMMAND_DEMAND_INTO_RESULT", "CONFIRM_SUBLOT_AGAINST_DEMAND_BEFORE_SENDING", "REPLAY_SAME_HANDOFF_RECORD_AFTER_RESTART", "KEEP_RECOVERY_CONTEXT_UNLESS_ISOLATION_ACKNOWLEDGED"],
  });
  assert.deepEqual(expected.forbiddenSideEffects, [...DEFAULT_SIDE_EFFECTS, "isolation-on-a-demand-without-handoff-record", "handoff-record-proves-empty-slot-or-ready-vehicle", "demand-left-blocked-after-acknowledged-isolation", "recovery-context-cleared-on-failed-or-unknown-forced-recovery"]);
  // The G3 claim review maps a server check onto this vector's released final state; it does not move.
  assert.deepEqual(expected.finalState, { readiness: "RECOVERY_REQUIRED_OR_UNIQUELY_RECONCILED", business: "NO_DUPLICATE_COMMIT", physical: "NO_UNPROVEN_STATE" });
  assert.equal(expected.stableErrorCode, null);
});

test("FP-IS-07 binds the new vector and names the close reason and the handoff record in its outcomes and responsibilities", () => {
  const slice = readJson("integration-slices/index.json").slices.find((item) => item.integrationSliceId === "FP-IS-07");
  assert.ok(slice.vectorIds.includes(CLOSED_VECTOR));
  assert.ok(slice.vectorIds.includes(FORCED_VECTOR));
  assert.ok(slice.definition.requiredOutcomes.includes("FORCED_ISOLATION_ON_A_DEMAND_SETTLES_ON_A_NAMED_HANDOFF"));
  assert.ok(slice.definition.requiredOutcomes.includes("UNRECONCILED_SESSION_CLOSE_STATES_ITS_REASON"));
  assert.ok(slice.definition.authorityModel.wireMessages.includes(SNAPSHOT));
  assert.ok(slice.definition.ownerResponsibilities.controlServer.includes("CLOSE_UNRECONCILED_SESSION_WITH_REASON"));
  assert.ok(slice.definition.ownerResponsibilities.onboardHmi.includes("RECORD_FORCED_REMOVAL_HANDOFF"));
});
