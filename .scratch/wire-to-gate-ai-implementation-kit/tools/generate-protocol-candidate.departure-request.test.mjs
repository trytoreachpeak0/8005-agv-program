// Acceptance checks for the operator's departure request, the charging-required departure and the staging cargo-holding
// deadline in the protocol 4.0.0 candidate (8005-agv-protocol#13, #15 and #17; program#185 CP-0012, program#188 CP-0013 and
// program#191 CP-0014, section 3 of each).
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
const COMMON = "https://schemas.8005-agv.local/agv-full-product/v6/common/types.schema.json#/$defs/";
const REQUEST = "CurrentStopDepartureRequested";
const RESULT = "CurrentStopDepartureResult";
const DEFAULT_SIDE_EFFECTS = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];
// The three machine pickup departures of protocol#17 (CP-0014 section 3 item 4, point 6).
const MACHINE_HOLDING = "CV-CURRENT-STOP-DEPARTURE-MACHINE-CARGO-HOLDING";
const MACHINE_STATION_WAIT = "CV-CURRENT-STOP-DEPARTURE-MACHINE-STATION-WAIT";
const MACHINE_INCOMPLETE = "CV-CURRENT-STOP-DEPARTURE-MACHINE-LOADING-INCOMPLETE";
const MACHINE_VECTORS = [MACHINE_HOLDING, MACHINE_STATION_WAIT, MACHINE_INCOMPLETE];
const DEPARTURE_VECTORS = ["CV-CURRENT-STOP-DEPARTURE-ACCEPTED", "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION", "CV-CURRENT-STOP-DEPARTURE-NOT-ALLOWED", "CV-CURRENT-STOP-DEPARTURE-STATION-MISMATCH", "CV-CURRENT-STOP-DEPARTURE-DUPLICATE-REQUEST", ...MACHINE_VECTORS];
const CHARGING_VECTOR = "CV-STAGING-CHARGING-REQUIRED-DEPARTURE-WITH-CARGO";
// The staging cargo-holding deadline of protocol#17 (CP-0014 section 3 item 4, points 3 and 4).
const STAGING_DEADLINE_MOVED = "CV-STAGING-CARGO-HOLDING-DEADLINE-MOVED";
const STAGING_TIMEOUT = "CV-STAGING-CARGO-HOLDING-TIMEOUT";
const STAGING_HOLDING_VECTORS = [STAGING_DEADLINE_MOVED, STAGING_TIMEOUT];
// Every side effect and product assertion that confined the departure to the staging station before CP-0014.
const STAGING_ONLY_NAMES = ["departure-accepted-at-a-machine-pickup-stop", "ACCEPT_DEPARTURE_ONLY_AT_STAGING_PICKUP_STOP", "OFFER_DEPART_ONLY_AT_STAGING_PICKUP_STOP", "REJECT_DEPARTURE_OUTSIDE_STAGING_PICKUP_STOP"];
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
  // activePurpose takes no new value: the charging-required departure stays TRANSPORT.
  assert.deepEqual(payloadSchemaOf("VehicleBusinessStateSnapshot").properties.activePurpose.anyOf[0].enum, ["TRANSPORT", "CHARGING", "CLEARING_MAINTENANCE", "IDLE_RETURN"]);
});

test("a transport snapshot below the mandatory charge line closed with CHARGING_REQUIRED is valid as it stands", () => {
  // Deliver first, charge afterwards (protocol#15): the departing vehicle keeps TRANSPORT and is not charging yet.
  const business = validOf("VehicleBusinessStateSnapshot").payload;
  const value = { ...business, activePurpose: "TRANSPORT", batteryState: "MANDATORY_CHARGE", chargingCycleState: "NOT_CHARGING", loadingPhase: { state: "CLOSED", cargoHoldingDeadlineAt: null, closedReason: "CHARGING_REQUIRED" } };
  assert.equal(accepts("VehicleBusinessStateSnapshot", value), true);
});

// --- vectors and slices ---

test("eight departure vectors cover acceptance, a stale revision, a refused state, another stop, a duplicate request and the three machine pickup cases", () => {
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
  assert.equal(expected["CV-CURRENT-STOP-DEPARTURE-STATION-MISMATCH"].stableErrorCode, "STATION_MISMATCH");
  assert.ok(expected["CV-CURRENT-STOP-DEPARTURE-STATION-MISMATCH"].productAssertions.controlServer.includes("CHECK_STATION_BEFORE_WORKLIST_REVISION"));
  const duplicate = expected["CV-CURRENT-STOP-DEPARTURE-DUPLICATE-REQUEST"];
  assert.equal(duplicate.orderedExpectedMessages.filter((type) => type === REQUEST).length, 2);
  assert.equal(duplicate.orderedExpectedMessages.filter((type) => type === RESULT).length, 2);
  assert.ok(duplicate.forbiddenSideEffects.includes("second-departure-on-duplicate-request"));
  assert.ok(duplicate.productAssertions.controlServer.includes("DEDUPLICATE_DEPARTURE_ON_REQUEST_ID"));
});

// CP-0014 (program#191) section 3 item 4, point 1: a machine pickup stop accepts the departure too, once its committed loads
// are complete with a basket on board. No vector may still say the departure is confined to the staging station.
test("no vector confines the departure to the staging station any longer", () => {
  for (const vectorId of [...DEPARTURE_VECTORS, CHARGING_VECTOR, ...STAGING_HOLDING_VECTORS]) {
    const value = expectedOf(vectorId);
    const names = [...value.forbiddenSideEffects, ...value.productAssertions.controlServer, ...value.productAssertions.onboardHmi];
    for (const name of STAGING_ONLY_NAMES) assert.ok(!names.includes(name), `${vectorId} still carries ${name}`);
  }
  const refused = expectedOf("CV-CURRENT-STOP-DEPARTURE-NOT-ALLOWED");
  assert.ok(refused.productAssertions.controlServer.includes("REJECT_DEPARTURE_DURING_SLOT_OPERATION_OR_CORRECTION"));
  assert.ok(refused.forbiddenSideEffects.includes("departure-during-slot-operation-or-correction"));
});

test("a machine pickup stop in cargo-holding wait accepts the departure as the cargo-holding deadline expiring now", () => {
  // Point 2: the phase closes with OPERATOR_DEPARTED, the appended stops not yet loaded go back as on a cargo-holding
  // timeout, and the vehicle leaves at once through the DEPARTURE check without waiting out the station deadline.
  const value = expectedOf(MACHINE_HOLDING);
  assert.equal(value.stableErrorCode, null);
  assert.deepEqual(value.orderedExpectedMessages.slice(0, 4), [REQUEST, "DurableAck", RESULT, "DurableAck"]);
  assert.ok(value.orderedExpectedMessages.includes("VehicleBusinessStateSnapshot"), "the closed loading phase is published");
  assert.ok(value.orderedExpectedMessages.includes("UpcomingStopPlanSnapshot"), "the released appended stops leave the plan");
  // Every committed load of this stop is complete, so nothing at the current stop is released and no empty worklist goes out.
  assert.ok(!value.orderedExpectedMessages.includes("CurrentStopWorklistSnapshot"), "the current stop sends no worklist");
  assert.deepEqual(value.orderedExpectedMessages.slice(-2), ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"]);
  for (const assertion of ["ACCEPT_DEPARTURE_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE", "TREAT_DEPARTURE_AS_CARGO_HOLDING_DEADLINE_EXPIRING_NOW", "CLOSE_LOADING_PHASE_WITH_OPERATOR_DEPARTED", "RELEASE_UNLOADED_APPENDED_STOPS_AS_ON_CARGO_HOLDING_TIMEOUT", "KEEP_LOADED_DEMANDS_ON_JOURNEY", "END_STOP_WITHOUT_WAITING_OUT_STATION_DEPARTURE_DEADLINE", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK"]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  for (const effect of ["departure-cancels-or-suppresses-unloaded-demand", "departure-counts-against-station-timeout-release-limit", "departure-waits-out-station-departure-deadline", "departure-bypasses-correction-gate-or-safety-check", "loaded-demand-released-on-departure"]) assert.ok(value.forbiddenSideEffects.includes(effect), effect);
  assert.ok(value.productAssertions.onboardHmi.includes("OFFER_DEPART_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE"));
  assert.match(value.finalState.business, /OPERATOR_DEPARTED/);
});

test("a machine pickup stop with only the station departure wait left accepts the departure and keeps its closedReason", () => {
  // Point 2: the loading phase has already ended (full, a zone that forbids en-route appends, holding expired), so the
  // departure only ends the station departure wait; loadingPhase and its closedReason stay as they were.
  const value = expectedOf(MACHINE_STATION_WAIT);
  assert.equal(value.stableErrorCode, null);
  assert.deepEqual(value.orderedExpectedMessages.slice(0, 4), [REQUEST, "DurableAck", RESULT, "DurableAck"]);
  assert.ok(!value.orderedExpectedMessages.includes("VehicleBusinessStateSnapshot"), "the loading phase does not change");
  assert.deepEqual(value.orderedExpectedMessages.slice(-2), ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"]);
  for (const assertion of ["ACCEPT_DEPARTURE_AT_MACHINE_PICKUP_STOP_ONCE_COMMITTED_LOADS_COMPLETE", "KEEP_LOADING_PHASE_AND_CLOSED_REASON_ON_DEPARTURE", "END_STOP_WITHOUT_WAITING_OUT_STATION_DEPARTURE_DEADLINE", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK"]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  for (const effect of ["closed-reason-rewritten-by-departure", "departure-waits-out-station-departure-deadline", "departure-bypasses-correction-gate-or-safety-check"]) assert.ok(value.forbiddenSideEffects.includes(effect), effect);
  assert.match(value.finalState.business, /CLOSED_REASON_UNCHANGED/);
});

test("a machine pickup stop refuses the departure before its committed loads are complete", () => {
  const value = expectedOf(MACHINE_INCOMPLETE);
  assert.equal(value.stableErrorCode, "ACTION_NOT_ALLOWED_IN_STATE");
  assert.deepEqual(value.orderedExpectedMessages, [REQUEST, "DurableAck", RESULT, "DurableAck"]);
  for (const assertion of ["REJECT_DEPARTURE_AT_MACHINE_PICKUP_STOP_BEFORE_COMMITTED_LOADS_COMPLETE", "REJECT_DEPARTURE_AT_MACHINE_PICKUP_STOP_WITH_NOTHING_LOADED", "CHANGE_NOTHING_ON_REJECTED_DEPARTURE"]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  for (const effect of ["departure-accepted-before-committed-loads-complete", "business-state-changed-by-rejected-departure"]) assert.ok(value.forbiddenSideEffects.includes(effect), effect);
  assert.ok(value.productAssertions.onboardHmi.includes("NEVER_OFFER_DEPART_AT_MACHINE_PICKUP_STOP_BEFORE_COMMITTED_LOADS_COMPLETE"));
  assert.equal(value.finalState.business, "UNCHANGED_DEPARTURE_REJECTED");
});

// CP-0014 section 3 item 4, points 3 and 4: the staging pickup stop gains a cargo-holding deadline once cargo is on board.
test("a staging cargo-holding deadline is set by the first loaded basket and moved by each demand appended for the station", () => {
  const value = expectedOf(STAGING_DEADLINE_MOVED);
  assert.equal(value.stableErrorCode, null);
  assert.equal(value.orderedExpectedMessages.filter((type) => type === "VehicleBusinessStateSnapshot").length, 2, "set, then moved");
  // Review M2: the append opens a new stop at the same station, so it reaches the vehicle in the plan between the two
  // business snapshots; the current worklist does not change.
  assert.deepEqual(value.orderedExpectedMessages, ["VehicleBusinessStateSnapshot", "SnapshotAppliedAck", "UpcomingStopPlanSnapshot", "SnapshotAppliedAck", "VehicleBusinessStateSnapshot", "SnapshotAppliedAck"]);
  for (const assertion of ["SET_STAGING_CARGO_HOLDING_DEADLINE_ON_FIRST_LOADED_BASKET", "MOVE_STAGING_CARGO_HOLDING_DEADLINE_ON_DEMAND_APPENDED_FOR_THE_STATION", "KEEP_STAGING_CARGO_HOLDING_DEADLINE_ON_RELEASE_CANCELLATION_OR_OTHER_WORKLIST_CHANGE", "CLEAR_STAGING_CARGO_HOLDING_DEADLINE_WHEN_NO_CARGO_REMAINS"]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  for (const effect of ["cargo-holding-deadline-set-with-nothing-loaded", "cargo-holding-deadline-not-moved-on-append", "cargo-holding-deadline-moved-by-release-cancellation-or-other-worklist-change"]) assert.ok(value.forbiddenSideEffects.includes(effect), effect);
  assert.ok(value.productAssertions.onboardHmi.includes("DISPLAY_CARGO_HOLDING_COUNTDOWN_AT_STAGING_PICKUP_STOP"));
  // protocol#19: the append leaves a demand to load at this station, so the control server sends LOADING with the moved
  // deadline (LoadingPhaseMachine: pending loads -> LOADING, none -> CARGO_HOLDING_WAIT), not CARGO_HOLDING_WAIT; the
  // onboard HMI shows the countdown from cargoHoldingDeadlineAt whatever the state.
  for (const assertion of ["SEND_LOADING_WHILE_A_DEMAND_REMAINS_TO_LOAD_AT_THE_STATION", "SEND_CARGO_HOLDING_DEADLINE_IN_LOADING_AND_CARGO_HOLDING_WAIT"]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  assert.ok(value.productAssertions.onboardHmi.includes("DISPLAY_CARGO_HOLDING_COUNTDOWN_FROM_DEADLINE_NOT_FROM_STATE"));
  assert.ok(value.forbiddenSideEffects.includes("cargo-holding-wait-sent-while-a-demand-remains-to-load"));
  assert.equal(value.finalState.business, "STAGING_LOADING_WITH_CARGO_HOLDING_DEADLINE_MOVED_TO_APPEND");
  assert.doesNotMatch(JSON.stringify(value), /STAGING_CARGO_HOLDING_WAIT_DEADLINE_MOVED/);
});

test("a staging cargo-holding timeout closes with CARGO_HOLDING_TIMEOUT and ends the worklist with DEMAND_RELEASED", () => {
  const value = expectedOf(STAGING_TIMEOUT);
  assert.equal(value.stableErrorCode, null);
  assert.ok(!value.orderedExpectedMessages.includes(REQUEST), "the control server decides, not an operator");
  assert.ok(value.orderedExpectedMessages.includes("CurrentStopWorklistSnapshot"), "the released demands leave the worklist");
  assert.deepEqual(value.orderedExpectedMessages.slice(-2), ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"]);
  for (const assertion of ["CLOSE_STAGING_LOADING_PHASE_WITH_CARGO_HOLDING_TIMEOUT", "END_EMPTY_WORKLIST_WITH_DEMAND_RELEASED", "RELEASE_UNLOADED_DEMANDS_WITHOUT_CANCEL_OR_SUPPRESSION", "KEEP_LOADED_DEMANDS_ON_JOURNEY", "LET_SLOT_OPERATION_OR_CORRECTION_SETTLE_BEFORE_EXPIRY", "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK"]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  for (const effect of ["operator-departed-reason-on-cargo-holding-timeout", "cargo-holding-timeout-cancels-or-suppresses-unloaded-demand", "cargo-holding-timeout-counts-against-station-timeout-release-limit", "cargo-holding-timeout-interrupts-slot-operation-or-correction", "loaded-demand-released-on-cargo-holding-timeout"]) assert.ok(value.forbiddenSideEffects.includes(effect), effect);
  assert.match(value.finalState.business, /CARGO_HOLDING_TIMEOUT/);
});

test("the staging cargo-holding snapshots are valid as they stand, no schema change needed", () => {
  const business = validOf("VehicleBusinessStateSnapshot").payload;
  const holding = { ...business, activePurpose: "TRANSPORT", loadingPhase: { state: "CARGO_HOLDING_WAIT", cargoHoldingDeadlineAt: "2026-10-15T08:05:00Z", closedReason: null } };
  assert.equal(accepts("VehicleBusinessStateSnapshot", holding), true);
  const expired = { ...business, activePurpose: "TRANSPORT", loadingPhase: { state: "CLOSED", cargoHoldingDeadlineAt: "2026-10-15T08:05:00Z", closedReason: "CARGO_HOLDING_TIMEOUT" } };
  assert.equal(accepts("VehicleBusinessStateSnapshot", expired), true);
  assert.ok(payloadSchemaOf("CurrentStopWorklistSnapshot").properties.stopEndedReason.anyOf[0].enum.includes("DEMAND_RELEASED"));
});

test("the charging-required vector departs with cargo through the DEPARTURE check and puts no charger in the journey", () => {
  const expected = expectedOf(CHARGING_VECTOR);
  assert.equal(expected.stableErrorCode, null);
  assert.deepEqual(expected.orderedExpectedMessages.slice(-2), ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"], "the vehicle leaves through the safety check");
  assert.ok(expected.orderedExpectedMessages.includes("CurrentStopWorklistSnapshot"), "the released demands leave the worklist");
  assert.deepEqual(expected.forbiddenSideEffects.slice(0, DEFAULT_SIDE_EFFECTS.length), DEFAULT_SIDE_EFFECTS);
  for (const effect of ["charger-stop-in-transport-journey", "transport-purpose-replaced-by-charging", "loaded-demand-released-for-charging", "departure-cancels-or-suppresses-unloaded-demand", "return-to-staging-before-dropoff"]) assert.ok(expected.forbiddenSideEffects.includes(effect), effect);
  for (const assertion of ["CLOSE_LOADING_PHASE_WITH_CHARGING_REQUIRED", "RELEASE_UNLOADED_DEMANDS_WITHOUT_CANCEL_OR_SUPPRESSION", "INSERT_NO_CHARGER_STOP_IN_TRANSPORT_JOURNEY", "CHARGE_THROUGH_CHARGING_ALLOCATION_AFTER_JOURNEY_ENDS"]) assert.ok(expected.productAssertions.controlServer.includes(assertion), assertion);
  assert.ok(expected.productAssertions.onboardHmi.includes("NEVER_DEPART_LOCALLY"));
  // The withdrawn charging-stop vector is gone, not kept beside its replacement.
  assert.equal(fs.existsSync(path.join(tree, "vectors", "CV-TRANSPORT-CHARGING-STOP-WITH-CARGO")), false);
});

test("FP-IS-02 binds the departure and staging cargo-holding vectors and messages, FP-IS-13 the charging vector, and no other slice binds them", () => {
  const is02 = sliceOf("FP-IS-02");
  for (const vectorId of [...DEPARTURE_VECTORS, ...STAGING_HOLDING_VECTORS]) assert.ok(is02.vectorIds.includes(vectorId), vectorId);
  for (const messageType of [REQUEST, RESULT]) assert.ok(is02.definition.authorityModel.wireMessages.includes(messageType), messageType);
  assert.ok(is02.definition.ownerResponsibilities.controlServer.includes("DECIDE_PICKUP_DEPARTURE_ON_REQUEST"));
  assert.ok(is02.definition.ownerResponsibilities.controlServer.includes("RUN_STAGING_CARGO_HOLDING_DEADLINE"));
  assert.ok(is02.definition.ownerResponsibilities.onboardHmi.includes("REQUEST_PICKUP_DEPARTURE_WITH_OPERATOR"));
  assert.ok(is02.definition.requiredOutcomes.includes("PICKUP_DEPARTURE_ON_OPERATOR_REQUEST_RELEASES_UNLOADED_DEMANDS"));
  assert.ok(is02.definition.requiredOutcomes.includes("STAGING_CARGO_HOLDING_DEADLINE_RUNS_WITH_CARGO_ON_BOARD"));
  assert.ok(!JSON.stringify(is02.definition).includes("STAGING_DEPARTURE"), "FP-IS-02 still scopes the departure to the staging station");
  const is13 = sliceOf("FP-IS-13");
  assert.ok(is13.vectorIds.includes(CHARGING_VECTOR));
  assert.ok(is13.definition.requiredOutcomes.includes("STAGING_CARGO_DELIVERED_BEFORE_CHARGING"));
  assert.ok(!is13.definition.requiredOutcomes.includes("STAGING_CARGO_CHARGES_WITHIN_TRANSPORT_JOURNEY"));
  assert.ok(is13.definition.ownerResponsibilities.controlServer.includes("DELIVER_STAGING_CARGO_BEFORE_CHARGING"));
  const others = readJson("integration-slices/index.json").slices.filter((slice) => !["FP-IS-02", "FP-IS-13"].includes(slice.integrationSliceId));
  const stray = others.filter((slice) => slice.vectorIds.some((vectorId) => [...DEPARTURE_VECTORS, CHARGING_VECTOR, ...STAGING_HOLDING_VECTORS].includes(vectorId)));
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

test("the wire notes give staging pickup stops no station deadline, a cargo-holding deadline once loaded, and say how their stop ends", () => {
  const body = section("Staging pickup stops");
  assert.match(body, /fixed origin station of `STAGING_TO_WIRE`/);
  assert.match(body, /CP-0014 \(program#191\)/);
  assert.match(body, /`CurrentStopWorklistSnapshot\.stationDepartureDeadlineAt` is always `null` at a staging pickup stop/);
  // CP-0014 section 3 item 4, point 3: null only while nothing is loaded, then set, then moved by appended demands.
  // protocol#19: the state follows what is left to load, not the station; the deadline is independent of the state.
  assert.match(body, /`VehicleBusinessStateSnapshot\.loadingPhase\.state` is `LOADING` while a demand of this stop remains to be loaded, and `CARGO_HOLDING_WAIT` once none remains and at least one basket is loaded/);
  assert.match(body, /`cargoHoldingDeadlineAt` is `null` until a basket is loaded/);
  assert.match(body, /`cargoHoldingDeadlineAt` may be non-null in either state, `LOADING` or `CARGO_HOLDING_WAIT`: the onboard HMI shows the cargo-holding countdown from `cargoHoldingDeadlineAt` alone, never from `state`/);
  assert.match(body, /A demand appended for this station opens a new stop at it, so `state` returns to `LOADING`, carrying the moved deadline, until that demand is loaded/);
  assert.match(body, /At a machine pickup stop likewise, once the first load batch closes safely while loads committed to the stop remain, `state` is `LOADING` with `cargoHoldingDeadlineAt` already set \(ADR-cross-0057\)/);
  assert.doesNotMatch(body, /`state` `CARGO_HOLDING_WAIT` with `cargoHoldingDeadlineAt` `null` while no basket is loaded/);
  assert.doesNotMatch(body, /At a staging pickup stop `VehicleBusinessStateSnapshot\.loadingPhase` is `state` `CARGO_HOLDING_WAIT`/);
  assert.match(body, /Once a basket is loaded `cargoHoldingDeadlineAt` is set, counted from the safe closure of the load batch that put cargo on board, with the same duration as at a machine pickup stop/);
  assert.match(body, /Each demand with this station as its pickup station appended to the vehicle afterwards moves it to the time of the append plus that duration; a release, a cancellation or any other worklist change does not move it/);
  assert.match(body, /whose `cargoHoldingDeadlineAt` never moves once given/);
  // Point 4: the expiry uses the released cargo-holding timeout values.
  assert.match(body, /`closedReason` `CARGO_HOLDING_TIMEOUT`/);
  assert.match(body, /if an empty worklist is sent because of the release, it carries `stopEndedReason` `DEMAND_RELEASED`, as at a machine pickup stop/);
  assert.doesNotMatch(body, /the empty worklist then carries `stopEndedReason` `DEMAND_RELEASED`/);
  assert.match(body, /The expiry does not interrupt a running slot operation, load correction or cancellation/);
  assert.match(body, /`stopEndedReason` `OPERATOR_DEPARTED` or `CHARGING_REQUIRED`, never `DEMAND_RELEASED` and never a timeout reason/);
  assert.match(body, /When every demand of the stop is loaded the vehicle leaves as before and no empty worklist is sent/);
  assert.match(body, /if the control server sends another one after a departure, it carries `OPERATOR_DEPARTED`/);
  // The pre-CP-0014 sentences are gone.
  assert.doesNotMatch(body, /with no cargo-holding deadline\. The program#94 table gives `null` only before the first load batch closes safely or where cargo-holding wait does not apply; this is the one further case\.\n/);
  assert.doesNotMatch(body, /may be `state` `CARGO_HOLDING_WAIT` with `cargoHoldingDeadlineAt` `null` at a staging pickup stop/);
});

test("the wire notes scope the departure to staging and to loaded machine pickup stops, order its checks and say how it is answered", () => {
  const body = section("`CurrentStopDepartureRequested` and `CurrentStopDepartureResult`");
  assert.doesNotMatch(body, /only at a staging pickup stop/);
  assert.match(body, /CP-0014 \(program#191\)/);
  // CP-0014 section 3 item 4, point 1.
  assert.match(body, /accepts a departure request at a staging pickup stop, and at a machine pickup stop once every load committed to that stop is complete, at least one basket is loaded and the vehicle has not yet asked to leave, whether the vehicle is still in cargo-holding wait or its loading phase has already ended and only the station departure wait remains/);
  // Review M1: a journey that does not hold cargo never announces the end of its loading phase, so the shown state cannot
  // be what offers or refuses the departure.
  assert.match(body, /The `loadingPhase` the vehicle shows does not decide this: on a journey that does not hold cargo, because every zone the vehicle serves forbids en-route appends, it still reads the last `LOADING` sent/);
  assert.doesNotMatch(body, /\(`VEHICLE_FULL` or `CLOSED`\)/);
  assert.match(body, /`ACTION_NOT_ALLOWED_IN_STATE` when the stop accepts no departure in its present state: a machine pickup stop whose committed loads are not all complete or that has no basket loaded, a stop that is not a pickup stop, a vehicle that has already asked to leave, a running slot operation, an open load correction or a cancellation in progress/);
  // Point 2.
  assert.match(body, /At a machine pickup stop accepted in `CARGO_HOLDING_WAIT`, the departure counts as the cargo-holding deadline expiring now: `loadingPhase` is `CLOSED` with `closedReason` `OPERATOR_DEPARTED`/);
  assert.match(body, /appended stops not yet loaded are released back to dispatch as on a cargo-holding timeout/);
  assert.match(body, /Accepted after `loadingPhase` has ended, `loadingPhase` stays as it was, `closedReason` included/);
  assert.match(body, /does not wait out the rest of the station departure deadline \(`stationDepartureDeadlineAt`\), keeps no correction grace/);
  assert.match(body, /an empty worklist sent for it carries `stopEndedReason` `OPERATOR_DEPARTED`/);
  assert.match(body, /journals the request before it sends it/);
  assert.match(body, /identifies the stop by `stationId` and `worklistRevision`/);
  assert.match(body, /`operationSessionId` is `null` when that worklist carries none/);
  // The three refusals in their order: the first check that fails decides.
  const order = ["STATION_MISMATCH", "WORKLIST_REVISION_STALE", "ACTION_NOT_ALLOWED_IN_STATE"].map((code) => body.indexOf(`\`${code}\` when`));
  assert.ok(order.every((index) => index >= 0), `positions ${order}`);
  assert.deepEqual([...order].sort((a, b) => a - b), order);
  assert.match(body, /checks in this order and the first check that fails decides/);
  assert.match(body, /never cancelled or suppressed and never counted against the station-timeout release limit/);
  assert.match(body, /With at least one basket loaded, `loadingPhase` is `CLOSED` with `closedReason` `OPERATOR_DEPARTED`/);
  assert.match(body, /With nothing loaded the journey closes, `loadingPhase` is `null`/);
  assert.match(body, /replaying the stored result exactly as it was first decided, `currentWorklistRevision` included, never recomputed/);
  assert.match(body, /answered with `ProtocolProblem` carrying `BUSINESS_ID_CONTENT_CONFLICT`\. No `CurrentStopDepartureResult` is sent/);
});

test("candidate limitations do not claim the error registry changed", () => {
  const limitations = read("docs/candidate-limitations.md");
  assert.match(limitations, /the error registry is carried over unchanged/);
  assert.doesNotMatch(limitations, /the error registry and the conformance index all change/);
});

test("the wire notes deliver the cargo before charging and close the loading phase with CHARGING_REQUIRED", () => {
  const body = section("Charging required at a staging pickup stop");
  assert.match(body, /delivers its cargo first and charges afterwards/);
  assert.match(body, /at least one basket loaded and no slot operation running, a vehicle below the mandatory charge line departs as for an accepted departure/);
  assert.match(body, /`loadingPhase` is `CLOSED` with `closedReason` `CHARGING_REQUIRED`, the loaded demands stay on the journey/);
  assert.match(body, /never cancelled or suppressed and never counted against the station-timeout release limit/);
  assert.match(body, /through the correction gate and the `DEPARTURE` safety check/);
  assert.match(body, /gains no `CHARGER` leg, `activePurpose` stays `TRANSPORT` and `chargingCycleState` stays `NOT_CHARGING` while the journey lasts/);
  assert.match(body, /Once the journey ends the existing charging allocation takes the vehicle/);
  assert.match(body, /`activePurpose` becomes `CHARGING`, its moves are `NON_BUSINESS_MOVE` checks/);
  assert.match(body, /does not return to the staging station before it charges/);
  assert.match(body, /`closedReason` `CHARGING_REQUIRED` appears only with cargo on board/);
});

test("the wire notes no longer charge with cargo inside a TRANSPORT journey", () => {
  // protocol#15 withdrew the charging stop CP-0012 gave this candidate; none of its semantics may survive anywhere.
  const notes = read("docs/wire-notes.md");
  assert.doesNotMatch(notes, /## Charging with cargo within a `TRANSPORT` journey/);
  assert.doesNotMatch(notes, /takes its cargo to a charger/);
  assert.doesNotMatch(notes, /`stopPurposeCategory` `CHARGER`/);
  assert.doesNotMatch(notes, /Under `TRANSPORT` all three values of `UnableToChargeFieldConfirmationResult/);
  assert.doesNotMatch(notes, /runs `ALLOCATED`, `EN_ROUTE`, `CHARGING`, `COMPLETE`/);
});
