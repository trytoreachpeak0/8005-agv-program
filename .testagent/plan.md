# Ticket 4 exact API cutover vertical test plan

Add one failing public-seam test, run only that method/class, make the minimum
production change, and continue. Do not run Tier 1 until product, tests,
canonical OpenAPI, and package inputs are final.

## 1. Old-epoch Host contract and client signal

### `ExternallyReadableDemandCatalogTests.cs`

Convert the existing old-epoch test to
`Conditional_catalog_identity_from_an_old_history_epoch_returns_typed_409_mismatch`:

- Reuse its minimum old/new databases and old weak ETag.
- Assert 409, `application/json`, exact `code`/`error` plus the non-null
  `currentHistoryEpoch`/`suppliedHistoryEpoch` UUIDs, and exact
  `HISTORY_EPOCH_MISMATCH`.
- Assert no misleading 304/body/ETag and no database identity mutation.

### `NewMesIngestOpenApiContractTests.cs`

Extend the frozen semantics test: catalog has 409, description includes the
stable code, and JSON content uses the typed error schema.

### `HttpExternallyReadableDemandCatalogClientTests.cs`

Add
`Conditional_old_epoch_409_maps_the_typed_history_epoch_mismatch_signal`:

- Exact contract discovery then the four-field catalog 409 typed body.
- Assert the dedicated stable signal preserves status/code/detail.
- A 409 with another code and other statuses retain generic error behavior.

## 2. ReferenceConsumer single retry

### `DemandCatalogReferenceConsumerTests.cs`

Add
`Refresh_old_epoch_conflict_discards_the_stale_cache_and_retries_once_unconditionally`:

- First refresh installs old snapshot.
- Next refresh call identities are exactly `[old identity, null]`.
- Unconditional read returns new epoch; returned/cache identity is wholly new.
- A later refresh conditions on the new identity.

Add
`Refresh_old_epoch_conflict_does_not_loop_when_the_unconditional_retry_fails`:

- Seed old cache; mismatch conditional read; fail unconditional retry.
- Assert exactly two reads, terminal error escapes, and next refresh begins
  with `knownIdentity: null`, proving stale cache clear.
- Do not add retry to already-unconditional `AcceptAsync`.

## 3. Explicit by-key query contract

### `NewMesIngestOpenApiContractTests.cs`

Add theory
`Demand_series_by_key_missing_empty_or_repeated_identity_is_typed_invalid_query`
with these rows:

1. no query;
2. only `workType`;
3. only `sublot`;
4. empty `workType`;
5. empty `sublot`;
6. whitespace-only `workType`;
7. whitespace-only `sublot`;
8. repeated equal `workType`;
9. repeated different `workType`;
10. repeated equal `sublot`;
11. repeated different `sublot`.

Every row asserts 400, JSON content type, exactly `code`/`error`, exact
`INVALID_DEMAND_SERIES_QUERY`, and nonblank error. Use the isolated fixture;
invalid input must not reach SQL. Retain existing evidence that a nonblank
whitespace-preserving key is not trimmed.

## 4. Raw `fields` compatibility

### `ErrorSearchDetailTests.cs`

Extend/rename the existing minimum authorized test to
`Raw_evidence_accepts_comma_repeated_and_mixed_fields_with_the_same_bounded_projection`.

On one snapshot/evidence fixture compare:

- `fields=workType,package`;
- `fields=workType&fields=package`;
- `fields=workType,package&fields=package`.

Assert all succeed with identical `includedFields`, item field names/order,
redaction, item count, and bounded payload. Preserve authorization-first and
disallowed-field coverage.

### `NewMesIngestOpenApiContractTests.cs`

Freeze `fields` as the exact seven-value string array, `style=form`, effective
explode true (explicit or OpenAPI default), and text stating repeated keys are
canonical while comma segments remain compatible. Keep the Watch comma URI
test as a compatibility canary; no UI change.

## 5. 503, storage enum, scheduler DTO

### `NewMesIngestOpenApiContractTests.cs`

Add/extend
`Openapi_publishes_both_not_current_causes_storage_status_and_exact_scheduler_shape`:

- Catalog 503 includes `INGEST_NOT_CURRENT`, `StoragePressurePause`, and pending
  HistoryReset acknowledgement.
- `StoragePressureStateDto.status` enum is exactly `HEALTHY`,
  `CRITICAL_WARNING`, `STORAGE_PRESSURE_PAUSE`.
- Current Attention 200 references the actual operational DTO and contains
  `pollScheduler`.
- `PollSchedulerStateDto` contains exactly five Ticket 3 fields.
- Integers are non-nullable; `nextAllowedStart`, `lastSuccessAt`, and
  `pollTraceId` are explicitly nullable; timestamps are `date-time`. Keep the
  existing repository required-vs-nullable convention without globally
  changing unrelated DTOs.

### `SingleFlightPollLoopTests.cs`

Retain existing 60/120/300/reset tests as the only scheduling-math authority.
Refocus the current serialization evidence into:

- `Not_started_scheduler_state_serializes_the_exact_five_field_nullable_contract`
  asserting exact `0,0,null,null,null`.
- `Current_attention_copies_the_coordinator_observer_snapshot_without_recomputing_backoff`
  seeding deliberately non-derived values (e.g. failure count 7/backoff level
  2) and asserting exact copy. This kills Host recalculation.

### `WatchV2ApiClientTests.cs`

Add
`Current_attention_consumes_the_exact_scheduler_wire_without_a_UI_fallback`:

- Script exact v2.4 contract and all five scheduler fields.
- Assert the non-UI returned model carries the values.
- Missing/malformed scheduler fails as a contract violation, not defaults or
  ignored data.
- Touch no presentation/view/window/XAML/layout/visual code.

## 6. Exact v2.4/schema 29 identity

### `NewMesIngestContractFreezeTests.cs`

Freeze:

- `2026.08.new-mes-ingest.v2.4`, schema `29`;
- recommended changed capabilities
  `CURRENT_INGEST_ATTENTION/2.1`, `DEMAND_SERIES/2.1`, `ERROR_SEARCH/2.2`,
  `EXTERNALLY_READABLE_DEMAND_CATALOG/2.1`;
- all other IDs/versions/GET paths unchanged; no V3/old surface.

Compatibility cases must reject v2.3, schema drift, each old changed capability
version, missing/extra/duplicate/null capability, and missing fields before
business interpretation.

### `EmptyDatabaseBootstrapTests.cs`

Replace the old migration evidence with:

- `Exact_v2_3_schema_29_identity_migrates_to_v2_4_without_replacing_history`:
  capture HistoryEpoch, signing-key hash, table/PollTrace evidence; assert only
  ContractVersion advances and schema remains 29.
- `Structurally_drifted_v2_3_schema_29_is_rejected_before_identity_migration`:
  preserve existing column-drift mutation and assert identity/history unchanged.
- Update unapproved identity rows so v2.2/arbitrary versions cannot skip the
  sole v2.3 -> v2.4 transition.

### Consumer identities

- Extend
  `WatchV2ApiClientTests.Contract_discovery_rejects_an_old_capability_version_before_business_reads`
  for v2.3 and all changed old capability versions, asserting zero business
  requests.
- Extend
  `HttpExternallyReadableDemandCatalogClientTests.Contract_discovery_mismatch_refuses_business_interpretation_before_catalog_read`
  identically.
- Continue using centralized `RequireExactCompatibility`; no fallback tables.

## 7. Canonical and package/release gates

1. After runtime schema is final, use the existing one-shot exporter with
   `MES_INGEST_EXPORT_V2_OPENAPI=1` to update only
   `pack/openapi/v2.json` (indented LF plus final newline).
2. Run
   `NewMesIngestOpenApiContractTests.Live_v2_openapi_matches_the_canonical_pack_snapshot`
   for semantic exactness.
3. Retain
   `ReleasePackageValidationTests.Release_smoke_rejects_semantically_equal_openapi_byte_drift_before_database_access`
   for byte exactness.
4. Extend OpenAPI classifier coverage so scheduler fields/nullability, 409,
   storage enum, and query serialization drift remain observable.
5. Update existing package assertions, not a second flow:
   - `Complete_read_only_package_is_accepted_and_gets_a_hashed_manifest`;
   - `Missing_or_noncanonical_v2_openapi_is_rejected`;
   - `Watch_built_against_a_different_contract_assembly_is_rejected`;
   - install/upgrade text tests;
   - affected cutover/release/factory/scale identity fixtures.
6. Keep `Package_with_test_fake_or_visual_candidate_is_rejected` green.

## Suggested narrow feedback order

Use the `run-tests` skill for exact xUnit/VSTest filter syntax before execution:

1. `HttpExternallyReadableDemandCatalogClientTests`
2. `DemandCatalogReferenceConsumerTests`
3. converted old-epoch catalog method
4. by-key/OpenAPI methods
5. raw-evidence method
6. scheduler/Watch client methods
7. `NewMesIngestContractFreezeTests`
8. exact `EmptyDatabaseBootstrapTests` migration methods
9. canonical semantic test
10. affected release/install/cutover/scale identity methods

No Tier 2/3. No Tier 1 during slices.

## Final audit and one Tier 1 run

- Verify exact 409 runtime/OpenAPI agreement.
- Verify consumer requests `[old,null]`, no third call, cache clear on failure.
- Verify every missing/empty/repeated by-key row and both raw serialization forms.
- Verify scheduler exact fields/nulls come from observer and Watch consumes them.
- Verify v2.4/schema 29/capabilities across Host, SQL, clients, canonical, package,
  release/factory/cutover/scale inputs.
- Verify live/canonical semantic equality and package byte/hash equality.
- Verify diff has no Ticket 5, `*.xaml`, UI/layout/visual baseline, prototype,
  fake data, or unrelated ADR.
- Then run exactly once from `mes/ingest/csharp`:
  `dotnet test MesIngest.Tests`.
- Report Passed/Failed/Skipped. If SQL environment variables are absent, report
  skips explicitly. Rerun only if production/test/contract inputs change after
  that run, per root `AGENTS.md`.

## Requirement | planned evidence

| User requirement (verbatim) | Planned concrete evidence |
| --- | --- |
| `旧 HistoryEpoch ETag 返回 HTTP 409，稳定 code=HISTORY_EPOCH_MISMATCH 与明确 typed body` | `Conditional_catalog_identity_from_an_old_history_epoch_returns_typed_409_mismatch` plus OpenAPI 409 assertions. |
| `ReferenceConsumer 识别该响应，丢弃 stale conditional cache，并且只重试一次无条件请求，防止循环` | Client mapping plus both `Refresh_old_epoch_conflict_*` sequence tests. |
| `缺失、空值和重复 workType/sublot 都返回稳定 INVALID_DEMAND_SERIES_QUERY typed JSON` | `Demand_series_by_key_missing_empty_or_repeated_identity_is_typed_invalid_query` rows 1-11. |
| `raw-evidence fields 同时接受重复 query key 和逗号分隔形式，保持兼容；修正 OpenAPI serialization/documentation` | Raw equivalence test plus style/explode/docs freeze. |
| `INGEST_NOT_CURRENT 的 503 文档同时覆盖 StoragePressurePause 与未确认 HistoryReset` | Combined OpenAPI exact test. |
| `StoragePressureStateDto.status 发布准确 enum：HEALTHY、CRITICAL_WARNING、STORAGE_PRESSURE_PAUSE` | Exact three-value assertion in combined OpenAPI test. |
| `正式发布 Ticket 3 的 scheduler state DTO/字段到 exact contract，字段来源必须是 coordinator observer，不在 Host 重算退避` | Not-started/exact-copy tests, OpenAPI schema, Watch non-UI wire test. |
| `一次性升级到 v2.4/schema 29` | Contract freeze, exact v2.3->v2.4 SQL transition, clients, canonical, package/release tests. |
| `不得把 prototype vocabulary 或 fake data 带入生产` | Existing package rejection test plus diff audit. |
| `不得运行 Tier 2/3，因为不改 UI/XAML` | Validation log shows narrow tests and one final Tier 1 only; diff audit shows no UI/XAML. |
