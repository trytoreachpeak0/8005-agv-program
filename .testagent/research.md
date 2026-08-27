# Ticket 4 exact API cutover test research

## Scope and authority

- Detached HEAD is exactly `b5c013b0bf86c5d6551b0fc210ddec979c37ec86`.
- Authority: root `AGENTS.md`, the 2026-08-27 host-remediation handoff,
  `.scratch/mes-ingest-bounded-storage-low-memory/spec.md`, historical Ticket
  20, Ticket 19, `.scratch/new-mes-ingest/spec.md`, and the current Ticket 3
  scheduler observer seam.
- Ticket 20 is earlier exact-cutover prior art (then v2.1/schema 28), not the
  current version authority. This task is one v2.4/schema 29 cutover from the
  current v2.3/schema 29 baseline.
- No spec imposes stronger scheduler field names than Ticket 3. Its names are
  authoritative: `consecutiveFailures`, `backoffLevel`, `nextAllowedStart`,
  `lastSuccessAt`, `pollTraceId`.
- This pass changes only `.testagent/research.md` and `.testagent/plan.md`; it
  runs no tests and touches no product/test code, Ticket 5, Watch UI/XAML,
  visual baseline, prototype, or ADR.
- `find-untested-sources` is unavailable (`Get-Command` found nothing), so one
  bounded `rg` source/test pairing pass was used.

## Actual repository test conventions

- `MesIngest.Tests` is xUnit 2.4.2 on `net8.0-windows` through VSTest. There is
  no MSTest package. New tests must use existing `[Fact]`/`[Theory]`, direct
  xUnit assertions, and descriptive snake-case names.
- HTTP contracts use production `WebApplicationFactory<Program>`, `HttpClient`,
  and exact `JsonDocument`/`JsonNode` assertions. Invalid-query tests can use
  the isolated contract fixture without SQL/Oracle.
- SQL tests use `[Collection("Ticket01SqlServer")]`,
  `[Ticket01SqlServerFact]`, a minimum disposable database, and public HTTP/SQL
  identity evidence.
- Client tests use scripted `HttpMessageHandler` or small interface doubles and
  assert request sequences rather than private cache state.
- `Live_v2_openapi_matches_the_canonical_pack_snapshot` is the semantic
  runtime/canonical gate. `ReleasePackageValidationTests` supplies canonical
  byte/hash drift coverage. The exporter writes indented LF JSON with one final
  newline.

## Verified gaps and bounded targets

### Old HistoryEpoch ETag

- Catalog Host catches `IngestNotCurrentException` but not
  `HistoryEpochMismatchException`, so stale epoch currently escapes as 500/test
  exception.
- Stable `HISTORY_EPOCH_MISMATCH` already exists. The cutover publishes the
  dedicated non-null body `{code,error,currentHistoryEpoch,suppliedHistoryEpoch}`
  so recovery does not parse prose and both identities are deterministic UUIDs.
- HTTP ReferenceConsumer client maps every non-200/304 to generic
  `HttpRequestException`; `DemandCatalogReferenceConsumer.RefreshAsync` has no
  stale-cache recovery.
- Convert existing
  `ExternallyReadableDemandCatalogTests.Conditional_catalog_identity_from_an_old_history_epoch_is_rejected`
  to public 409 evidence. Add direct HTTP client signal mapping and consumer
  call-sequence tests `[old identity, null]`, including a failed unconditional
  retry proving no third request and cache clear.

### Demand-series by-key

- Handler parameters are non-nullable auto-bound strings. Missing values may be
  rejected before the stable handler body; duplicates are not explicitly
  rejected.
- Explicit `HttpRequest.Query` parsing must make missing, empty,
  whitespace-only, repeated-same, and repeated-different `workType`/`sublot`
  return 400 `{code,error}` with `INVALID_DEMAND_SERIES_QUERY`.
- Preserve ordinal/case-sensitive/whitespace-preserving identity; do not trim a
  valid nonblank key.

### Raw-evidence `fields`

- Parser accepts only one comma-joined value because it calls
  `ReadErrorSearchSingle`; OpenAPI publishes a form array whose effective
  exploded representation sends repeated keys.
- Flatten all repeated values and split each by comma before existing
  trim/distinct/allow-list validation. Keep comma-form Watch compatibility.
- Reuse
  `ErrorSearchDetailTests.Raw_evidence_requires_explicit_authorization_and_returns_only_whitelisted_redacted_bounded_fields`
  to compare comma, repeated, and mixed forms in one minimum fixture.
- Publish standard `style=form` exploded-array semantics and explicitly
  document comma compatibility.

### 503 and storage enum

- Catalog 503 docs mention only StoragePressurePause, but Ticket 19/spec also
  require 503 `INGEST_NOT_CURRENT` while HistoryReset acknowledgement is pending.
- `StoragePressureStateDto.status` lacks the exact OpenAPI enum although core
  constants already define `HEALTHY`, `CRITICAL_WARNING`, and
  `STORAGE_PRESSURE_PAUSE`.

### Ticket 3 scheduler publication

- Scheduler math is already authoritative in `SingleFlightPollLoop`, which
  emits immutable `PollSchedulerStateSnapshot` through
  `IPollSchedulerStateObserver`; Host stores it in singleton
  `PollSchedulerState`.
- Runtime Current Attention already serializes a Host operational wrapper with
  `pollScheduler`, but OpenAPI advertises `CurrentIngestAttentionDto` and omits
  it. Watch wire also stops at `storagePressure` and ignores the runtime field.
- Exact five-field not-started state is `0,0,null,null,null`. Tests must prove
  runtime copies deliberately non-derived observer values so Host-side backoff
  recalculation cannot pass.
- Watch changes are limited to exact identity/wire consumption and missing-field
  rejection; no presentation, UI, XAML, layout, or fake data.

### v2.4/schema 29 identity/package

- Current identity is v2.3/schema 29. The bounded capability recommendation is
  `CURRENT_INGEST_ATTENTION/2.1`, `DEMAND_SERIES/2.1`, `ERROR_SEARCH/2.2`, and
  `EXTERNALLY_READABLE_DEMAND_CATALOG/2.1`; leave other versions unchanged. No
  spec provides stronger assignments.
- Current SQL-only approved identity migration is v2.2 -> v2.3. Replace it with
  exactly v2.3/schema 29 -> v2.4/schema 29, preserving HistoryEpoch, signing
  key, history, and structure while refusing v2.2, unknown identities, and
  structural drift.
- Update core freeze, canonical OpenAPI, embedded client fixtures, SQL identity
  transition, Watch/ReferenceConsumer compatibility, release-package validator,
  release smoke, factory acceptance, cutover/scale identity fixtures, and
  upgrade text together. Do not add V3, fallback DTOs, or dual routes.

## Source/test pairing

| Target | Existing test home | Ticket 4 evidence |
| --- | --- | --- |
| Catalog stale epoch Host mapping | `ExternallyReadableDemandCatalogTests` | Typed 409/code/body and no stale ETag/304. |
| Reference HTTP client | `HttpExternallyReadableDemandCatalogClientTests` | Decode only exact 409/code as stale-epoch signal. |
| Reference cache recovery | `DemandCatalogReferenceConsumerTests` | `[old,null]`, replace/clear cache, one retry only. |
| By-key parser | `NewMesIngestOpenApiContractTests` | Missing/empty/repeated HTTP theory. |
| Raw fields | `ErrorSearchDetailTests` | Comma/repeated/mixed equivalence. |
| OpenAPI | `NewMesIngestOpenApiContractTests` | 409 schema, fields style/docs, two 503 causes, enum, scheduler shape. |
| Coordinator/Host state | `SingleFlightPollLoopTests` | Keep existing math tests; freeze not-started/copy wire only. |
| Watch non-UI wire | `WatchV2ApiClientTests` | Consume exact scheduler; reject missing/malformed. |
| Identity/capabilities | `NewMesIngestContractFreezeTests` | v2.4/schema 29 exact set. |
| SQL identity transition | `EmptyDatabaseBootstrapTests` | v2.3 -> v2.4 only, preservation/drift rejection. |
| Canonical/package | OpenAPI classifier, release/install/cutover/scale tests | Semantic equality plus byte/hash and release identity. |

## Acceptance mapping

| Requirement | Planned evidence |
| --- | --- |
| 409 `HISTORY_EPOCH_MISMATCH` typed body | Converted real-SQL catalog test and OpenAPI 409 typed schema. |
| ReferenceConsumer clears stale cache/retries unconditionally once | HTTP mapping plus two consumer request-sequence tests. |
| Missing/empty/repeated by-key query is typed invalid query | One isolated HTTP theory covering both keys and every shape. |
| Repeated/comma raw fields and OpenAPI docs | One SQL equivalence test plus style/explode/description freeze. |
| Both 503 causes | Exact OpenAPI description assertion. |
| Exact storage enum | Exact three-value schema assertion. |
| Scheduler from coordinator observer | Runtime exact-copy/not-started, OpenAPI, and Watch wire tests; existing loop tests own math. |
| v2.4/schema 29 one cutover | Contract/SQL migration/consumer/canonical/package/release tests together. |
| No Ticket 5/UI/prototype | Final path diff audit. |
| One final Tier 1, no Tier 2/3 | Parent records narrow runs then one final Passed/Failed/Skipped summary. This pass ran none. |

## High-risk mutations

- Return 400/410/500 or an untyped/renamed old-epoch body.
- Retry conditionally, retry more than once, or retain stale cache after rebuild
  failure.
- Let Minimal API own missing-key failure, accept duplicate-same values, or trim
  nonblank identity.
- Accept only comma or only repeated raw fields.
- Document one 503 cause or arbitrary storage status.
- Serialize scheduler but omit it from OpenAPI/Watch, rename fields, or
  recalculate backoff in Host.
- Leave any capability/release validator on v2.3, permit v2.2 fallback, or allow
  semantic-equal but byte-different canonical packaging.
- Pull Ticket 5, Watch UI/XAML, prototype/fake data, or unrelated ADR into diff.
