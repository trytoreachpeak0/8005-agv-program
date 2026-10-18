// Acceptance checks for the wire-notes corrections made before protocol 5.0.0 is released (control-server#767, tracked in
// program#195): three findings of the protocol#23 and control-server#749 reviews, all in docs/wire-notes.md, none in a Schema.
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.v5-exit-wire-notes.test.mjs
// The seam is the generator's command line: generate a tree and read what was written.
// Expected wording comes from the ticket and from what the two implementations do, never from the generator's literals:
// - control-server JourneyRuntimeEngine.ClearanceMove.cs sends the charger leg it left as COMPLETED during a clearance move,
//   and onboard-hmi WireToGateStationClearance.cs reads the charger of the clearance from that leg (control-server#406);
// - control-server JourneyRuntimeEngine.StagingDeparture.cs refuses any basket loaded at the stop that is no longer loaded,
//   because it does not record when a basket left.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-v5-exit-wire-notes-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const section = (heading) => {
  const notes = fs.readFileSync(path.join(tree, "docs/wire-notes.md"), "utf8");
  const start = notes.indexOf(`\n## ${heading}\n`);
  assert.ok(start >= 0, `section "${heading}" not found`);
  const end = notes.indexOf("\n## ", start + 1);
  return notes.slice(start, end < 0 ? undefined : end);
};
const planNotes = () => section("`UpcomingStopPlanSnapshot` carries the remaining plan");
const departureNotes = () => section("`CurrentStopDepartureRequested` and `CurrentStopDepartureResult`");

// --- :75, the remaining plan has one exception: a clearance move keeps the charger leg it left ---

test("the remaining plan is the plan of a transport journey", () => {
  assert.match(planNotes(), /Stops already passed are not sent[^\n]*transport journey/);
});

test("a clearance move keeps the charger leg it left, as COMPLETED, and says why", () => {
  const body = planNotes();
  const bullet = body.split("\n- ").find((item) => /clearance/.test(item));
  assert.ok(bullet, "no bullet on the clearance move");
  assert.match(bullet, /`CHARGER` leg/);
  assert.match(bullet, /`COMPLETED`/);
  assert.match(bullet, /waiting point leg/);
  // The reason: the onboard HMI names the charger of the clearance from that leg.
  assert.match(bullet, /onboard HMI[^.]*charger[^.]*from (it|that leg)/);
  assert.match(bullet, /control-server#406/);
});

// --- :73, the Source line names the requirement change ---

test("the remaining plan section names CP-0015 and REQ-0196 as its source", () => {
  const source = planNotes().split("\n").find((line) => line.startsWith("Source:"));
  assert.ok(source, "no Source line");
  assert.match(source, /CP-0015 \(program#201\)/);
  assert.match(source, /REQ-0196/);
  assert.match(source, /protocol#23/);
});

// --- :46, condition (4) may be judged more strictly by a control server that does not record when a basket left ---

test("condition (4) lets a control server count every basket no longer loaded as having left", () => {
  const body = departureNotes();
  const bullet = body.split("\n- ").find((item) => /\(4\) since the requested revision/.test(item));
  assert.ok(bullet, "no bullet with condition (4)");
  // The existing wording stays: this is an allowance, not a new condition.
  assert.match(bullet, /none of the baskets already loaded has left it \(terminated or removed\)/);
  assert.match(bullet, /A control server that does not record when a basket left the stop may treat every basket loaded at this stop that is no longer loaded as having left it since the requested revision/);
  // The cost of the allowance, so an implementation reading it knows it is only conservative.
  assert.match(bullet, /`WORKLIST_REVISION_STALE`[^.]*press(es)? again/);
});
