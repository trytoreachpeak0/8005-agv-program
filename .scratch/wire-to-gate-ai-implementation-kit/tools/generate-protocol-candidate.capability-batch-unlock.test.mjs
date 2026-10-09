// Acceptance checks for dropping CapabilitySnapshot.supportsBatchUnlock and the word batch from the
// FP-IS-04 scope in the protocol 3.0.0 candidate (8005-agv-program#148, REQ-0357, CP-0004 section 5).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.capability-batch-unlock.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written.
// Expected shapes are the released protocol-v2.0.0 tree (protocol commit 86575456), copied here as
// literals, never the generator's own values.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const COMMON = "https://schemas.8005-agv.local/agv-full-product/v4/common/types.schema.json#/$defs/";
const ref = (name) => ({ $ref: `${COMMON}${name}` });
const DROPPED = "supportsBatchUnlock";

// CapabilitySnapshot payload fields as protocol-v2.0.0 released them, minus supportsBatchUnlock, in
// release order. The only other difference is the schema base, v3 there and v4 in this candidate.
const V2_FIELDS_KEPT = {
  capabilityVersion: ref("Revision"),
  observedAt: ref("Instant"),
  slotModelVersion: { type: "string", minLength: 1 },
  activeSlotConfigurationVersion: { type: "string", minLength: 1 },
  activeSlotConfigurationFingerprint: ref("Sha256"),
  slotStates: { type: "array", items: ref("SlotState"), minItems: 8, maxItems: 8, uniqueItems: true },
  onboardJournalFormatVersion: { type: "integer", minimum: 1 },
};

// FP-IS-04 as protocol-v2.0.0 released it; only definition.scope changes.
const V2_FP_IS_04 = {
  integrationSliceId: "FP-IS-04",
  sequence: 4,
  prerequisites: ["FP-IS-03"],
  vectorIds: ["CV-DESTINATION-UNLOAD-ALL-EMPTY"],
  gates: ["G1", "CONTROL_SERVER_G2", "ONBOARD_HMI_G2", "G3"],
  definition: {
    scope: "DESTINATION_BATCH_UNLOAD",
    requiredOutcomes: ["UNLOAD_COMMITTED_ONCE", "FINAL_PHYSICAL_STATE_PROVEN_EMPTY"],
    authorityModel: { controlServerFact: "OperationSession", wireMessages: ["SlotOperationCommand", "OperationResult"], onboardMode: ["PHYSICAL_EXECUTION_AUTHORITY"] },
    ownerResponsibilities: { controlServer: ["COMMIT_UNLOAD_ONCE"], onboardHmi: ["UNLOAD_AUTHORIZED_SLOTS_ONLY", "REPORT_FINAL_PHYSICAL_STATE"] },
  },
  forbidUnclosedFailOrInconclusive: true,
};
// Named after the slice's only vector, CV-DESTINATION-UNLOAD-ALL-EMPTY.
const NEW_FP_IS_04_SCOPE = "DESTINATION_UNLOAD";

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-capability-batch-unlock-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));
const payloadSchema = () => readJson("schemas/messages/CapabilitySnapshot.schema.json").properties.payload;

test("CapabilitySnapshot payload keeps every other protocol-v2.0.0 field unchanged and drops supportsBatchUnlock", () => {
  const payload = payloadSchema();
  assert.deepEqual(payload.properties, V2_FIELDS_KEPT);
  assert.deepEqual(payload.required, Object.keys(V2_FIELDS_KEPT));
  assert.equal(payload.additionalProperties, false);
  assert.ok(!(DROPPED in payload.properties), `${DROPPED} still in properties`);
  assert.ok(!payload.required.includes(DROPPED), `${DROPPED} still required`);
});

// G1 runs every example through ajv, but only in a protocol clone. This evaluates the payload object
// against the generated schema's own properties, required and additionalProperties, so an example that
// keeps the dropped field, or a schema that tolerates it, is caught here.
const payloadViolations = (schema, payload) => [
  ...schema.required.filter((key) => !(key in payload)).map((key) => `missing ${key}`),
  ...(schema.additionalProperties === false ? Object.keys(payload).filter((key) => !(key in schema.properties)).map((key) => `additional ${key}`) : []),
];

test("the minimal valid CapabilitySnapshot has no supportsBatchUnlock and satisfies the payload schema", () => {
  const payload = readJson("examples/valid/CapabilitySnapshot/V-CapabilitySnapshot-MIN-001.json").payload;
  assert.ok(!(DROPPED in payload), `${DROPPED} still in the valid example`);
  assert.deepEqual(Object.keys(payload), Object.keys(V2_FIELDS_KEPT));
  assert.deepEqual(payloadViolations(payloadSchema(), payload), []);
});

test("a CapabilitySnapshot that still carries supportsBatchUnlock is rejected as an additional property", () => {
  const payload = { ...readJson("examples/valid/CapabilitySnapshot/V-CapabilitySnapshot-MIN-001.json").payload, [DROPPED]: false };
  assert.deepEqual(payloadViolations(payloadSchema(), payload), [`additional ${DROPPED}`]);
});

test("the two per-field negatives for supportsBatchUnlock are no longer produced", () => {
  const produced = fs.readdirSync(path.join(tree, "examples/invalid/CapabilitySnapshot"));
  assert.deepEqual(produced.filter((name) => name.includes(DROPPED)), []);
  // The loop that produced them still runs for the kept fields.
  for (const field of Object.keys(V2_FIELDS_KEPT)) {
    assert.ok(produced.includes(`I-CapabilitySnapshot-REQUIRED-PAYLOAD-${field}.json`), `REQUIRED-PAYLOAD-${field} missing`);
    assert.ok(produced.includes(`I-CapabilitySnapshot-TYPE-${field}.json`), `TYPE-${field} missing`);
  }
});

test(`FP-IS-04 scope is ${NEW_FP_IS_04_SCOPE} and the rest of the slice is protocol-v2.0.0 verbatim`, () => {
  const slice = readJson("integration-slices/index.json").slices.find((entry) => entry.integrationSliceId === "FP-IS-04");
  assert.ok(slice, "FP-IS-04 missing");
  assert.deepEqual(slice, { ...V2_FP_IS_04, definition: { ...V2_FP_IS_04.definition, scope: NEW_FP_IS_04_SCOPE } });
  assert.doesNotMatch(slice.definition.scope, /BATCH/);
});
