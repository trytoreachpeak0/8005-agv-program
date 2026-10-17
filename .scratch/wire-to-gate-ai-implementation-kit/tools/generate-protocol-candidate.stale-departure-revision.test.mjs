// Acceptance checks for the second revision of the protocol 5.0.0 candidate (8005-agv-protocol#23, tracked in
// program#195; requirement program#201 CP-0015; server control-server#742): a departure request at a machine pickup stop
// whose worklistRevision is stale but differs in nothing material is decided by the remaining checks, and the journey plan
// vector and its slice speak of the remaining plan.
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.stale-departure-revision.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written.
// Expected wording comes from the ticket's definition of "no material change", never from the generator's literals.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const generatorPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "generate-protocol-candidate.mjs");
const REQUEST = "CurrentStopDepartureRequested";
const RESULT = "CurrentStopDepartureResult";
const DEFAULT_SIDE_EFFECTS = ["duplicate-riot-order", "duplicate-slot-unlock", "expanded-active-unlock-set", "duplicate-business-commit", "ready-before-reconciliation", "unknown-as-success"];
const STALE = "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION";
const STALE_ACCEPTED = "CV-CURRENT-STOP-DEPARTURE-STALE-REVISION-ACCEPTED";
const PLAN = "CV-MULTI-STOP-PLAN-NINE-LEGS";

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-stale-departure-revision-"));
  tree = path.join(scratch, "tree");
  const run = spawnSync(process.execPath, [generatorPath, tree], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative) => fs.readFileSync(path.join(tree, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const expectedOf = (vectorId) => readJson(`vectors/${vectorId}/expected.json`);
const sliceOf = (sliceId) => readJson("integration-slices/index.json").slices.find((item) => item.integrationSliceId === sliceId);
const section = (heading) => {
  const notes = read("docs/wire-notes.md");
  const start = notes.indexOf(`## ${heading}\n`);
  assert.ok(start >= 0, `section ${heading} not found`);
  const end = notes.indexOf("\n## ", start + 1);
  return notes.slice(start, end < 0 ? undefined : end);
};
const departureNotes = () => section("`CurrentStopDepartureRequested` and `CurrentStopDepartureResult`");

// --- the new vector ---

test(`${STALE_ACCEPTED} exists, is ACCEPTED with no error code and leaves through the DEPARTURE check`, () => {
  assert.ok(fs.existsSync(path.join(tree, "vectors", STALE_ACCEPTED, "input.ndjson")), "input.ndjson missing");
  const value = expectedOf(STALE_ACCEPTED);
  assert.equal(value.vectorId, STALE_ACCEPTED);
  assert.equal(value.stableErrorCode, null, "an accepted departure carries no stable error code");
  assert.deepEqual(value.orderedExpectedMessages.slice(0, 4), [REQUEST, "DurableAck", RESULT, "DurableAck"]);
  assert.deepEqual(value.orderedExpectedMessages.slice(-2), ["PreDepartureSafetyCheck", "PreDepartureSafetyCheckResult"]);
  assert.deepEqual(value.forbiddenSideEffects.slice(0, DEFAULT_SIDE_EFFECTS.length), DEFAULT_SIDE_EFFECTS);
  assert.ok(value.persistenceCheckpoints.includes("departure-request-journaled-before-send"));
  assert.notEqual(value.finalState.business, "UNCHANGED_DEPARTURE_REJECTED");
});

test(`${STALE_ACCEPTED} states each condition of "no material change" and that the remaining checks still decide`, () => {
  const value = expectedOf(STALE_ACCEPTED);
  for (const assertion of [
    "ACCEPT_STALE_REVISION_WITHOUT_MATERIAL_CHANGE_AT_MACHINE_PICKUP_STOP",
    "DECIDE_STALE_REVISION_WITHOUT_MATERIAL_CHANGE_BY_REMAINING_CHECKS",
    "REQUIRE_REQUESTED_REVISION_LOWER_WITHIN_CURRENT_STOP_AT_CURRENT_STATION",
    "REQUIRE_OPERATION_SESSION_MATCH_WHEN_REQUEST_CARRIES_ONE",
    "REQUIRE_EMPTY_ITEMS_IN_EVERY_WORKLIST_FROM_REQUESTED_TO_CURRENT_REVISION",
    "REQUIRE_NO_LOAD_SETTLED_NO_LOADED_BASKET_LEFT_AND_NO_CORRECTION_SINCE_REQUESTED_REVISION",
    "TIME_LOAD_SETTLEMENT_AND_CORRECTION_BY_SERVER_RECEIPT",
    "NEVER_APPLY_STALE_REVISION_EXCEPTION_AT_STAGING_PICKUP_STOP",
    "DEPART_THROUGH_CORRECTION_GATE_AND_SAFETY_CHECK",
  ]) assert.ok(value.productAssertions.controlServer.includes(assertion), assertion);
  for (const effect of ["departure-refused-on-stale-revision-without-material-change", "stale-revision-exception-skips-remaining-checks", "stale-revision-exception-at-staging-pickup-stop", "departure-bypasses-correction-gate-or-safety-check"]) assert.ok(value.forbiddenSideEffects.includes(effect), effect);
  // The vehicle changes no business logic: it adopts an ACCEPTED it may receive for an older revision.
  assert.ok(value.productAssertions.onboardHmi.includes("ADOPT_ACCEPTED_DEPARTURE_ON_STALE_REVISION"));
  assert.ok(value.productAssertions.onboardHmi.includes("NEVER_DEPART_LOCALLY"));
});

test(`FP-IS-02 binds ${STALE_ACCEPTED} and no other slice does`, () => {
  assert.ok(sliceOf("FP-IS-02").vectorIds.includes(STALE_ACCEPTED));
  const stray = readJson("integration-slices/index.json").slices.filter((slice) => slice.integrationSliceId !== "FP-IS-02" && slice.vectorIds.includes(STALE_ACCEPTED));
  assert.deepEqual(stray.map((slice) => slice.integrationSliceId), []);
});

test(`the G1 gate requires ${STALE_ACCEPTED} and checks that it is accepted and the stale one refused`, () => {
  const g1 = read("tools/g1-validate.mjs");
  assert.ok(g1.includes(`"${STALE_ACCEPTED}"`), "missing from requiredVectors");
  assert.match(g1, /stale-revision departure vectors/);
});

// --- the old vector is confined to a material change ---

test(`${STALE} is refused only on a material change`, () => {
  const value = expectedOf(STALE);
  assert.equal(value.stableErrorCode, "WORKLIST_REVISION_STALE");
  assert.ok(value.productAssertions.controlServer.includes("REJECT_DEPARTURE_ON_STALE_WORKLIST_REVISION_WITH_MATERIAL_CHANGE"));
  assert.ok(!value.productAssertions.controlServer.includes("REJECT_DEPARTURE_ON_STALE_WORKLIST_REVISION"), "the unqualified refusal is still asserted");
  assert.ok(value.forbiddenSideEffects.includes("departure-on-stale-worklist-revision-with-material-change"));
  assert.ok(!value.forbiddenSideEffects.includes("departure-on-stale-worklist-revision"), "the unqualified side effect is still forbidden");
  assert.equal(value.finalState.business, "UNCHANGED_DEPARTURE_REJECTED");
});

// --- the wire notes ---

test("the wire notes keep the check order and make WORKLIST_REVISION_STALE subject to the exception", () => {
  const body = departureNotes();
  const order = ["STATION_MISMATCH", "WORKLIST_REVISION_STALE", "ACTION_NOT_ALLOWED_IN_STATE"].map((code) => body.indexOf(`\`${code}\` when`));
  assert.ok(order.every((index) => index >= 0), `positions ${order}`);
  assert.deepEqual([...order].sort((a, b) => a - b), order);
  assert.match(body, /`WORKLIST_REVISION_STALE` when `worklistRevision` is not the current worklist revision of that stop \(`currentWorklistRevision` names it\) and the exception for a stale revision without material change below does not apply;/);
  assert.match(body, /protocol#23/);
  assert.match(body, /CP-0015 \(program#201\)/);
});

test("the wire notes state the definition of no material change, condition by condition", () => {
  const body = departureNotes();
  assert.match(body, /At a machine pickup stop, when the `worklistRevision` of a departure request is not the current one, the two revisions differ in nothing material only when all of the following hold:/);
  assert.match(body, /\(1\) the requested revision is lower than the current one, lies within the worklist revisions of the current stop itself, and the worklist of that revision has the current station as its `stationId`;/);
  assert.match(body, /\(2\) when the request carries an `operationSessionId`, it equals the current stop's; a `null` one is not compared;/);
  assert.match(body, /\(3\) every worklist sent for this stop, from the requested revision up to and including the current one, has empty `items`;/);
  assert.match(body, /\(4\) since the requested revision no load has settled at this stop, none of the baskets already loaded has left it \(terminated or removed\), and no load correction has been opened at it; when a load settled and when a correction was opened are taken at the control server's receipt\./);
  assert.match(body, /If any of them fails the answer is still `WORKLIST_REVISION_STALE`\. If all hold, the request is decided by the remaining checks, and answered `ACCEPTED` when they pass\./);
  assert.match(body, /The exception does not apply at a staging pickup stop\./);
});

// --- the journey plan speaks of the remaining plan ---

test(`${PLAN} and FP-IS-08 speak of the remaining plan of at most nine legs`, () => {
  const value = expectedOf(PLAN);
  assert.ok(value.productAssertions.onboardHmi.includes("DISPLAY_REMAINING_JOURNEY_PLAN"));
  const definition = sliceOf("FP-IS-08").definition;
  assert.ok(definition.ownerResponsibilities.onboardHmi.includes("DISPLAY_REMAINING_JOURNEY_PLAN"));
  assert.ok(definition.requiredOutcomes.includes("UP_TO_NINE_REMAINING_LEGS_PLANNED"));
  const tree = JSON.stringify([value, definition]);
  assert.doesNotMatch(tree, /DISPLAY_FULL_JOURNEY_PLAN/);
  assert.doesNotMatch(tree, /"UP_TO_NINE_LEGS_PLANNED"/);
  // The vector keeps its id: two implementations carry it in test traits.
  assert.equal(value.vectorId, PLAN);
});

test("the plan schema keeps maxItems 9", () => {
  const payload = readJson("schemas/messages/UpcomingStopPlanSnapshot.schema.json").properties.payload;
  const arrays = Object.values(payload.properties).filter((property) => property.type === "array");
  assert.ok(arrays.some((property) => property.maxItems === 9), "no array with maxItems 9");
});

test("the wire notes say the plan holds the current stop and the stops after it that are not complete", () => {
  const body = section("`UpcomingStopPlanSnapshot` carries the remaining plan");
  assert.match(body, /protocol#23/);
  assert.match(body, /the vehicle's current stop and the stops after it that are not yet complete/);
  assert.match(body, /Stops already passed are not sent/);
  assert.match(body, /`maxItems` 9/);
});

// --- the candidate describes the revision ---

test("the compatibility report adds one sentence for this revision and keeps the identity of the 5.0.0 candidate", () => {
  const report = readJson("compatibility/report.json");
  assert.equal(report.candidateVersion, "5.0.0");
  assert.equal(report.protocolVersion, 6);
  assert.equal(report.changeSummary.length, 2);
  const sentence = report.changeSummary[1];
  assert.match(sentence, /stale worklistRevision.*no material change/);
  assert.match(sentence, /remaining plan/);
  assert.match(sentence, /\.$/);
  assert.doesNotMatch(sentence, /\. /);
});

test("candidate limitations no longer claim the vectors and slices stay as 4.0.0 released them", () => {
  const lastParagraph = read("docs/candidate-limitations.md").trim().split("\n\n").at(-1);
  assert.doesNotMatch(lastParagraph, /the vectors and the integration slices stay as 4\.0\.0 released them/);
  assert.match(lastParagraph, /every other schema stays as 4\.0\.0 released it/);
  assert.match(lastParagraph, /protocol#23/);
});
