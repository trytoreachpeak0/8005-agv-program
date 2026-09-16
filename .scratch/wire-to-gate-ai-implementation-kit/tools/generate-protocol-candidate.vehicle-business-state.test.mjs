// Acceptance checks for VehicleBusinessStateSnapshot in the protocol 2.0.0 candidate (8005-agv-program#94).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.vehicle-business-state.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written.
// Expected values come from the ticket and from full-product ticket 06's B5 table
// (.scratch/8005-full-product/issues/06-answer.md), never from the generator's own literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const toolsDirectory = path.dirname(fileURLToPath(import.meta.url));
const generatorPath = path.join(toolsDirectory, "generate-protocol-candidate.mjs");
const MESSAGE = "VehicleBusinessStateSnapshot";

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-vehicle-business-state-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));
const payloadSchema = () => readJson(`schemas/messages/${MESSAGE}.schema.json`).properties.payload;

test("batteryState appends MANDATORY_CHARGE, chargingCycleState carries the seven B5 values, manualChargingHold stays a required boolean", () => {
  const payload = payloadSchema();
  assert.deepEqual(payload.properties.batteryState, { type: "string", enum: ["SUFFICIENT", "LOW", "UNKNOWN", "MANDATORY_CHARGE"] });
  assert.deepEqual(payload.properties.chargingCycleState, {
    type: "string",
    enum: ["NOT_CHARGING", "ALLOCATED", "EN_ROUTE", "CHARGING", "COMPLETE", "UNABLE_TO_CHARGE", "UNKNOWN"],
  });
  assert.deepEqual(payload.properties.manualChargingHold, { type: "boolean" });
  for (const field of ["batteryState", "chargingCycleState", "manualChargingHold"]) assert.ok(payload.required.includes(field), `${field} not required`);
});

// The object branch of a nullable field: the non-null option of its anyOf.
const objectBranch = (schema) => schema.anyOf?.find((option) => option.type === "object");

test("loadingPhase is required and nullable, and its object carries exactly state, cargoHoldingDeadlineAt and closedReason", () => {
  const payload = payloadSchema();
  assert.ok(payload.required.includes("loadingPhase"), "loadingPhase not required");
  const loadingPhase = payload.properties.loadingPhase;
  assert.ok(loadingPhase.anyOf?.some((option) => option.type === "null"), "loadingPhase does not admit null");
  const phase = objectBranch(loadingPhase);
  assert.ok(phase, "loadingPhase has no object branch");
  assert.equal(phase.additionalProperties, false);
  assert.deepEqual([...phase.required].sort(), ["cargoHoldingDeadlineAt", "closedReason", "state"]);
  assert.deepEqual(Object.keys(phase.properties).sort(), ["cargoHoldingDeadlineAt", "closedReason", "state"]);
  assert.deepEqual(phase.properties.state, { type: "string", enum: ["LOADING", "CARGO_HOLDING_WAIT", "VEHICLE_FULL", "CLOSED"] });
  const nonNull = (schema) => {
    assert.ok(schema.anyOf?.some((option) => option.type === "null"), "not nullable");
    return schema.anyOf.find((option) => option.type !== "null");
  };
  assert.match(nonNull(phase.properties.cargoHoldingDeadlineAt).$ref, /\/common\/types\.schema\.json#\/\$defs\/Instant$/);
  assert.deepEqual(nonNull(phase.properties.closedReason), {
    type: "string",
    enum: ["VEHICLE_FULL", "CARGO_HOLDING_TIMEOUT", "WAITING_STATION_YIELD", "PLANNED_LOADING_COMPLETE"],
  });
});

// G1 runs every valid example through ajv and requires every schema negative to be rejected, so the
// schema's behaviour is proven there; this test pins the shape both implementations will read.
test("closedReason is non-null exactly when state is CLOSED, stated as if/then/else on the loadingPhase object", () => {
  const phase = objectBranch(payloadSchema().properties.loadingPhase);
  assert.deepEqual(phase.if, { properties: { state: { const: "CLOSED" } }, required: ["state"] });
  assert.deepEqual(phase.then, { properties: { closedReason: { type: "string" } } });
  assert.deepEqual(phase.else, { properties: { closedReason: { type: "null" } } });
});

test("the minimal valid example is a transport vehicle still loading, with no closedReason", () => {
  const payload = readJson(`examples/valid/${MESSAGE}/V-${MESSAGE}-MIN-001.json`).payload;
  assert.equal(payload.activePurpose, "TRANSPORT");
  assert.equal(payload.chargingCycleState, "NOT_CHARGING");
  assert.deepEqual(Object.keys(payload.loadingPhase).sort(), ["cargoHoldingDeadlineAt", "closedReason", "state"]);
  assert.equal(payload.loadingPhase.state, "LOADING");
  assert.equal(payload.loadingPhase.closedReason, null);
});

// A negative must break the valid example at one place and nowhere else, or G1's "rejected" says
// nothing about the field it is named for.
const pointerParts = (pointer) => pointer.split("/").filter(Boolean);
const valueAt = (value, pointer) => pointerParts(pointer).reduce((current, part) => current?.[part], value);
const withoutPointer = (value, pointer) => {
  const copy = structuredClone(value);
  const parts = pointerParts(pointer);
  delete parts.slice(0, -1).reduce((current, part) => current[part], copy)[parts.at(-1)];
  return copy;
};
const STATES = ["LOADING", "CARGO_HOLDING_WAIT", "VEHICLE_FULL", "CLOSED"];
const REASONS = ["VEHICLE_FULL", "CARGO_HOLDING_TIMEOUT", "WAITING_STATION_YIELD", "PLANNED_LOADING_COMPLETE"];
const CYCLE = ["NOT_CHARGING", "ALLOCATED", "EN_ROUTE", "CHARGING", "COMPLETE", "UNABLE_TO_CHARGE", "UNKNOWN"];
const notString = (value) => value !== undefined && typeof value !== "string";
const notStringOrNull = (value) => value !== undefined && value !== null && typeof value !== "string";

// [negative id suffix, fieldPath the gate reports, rule, the region allowed to differ, what the broken value must be]
const negatives = [
  ["REQUIRED-PAYLOAD-chargingCycleState", "/payload/chargingCycleState", "required", "/payload/chargingCycleState", (payload) => !("chargingCycleState" in payload)],
  ["TYPE-chargingCycleState", "/payload/chargingCycleState", "type", "/payload/chargingCycleState", (payload) => notString(payload.chargingCycleState)],
  ["ENUM-chargingCycleState", "/payload/chargingCycleState", "enum-or-const", "/payload/chargingCycleState", (payload) => typeof payload.chargingCycleState === "string" && !CYCLE.includes(payload.chargingCycleState)],
  ["REQUIRED-PAYLOAD-loadingPhase", "/payload/loadingPhase", "required", "/payload/loadingPhase", (payload) => !("loadingPhase" in payload)],
  ["TYPE-loadingPhase", "/payload/loadingPhase", "type", "/payload/loadingPhase", (payload) => payload.loadingPhase !== null && typeof payload.loadingPhase !== "object"],
  ["REQUIRED-PAYLOAD-loadingPhase-state", "/payload/loadingPhase/state", "required", "/payload/loadingPhase/state", (payload) => !("state" in payload.loadingPhase)],
  ["REQUIRED-PAYLOAD-loadingPhase-cargoHoldingDeadlineAt", "/payload/loadingPhase/cargoHoldingDeadlineAt", "required", "/payload/loadingPhase/cargoHoldingDeadlineAt", (payload) => !("cargoHoldingDeadlineAt" in payload.loadingPhase)],
  ["REQUIRED-PAYLOAD-loadingPhase-closedReason", "/payload/loadingPhase/closedReason", "required", "/payload/loadingPhase/closedReason", (payload) => !("closedReason" in payload.loadingPhase)],
  ["TYPE-loadingPhase-state", "/payload/loadingPhase/state", "type", "/payload/loadingPhase/state", (payload) => notString(payload.loadingPhase.state)],
  ["TYPE-loadingPhase-cargoHoldingDeadlineAt", "/payload/loadingPhase/cargoHoldingDeadlineAt", "type", "/payload/loadingPhase/cargoHoldingDeadlineAt", (payload) => notStringOrNull(payload.loadingPhase.cargoHoldingDeadlineAt)],
  ["TYPE-loadingPhase-closedReason", "/payload/loadingPhase/closedReason", "type", "/payload/loadingPhase/closedReason", (payload) => notStringOrNull(payload.loadingPhase.closedReason)],
  ["ENUM-loadingPhase-state", "/payload/loadingPhase/state", "enum-or-const", "/payload/loadingPhase/state", (payload) => typeof payload.loadingPhase.state === "string" && !STATES.includes(payload.loadingPhase.state)],
  ["ENUM-loadingPhase-closedReason", "/payload/loadingPhase/closedReason", "enum-or-const", "/payload/loadingPhase/closedReason", (payload) => typeof payload.loadingPhase.closedReason === "string" && !REASONS.includes(payload.loadingPhase.closedReason)],
  ["ADDITIONAL-loadingPhase", "/payload/loadingPhase", "additionalProperties", "/payload/loadingPhase", (payload, valid) => Object.keys(payload.loadingPhase).length === Object.keys(valid.loadingPhase).length + 1],
  // The two sides of the CLOSED correspondence: a closed phase without a reason, an open phase with one.
  ["IF-THEN-loadingPhase-closedReason-CLOSED", "/payload/loadingPhase/closedReason", "if-then", "/payload/loadingPhase", (payload) => payload.loadingPhase.state === "CLOSED" && payload.loadingPhase.closedReason === null],
  ["IF-THEN-loadingPhase-closedReason-OPEN", "/payload/loadingPhase/closedReason", "if-then", "/payload/loadingPhase", (payload) => payload.loadingPhase.state !== "CLOSED" && STATES.includes(payload.loadingPhase.state) && REASONS.includes(payload.loadingPhase.closedReason)],
];

for (const [suffix, fieldPath, rule, region, isBroken] of negatives) {
  test(`automatic negative ${suffix} breaks the valid example only at ${region}`, () => {
    const valid = readJson(`examples/valid/${MESSAGE}/V-${MESSAGE}-MIN-001.json`);
    const vectorId = `I-${MESSAGE}-${suffix}`;
    const file = `examples/invalid/${MESSAGE}/${vectorId}.json`;
    assert.ok(fs.existsSync(path.join(tree, file)), `${file} was not generated`);
    const negative = readJson(file);
    assert.equal(negative.vectorId, vectorId);
    assert.deepEqual(negative.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath, rule });
    assert.deepEqual(withoutPointer(negative.message, region), withoutPointer(valid, region));
    assert.ok(isBroken(negative.message.payload, valid.payload), `broken value at ${region}: ${JSON.stringify(valueAt(negative.message, region))}`);
  });
}
