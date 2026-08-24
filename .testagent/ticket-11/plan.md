# Ticket 11 TDD plan

Work one vertical slice at a time. This pass implements only the first red tests; production changes belong to the parent implementation run.

## Phase 1 — first red object-boundary regressions

Add `MesIngest.Tests/PollTraceRawEvidenceCutoverTests.cs` with:

1. `PollTrace_read_is_bound_to_exact_trace_and_commit_and_preserves_the_raw_multiset`
   - Real SQL Server + production domain + V2 HTTP.
   - Seeds duplicate, invalid, null, and unassigned evidence.
   - Injects a referentially valid foreign-commit observation under the target PollTraceId.
   - Asserts exact PollTrace/ProjectionCommit identity, HistoryEpoch, earliest Host UTC boundary, exact ordinals, duplicates, nulls, and invalid raw values.
   - Covers checklist items 1, 2, 3, and the available branch of item 4.

2. `PollTrace_read_distinguishes_expired_from_never_existing_and_shares_the_earliest_boundary`
   - Real SQL Server + production domain + V2 HTTP.
   - Keeps the old PollTrace identity but deletes its raw rows, leaving a newer retained PollTrace as the earliest available object.
   - Asserts 410 `MES_INGEST_HISTORY_EXPIRED` versus 404 `POLL_TRACE_NOT_FOUND`, with the same HistoryEpoch and earliest boundary on both errors and the successful retained read.
   - Covers the three-state branch of checklist item 4 and checklist item 5.

3. `Packaged_scale_gate_requires_real_SQL_bounds_for_PollTrace_and_raw_evidence_reads`
   - Fail-closed source contract for the packaged real-SQL evidence runner.
   - Requires selectable PollTrace and raw-evidence surfaces, actual response-byte capture, explicit response-size rejection, logical-read/grant growth checks, spill rejection, and abnormal-grant rejection.
   - Covers checklist items 6–9 without fabricating performance numbers in a unit test.

Expected first-red failures on the current production code:

- PollTrace JSON has no `historyEpoch` or `earliestAvailableHostUtc`.
- Raw observations are filtered only by PollTraceId, so the injected foreign-commit row leaks.
- A formerly populated PollTrace whose raw rows are unavailable returns 200 instead of 410.
- The packaged scale gate has no `PollTrace` query-surface declaration or PollTrace response-size limit.

## Phase 2 — green domain/SQL/HTTP cutover

- Introduce a typed historical-object read result that distinguishes Available / Expired / NotFound without making absence an empty collection.
- Bind the successful PollTrace read to one HistoryEpoch, PollTraceId, and optional ProjectionCommit; seek observations using both PollTraceId and ProjectionCommitId.
- Read the shared earliest available Host UTC boundary from one SQL source and expose it consistently on historical success/error responses.
- Preserve zero-row FAILURE/INCOMPLETE PollTrace semantics while treating missing expected SUCCESS evidence as unavailable.
- Map Available to 200, Expired to 410 `MES_INGEST_HISTORY_EXPIRED`, and NotFound to 404 `POLL_TRACE_NOT_FOUND`.

## Phase 3 — green fixed-sample real-SQL evidence gate

- Add `PollTrace` to the existing Ticket 10 actual-plan runner and select a stable seeded PollTraceId.
- Keep the existing `RawEvidence` evidence-ID surface and ensure both surfaces produce actual statement and ShowPlan evidence.
- Record per-surface response bytes, logical reads, grant completeness/max grant, and spills.
- Fail closed on missing evidence, spills, abnormal grants, response-size overflow, or empty-vs-representative history growth.
- Run exactly two deterministic samples on the same build identity: the 600-row baseline and 400 historical rounds plus baseline (240,600 rows total).
- Do not introduce PollTrace-specific paging/token identity. Use a larger sample only if the fixed plans scan unrelated rounds, exceed an object bound, or disagree on earliest-available identity.

## Phase 4 — validation and review

- Run the new focused tests with the real-SQL environment; no skipped SQL tests may be accepted for Ticket 11 evidence.
- Run Tier 1 from `mes/ingest/csharp`: `dotnet test MesIngest.Tests`; report both Failed and Skipped counts.
- Re-open the test file and map every checklist item to the exact test/assertions above.
- Review assertion quality and behavior gaps; record findings in `.testagent/ticket-11/status.md` during the green implementation.
- Do not enter Tier 2 or Tier 3 without explicit user approval.
