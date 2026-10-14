// Acceptance checks for the operator's departure request and charging with cargo in the protocol 4.0.0 candidate
// (8005-agv-protocol#13, program#185 CP-0012 section 3).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.departure-request.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written.
// Expected shapes come from the ticket and the released protocol-v3.0.0 tree, never from the generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const COMMON = "https://schemas.8005-agv.local/agv-full-product/v5/common/types.schema.json#/$defs/";
const REQUEST = "CurrentStopDepartureRequested";
const RESULT = "CurrentStopDepartureResult";
const DEFAULT_SIDE_EFFECTS = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];
const DEPARTURE_VECTORS = ["CV-CURRENT-STOP-DEPARTURE-ACCEPTED", "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION", "CV-CURRENT-STOP-DEPARTURE-NOT-ALLOWED", "CV-CURRENT-STOP-DEPARTURE-DUPLICATE-REQUEST"];
const CHARGING_VECTOR = "CV-TRANSPORT-CHARGING-STOP-WITH-CARGO";
// The values protocol-v3.0.0 released for the two closed enums (3f091cb2); 4.0.0 only appends.
const V3_CLOSED_REASONS = ["VEHICLE_FULL", "CARGO_HOLDING_TIMEOUT", "WAITING_STATION_YIELD", "PLANNED_LOADING_COMPLETE"];
const V3_STOP_ENDED_REASONS = ["COMPLETED", "STATION_DEADLINE_EXPIRED", "LOAD_CANCELLED", "LOAD_COMPENSATED", "CARGO_HANDED_OFF", "DEMAND_RELEASED", "TRIP_TERMINATED"];
const NEW_REASONS = ["OPERATOR_DEPARTED", "CHARGING_REQUIRED"];

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-departure-request-"));
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
const ref = (name) => ({ $ref: `${COMMON}${name}` });
const nullable = (schema) => ({ anyOf: [schema, { type: "null" }] });

// The subset of JSON Schema 2020-12 the generated message schemas use, as in the contract-corrections test. A keyword
// outside the subset throws rather than being skipped. format is not checked (G1 runs ajv-formats).
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
const problem = (reasonCode) => ({ reasonCode, fieldPath: null, displayMessage: null });

// --- the two messages ---

// The press is journaled before it is sent and the answer is durable and replayed, so neither is lost to a disconnect; a
// refusal must reach the vehicle, which a DurableAck alone ("received") never says. Neither is a response, so correlationId
// stays null and departureRequestId alone ties the two together.
for (const [messageType, direction, recoveryRole] of [
  [REQUEST, "O_TO_C", "CURRENT_STOP_DEPARTURE"],
  [RESULT, "C_TO_O", "PENDING_RESULT_REPLAY"],
]) {
  test(`${messageType} is ${direction}, RELIABLE, durable on both ends, deduplicated by departureRequestId, with a null correlationId`, () => {
    const entry = readJson("manifest/release.json").messages[messageType];
    assert.ok(entry, `${messageType} missing from the manifest`);
    assert.equal(entry.direction, direction);
    assert.equal(entry.deliveryClass, "RELIABLE");
    assert.equal(entry.durableBeforeSend, true);
    assert.equal(entry.durableBeforeAck, true);
    assert.deepEqual(entry.businessDedupKeys, ["departureRequestId"]);
    assert.equal(entry.correlationRule, "MUST_BE_NULL");
    assert.equal(entry.recoveryRole, recoveryRole);
    assert.deepEqual(schemaOf(messageType).properties.correlationId, { type: "null" });
    assert.equal(validOf(messageType).correlationId, null);
    const bundle = readJson("schemas/bundle/protocol.schema.json").oneOf.map((item) => item.$ref.split("/").at(-1));
    assert.ok(bundle.includes(`${messageType}.schema.json`), `${messageType} missing from the bundle`);
  });
}

test(`${REQUEST} carries the five fields of protocol#13, operationSessionId nullable to echo an empty worklist`, () => {
  const payload = payloadSchemaOf(REQUEST);
  assert.deepEqual(payload.required, ["departureRequestId", "operationSessionId", "stationId", "worklistRevision", "operator"]);
  assert.deepEqual(Object.keys(payload.properties), payload.required);
  assert.equal(payload.additionalProperties, false);
  assert.deepEqual(payload.properties.departureRequestId, ref("Id"));
  assert.deepEqual(payload.properties.operationSessionId, nullable(ref("Id")));
  assert.deepEqual(payload.properties.stationId, { type: "string", minLength: 1 });
  assert.deepEqual(payload.properties.worklistRevision, ref("Revision"));
  assert.deepEqual(payload.properties.operator, ref("OperatorContext"));
  // The worklist the request echoes: the same nullability, so whatever the vehicle shows it can send back.
  assert.deepEqual(payloadSchemaOf("CurrentStopWorklistSnapshot").properties.operationSessionId, nullable(ref("Id")));
  const sample = validOf(REQUEST).payload;
  assert.equal(accepts(REQUEST, sample), true);
  assert.equal(accepts(REQUEST, { ...sample, operationSessionId: null }), true, "a vehicle holding cargo behind an empty worklist must be able to depart");
});

test(`${RESULT} carries departureRequestId, outcome, a nullable problem and the current worklist revision`, () => {
  const payload = payloadSchemaOf(RESULT);
  assert.deepEqual(payload.required, ["departureRequestId", "outcome", "problem", "currentWorklistRevision"]);
  assert.deepEqual(Object.keys(payload.properties), payload.required);
  assert.deepEqual(payload.properties.outcome, { type: "string", enum: ["ACCEPTED", "REJECTED"] });
  assert.deepEqual(payload.properties.problem, nullable(ref("Problem")));
  assert.deepEqual(payload.properties.currentWorklistRevision, ref("Revision"));
});

test("problem is non-null exactly when the departure is REJECTED", () => {
  const sample = validOf(RESULT).payload;
  assert.equal(sample.outcome, "ACCEPTED");
  assert.equal(sample.problem, null);
  assert.equal(accepts(RESULT, sample), true);
  for (const code of ["WORKLIST_REVISION_STALE", "STATION_MISMATCH", "ACTION_NOT_ALLOWED_IN_STATE"]) {
    assert.equal(accepts(RESULT, { ...sample, outcome: "REJECTED", problem: problem(code) }), true, `REJECTED with ${code}`);
    assert.equal(accepts(RESULT, { ...sample, problem: problem(code) }), false, `ACCEPTED with ${code}`);
  }
  assert.equal(accepts(RESULT, { ...sample, outcome: "REJECTED" }), false, "REJECTED without a problem");
  for (const suffix of ["IF-THEN-problem-REJECTED", "IF-THEN-problem-ACCEPTED"]) {
    const negative = readJson(`examples/invalid/${RESULT}/I-${RESULT}-${suffix}.json`);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/problem", rule: "if-then" });
    assert.equal(accepts(RESULT, negative.message.payload), false, suffix);
  }
});

test("a request missing any field is a schema negative, one per field", () => {
  for (const field of payloadSchemaOf(REQUEST).required) {
    const negative = readJson(`examples/invalid/${REQUEST}/I-${REQUEST}-REQUIRED-PAYLOAD-${field}.json`);
    assert.equal(field in negative.message.payload, false, field);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: `/payload/${field}`, rule: "required" });
  }
});

test("the departure reuses released error codes and adds none", () => {
  const codes = readJson("errors/error-codes.json").codes;
  assert.equal(codes.length, 62);
  for (const code of ["WORKLIST_REVISION_STALE", "STATION_MISMATCH", "ACTION_NOT_ALLOWED_IN_STATE", "BUSINESS_ID_CONTENT_CONFLICT"]) {
    const entry = codes.find((item) => item.code === code);
    assert.ok(entry, code);
    assert.deepEqual(entry.allowedMessageTypes, ["*"], `${code} must be allowed in ${RESULT}`);
  }
});

// --- the two closed enums ---

test("closedReason and stopEndedReason keep their released values and append OPERATOR_DEPARTED and CHARGING_REQUIRED", () => {
  const phase = payloadSchemaOf("VehicleBusinessStateSnapshot").properties.loadingPhase.anyOf.find((option) => option.type === "object");
  assert.deepEqual(phase.properties.closedReason.anyOf[0].enum, [...V3_CLOSED_REASONS, ...NEW_REASONS]);
  assert.deepEqual(payloadSchemaOf("CurrentStopWorklistSnapshot").properties.stopEndedReason.anyOf[0].enum, [...V3_STOP_ENDED_REASONS, ...NEW_REASONS]);
  // activePurpose takes no new value: charging with cargo stays TRANSPORT.
  assert.deepEqual(payloadSchemaOf("VehicleBusinessStateSnapshot").properties.activePurpose.anyOf[0].enum, ["TRANSPORT", "CHARGING", "CLEARING_MAINTENANCE", "IDLE_RETURN"]);
});

test("a transport snapshot charging with cargo and a plan with a CHARGER leg are valid as they stand", () => {
  const business = validOf("VehicleBusinessStateSnapshot").payload;
  for (const chargingCycleState of ["ALLOCATED", "EN_ROUTE", "CHARGING", "COMPLETE", "UNABLE_TO_CHARGE"]) {
    const value = { ...business, activePurpose: "TRANSPORT", chargingCycleState, loadingPhase: { state: "CLOSED", cargoHoldingDeadlineAt: null, closedReason: "CHARGING_REQUIRED" } };
    assert.equal(accepts("VehicleBusinessStateSnapshot", value), true, chargingCycleState);
  }
  const plan = validOf("UpcomingStopPlanSnapshot").payload;
  const [leg] = plan.legs;
  const legs = [
    { ...leg, sequence: 1, legType: "TO_PICKUP", stopPurposeCategory: "BUSINESS", state: "COMPLETED" },
    { ...leg, movementLegId: "00000000-0000-4000-8000-0000000000a1", sequence: 2, legType: null, stopPurposeCategory: "CHARGER", demandId: null, publicStationFunction: null, state: "ACTIVE" },
    { ...leg, movementLegId: "00000000-0000-4000-8000-0000000000a2", sequence: 3, legType: "TO_DROPOFF", stopPurposeCategory: "BUSINESS", state: "PLANNED" },
  ];
  assert.equal(accepts("UpcomingStopPlanSnapshot", { ...plan, legs }), true);
});

// --- vectors and slices ---

test("four departure vectors cover acceptance, a stale revision, a refused state and a duplicate request", () => {
  const expected = Object.fromEntries(DEPARTURE_VECTORS.map((vectorId) => [vectorId, expectedOf(vectorId)]));
  for (const [vectorId, value] of Object.entries(expected)) {
    assert.equal(value.vectorId, vectorId);
    assert.equal(value.orderedExpectedMessages[0], REQUEST, `${vectorId} starts with the request`);
    assert.equal(value.orderedExpectedMessages[1], "DurableAck", `${vectorId}: the request is acknowledged as RELIABLE`);
    assert.equal(value.orderedExpectedMessages[2], RESULT, `${vectorId}: the result follows`);
    assert.deepEqual(value.forbiddenSideEffects.slice(0, DEFAULT_SIDE_EFFECTS.length), DEFAULT_SIDE_EFFECTS);
    assert.ok(value.persistenceCheckpoints.includes("departure-request-journaled-before-send"), vectorId);
    assert.ok(value.productAssertions.controlServer.length > 0 && value.productAssertions.onboardHmi.length > 0, vectorId);
  }
  assert.equal(expected["CV-CURRENT-STOP-DEPARTURE-ACCEPTED"].stableErrorCode, null);
  assert.ok(expected["CV-CURRENT-STOP-DEPARTURE-ACCEPTED"].orderedExpectedMessages.includes("VehicleBusinessStateSnapshot"));
  assert.ok(expected["CV-CURRENT-STOP-DEPARTURE-ACCEPTED"].forbiddenSideEffects.includes("departure-cancels-or-suppresses-unloaded-demand"));
  assert.ok(expected["CV-CURRENT-STOP-DEPARTURE-ACCEPTED"].productAssertions.controlServer.includes("RELEASE_UNLOADED_DEMANDS_WITHOUT_CANCEL_OR_SUPPRESSION"));
  assert.equal(expected["CV-CURRENT-STOP-DEPARTURE-STALE-REVISION"].stableErrorCode, "WORKLIST_REVISION_STALE");
  assert.equal(expected["CV-CURRENT-STOP-DEPARTURE-NOT-ALLOWED"].stableErrorCode, "ACTION_NOT_ALLOWED_IN_STATE");
  const duplicate = expected["CV-CURRENT-STOP-DEPARTURE-DUPLICATE-REQUEST"];
  assert.equal(duplicate.orderedExpectedMessages.filter((type) => type === REQUEST).length, 2);
  assert.equal(duplicate.orderedExpectedMessages.filter((type) => type === RESULT).length, 2);
  assert.ok(duplicate.forbiddenSideEffects.includes("second-departure-on-duplicate-request"));
  assert.ok(duplicate.productAssertions.controlServer.includes("DEDUPLICATE_DEPARTURE_ON_REQUEST_ID"));
});

test("the charging-with-cargo vector keeps TRANSPORT and forbids replacing it or opening a slot at the charger", () => {
  const expected = expectedOf(CHARGING_VECTOR);
  assert.equal(expected.stableErrorCode, null);
  assert.ok(expected.orderedExpectedMessages.includes("UpcomingStopPlanSnapshot"));
  assert.ok(expected.orderedExpectedMessages.filter((type) => type === "VehicleBusinessStateSnapshot").length >= 2, "the charging cycle advances across snapshots");
  for (const effect of ["transport-purpose-replaced-by-charging", "slot-operation-at-charger", "return-to-staging-before-dropoff"]) assert.ok(expected.forbiddenSideEffects.includes(effect), effect);
  assert.ok(expected.productAssertions.controlServer.includes("KEEP_TRANSPORT_PURPOSE_WHILE_CHARGING_WITH_CARGO"));
  assert.ok(expected.productAssertions.onboardHmi.includes("NEVER_LOAD_OR_OPEN_SLOT_AT_CHARGER"));
});

test("FP-IS-02 binds the departure vectors and messages, FP-IS-13 the charging vector, and no other slice binds them", () => {
  const is02 = sliceOf("FP-IS-02");
  for (const vectorId of DEPARTURE_VECTORS) assert.ok(is02.vectorIds.includes(vectorId), vectorId);
  for (const messageType of [REQUEST, RESULT]) assert.ok(is02.definition.authorityModel.wireMessages.includes(messageType), messageType);
  assert.ok(is02.definition.ownerResponsibilities.controlServer.includes("DECIDE_STAGING_DEPARTURE_ON_REQUEST"));
  assert.ok(is02.definition.ownerResponsibilities.onboardHmi.includes("REQUEST_STAGING_DEPARTURE_WITH_OPERATOR"));
  const is13 = sliceOf("FP-IS-13");
  assert.ok(is13.vectorIds.includes(CHARGING_VECTOR));
  assert.ok(is13.definition.requiredOutcomes.includes("STAGING_CARGO_CHARGES_WITHIN_TRANSPORT_JOURNEY"));
  const others = readJson("integration-slices/index.json").slices.filter((slice) => !["FP-IS-02", "FP-IS-13"].includes(slice.integrationSliceId));
  const stray = others.filter((slice) => slice.vectorIds.some((vectorId) => [...DEPARTURE_VECTORS, CHARGING_VECTOR].includes(vectorId)));
  assert.deepEqual(stray.map((slice) => slice.integrationSliceId), []);
});

// --- the wire notes carry the semantics the Schema cannot ---

const section = (heading) => {
  const notes = read("docs/wire-notes.md");
  const start = notes.indexOf(`## ${heading}\n`);
  assert.ok(start >= 0, `section ${heading} not found`);
  const end = notes.indexOf("\n## ", start + 1);
  return notes.slice(start, end < 0 ? undefined : end);
};

test("the wire notes scope the departure to the staging station and list its answers", () => {
  const body = section("`CurrentStopDepartureRequested` and `CurrentStopDepartureResult`");
  assert.match(body, /fixed origin station of `STAGING_TO_WIRE`/);
  assert.match(body, /journals the request before it sends it/);
  assert.match(body, /`operationSessionId` is `null` when that worklist carries none/);
  for (const code of ["WORKLIST_REVISION_STALE", "STATION_MISMATCH", "ACTION_NOT_ALLOWED_IN_STATE", "BUSINESS_ID_CONTENT_CONFLICT"]) assert.match(body, new RegExp(`\`${code}\``));
  assert.match(body, /never cancelled or suppressed and never counted against the station-timeout release limit/);
  assert.match(body, /`closedReason` `OPERATOR_DEPARTED`/);
  assert.match(body, /`stopEndedReason` `OPERATOR_DEPARTED`/);
});

test("the wire notes state charging with cargo under TRANSPORT and the DEPARTURE check on the anchor demand", () => {
  const body = section("Charging with cargo within a `TRANSPORT` journey");
  assert.match(body, /`activePurpose` stays `TRANSPORT`; no purpose value is added/);
  assert.match(body, /`ALLOCATED`, `EN_ROUTE`, `CHARGING`, `COMPLETE` or ends `UNABLE_TO_CHARGE`/);
  assert.match(body, /`closedReason` `CHARGING_REQUIRED`/);
  assert.match(body, /`stopPurposeCategory` `CHARGER`, `legType` `null` and `demandId` `null`/);
  assert.match(body, /opens no entry and no slot/);
  assert.match(body, /does not return to the staging station/);
  assert.match(body, /`checkPurpose` `DEPARTURE` carrying the journey's anchor demand/);
});
