// Acceptance checks for the wire notes written with the 3.0.0 candidate identity (8005-agv-program#146).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.wire-notes.test.mjs
// Same seam as the identity test: generate a tree through the command line and read what was written.
// The sentences checked here come from CP-0005 section 4.1 and specification 23.5, not from the generator.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const NOTES = "docs/wire-notes.md";

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-wire-notes-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative) => fs.readFileSync(path.join(tree, relative), "utf8");
// The body of one "## " section, so a sentence is checked where it belongs and not just somewhere.
const section = (heading) => {
  const notes = read(NOTES);
  const start = notes.indexOf(`\n## ${heading}\n`);
  assert.ok(start >= 0, `section "${heading}" not found`);
  const end = notes.indexOf("\n## ", start + 1);
  return notes.slice(start, end < 0 ? undefined : end);
};

test("the wire notes defer to the Schema and the docs README lists them", () => {
  assert.match(read(NOTES), /^# Wire notes\n/);
  assert.match(read(NOTES), /where a note and a Schema disagree, the Schema wins/);
  assert.match(read("docs/README.md"), /`docs\/wire-notes\.md`/);
});

test("SLOT_EXPECTED_ACTION_OVERDUE is registered as an alarm code without a schema change", () => {
  const alarm = section("Alarm code `SLOT_EXPECTED_ACTION_OVERDUE`");
  assert.match(alarm, /`AlarmEntry\.code` is an open set/);
  assert.match(alarm, /changes no schema/);
  assert.match(alarm, /`OnboardAlarmSnapshot`/);
  assert.match(alarm, /`subjectType` is `SLOT`/);
  assert.match(alarm, /`subjectId` is the slot number/);
  assert.match(alarm, /`raisedAt` is the instant the wait crossed the threshold/);
  assert.match(alarm, /`displayMessage` is the action the vehicle expects/);
  assert.match(alarm, /derived from `raisedAt` and the threshold/);
  // OperationProgress may help but is never the basis: it is TELEMETRY and can be lost.
  assert.match(alarm, /`OperationProgress`[^\n]*`TELEMETRY`[^\n]*never the basis/);
  assert.match(alarm, /readings[^\n]*`SafetyStateSnapshot`/);
  assert.match(alarm, /precondition of `SlotFaultDeclarationCommand`[^\n]*REQ-0359/);
});

test("expiresOnRevisionChange keeps its value and says what a revision change is", () => {
  const entry = section("`SublotEntryRequested.expiresOnRevisionChange`");
  assert.match(entry, /stays `const: true`/);
  assert.match(entry, /neither its value nor its type changes/);
  // The four events that are a revision change, in one sentence.
  assert.match(entry, /a revision change is: the stop ended, the operation session or the station changed, the worklist became empty, or the control server rejected the submission with `WORKLIST_REVISION_STALE`\./);
  // And the one that is not.
  assert.match(entry, /A worklist revision advancing within the same operation session at the same station is not a revision change/);
  assert.match(entry, /specification 23\.5/);
});
