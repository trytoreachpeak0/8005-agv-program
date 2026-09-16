// Acceptance checks for the recovery messages' slotOperationAttemptId (8005-agv-program#95).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.recovery-attempt.test.mjs
// Same seam as the identity test: generate a tree through the command line and read what was written.
// Expected shapes, positions and dedup keys come from the ticket and protocol-v0.3.0 dbae7b9, not from
// the generator's constants.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const ID_REF = "https://schemas.8005-agv.local/agv-full-product/v3/common/types.schema.json#/$defs/Id";

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-recovery-attempt-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(tree, relative), "utf8"));
const payloadSchemaOf = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`).properties.payload;

// One row per message: the field it follows, and its business dedup keys as protocol-v1.0.0 released them.
const recoveryMessages = [
  { messageType: "ExceptionRecoverySessionOpened", after: "demandId", businessDedupKeys: ["requestId", "exceptionRecoverySessionId", "eventId"] },
  { messageType: "ExceptionRecoverySessionSnapshot", after: "demandId", businessDedupKeys: ["exceptionRecoverySessionId", "eventId"] },
  { messageType: "RecoveryActionAccepted", after: "exceptionRecoverySessionId", businessDedupKeys: ["recoveryActionId", "exceptionRecoverySessionId"] },
];

for (const { messageType, after: previous } of recoveryMessages) {
  test(`${messageType} requires a nullable slotOperationAttemptId right after ${previous}`, () => {
    const payload = payloadSchemaOf(messageType);
    assert.deepEqual(payload.properties.slotOperationAttemptId, { anyOf: [{ $ref: ID_REF }, { type: "null" }] });
    const propertyNames = Object.keys(payload.properties);
    assert.equal(propertyNames[propertyNames.indexOf(previous) + 1], "slotOperationAttemptId", "properties position");
    assert.equal(payload.required[payload.required.indexOf(previous) + 1], "slotOperationAttemptId", "required position");
    assert.equal(payload.additionalProperties, false);
  });

  test(`${messageType} negative examples cover slotOperationAttemptId as missing and as the wrong type`, () => {
    const directory = `examples/invalid/${messageType}`;
    const missing = readJson(`${directory}/I-${messageType}-REQUIRED-PAYLOAD-slotOperationAttemptId.json`);
    assert.equal("slotOperationAttemptId" in missing.message.payload, false);
    assert.deepEqual(missing.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/slotOperationAttemptId", rule: "required" });
    const wrongType = readJson(`${directory}/I-${messageType}-TYPE-slotOperationAttemptId.json`);
    const value = wrongType.message.payload.slotOperationAttemptId;
    assert.ok(value !== null && typeof value !== "string", `wrong-type value is ${JSON.stringify(value)}`);
    assert.deepEqual(wrongType.expected, { code: "PROTOCOL_SCHEMA_INVALID", fieldPath: "/payload/slotOperationAttemptId", rule: "type" });
    // Every other negative of this message must carry the field, or it would also fail for its absence.
    for (const file of fs.readdirSync(path.join(tree, directory))) {
      if (file.includes("slotOperationAttemptId") || file.includes("REQUIRED-ENVELOPE-payload")) continue;
      const example = readJson(`${directory}/${file}`);
      if (Array.isArray(example.message.payload) || typeof example.message.payload !== "object") continue;
      assert.ok("slotOperationAttemptId" in example.message.payload, `${file} lacks slotOperationAttemptId`);
    }
    assert.ok("slotOperationAttemptId" in readJson(`examples/valid/${messageType}/V-${messageType}-MIN-001.json`).payload);
  });
}

test("the recovery messages keep their released business dedup keys in the manifest", () => {
  const messages = readJson("manifest/release.json").messages;
  for (const { messageType, businessDedupKeys } of recoveryMessages) {
    assert.deepEqual(messages[messageType].businessDedupKeys, businessDedupKeys, messageType);
  }
});
