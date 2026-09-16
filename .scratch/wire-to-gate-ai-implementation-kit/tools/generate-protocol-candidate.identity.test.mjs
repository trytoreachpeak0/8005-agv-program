// Acceptance checks for the protocol 2.0.0 candidate identity (8005-agv-program#90).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.identity.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written,
// never the generator's internals. Expected values come from the ticket and specification 6.2, not
// from the generator's constants.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const toolsDirectory = path.dirname(fileURLToPath(import.meta.url));
const generatorPath = path.join(toolsDirectory, "generate-protocol-candidate.mjs");
const contextPath = path.resolve(toolsDirectory, "../../../CONTEXT.md");

const V3_BASE = "https://schemas.8005-agv.local/agv-full-product/v3/";
const PROFILE_ID = "AGV_FULL_PRODUCT";
// The 54 codes protocol-v1.0.0 released, anchored at both ends of that registry.
const RELEASED_CODE_COUNT = 54;

const generate = (generator, target) => {
  const run = spawnSync(process.execPath, [generator, target], { encoding: "utf8" });
  assert.equal(run.status, 0, `generator exited ${run.status}: ${run.stderr}`);
};
const walk = (directory) => fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
  const child = path.join(directory, entry.name);
  return entry.isDirectory() ? walk(child) : [child];
});

let scratch;
let tree;
before(() => {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "protocol-identity-"));
  tree = path.join(scratch, "tree");
  generate(generatorPath, tree);
});
after(() => fs.rmSync(scratch, { recursive: true, force: true }));

const read = (relative, root = tree) => fs.readFileSync(path.join(root, relative), "utf8");
const readJson = (relative, root = tree) => JSON.parse(read(relative, root));
const payloadOf = (messageType) => readJson(`schemas/messages/${messageType}.schema.json`).properties.payload.properties;

test("every schema $id and $ref sits under agv-full-product/v3 and no v2 URI remains", () => {
  const uris = [];
  const collect = (value) => {
    if (Array.isArray(value)) return value.forEach(collect);
    if (value === null || typeof value !== "object") return;
    for (const [key, child] of Object.entries(value)) {
      if ((key === "$id" || key === "$ref") && typeof child === "string" && child.startsWith("https://")) uris.push(child);
      else collect(child);
    }
  };
  const files = walk(tree);
  files.filter((file) => file.endsWith(".json")).forEach((file) => collect(JSON.parse(fs.readFileSync(file, "utf8"))));
  assert.ok(uris.length > 0, "no $id or $ref found");
  assert.deepEqual(uris.filter((uri) => !uri.startsWith(V3_BASE)), []);
  const v2Hits = files.filter((file) => fs.readFileSync(file, "utf8").includes("agv-full-product/v2"));
  assert.deepEqual(v2Hits.map((file) => path.relative(tree, file)), []);
});

test("ProtocolVersion is 3 wherever the wire pins it, under an unchanged profileId", () => {
  const envelope = readJson("schemas/envelope.schema.json");
  assert.equal(envelope.properties.protocolVersion.const, 3);
  assert.equal(envelope.properties.profileId.const, PROFILE_ID);
  const messageFiles = fs.readdirSync(path.join(tree, "schemas/messages"));
  assert.ok(messageFiles.length > 0);
  for (const file of messageFiles) {
    const schema = readJson(`schemas/messages/${file}`);
    assert.equal(schema.properties.protocolVersion.const, 3, file);
    assert.equal(schema.properties.profileId.const, PROFILE_ID, file);
  }
  assert.equal(payloadOf("SessionHello").supportedProtocolVersion.const, 3);
  assert.equal(payloadOf("SessionHello").profileId.const, PROFILE_ID);
  assert.equal(payloadOf("SessionRejected").expectedProtocolVersion.const, 3);
  assert.equal(payloadOf("ProtocolProblem").expectedProtocolVersion.const, 3);
  assert.equal(payloadOf("ProtocolProblem").expectedProfileId.const, PROFILE_ID);
  const identity = readJson("schemas/common/types.schema.json").$defs.ProtocolReleaseIdentity.properties;
  assert.equal(identity.protocolVersion.const, 3);
  assert.equal(identity.profileId.const, PROFILE_ID);
});

test("release version is 2.0.0 in the package, the seed manifest and a still-pending attestation template", () => {
  assert.equal(readJson("package.json").version, "2.0.0");
  const manifest = readJson("manifest/release.json");
  assert.equal(manifest.releaseVersion, "2.0.0");
  assert.equal(manifest.protocolVersion, 3);
  assert.equal(manifest.profileId, PROFILE_ID);
  const template = readJson("attestations/release-approval.template.json");
  assert.equal(template.candidateVersion, "2.0.0");
  assert.equal(template.status, "PENDING");
});

test("the codes released in 1.0.0 keep introducedInRelease 1.0.0 under registry version 1.1.0", () => {
  const registry = readJson("errors/error-codes.json");
  assert.equal(registry.registryVersion, "1.1.0");
  assert.equal(registry.appendOnly, true);
  const released = registry.codes.slice(0, RELEASED_CODE_COUNT);
  assert.equal(released.length, RELEASED_CODE_COUNT);
  assert.equal(released[0].code, "PROTOCOL_ENVELOPE_INVALID");
  assert.equal(released[RELEASED_CODE_COUNT - 1].code, "RECOVERY_RESULT_REQUIRED");
  assert.deepEqual(released.filter((entry) => entry.introducedInRelease !== "1.0.0").map((entry) => entry.code), []);
});

test("an introducedInRelease override on an existing code reaches the registry", () => {
  // A throwaway copy of the generator with one override added, as an uncommitted edit would.
  const patchedTools = path.join(scratch, "patched-tools");
  fs.cpSync(toolsDirectory, patchedTools, { recursive: true, filter: (source) => !source.endsWith(".test.mjs") });
  const patchedGenerator = path.join(patchedTools, "generate-protocol-candidate.mjs");
  const original = '["PROTOCOL_ENVELOPE_INVALID", "PROTOCOL", "NEVER"],';
  const source = fs.readFileSync(patchedGenerator, "utf8");
  assert.ok(source.includes(original), "override anchor not found in generator");
  fs.writeFileSync(patchedGenerator, source.replace(original, '["PROTOCOL_ENVELOPE_INVALID", "PROTOCOL", "NEVER", { introducedInRelease: "2.0.0" }],'));
  const patchedTree = path.join(scratch, "patched-tree");
  generate(patchedGenerator, patchedTree);
  const codes = readJson("errors/error-codes.json", patchedTree).codes;
  assert.equal(codes.find((entry) => entry.code === "PROTOCOL_ENVELOPE_INVALID").introducedInRelease, "2.0.0");
  assert.deepEqual(
    codes.slice(1, RELEASED_CODE_COUNT).filter((entry) => entry.introducedInRelease !== "1.0.0").map((entry) => entry.code),
    [],
  );
});

test("release governance scopes ProtocolVersion to a profileId", () => {
  const governance = read("docs/release-governance.md");
  assert.match(governance, /ProtocolVersion is exactly 3 for this candidate/);
  assert.match(governance, /increases monotonically only within one `profileId`/);
  assert.match(governance, /`WIRE_TO_GATE_MVP` 0\.2\.0 and `AGV_FULL_PRODUCT` 1\.0\.0 are both ProtocolVersion 2/);
  assert.match(governance, /`WIRE_TO_GATE_MVP` 0\.3\.0 and `AGV_FULL_PRODUCT` 2\.0\.0 are both ProtocolVersion 3/);
  assert.match(governance, /complete `ProtocolReleaseIdentity`/);
  assert.match(governance, /`\(profileId, ProtocolVersion\)`/);
  assert.doesNotMatch(governance, /branched before that change reached/);
});

test("candidate limitations describe the 2.0.0 candidate against protocol-v1.0.0", () => {
  const limitations = read("docs/candidate-limitations.md");
  const lastParagraph = limitations.trim().split("\n\n").at(-1);
  assert.match(lastParagraph, /`protocol-v1\.0\.0` remains immutable/);
  assert.match(lastParagraph, /`2\.0\.0` candidate/);
  assert.match(lastParagraph, /ProtocolVersion increase to 3/);
  assert.match(lastParagraph, /`protocol-v2\.0\.0`/);
  assert.doesNotMatch(limitations, /0\.1\.1/);
});

test("compatibility report is based on protocol-v1.0.0 and summarises the seven changes", () => {
  const report = readJson("compatibility/report.json");
  assert.equal(report.candidateVersion, "2.0.0");
  assert.equal(report.protocolVersion, 3);
  assert.equal(report.profileId, PROFILE_ID);
  assert.equal(report.baseRelease, "protocol-v1.0.0");
  assert.equal(report.classification, "BREAKING_PROTOCOL_VERSION_INCREASE");
  assert.equal(report.wireCompatibility, "INCOMPATIBLE_EXACT_IDENTITY_REQUIRED");
  // Specification 6.3 items 1-6 plus 19.4's seventh, in that order, each named by the field it adds.
  const anchors = ["stationDepartureDeadlineAt", "expectedSublots", "slotResults", "SublotRejected", "chargingCycleState", "loadingPhase", "slotOperationAttemptId"];
  assert.ok(Array.isArray(report.changeSummary), "changeSummary is not a list");
  assert.equal(report.changeSummary.length, anchors.length);
  anchors.forEach((anchor, index) => assert.match(report.changeSummary[index], new RegExp(anchor), `item ${index + 1}`));
});

test("CONTEXT.md scopes ProtocolVersion to a profileId and no profile entry binds a single integer", () => {
  const context = fs.readFileSync(contextPath, "utf8").replace(/\r\n/g, "\n");
  const entry = (heading) => {
    const start = context.indexOf(`**${heading}**:`);
    assert.ok(start >= 0, `entry ${heading} not found`);
    const end = context.indexOf("\n\n", start);
    return context.slice(start, end < 0 ? undefined : end);
  };
  const protocolVersion = entry("ProtocolVersion（车载通信协议版本）");
  assert.doesNotMatch(protocolVersion, /第一版固定为 1/);
  assert.match(protocolVersion, /同一 `?profileId`? 内/);
  assert.match(protocolVersion, /WIRE_TO_GATE_MVP.*0\.2\.0.*AGV_FULL_PRODUCT.*1\.0\.0/s);
  assert.match(protocolVersion, /WIRE_TO_GATE_MVP.*0\.3\.0.*AGV_FULL_PRODUCT.*2\.0\.0/s);
  assert.match(protocolVersion, /ProtocolReleaseIdentity/);
  assert.match(protocolVersion, /\(profileId, ProtocolVersion\)/);
  assert.match(protocolVersion, /破坏性变更都?必须升级版本/);
  const mvpProfile = entry("WireToGateMvpProtocolProfile（WIRE_TO_GATE MVP 协议剖面）");
  assert.doesNotMatch(mvpProfile, /ProtocolVersion 1 中|ProtocolVersion 1 的剖面/);
  const fullProductProfile = entry("AgvFullProductProtocolProfile（完整产品协议剖面）");
  assert.doesNotMatch(fullProductProfile, /ProtocolVersion 2 中为/);
  assert.match(fullProductProfile, /1\.0\.0.*2.*2\.0\.0.*3/s);
});
