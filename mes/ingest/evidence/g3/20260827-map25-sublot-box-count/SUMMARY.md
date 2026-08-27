# Map 25 SUBLOT_BOX_COUNT contract readiness

Result: `PUBLISHED_AND_DEPLOYED_V2_3_WITH_READ_ONLY_SUBLOT_BOX_COUNT_VERIFIED_FIELD_GATES_OPEN`

This evidence records a published and live-deployed, read-only MesIngest implementation
prerequisite for Wayfinder Map 25. It is not a formal W2G-IS-00 through W2G-IS-07 G3
PASS, did not call a RIoT mutation, and did not move a vehicle. The deployed product
revision is `c362b37950185fbff64a067b7a834521257a130d`.

## Frozen contract

- Contract: `2026.08.new-mes-ingest.v2.3`, schema `29`.
- Capability: `SUBLOT_BOX_COUNT|1.0|GET /api/v2/sublot-box-count`.
- Oracle artifact: `SUBLOT_BOX_COUNT/sha256:9aaee872311ee0c7a68e5722f8e7c97cf52e404d2d7c21c28794a599fafe6a24`.
- Input: exactly one non-blank `sublot`, at most 256 characters, passed as one
  provider bind parameter without SQL concatenation.
- Output: exact `queryId`, original `sublot`, positive integer `maxBoxCount`, and
  `observedAt` UTC identity. Missing, malformed, non-positive, fractional,
  overflowing, unavailable, or timed-out results fail closed.
- The release package carries exactly the two approved, hash-pinned, read-only SQL
  artifacts: `MES_TASK_UNION` and `SUBLOT_BOX_COUNT`. Publish, smoke, factory
  acceptance, scale/query, and manifest validation use the same allowlist.

## Verification

- Oracle statement-terminator regressions were demonstrated red before the artifact fix,
  then passed `2/2` after the fix. The tests cover the canonical SQL artifact and both
  Thin and Thick executor command text.
- Expanded endpoint, Oracle mode, canonical artifact, package, and evidence-gate filter:
  `118 passed, 0 failed, 0 skipped`.
- Release non-incremental solution build: `0 warnings, 0 errors`.
- Changed C# files pass targeted `dotnet format --verify-no-changes`; all changed
  PowerShell scripts pass the PowerShell parser; `git diff --check` passes.
- Final Tier 1 `dotnet test MesIngest.Tests`: `808 passed, 0 failed, 136 skipped`. The
  skipped tests require external SQL opt-in; the schema migration path is covered by the
  separate real-SQL runs below.

## Open gates

- The user explicitly authorized publishing the implementation branch together with
  its existing unpublished factory-validation ancestors and directly deploying Host and
  SQL Server without backups. The final product implementation is published as
  `codex/map25-sublot-box-count@c362b37950185fbff64a067b7a834521257a130d`
  and was fetched back from the remote at the same commit.
- The live Windows Service is deployed from that commit, is `Running`, starts
  automatically as `LocalSystem`, and advertises the exact v2.3/schema 29 capability.
- Map 25 still has seven unresolved AREA/EQP assignments. Battery threshold,
  approved runtime package-capacity configuration, Onboard credential, and a real
  stopped/parking signal provider remain open.
- RIoT mutation and vehicle movement still require separate authorization.

## 2026-08-27 v2.2 to v2.3 deployment finding and owner fix

The deployment owner authorized a direct Host-only publish without a Host or SQL Server
backup. The first v2.3 package replacement correctly refused to start against the live
v2.2/schema 29 database with SQL error 51008 because the database contract identity was
still v2.2. The failed start did not update the database. A temporary current-user Host
rebuilt from the exact former source commit `ea778a05195f701095e5ae8492a4c4a7ad83be56`
restored the v2.2 loopback API and successful Oracle polling while the Windows Service
remained stopped.

The owning branch now publishes the bounded migration fix as
`codex/map25-sublot-box-count@1d95e36395b162da9f033e514e12c967493dd12d`.
It advances only an otherwise fully validated v2.2/schema 29 database to v2.3 inside the
existing schema application lock and serializable transaction. It changes exactly
`mesingest.SchemaInfo.ContractVersion`; HistoryEpoch, snapshot signing key, tables, and
history remain unchanged. Unknown contract versions and every structural drift still fail
closed before the identity update.

- Focused migration regression: `3 passed, 0 failed, 0 skipped` on the real SQL Server.
- Complete empty-database/schema gate: `20 passed, 0 failed, 0 skipped` on the real SQL
  Server, using owned temporary databases that were removed by the harness.
- Release non-incremental solution build: `0 warnings, 0 errors`.
- Final Tier 1 `dotnet test MesIngest.Tests`: `808 passed, 0 failed, 136 skipped`. The
  skipped tests require the external SQL opt-in; the changed migration path is covered by
  the separate real-SQL 20/20 run above.
- The Host-only package generated from `1d95e363` passed its 866-file release-manifest
  validation.

The first successful v2.3 Windows Service deployment applied the approved bounded database
identity migration, after which the live supplemental read failed closed with HTTP 503.
The Windows Application log identified ODP.NET `ORA-00911`; the canonical supplemental
query carried a client statement terminator that ODP.NET does not accept. Product revision
`c362b37950185fbff64a067b7a834521257a130d` removes only that terminator, updates every
hash-pinned release surface to
`9aaee872311ee0c7a68e5722f8e7c97cf52e404d2d7c21c28794a599fafe6a24`, and adds regression
coverage. Its Host-only package passed the 866-file release-manifest validation.

The final no-backup administrator replacement completed successfully:

- Windows Service `MesIngest`: `Running`, `Auto`, `LocalSystem`.
- Installed source commit: `c362b37950185fbff64a067b7a834521257a130d`.
- Live contract: `2026.08.new-mes-ingest.v2.3`, schema `29`, exact capability
  `SUBLOT_BOX_COUNT|1.0|GET /api/v2/sublot-box-count`.
- Live SQL `mesingest.SchemaInfo`: v2.3/schema 29, 32-byte signing key, established
  HistoryEpoch, reset state `NOT_REQUIRED`.
- A current, non-blank WIRE_TO_GATE Sublot from the externally readable catalog was kept
  redacted and used for one live read-only Oracle request. The response query identity and
  Sublot identity matched, `maxBoxCount` was the positive integer `4`, and `observedAt`
  carried a zero UTC offset. A blank Sublot returned HTTP 400.

This closes only the deployable MesIngest prerequisite. Seven AREA/EQP assignments,
battery threshold, approved runtime package-capacity configuration, Onboard credential,
and a real stopped/parking signal provider remain open before formal G3. No RIoT mutation
or vehicle movement occurred.
