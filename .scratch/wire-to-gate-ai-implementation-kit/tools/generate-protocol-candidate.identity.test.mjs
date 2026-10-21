// Acceptance checks for the protocol 6.0.0 candidate identity (8005-agv-protocol#26; 5.0.0 was 8005-agv-protocol#21,
// 4.0.0 was 8005-agv-protocol#13, 3.0.0 was 8005-agv-program#146, 2.0.0 was #90).
// Run: node --test .scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.identity.test.mjs
// The seam is the generator's command line: every check generates a tree and reads what was written,
// never the generator's internals. Expected values come from the ticket, specification 6.2 and the
// released protocol-v5.0.0 tree, not from the generator's constants.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const toolsDirectory = path.dirname(fileURLToPath(import.meta.url));
const generatorPath = path.join(toolsDirectory, "generate-protocol-candidate.mjs");
const contextPath = path.resolve(toolsDirectory, "../../../CONTEXT.md");

const V7_BASE = "https://schemas.8005-agv.local/agv-full-product/v7/";
const PROFILE_ID = "AGV_FULL_PRODUCT";
// The 54 codes protocol-v1.0.0 released, anchored at both ends of that registry.
const RELEASED_CODE_COUNT = 54;
// The 58 codes protocol-v2.0.0 released: sha256 of JSON.stringify(codes) read from errors/error-codes.json
// at protocol commit 86575456 (tag protocol-v2.0.0). The registry is appendOnly, so a later release may
// only add codes after these; every one of them must stay byte-for-byte what 2.0.0 shipped.
const V2_RELEASED_CODE_COUNT = 58;
const V2_RELEASED_CODES_SHA256 = "af99e73b860560586aa027b0131fd09e1276e1840a051f86ad38bf683d4c388a";
// The 62 codes protocol-v3.0.0 released, hashed the same way from errors/error-codes.json at protocol commit 3f091cb2
// (tag protocol-v3.0.0). 4.0.0 and 5.0.0 add no code, so protocol-v5.0.0 released exactly these; 6.0.0 appends after them.
const V3_RELEASED_CODE_COUNT = 62;
const V3_RELEASED_CODES_SHA256 = "46fb60f3c2f649ecd379c3a1cbe7546ee836f28febaa806510d825267f803460";

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

test("every schema $id and $ref sits under agv-full-product/v7 and no v2, v3, v4, v5 or v6 URI remains", () => {
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
  assert.deepEqual(uris.filter((uri) => !uri.startsWith(V7_BASE)), []);
  // No file mentions an earlier segment at all, prose included.
  for (const earlier of ["agv-full-product/v2", "agv-full-product/v3", "agv-full-product/v4", "agv-full-product/v5", "agv-full-product/v6"]) {
    const hits = files.filter((file) => fs.readFileSync(file, "utf8").includes(earlier));
    assert.deepEqual(hits.map((file) => path.relative(tree, file)), [], earlier);
  }
});

test("ProtocolVersion is 7 wherever the wire pins it, under an unchanged profileId", () => {
  const envelope = readJson("schemas/envelope.schema.json");
  assert.equal(envelope.properties.protocolVersion.const, 7);
  assert.equal(envelope.properties.profileId.const, PROFILE_ID);
  const messageFiles = fs.readdirSync(path.join(tree, "schemas/messages"));
  assert.ok(messageFiles.length > 0);
  for (const file of messageFiles) {
    const schema = readJson(`schemas/messages/${file}`);
    assert.equal(schema.properties.protocolVersion.const, 7, file);
    assert.equal(schema.properties.profileId.const, PROFILE_ID, file);
  }
  assert.equal(payloadOf("SessionHello").supportedProtocolVersion.const, 7);
  assert.equal(payloadOf("SessionHello").profileId.const, PROFILE_ID);
  assert.equal(payloadOf("SessionRejected").expectedProtocolVersion.const, 7);
  assert.equal(payloadOf("ProtocolProblem").expectedProtocolVersion.const, 7);
  assert.equal(payloadOf("ProtocolProblem").expectedProfileId.const, PROFILE_ID);
  const identity = readJson("schemas/common/types.schema.json").$defs.ProtocolReleaseIdentity.properties;
  assert.equal(identity.protocolVersion.const, 7);
  assert.equal(identity.profileId.const, PROFILE_ID);
});

test("release version is 6.0.0 in the package, the seed manifest and a still-pending attestation template", () => {
  assert.equal(readJson("package.json").version, "6.0.0");
  const manifest = readJson("manifest/release.json");
  assert.equal(manifest.releaseVersion, "6.0.0");
  assert.equal(manifest.protocolVersion, 7);
  assert.equal(manifest.profileId, PROFILE_ID);
  const template = readJson("attestations/release-approval.template.json");
  assert.equal(template.candidateVersion, "6.0.0");
  assert.equal(template.status, "PENDING");
});

test("the codes released in 1.0.0 keep introducedInRelease 1.0.0 under registry version 1.3.0", () => {
  const registry = readJson("errors/error-codes.json");
  assert.equal(registry.registryVersion, "1.3.0");
  assert.equal(registry.appendOnly, true);
  const released = registry.codes.slice(0, RELEASED_CODE_COUNT);
  assert.equal(released.length, RELEASED_CODE_COUNT);
  assert.equal(released[0].code, "PROTOCOL_ENVELOPE_INVALID");
  assert.equal(released[RELEASED_CODE_COUNT - 1].code, "RECOVERY_RESULT_REQUIRED");
  assert.deepEqual(released.filter((entry) => entry.introducedInRelease !== "1.0.0").map((entry) => entry.code), []);
});

test("the 58 codes released in 2.0.0 stay byte-for-byte at the head of the registry", () => {
  const codes = readJson("errors/error-codes.json").codes;
  assert.ok(codes.length >= V2_RELEASED_CODE_COUNT, `registry has ${codes.length} codes`);
  const released = codes.slice(0, V2_RELEASED_CODE_COUNT);
  assert.equal(crypto.createHash("sha256").update(JSON.stringify(released)).digest("hex"), V2_RELEASED_CODES_SHA256);
  // Readable restatement of what the hash pins: 54 codes from 1.0.0, then the four 2.0.0 added.
  assert.deepEqual(
    released.slice(RELEASED_CODE_COUNT).map((entry) => `${entry.code}@${entry.introducedInRelease}`),
    ["SUBLOT_NOT_IN_DISPATCH_SCOPE@2.0.0", "SUBLOT_BOX_COUNT_UNAVAILABLE@2.0.0", "PACKAGE_CAPACITY_UNRESOLVED@2.0.0", "OPERATOR_TIMEOUT@2.0.0"],
  );
});

test("every code appended after the 58 released in 2.0.0 and before the 3.0.0 boundary is introduced in 3.0.0", () => {
  const appended = readJson("errors/error-codes.json").codes.slice(V2_RELEASED_CODE_COUNT, V3_RELEASED_CODE_COUNT);
  assert.equal(appended.length, V3_RELEASED_CODE_COUNT - V2_RELEASED_CODE_COUNT);
  assert.deepEqual(appended.filter((entry) => entry.introducedInRelease !== "3.0.0").map((entry) => `${entry.code}@${entry.introducedInRelease}`), []);
});

test("the 62 codes released in 3.0.0 stay byte-for-byte at the head of the registry", () => {
  // 4.0.0 reuses WORKLIST_REVISION_STALE, STATION_MISMATCH and ACTION_NOT_ALLOWED_IN_STATE and adds no code, nor does 5.0.0, so
  // protocol-v5.0.0 (18d4fb34) released exactly these 62 under registry version 1.2.0.
  const codes = readJson("errors/error-codes.json").codes;
  assert.ok(codes.length >= V3_RELEASED_CODE_COUNT, `registry has ${codes.length} codes`);
  assert.equal(crypto.createHash("sha256").update(JSON.stringify(codes.slice(0, V3_RELEASED_CODE_COUNT))).digest("hex"), V3_RELEASED_CODES_SHA256);
});

test("6.0.0 appends exactly its three codes after the 62 protocol-v5.0.0 released, under registry version 1.3.0", () => {
  // 8005-agv-protocol#26 (CP-0021): the skipped-slot marker, the skip refused with nothing loaded, and the cancellation refused
  // once a basket is loaded. generate-protocol-candidate.remaining-baskets-skip.test.mjs checks what each of them says.
  const registry = readJson("errors/error-codes.json");
  assert.equal(registry.registryVersion, "1.3.0");
  assert.deepEqual(
    registry.codes.slice(V3_RELEASED_CODE_COUNT).map((entry) => `${entry.code}@${entry.introducedInRelease}`),
    ["REMAINING_BASKET_SKIPPED@6.0.0", "REMAINING_BASKETS_SKIP_NOTHING_LOADED@6.0.0", "LOAD_CANCELLATION_BASKET_LOADED@6.0.0"],
  );
});

test("the rendered finalize tool stamps the content snapshot with the 6.0.0 identity", () => {
  // finalize-manifest.mjs is rendered from a template; the snapshot it writes is what G1 and both products
  // compare, so its identity is checked where it is rendered, not in the template.
  const finalize = read("tools/finalize-manifest.mjs");
  assert.match(finalize, /releaseVersion:"6\.0\.0",protocolVersion:7,profileId:"AGV_FULL_PRODUCT"/);
  assert.doesNotMatch(finalize, /__[A-Z0-9_]+__/);
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
  assert.match(governance, /ProtocolVersion is exactly 7 for this candidate/);
  assert.match(governance, /increases monotonically only within one `profileId`/);
  assert.match(governance, /`WIRE_TO_GATE_MVP` 0\.2\.0 and `AGV_FULL_PRODUCT` 1\.0\.0 are both ProtocolVersion 2/);
  assert.match(governance, /`WIRE_TO_GATE_MVP` 0\.3\.0 and `AGV_FULL_PRODUCT` 2\.0\.0 are both ProtocolVersion 3/);
  assert.match(governance, /`AGV_FULL_PRODUCT` 3\.0\.0 is ProtocolVersion 4/);
  assert.match(governance, /`AGV_FULL_PRODUCT` 4\.0\.0 is ProtocolVersion 5/);
  assert.match(governance, /`AGV_FULL_PRODUCT` 5\.0\.0 is ProtocolVersion 6/);
  assert.match(governance, /`AGV_FULL_PRODUCT` 6\.0\.0 is ProtocolVersion 7/);
  assert.match(governance, /complete `ProtocolReleaseIdentity`/);
  assert.match(governance, /`\(profileId, ProtocolVersion\)`/);
  assert.doesNotMatch(governance, /branched before that change reached/);
});

test("candidate limitations describe the 6.0.0 candidate against protocol-v5.0.0", () => {
  const limitations = read("docs/candidate-limitations.md");
  const lastParagraph = limitations.trim().split("\n\n").at(-1);
  assert.match(lastParagraph, /`protocol-v5\.0\.0` remains immutable/);
  assert.match(lastParagraph, /`6\.0\.0` candidate/);
  assert.match(lastParagraph, /ProtocolVersion increase to 7/);
  assert.match(lastParagraph, /`protocol-v6\.0\.0`/);
  assert.doesNotMatch(limitations, /`5\.0\.0` candidate|`4\.0\.0` candidate|`3\.0\.0` candidate|`2\.0\.0` candidate|protocol-v1\.0\.0|protocol-v2\.0\.0/);
  assert.doesNotMatch(limitations, /0\.1\.1/);
});

test("compatibility report is based on protocol-v5.0.0 and summarises its changes", () => {
  const report = readJson("compatibility/report.json");
  assert.equal(report.candidateVersion, "6.0.0");
  assert.equal(report.protocolVersion, 7);
  assert.equal(report.profileId, PROFILE_ID);
  assert.equal(report.baseRelease, "protocol-v5.0.0");
  assert.equal(report.classification, "BREAKING_PROTOCOL_VERSION_INCREASE");
  assert.equal(report.wireCompatibility, "INCOMPATIBLE_EXACT_IDENTITY_REQUIRED");
  // The 5.0.0 sentences are released history: protocol-v5.0.0 (18d4fb34) carries them. 6.0.0 has the one change of
  // protocol#26; generate-protocol-candidate.remaining-baskets-skip.test.mjs checks what that sentence says.
  const anchors = [/RemainingBasketsSkipRequested.*RemainingBasketsSkipResult/];
  assert.ok(Array.isArray(report.changeSummary), "changeSummary is not a list");
  assert.equal(report.changeSummary.length, anchors.length);
  anchors.forEach((anchor, index) => assert.match(report.changeSummary[index], anchor, `item ${index + 1}`));
  // One change per sentence: a full stop followed by a space would start a second sentence.
  report.changeSummary.forEach((sentence, index) => {
    assert.match(sentence, /\.$/, `item ${index + 1} does not end a sentence`);
    assert.doesNotMatch(sentence, /\. /, `item ${index + 1} holds more than one sentence`);
  });
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
  assert.match(protocolVersion, /`AGV_FULL_PRODUCT` 3\.0\.0 为 4，4\.0\.0 为 5，5\.0\.0 为 6，6\.0\.0 为 7/);
  assert.match(protocolVersion, /ProtocolReleaseIdentity/);
  assert.match(protocolVersion, /\(profileId, ProtocolVersion\)/);
  assert.match(protocolVersion, /破坏性变更都?必须升级版本/);
  const mvpProfile = entry("WireToGateMvpProtocolProfile（WIRE_TO_GATE MVP 协议剖面）");
  assert.doesNotMatch(mvpProfile, /ProtocolVersion 1 中|ProtocolVersion 1 的剖面/);
  const fullProductProfile = entry("AgvFullProductProtocolProfile（完整产品协议剖面）");
  assert.doesNotMatch(fullProductProfile, /ProtocolVersion 2 中为/);
  assert.match(fullProductProfile, /1\.0\.0.*2.*2\.0\.0.*3/s);
  assert.match(fullProductProfile, /3\.0\.0 为 ProtocolVersion 4，4\.0\.0 为 ProtocolVersion 5，5\.0\.0 为 ProtocolVersion 6，6\.0\.0 为 ProtocolVersion 7/);
});
