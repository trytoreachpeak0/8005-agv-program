# Ticket 15 TDD plan and requirement evidence

## Red-green vertical slices

1. Canonical artifact: source/build/runtime raw hashes match; missing, empty,
   tampered, or alternate SQL is rejected before the executor; static policy is
   one read-only SELECT with the six approved branches.
2. Oracle mapping: one executor call and one result map complete provider metadata
   to a `SUCCESS` round without trimming or de-duplicating raw values; bad/null
   field values remain evidence, while missing/duplicate/incompatible columns are
   `INCOMPLETE`.
3. Failure safety: timeout, command cancellation, execution, configuration, and
   artifact failures produce stable stage/code diagnostics with no SQL, credential,
   datasource, or raw-row values.
4. Provider modes: Thin is default; Thin and Thick select distinct adapters but
   share the exact canonical artifact/result contract; invalid Thick configuration
   fails diagnostically and never falls back to Thin.
5. Production polling: source -> runner -> `RoundIngestor`; only `SUCCESS` creates
   business projection state. The hosted service is single-flight and tied only to
   the Service host cancellation token.
6. Package/probe: one deployed SQL copy plus a verified manifest; Thin/Thick live
   probes record requested/actual mode, driver, query version/hash/outcome/count,
   while unavailable live Oracle is explicitly `NOT_EXECUTED`.
7. Formal SQL tracer: Production V2 Host with a fake Oracle executor commits the
   canonical `SUCCESS` round into real SQL Server and reads it from
   `/api/v2/poll-traces/{id}`; later failure/incomplete rounds create no business commit.

## Completed named evidence

| Requirement | Public-seam test evidence |
| --- | --- |
| One six-branch command/result | `One_round_passes_the_complete_six_branch_artifact_to_exactly_one_executor_call_and_one_result` |
| Canonical artifact integrity | `Source_build_output_and_runtime_artifact_have_identical_raw_sha256`; tamper/package tests |
| Read-only, timeout, cancellation | `Canonical_artifact_is_one_read_only_select_and_has_no_DML_DDL`; timeout/cancel source tests |
| Value anomaly vs structural outcome | `Complete_metadata_with_null_blank_invalid_and_duplicate_values_is_SUCCESS_and_preserves_exact_observations`; structural theory |
| Deep fake seam/digest/sanitization | executor request assertions, `MesTaskUnionRoundDigestTests`, safe diagnostic tests |
| Thin/Thick configuration | `Default_is_Thin`; provider-factory tests with no fallback |
| Factory probe truth | Oracle probe and factory manifest tests for `PASSED` / `FAILED` / `NOT_EXECUTED` |
| Production entry and Service ownership | `OracleMesTaskUnionProductionEntryTests`; hosted-service tests |
