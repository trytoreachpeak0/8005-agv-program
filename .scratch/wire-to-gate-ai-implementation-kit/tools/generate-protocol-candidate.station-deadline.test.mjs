// Acceptance checks for stationDepartureDeadlineAt and OPERATOR_TIMEOUT (8005-agv-program#91).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.station-deadline.test.mjs
// Same seam as the identity tests: generate a tree through the command line and read what was written,
// never the generator's internals. Expected values come from the ticket, specification 6.3 item 1 and
// the protocol-v0.3.0 commits the change is ported from (345c53c for the field, dbae7b9 for the code).
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const toolsDirectory = path.dirname(fileURLToPath(import.meta.url));
const generatorPath = path.join(toolsDirectory, "generate-protocol-candidate.mjs");

const MESSAGE = "CurrentStopWorklistSnapshot";
const FIELD = "stationDepartureDeadlineAt";

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-station-deadline-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));

test("CurrentStopWorklistSnapshot requires a nullable Instant stationDepartureDeadlineAt right after operationSessionId", () => {
  const payload = readJson(`schemas/messages/${MESSAGE}.schema.json`).properties.payload;
  const properties = Object.keys(payload.properties);
  assert.equal(properties.indexOf(FIELD), properties.indexOf("operationSessionId") + 1, `properties: ${properties.join(", ")}`);
  assert.equal(payload.required.indexOf(FIELD), payload.required.indexOf("operationSessionId") + 1, `required: ${payload.required.join(", ")}`);
  const { anyOf } = payload.properties[FIELD];
  assert.equal(anyOf?.length, 2);
  assert.match(anyOf[0].$ref, /\/common\/types\.schema\.json#\/\$defs\/Instant$/);
  assert.deepEqual(anyOf[1], { type: "null" });
  assert.equal(payload.additionalProperties, false);
});

test("the generated negatives cover the new field and every earlier worklist negative still carries a valid deadline", () => {
  const directory = `examples/invalid/${MESSAGE}`;
  const valid = readJson(`examples/valid/${MESSAGE}/V-${MESSAGE}-MIN-001.json`);
  assert.match(valid.payload[FIELD] ?? "", /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/, "valid example carries an instant");

  const required = readJson(`${directory}/I-${MESSAGE}-REQUIRED-PAYLOAD-${FIELD}.json`);
  assert.equal(Object.hasOwn(required.message.payload, FIELD), false);
  assert.deepEqual(required.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: `/payload/${FIELD}`, rule: "required" });

  const type = readJson(`${directory}/I-${MESSAGE}-TYPE-${FIELD}.json`);
  const wrong = type.message.payload[FIELD];
  assert.ok(wrong !== null && typeof wrong !== "string", `TYPE negative carries ${JSON.stringify(wrong)}`);
  assert.deepEqual(type.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: `/payload/${FIELD}`, rule: "type" });

  // A negative that lost the deadline would fail for a second reason and hide the rule it exists to test.
  // The ticket names a spot check of two; every other negative that has a payload is held to the same bar.
  const own = new Set([`I-${MESSAGE}-REQUIRED-PAYLOAD-${FIELD}.json`, `I-${MESSAGE}-TYPE-${FIELD}.json`]);
  const earlier = fs.readdirSync(path.join(tree, directory)).filter((file) => !own.has(file));
  for (const spotCheck of [`I-${MESSAGE}-REQUIRED-PAYLOAD-items.json`, `I-${MESSAGE}-TYPE-stationId.json`]) {
    assert.ok(earlier.includes(spotCheck), `${spotCheck} missing`);
  }
  const withPayload = earlier.map((file) => [file, readJson(`${directory}/${file}`).message]).filter(([, message]) => message.payload);
  assert.ok(withPayload.length >= 18, `only ${withPayload.length} earlier negatives with a payload`);
  for (const [file, message] of withPayload) assert.equal(message.payload[FIELD], valid.payload[FIELD], file);
});

test("OPERATOR_TIMEOUT is appended after the codes registered before it, narrowed to OperationResult", () => {
  const registry = readJson("errors/error-codes.json");
  const codes = registry.codes.map((entry) => entry.code);
  const at = codes.indexOf("OPERATOR_TIMEOUT");
  // When this ticket branched the registry held 57 codes, PACKAGE_CAPACITY_UNRESOLVED (program#93) last.
  assert.equal(at, 57, `OPERATOR_TIMEOUT at ${at}`);
  assert.equal(codes[0], "PROTOCOL_ENVELOPE_INVALID");
  assert.equal(codes[56], "PACKAGE_CAPACITY_UNRESOLVED");
  assert.equal(codes.filter((code) => code === "OPERATOR_TIMEOUT").length, 1);
  assert.deepEqual(readJson("schemas/common/types.schema.json").$defs.ErrorCode.enum, codes);

  const entry = registry.codes[at];
  assert.equal(entry.category, "BUSINESS");
  assert.equal(entry.retryDisposition, "AFTER_STATE_CHANGE");
  assert.equal(entry.introducedInRelease, "2.0.0");
  // The MVP line emits it in exactly one place: SlotResult.reasonCodes of a FAILED slot in the
  // OperationResult that settles a SlotOperationCommand after the station deadline.
  assert.deepEqual(entry.allowedMessageTypes, ["OperationResult"]);
  assert.match(entry.meaning, /station departure deadline/);
  assert.match(entry.meaning, /door is closed/);
  assert.match(entry.meaning, /determinate failure/);
  assert.match(entry.meaning, /ADR-cross-0058 decision 5/);
  assert.match(entry.meaning, /protocol-v0\.3\.0/);
  // The code describes what happened to the slot, not which implementation is going to send it.
  assert.doesNotMatch(entry.meaning, /\b(will|shall)\b/i);
});

test("OPERATOR_TIMEOUT gets no vector and the trajectory set is unchanged", () => {
  const ids = fs.readdirSync(path.join(tree, "vectors"));
  assert.equal(ids.length, 33);
  const stableCodes = ids.map((id) => readJson(`vectors/${id}/expected.json`).stableErrorCode);
  assert.equal(stableCodes.includes("OPERATOR_TIMEOUT"), false);
  const references = readJson("integration-slices/index.json").slices.flatMap((slice) => slice.vectorIds);
  assert.equal(references.length, 36);
  assert.equal(new Set(references).size, 33);
});
