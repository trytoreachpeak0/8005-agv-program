// Acceptance checks for the seventh transport task type in the protocol 5.0.0 candidate (8005-agv-protocol#21, tracking
// 8005-agv-program#195, the user's decisions 6 and 7 of 2026-10-16): TransportTaskType appends WIRE_TO_FULL_INSPECTION,
// PublicStationFunction stays as released, and the closed-enum change is breaking, so both implementations change together.
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.full-inspection.test.mjs
// Expected values come from the ticket and the released protocol-v4.0.0 tree (protocol commit 3fb214e5), never from the
// generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const toolsDirectory = path.dirname(fileURLToPath(import.meta.url));
const generatorPath = path.join(toolsDirectory, "generate-protocol-candidate.mjs");
const TYPES = "https://schemas.8005-agv.local/agv-full-product/v6/common/types.schema.json#/$defs/";

// The two closed enums as protocol-v4.0.0 released them (schemas/common/types.schema.json at 3fb214e5).
const V4_TRANSPORT_TASK_TYPES = ["DIE_TO_WIRE_STAGING", "DIE_TO_OVEN", "WIRE_TO_GATE", "WIRE_TO_OPTICAL", "STAGING_TO_WIRE", "WIRE_TO_NITROGEN"];
const V4_PUBLIC_STATION_FUNCTIONS = ["WIRE_STAGING", "OVEN", "GATE", "OPTICAL", "NITROGEN"];
const NEW_TYPE = "WIRE_TO_FULL_INSPECTION";
const WORKLIST = "CurrentStopWorklistSnapshot";
const POSITIVE = `examples/valid/${WORKLIST}/V-${WORKLIST}-WIRE-TO-FULL-INSPECTION-001.json`;
const NEGATIVES = {
  MISSPELLED: "WIRE_TO_FULL_INSPECTON",
  LOWERCASE: "wire_to_full_inspection",
};

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-full-inspection-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative) => fs.readFileSync(path.join(tree, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const defs = () => readJson("schemas/common/types.schema.json").$defs;

test(`TransportTaskType appends ${NEW_TYPE} after the six values protocol-v4.0.0 released, in their order`, () => {
  assert.deepEqual(defs().TransportTaskType.enum, [...V4_TRANSPORT_TASK_TYPES, NEW_TYPE]);
});

test("PublicStationFunction keeps exactly the five values protocol-v4.0.0 released", () => {
  // The user decided on 2026-10-16 not to add FULL_INSPECTION: specification 5.3 no longer maintains the field and the
  // control server always sends null, so a value would have no sender.
  assert.deepEqual(defs().PublicStationFunction.enum, V4_PUBLIC_STATION_FUNCTIONS);
});

test("the worklist item and the clearance confirmation still take their type from TransportTaskType", () => {
  const worklistItem = readJson(`schemas/messages/${WORKLIST}.schema.json`).properties.payload.properties.items.items.properties;
  assert.equal(worklistItem.workType.$ref, `${TYPES}TransportTaskType`);
  const clearance = JSON.stringify(readJson("schemas/messages/ManualStationClearanceConfirmationRequested.schema.json"));
  assert.ok(clearance.includes(`"${TYPES}TransportTaskType"`), "ManualStationClearanceConfirmationRequested no longer references TransportTaskType");
});

test(`a valid ${WORKLIST} example carries ${NEW_TYPE} and otherwise matches the minimal example`, () => {
  const positive = readJson(POSITIVE);
  const minimal = readJson(`examples/valid/${WORKLIST}/V-${WORKLIST}-MIN-001.json`);
  assert.equal(positive.messageType, WORKLIST);
  assert.equal(positive.payload.items.length, 1);
  assert.equal(positive.payload.items[0].workType, NEW_TYPE);
  const normalised = structuredClone(positive);
  normalised.payload.items[0].workType = minimal.payload.items[0].workType;
  assert.deepEqual(normalised, minimal);
});

for (const [suffix, value] of Object.entries(NEGATIVES)) {
  test(`a ${suffix.toLowerCase()} task type in the worklist is a schema-invalid example (${value})`, () => {
    const wrapper = readJson(`examples/invalid/${WORKLIST}/I-${WORKLIST}-ENUM-items-workType-${suffix}.json`);
    assert.equal(wrapper.vectorId, `I-${WORKLIST}-ENUM-items-workType-${suffix}`);
    assert.deepEqual(wrapper.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/items/0/workType", rule: "enum-or-const" });
    assert.equal(wrapper.message.payload.items[0].workType, value);
    // The only difference from the positive example is the type itself.
    const restored = structuredClone(wrapper.message);
    restored.payload.items[0].workType = NEW_TYPE;
    assert.deepEqual(restored, readJson(POSITIVE));
  });
}

test("the compatibility report states the one breaking change against protocol-v4.0.0", () => {
  const report = readJson("compatibility/report.json");
  assert.equal(report.baseRelease, "protocol-v4.0.0");
  assert.equal(report.classification, "BREAKING_PROTOCOL_VERSION_INCREASE");
  assert.equal(report.changeSummary.length, 1);
  const [sentence] = report.changeSummary;
  assert.match(sentence, new RegExp(`TransportTaskType.*${NEW_TYPE}`));
  assert.match(sentence, /PublicStationFunction.*unchanged/);
  assert.match(sentence, /4\.0\.0 implementation.*rejects/);
  assert.match(sentence, /both implementations.*together/);
  assert.match(sentence, /\.$/);
  assert.doesNotMatch(sentence, /\. /);
});

test(`docs/wire-notes.md explains ${NEW_TYPE} and why both implementations change together`, () => {
  const notes = read("docs/wire-notes.md");
  const start = notes.indexOf(`## \`TransportTaskType\` \`${NEW_TYPE}\``);
  assert.ok(start >= 0, "section not found");
  const next = notes.indexOf("\n## ", start + 1);
  const section = notes.slice(start, next < 0 ? undefined : next);
  assert.match(section, /protocol#21/);
  assert.match(section, /program#195/);
  assert.match(section, /closed enum/);
  assert.match(section, /4\.0\.0 implementation.*rejects/s);
  assert.match(section, /both implementations.*together/s);
  assert.match(section, /`PublicStationFunction` is unchanged/);
});
