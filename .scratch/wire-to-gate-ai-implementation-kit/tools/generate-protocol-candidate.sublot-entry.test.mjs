// Acceptance checks for sublot entry scoped to the dispatch (8005-agv-program#92).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.sublot-entry.test.mjs
// Same seam as the identity checks: generate a tree through the command line and read what was
// written. Expected shapes come from the ticket's table, not from the generator's field helpers.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { isDeepStrictEqual } from "node:util";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-sublot-entry-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));
const messageSchema = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`);
const payloadSchema = (messageType) => messageSchema(messageType).properties.payload;

test("SublotEntryRequested offers the dispatch scope as expectedSublots and names no demand", () => {
  const payload = payloadSchema("SublotEntryRequested");
  assert.equal("demandId" in payload.properties, false);
  assert.equal("expectedSublot" in payload.properties, false);
  assert.ok(payload.required.includes("expectedSublots"), "expectedSublots is not required");
  const scope = payload.properties.expectedSublots;
  assert.equal(scope.type, "array");
  assert.equal(scope.items.type, "string");
  assert.equal(scope.minItems, 1);
  assert.equal(scope.maxItems, 8);
  assert.equal(scope.uniqueItems, true);
});

test("SublotSubmitted reports only what was scanned and leaves the demand to the control server", () => {
  const payload = payloadSchema("SublotSubmitted");
  assert.equal("demandId" in payload.properties, false);
  assert.equal(payload.required.includes("demandId"), false);
  for (const field of ["operationSessionId", "stationId", "worklistRevision", "sublot", "entryMethod", "operator"]) {
    assert.ok(payload.required.includes(field), `${field} is no longer required`);
  }
});

test("SublotRejected names the rejected SUBLOT and a demand that is null when the SUBLOT is out of scope", () => {
  const payload = payloadSchema("SublotRejected");
  assert.ok(payload.required.includes("demandId"), "demandId is not required");
  const demand = payload.properties.demandId;
  assert.ok(Array.isArray(demand.anyOf), "demandId is not a union");
  assert.equal(demand.anyOf.length, 2);
  const [original, nothing] = demand.anyOf;
  assert.match(original.$ref ?? "", /\/common\/types\.schema\.json#\/\$defs\/Id$/, "the non-null branch is not the original Id type");
  assert.deepEqual(nothing, { type: "null" });
  assert.ok(payload.required.includes("rejectedSublot"), "rejectedSublot is not required");
  assert.equal(payload.properties.rejectedSublot.type, "string");
});

test("the three Sublot schemas still refuse unknown fields in the envelope and in the payload", () => {
  for (const messageType of ["SublotEntryRequested", "SublotSubmitted", "SublotRejected"]) {
    const schema = messageSchema(messageType);
    assert.equal(schema.additionalProperties, false, `${messageType} envelope`);
    assert.equal(schema.properties.payload.additionalProperties, false, `${messageType} payload`);
  }
});

test("each Sublot message's businessDedupKeys names only fields its payload still carries", () => {
  const messages = readJson("manifest/release.json").messages;
  for (const messageType of ["SublotEntryRequested", "SublotSubmitted", "SublotRejected"]) {
    const keys = messages[messageType].businessDedupKeys;
    assert.ok(Array.isArray(keys), `${messageType} businessDedupKeys is not a list`);
    const fields = Object.keys(payloadSchema(messageType).properties);
    assert.deepEqual(keys.filter((key) => !fields.includes(key)), [], messageType);
  }
});

// A business id content conflict as both ends judge it: every businessDedupKeys value agrees and the
// payload does not. An empty key list declares no business identity, so it can never conflict.
const conflicts = (keys, first, second) =>
  keys.length > 0 && keys.every((key) => isDeepStrictEqual(first[key], second[key])) && !isDeepStrictEqual(first, second);
const judge = (messageType, first, second) => {
  const fields = Object.keys(payloadSchema(messageType).properties).sort();
  for (const payload of [first, second]) assert.deepEqual(Object.keys(payload).sort(), fields, `${messageType} scenario does not match its schema`);
  return conflicts(readJson("manifest/release.json").messages[messageType].businessDedupKeys, first, second);
};
const SESSION = "00000000-0000-4000-8000-000000000101";
const DEMAND = "00000000-0000-4000-8000-000000000201";
const problem = (reasonCode) => ({ reasonCode, fieldPath: null, displayMessage: null });

test("rescanning the same SUBLOT under one worklistRevision never makes the second SublotSubmitted a business id conflict", () => {
  const scanned = { operationSessionId: SESSION, stationId: "STATION-001", worklistRevision: 4, sublot: "SUBLOT-A", entryMethod: "SCANNER", operator: { operatorId: "OP-1", verificationMethod: "SESSION", verifiedAt: "2026-09-15T09:00:00Z" } };
  const typedIn = { ...scanned, entryMethod: "KEYBOARD", operator: { ...scanned.operator, verifiedAt: "2026-09-15T09:00:30Z" } };
  assert.equal(judge("SublotSubmitted", scanned, typedIn), false);
  assert.equal(judge("SublotSubmitted", scanned, { ...scanned, sublot: "SUBLOT-B" }), false, "a second SUBLOT in the same session");
});

test("rejecting a rescanned SUBLOT again never makes the second SublotRejected a business id conflict", () => {
  // BR-013 revalidates on every entry against live lookups, so the reason may change between scans.
  const first = { demandId: DEMAND, operationSessionId: SESSION, problem: problem("PACKAGE_CAPACITY_UNRESOLVED"), currentWorklistRevision: 4, rejectedSublot: "SUBLOT-A" };
  const second = { ...first, problem: problem("SUBLOT_BOX_COUNT_UNAVAILABLE") };
  assert.equal(judge("SublotRejected", first, second), false);
  // Out of scope there is no demand to name: two different SUBLOTs both carry demandId null.
  const outOfScope = { demandId: null, operationSessionId: SESSION, problem: problem("SUBLOT_NOT_IN_DISPATCH_SCOPE"), currentWorklistRevision: 4, rejectedSublot: "SUBLOT-X" };
  assert.equal(judge("SublotRejected", outOfScope, { ...outOfScope, rejectedSublot: "SUBLOT-Y" }), false, "two out-of-scope SUBLOTs");
});

test("SublotEntryRequested is identified by its worklistRevision within the operation session", () => {
  const request = { operationSessionId: SESSION, stationId: "STATION-001", worklistRevision: 4, expectedSublots: ["SUBLOT-A", "SUBLOT-B"], entryMethods: ["SCANNER", "KEYBOARD"], expiresOnRevisionChange: true };
  // The request expires on a revision change, so a new revision may carry a different scope...
  assert.equal(judge("SublotEntryRequested", request, { ...request, worklistRevision: 5, expectedSublots: ["SUBLOT-B"] }), false);
  // ...but one revision offers one scope, and a different scope under it is a real conflict.
  assert.equal(judge("SublotEntryRequested", request, { ...request, expectedSublots: ["SUBLOT-B"] }), true);
});
