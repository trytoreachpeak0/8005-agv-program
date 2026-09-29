// Acceptance checks for the server-side slot fault declaration in the protocol 3.0.0 candidate (8005-agv-program#147).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.slot-fault-declaration.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written.
// Expected shapes come from the ticket and CP-0005 section 4.3 items 1-4, never from the generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const COMMON = "https://schemas.8005-agv.local/agv-full-product/v4/common/types.schema.json#/$defs/";
const COMMAND = "SlotFaultDeclarationCommand";
const RESULT = "SlotFaultDeclarationResult";
// protocol-v2.0.0 released 58 codes; everything after them is new in 3.0.0.
const RELEASED_CODE_COUNT = 58;

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-slot-fault-declaration-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));
const schemaOf = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`);
const validOf = (messageType) => readJson(`examples/valid/${messageType}/V-${messageType}-MIN-001.json`);
const ref = (name) => ({ $ref: `${COMMON}${name}` });

// Both messages are RELIABLE: written durably before send, acknowledged only once durable, replayed on
// reconnect (CP-0005 4.3 items 1-2). Neither is a response, so correlationId stays null and the
// declaration is matched by declarationId alone.
for (const [messageType, direction, recoveryRole] of [
  [COMMAND, "C_TO_O", "SLOT_FAULT_DECLARATION"],
  [RESULT, "O_TO_C", "PENDING_RESULT_REPLAY"],
]) {
  test(`${messageType} is ${direction}, RELIABLE, durable on both ends, deduplicated by declarationId, with a null correlationId`, () => {
    const entry = readJson("manifest/release.json").messages[messageType];
    assert.ok(entry, `${messageType} missing from the manifest`);
    assert.equal(entry.direction, direction);
    assert.equal(entry.deliveryClass, "RELIABLE");
    assert.equal(entry.durableBeforeSend, true);
    assert.equal(entry.durableBeforeAck, true);
    assert.deepEqual(entry.businessDedupKeys, ["declarationId"]);
    assert.equal(entry.correlationRule, "MUST_BE_NULL");
    assert.equal(entry.recoveryRole, recoveryRole);
    assert.deepEqual(schemaOf(messageType).properties.correlationId, { type: "null" });
    assert.equal(validOf(messageType).correlationId, null);
    const negative = readJson(`examples/invalid/${messageType}/I-${messageType}-CORRELATION-001.json`);
    assert.equal(typeof negative.message.correlationId, "string");
    assert.deepEqual(negative.expected, { code: "CORRELATION_INVALID", fieldPath: "/correlationId", rule: "semantic-correlation" });
  });
}

test("SlotFaultDeclarationCommand carries exactly the nine fields of CP-0005 4.3 item 1, each with its type", () => {
  const payload = schemaOf(COMMAND).properties.payload;
  const expected = {
    declarationId: ref("Id"),
    demandId: ref("Id"),
    slotOperationAttemptId: ref("Id"),
    slotNo: ref("SlotNo"),
    administrator: ref("OperatorContext"),
    administratorRole: { type: "string", enum: ["MAINTENANCE_ADMINISTRATOR", "SYSTEM_ADMINISTRATOR"] },
    faultCategory: { type: "string", enum: ["LOCK", "LIGHT_CURTAIN", "DOOR_MECHANISM", "IO_MODULE"] },
    note: { type: "string", minLength: 1 },
    declaredAt: ref("Instant"),
  };
  assert.deepEqual(payload.properties, expected);
  assert.deepEqual(payload.required, Object.keys(expected));
  assert.equal(payload.additionalProperties, false);
  // Same role vocabulary as the recovery session request, not a copy that could drift.
  assert.deepEqual(payload.properties.administratorRole, schemaOf("ExceptionRecoverySessionRequested").properties.payload.properties.administratorRole);
});

test("SlotFaultDeclarationResult carries declarationId, slotOperationAttemptId, outcome and a nullable problem", () => {
  const payload = schemaOf(RESULT).properties.payload;
  const expected = {
    declarationId: ref("Id"),
    slotOperationAttemptId: ref("Id"),
    outcome: { type: "string", enum: ["APPLIED", "NOT_APPLICABLE"] },
    problem: { anyOf: [ref("Problem"), { type: "null" }] },
  };
  assert.deepEqual(payload.properties, expected);
  assert.deepEqual(payload.required, Object.keys(expected));
  assert.equal(payload.additionalProperties, false);
});

test("problem is non-null exactly when outcome is NOT_APPLICABLE, stated as if/then/else on the payload", () => {
  const payload = schemaOf(RESULT).properties.payload;
  assert.deepEqual(payload.if, { properties: { outcome: { const: "NOT_APPLICABLE" } }, required: ["outcome"] });
  assert.deepEqual(payload.then, { properties: { problem: { type: "object" } } });
  assert.deepEqual(payload.else, { properties: { problem: { type: "null" } } });
});

// G1 runs every example through ajv, but only in a protocol clone. This evaluates the one conditional
// the Result carries, read from the generated schema, so a sampler that forgets its special case (and
// writes an APPLIED example with a problem object) is caught here.
const typeOf = (value) => (value === null ? "null" : Array.isArray(value) ? "array" : typeof value);
const satisfiesProperties = (clause, value) => Object.entries(clause.properties ?? {}).every(([key, rule]) => {
  if (!(key in value)) return true;
  if ("const" in rule) return value[key] === rule.const;
  return typeOf(value[key]) === rule.type;
});
const conditionalHolds = (payloadSchema, payload) => {
  const matchesIf = (payloadSchema.if.required ?? []).every((key) => key in payload) && satisfiesProperties(payloadSchema.if, payload);
  return satisfiesProperties(matchesIf ? payloadSchema.then : payloadSchema.else, payload);
};

test("the minimal valid SlotFaultDeclarationResult satisfies its own outcome/problem correspondence", () => {
  const payloadSchema = schemaOf(RESULT).properties.payload;
  const payload = validOf(RESULT).payload;
  assert.deepEqual(Object.keys(payload), payloadSchema.required);
  assert.ok(payloadSchema.properties.outcome.enum.includes(payload.outcome), `outcome ${payload.outcome}`);
  assert.ok(conditionalHolds(payloadSchema, payload), `valid example violates its schema: ${JSON.stringify(payload)}`);
});

// A negative must break the valid example at one place and nowhere else, or G1's "rejected" says
// nothing about the rule it is named for.
const withoutProblemAndOutcome = ({ outcome, problem, ...rest }) => rest;
const problemShape = (value) => typeOf(value) === "object" && typeof value.reasonCode === "string" && "fieldPath" in value && "displayMessage" in value;
for (const [suffix, isBroken] of [
  ["IF-THEN-problem-NOT_APPLICABLE", (payload) => payload.outcome === "NOT_APPLICABLE" && payload.problem === null],
  ["IF-THEN-problem-APPLIED", (payload) => payload.outcome === "APPLIED" && problemShape(payload.problem)],
]) {
  test(`if-then negative ${suffix} breaks only the outcome/problem pair and is rejected by the conditional`, () => {
    const valid = validOf(RESULT);
    const vectorId = `I-${RESULT}-${suffix}`;
    const file = `examples/invalid/${RESULT}/${vectorId}.json`;
    assert.ok(fs.existsSync(path.join(tree, file)), `${file} was not generated`);
    const negative = readJson(file);
    assert.equal(negative.vectorId, vectorId);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/problem", rule: "if-then" });
    const { payload: brokenPayload, ...brokenEnvelope } = negative.message;
    const { payload: validPayload, ...validEnvelope } = valid;
    assert.deepEqual(brokenEnvelope, validEnvelope);
    assert.deepEqual(withoutProblemAndOutcome(brokenPayload), withoutProblemAndOutcome(validPayload));
    assert.ok(isBroken(brokenPayload), `broken payload: ${JSON.stringify(brokenPayload)}`);
    assert.equal(conditionalHolds(schemaOf(RESULT).properties.payload, brokenPayload), false, "the conditional accepts the negative");
  });
}

test("SLOT_FAULT_DECLARED is appended after the 2.0.0 codes, introduced in 3.0.0 and narrowed to OperationResult", () => {
  const { codes } = readJson("errors/error-codes.json");
  const index = codes.findIndex((entry) => entry.code === "SLOT_FAULT_DECLARED");
  assert.ok(index >= RELEASED_CODE_COUNT, `SLOT_FAULT_DECLARED at ${index}, inside the released segment`);
  const entry = codes[index];
  assert.equal(entry.introducedInRelease, "3.0.0");
  assert.deepEqual(entry.allowedMessageTypes, ["OperationResult"]);
  assert.equal(entry.category, "SAFETY_RECOVERY");
  assert.equal(entry.retryDisposition, "MANUAL_REVIEW");
  assert.match(entry.meaning, /SlotResult\.reasonCodes/);
  assert.match(entry.meaning, /\(REQ-0359[^)]*\)\.$/);
  assert.ok(readJson("schemas/common/types.schema.json").$defs.ErrorCode.enum.includes("SLOT_FAULT_DECLARED"));
});

// The vector names freeze with the candidate package; both implementations name a test after each.
const vectors = {
  "CV-SLOT-FAULT-DECLARATION-APPLIED": {
    // The vehicle records and sends its APPLIED result at the moment it decides to abort, then settles
    // the operation: SlotFaultDeclarationResult strictly before OperationResult.
    messages: [COMMAND, RESULT, "OperationResult", "DurableAck"],
    stableErrorCode: "SLOT_FAULT_DECLARED",
    controlServer: ["DECLARE_ONLY_ON_OVERDUE_SLOT_AWAITING_OPERATOR", "AUDIT_DECLARATION_AND_VEHICLE_RESULT", "BLOCK_JOURNEY_ON_DECLARED_UNKNOWN"],
    onboardHmi: ["APPLY_ONLY_TO_SAME_ATTEMPT_AND_SLOT_STILL_AWAITING", "NEVER_UNLOCK_AFTER_DECLARATION_APPLIED", "REPORT_DECLARED_SLOT_UNKNOWN_LATER_SLOTS_NOT_STARTED", "SEND_DECLARATION_RESULT_BEFORE_OPERATION_RESULT"],
    forbidden: ["unlock-after-declaration", "declaration-settles-business-or-cancels-demand"],
  },
  "CV-SLOT-FAULT-DECLARATION-NOT-APPLICABLE": {
    messages: [COMMAND, RESULT, "DurableAck"],
    stableErrorCode: "ACTION_NOT_ALLOWED_IN_STATE",
    controlServer: ["DECLARE_ONLY_ON_OVERDUE_SLOT_AWAITING_OPERATOR", "AUDIT_DECLARATION_AND_VEHICLE_RESULT", "WITHDRAW_DECLARATION_WITHOUT_BUSINESS_CHANGE"],
    onboardHmi: ["REJECT_DECLARATION_ON_SETTLED_UNKNOWN_OR_SUPERSEDED_ATTEMPT", "NEVER_APPLY_DECLARATION_TO_ANOTHER_ATTEMPT_OR_SLOT"],
    forbidden: ["unlock-after-declaration", "declaration-settles-business-or-cancels-demand", "business-state-changed-by-rejected-declaration"],
  },
};

for (const [vectorId, expectation] of Object.entries(vectors)) {
  test(`${vectorId} runs ${expectation.messages.join(" -> ")} with stable error code ${expectation.stableErrorCode}`, () => {
    const expected = readJson(`vectors/${vectorId}/expected.json`);
    assert.equal(expected.vectorId, vectorId);
    assert.deepEqual(expected.orderedExpectedMessages, expectation.messages);
    assert.equal(expected.stableErrorCode, expectation.stableErrorCode);
    const steps = fs.readFileSync(path.join(tree, `vectors/${vectorId}/input.ndjson`), "utf8").trim().split("\n").map((line) => JSON.parse(line));
    assert.deepEqual(steps.map((step) => step.messageType), expectation.messages);
    assert.equal(steps[0].action, "send");
  });

  test(`${vectorId} states the product assertions of both sides and forbids unlocking or settling on a declaration`, () => {
    const expected = readJson(`vectors/${vectorId}/expected.json`);
    assert.deepEqual(expected.productAssertions, { controlServer: expectation.controlServer, onboardHmi: expectation.onboardHmi });
    const missing = expectation.forbidden.filter((effect) => !expected.forbiddenSideEffects.includes(effect));
    assert.deepEqual(missing, []);
  });
}

test("FP-IS-07 binds both declaration vectors and names SlotFaultDeclarationCommand among its wire messages", () => {
  const slice = readJson("integration-slices/index.json").slices.find((entry) => entry.integrationSliceId === "FP-IS-07");
  for (const vectorId of Object.keys(vectors)) assert.ok(slice.vectorIds.includes(vectorId), `${vectorId} not bound to FP-IS-07`);
  assert.ok(slice.definition.authorityModel.wireMessages.includes(COMMAND));
  assert.ok(slice.definition.requiredOutcomes.includes("SLOT_FAULT_DECLARATION_APPLIED_ONLY_TO_AWAITING_SLOT"));
});
