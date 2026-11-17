// Acceptance checks for the machine number on the worklist in the protocol 7.0.0 candidate (8005-agv-protocol#29, tracking
// 8005-agv-program#210; the user's rulings of 2026-11-11): each CurrentStopWorklistSnapshot item carries eqp, MES's EQP as it
// is, for display on the pickup scan list and the unload list only.
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.worklist-eqp.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written. Whether each example
// really passes or fails its schema is G1's to prove on the regenerated tree; these checks pin the shapes and the examples.
// Expected values come from the ticket and the released protocol-v6.0.0 tree (protocol commit 98f17264), never from the
// generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const WORKLIST = "CurrentStopWorklistSnapshot";
const VECTOR = "CV-WORKLIST-EQP-DISPLAY-ONLY";
// The item as protocol-v6.0.0 released it (schemas/messages/CurrentStopWorklistSnapshot.schema.json at 98f17264), in order.
const V6_ITEM_FIELDS = ["demandId", "transportDemandKey", "sublot", "workType", "stopRole", "expectedBasketCount"];
const DEFAULT_FORBIDDEN = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-worklist-eqp-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative) => fs.readFileSync(path.join(tree, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const itemSchema = () => readJson(`schemas/messages/${WORKLIST}.schema.json`).properties.payload.properties.items.items;
const validOf = (suffix) => readJson(`examples/valid/${WORKLIST}/V-${WORKLIST}-${suffix}.json`);
const invalidOf = (suffix) => readJson(`examples/invalid/${WORKLIST}/I-${WORKLIST}-${suffix}.json`);
const section = (heading) => {
  const notes = read("docs/wire-notes.md");
  const start = notes.indexOf(`## ${heading}`);
  assert.ok(start >= 0, `wire-notes section ${heading} not found`);
  const next = notes.indexOf("\n## ", start + 1);
  return notes.slice(start, next < 0 ? undefined : next);
};

// --- the schema ---

test(`the ${WORKLIST} item appends eqp after the six fields protocol-v6.0.0 released and stays closed`, () => {
  const item = itemSchema();
  assert.deepEqual(Object.keys(item.properties), [...V6_ITEM_FIELDS, "eqp"]);
  assert.equal(item.additionalProperties, false);
  // Required and nullable, not optional: a missing eqp is a broken message, a null one says the demand has no EQP.
  assert.deepEqual(item.required, [...V6_ITEM_FIELDS, "eqp"]);
});

test("eqp is a non-empty string or null, with no format of its own", () => {
  // MES's EQP as it is: no pattern, enum or length cap the protocol could keep in step with MES. Empty is not a value,
  // so "no EQP" has exactly one spelling, null.
  assert.deepEqual(itemSchema().properties.eqp, { anyOf: [{ type: "string", minLength: 1 }, { type: "null" }] });
});

test(`${WORKLIST} is the only message that changes shape`, () => {
  // Every other message carries no eqp anywhere: it is a worklist display field, not a demand fact on the wire.
  const carriers = fs.readdirSync(path.join(tree, "schemas/messages"))
    .filter((file) => read(`schemas/messages/${file}`).includes('"eqp"'));
  assert.deepEqual(carriers, [`${WORKLIST}.schema.json`]);
  assert.doesNotMatch(read("schemas/common/types.schema.json"), /"eqp"/);
});

// --- examples ---

test("the minimal example carries an eqp, and a valid example with a null eqp differs from it in eqp alone", () => {
  const minimal = validOf("MIN-001");
  assert.equal(typeof minimal.payload.items[0].eqp, "string");
  assert.ok(minimal.payload.items[0].eqp.length > 0);
  const nullEqp = validOf("EQP-NULL-001");
  assert.equal(nullEqp.payload.items[0].eqp, null);
  const restored = structuredClone(nullEqp);
  restored.payload.items[0].eqp = minimal.payload.items[0].eqp;
  assert.deepEqual(restored, minimal);
});

for (const [suffix, rule, broken] of [
  ["REQUIRED-items-eqp", "required", (item) => { delete item.eqp; }],
  ["TYPE-items-eqp", "type", (item) => { item.eqp = 42; }],
  ["MIN-LENGTH-items-eqp", "minLength", (item) => { item.eqp = ""; }],
]) {
  test(`${suffix} is a schema-invalid example that breaks only eqp`, () => {
    const wrapper = invalidOf(suffix);
    assert.equal(wrapper.vectorId, `I-${WORKLIST}-${suffix}`);
    assert.deepEqual(wrapper.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/items/0/eqp", rule });
    const expected = structuredClone(validOf("MIN-001"));
    broken(expected.payload.items[0]);
    assert.deepEqual(wrapper.message, expected);
  });
}

test("the examples written for earlier releases carry eqp too", () => {
  // The 5.0.0 WIRE_TO_FULL_INSPECTION examples are the minimal one with another workType; they follow the item shape.
  assert.equal(typeof validOf("WIRE-TO-FULL-INSPECTION-001").payload.items[0].eqp, "string");
  for (const suffix of ["ENUM-items-workType-MISSPELLED", "ENUM-items-workType-LOWERCASE"]) {
    assert.equal(typeof invalidOf(suffix).message.payload.items[0].eqp, "string", suffix);
  }
});

// --- the vector ---

test(`${VECTOR} binds both implementations to display eqp and decide nothing by it`, () => {
  const expected = readJson(`vectors/${VECTOR}/expected.json`);
  assert.deepEqual(expected.orderedExpectedMessages, [WORKLIST, "SnapshotAppliedAck"]);
  assert.equal(expected.stableErrorCode, null);
  assert.deepEqual(expected.forbiddenSideEffects, [...DEFAULT_FORBIDDEN, "decision-taken-on-worklist-eqp"]);
  const { controlServer, onboardHmi } = expected.productAssertions;
  assert.deepEqual(controlServer, ["COPY_ACCEPTED_DEMAND_EQP_VERBATIM", "SEND_NULL_EQP_WHEN_THE_DEMAND_HAS_NONE", "NEVER_DECIDE_BY_WORKLIST_EQP"]);
  assert.deepEqual(onboardHmi, ["DISPLAY_EQP_BESIDE_SUBLOT_ON_PICKUP_SCAN_AND_UNLOAD_LISTS", "DISPLAY_NULL_EQP_AS_ABSENT_WITHOUT_BLOCKING", "NEVER_DECIDE_BY_WORKLIST_EQP"]);
  assert.deepEqual(expected.finalState, { readiness: "UNCHANGED", business: "UNCHANGED_DISPLAY_ONLY", physical: "UNCHANGED" });
});

test(`FP-IS-09, the onboard worklist slice, carries ${VECTOR}`, () => {
  const slices = readJson("integration-slices/index.json").slices;
  const carriers = slices.filter((slice) => slice.vectorIds.includes(VECTOR)).map((slice) => slice.integrationSliceId);
  assert.deepEqual(carriers, ["FP-IS-09"]);
  const is09 = slices.find((slice) => slice.integrationSliceId === "FP-IS-09");
  assert.ok(is09.definition.authorityModel.wireMessages.includes(WORKLIST));
  // Review L4: the slice's outcomes name what the vector binds, not only the selection.
  assert.ok(is09.definition.requiredOutcomes.includes("WORKLIST_EQP_DISPLAY_ONLY"));
});

test("G1 pins the worklist item with eqp among its required fields", () => {
  const g1 = read("tools/g1-validate.mjs");
  assert.ok(g1.includes(JSON.stringify([...V6_ITEM_FIELDS, "eqp"]).replaceAll(" ", "")), "G1 does not pin eqp");
});

test("G1 refuses a tree that drops the display-only binding, the null example or the slice of the eqp vector", () => {
  // Review L1: removing NEVER_DECIDE_BY_WORKLIST_EQP from either side, the EQP-NULL example or the vector's place in FP-IS-09
  // left G1 green; each now has a G1 check of its own, as protocol#26 did for the remaining-baskets skip.
  const g1 = read("tools/g1-validate.mjs");
  assert.match(g1, new RegExp(VECTOR));
  assert.match(g1, /worklist eqp is display-only on both ends/);
  assert.match(g1, /a valid worklist carries a null eqp/);
  assert.match(g1, /FP-IS-09 carries the worklist eqp vector/);
});

// --- prose ---

test("the wire notes say eqp is display-only, why it is required and nullable, and that both implementations change together", () => {
  const body = section(`\`${WORKLIST}\` item \`eqp\``);
  assert.match(body, /protocol#29/);
  assert.match(body, /`EQP`/);
  // Display only, on both ends.
  assert.match(body, /display-only/);
  assert.match(body, /pickup scan list/);
  assert.match(body, /unload list/);
  assert.match(body, /Neither side may/);
  // Why required and nullable.
  assert.match(body, /`RequiredMesFactsCriterion`/);
  assert.match(body, /required and nullable/);
  assert.match(body, /forgot/);
  assert.match(body, /No optional payload fields/);
  // Verbatim and how null shows.
  assert.match(body, /verbatim/);
  assert.match(body, /`null`/);
  // The breaking change.
  assert.match(body, /`additionalProperties: false`/);
  assert.match(body, /6\.0\.0 implementation rejects/);
  assert.match(body, /together/);
  // Review M1: an applied worklist is kept by revision, so the switch happens with no vehicle holding a non-empty one.
  assert.match(body, /dispatch gate closed/);
  assert.match(body, /every journey `Completed`/);
  assert.match(body, /non-empty worklist/);
  assert.match(body, /same `worklistRevision`/);
  assert.match(body, /`SNAPSHOT_REVISION_CONTENT_CONFLICT`/);
});

test("the compatibility report states the one 7.0.0 change in one sentence", () => {
  const [sentence, ...rest] = readJson("compatibility/report.json").changeSummary;
  assert.deepEqual(rest, []);
  assert.match(sentence, /CurrentStopWorklistSnapshot/);
  assert.match(sentence, /eqp/);
  assert.match(sentence, /display/);
  assert.match(sentence, new RegExp(VECTOR));
  assert.match(sentence, /6\.0\.0 implementation/);
});

test("candidate limitations describe what 7.0.0 changes and what it carries over", () => {
  const lastParagraph = read("docs/candidate-limitations.md").trim().split("\n\n").at(-1);
  assert.match(lastParagraph, /protocol#29/);
  assert.match(lastParagraph, /`CurrentStopWorklistSnapshot`/);
  assert.match(lastParagraph, /`eqp`/);
  assert.match(lastParagraph, /refuses every 7\.0\.0 message because its identity and ProtocolVersion differ/);
  assert.match(lastParagraph, /error registry is carried over unchanged/);
  assert.match(lastParagraph, /every other schema stays as 6\.0\.0 released it/);
  assert.match(lastParagraph, new RegExp(VECTOR));
  assert.doesNotMatch(lastParagraph, /RemainingBasketsSkipRequested/);
});
