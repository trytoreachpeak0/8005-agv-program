# Ticket 11 test-generation status

## Current state

- Research: complete.
- Plan: complete.
- First red tests: complete in `MesIngest.Tests/PollTraceRawEvidenceCutoverTests.cs`.
- Production implementation: intentionally not started in this test-only pass.
- Tier 2 / Tier 3: not entered.

## Focused run

Command (VSTest + xUnit v2, .NET SDK 8):

```text
dotnet test MesIngest.Tests --filter "FullyQualifiedName~MesIngest.Tests.PollTraceRawEvidenceCutoverTests" -v minimal
```

Result:

```text
Failed: 1, Passed: 0, Skipped: 2, Total: 3
```

- The test assembly and all referenced production projects compiled successfully.
- `Packaged_scale_gate_requires_real_SQL_bounds_for_PollTrace_and_raw_evidence_reads` failed at the first missing `PollTrace` gate declaration, which is the intended red behavior.
- Both `[Ticket01SqlServerFact]` tests were skipped because the real-SQL environment variables are not configured in this process. They are drafted red regressions, not executed evidence. Ticket 11 cannot be declared green until they run without skips against the required real SQL Server.

## Test-gap and assertion review

`test-gap-analysis` and its .NET/xUnit extension were applied as a static review. Empirical mutation verification was not appropriate because the new suite is intentionally red and the SQL tests cannot establish a runnable baseline in this environment. Findings below are therefore static/unverified.

Substantive pseudo-mutations killed by the drafted assertions:

- Drop `ProjectionCommitId` from the raw-object predicate: the injected foreign-commit row changes count, ordinals, and per-row commit assertions.
- Deduplicate the raw rows: exact duplicate cardinality falls from two to one.
- Fill null fields from the current projection or normalize the invalid AREA/date: exact null/raw-value assertions fail.
- Return an empty collection for missing retained raw rows: expected HTTP 410 and code fail.
- Collapse Expired and NotFound: distinct 410/404 and error-code assertions fail.
- Compute different earliest boundaries per response branch: the three exact timestamp assertions disagree.
- Omit HistoryEpoch or bind a different commit: exact database epoch and receipt commit assertions fail.
- Add PollTrace to the scale runner without response-size, spill, grant, or growth limits: fail-closed source assertions still fail.

Manual assertion-quality review:

- Assertions are concrete status/code/identity/value/cardinality checks; there are no tautological non-null-only assertions.
- Secondary observables include row count, ordinals, commit identity, duplicate cardinality, null preservation, and shared boundary.
- The xUnit DTO contract uses `UNASSIGNED`; the drafted assertion was corrected during review.

Deferred checks for the green implementation:

- Re-run both SQL tests with no skips and confirm the intended failure messages before production edits.
- Preserve legitimate zero-row FAILURE/INCOMPLETE and zero-row SUCCESS PollTrace behavior while detecting missing evidence for a formerly non-empty SUCCESS round; existing Ticket 15 tests remain the failure/incomplete canary.
- Re-open existing ErrorSearch evidence-ID and DemandSeries frozen-detail tests when wiring the shared earliest-boundary source, so Ticket 11 does not narrow their existing object identities.
- Run the packaged empty and representative-history PollTrace/RawEvidence evidence passes on the same build identity after the gate is implemented.

The optional `assertion-quality` skill is not installed in this session; the equivalent review was performed manually and recorded above.

## Green implementation and updated-ticket evidence

- Focused public-seam SQL run: `Failed: 0, Passed: 3, Skipped: 0`.
- Related PollTrace/schema/OpenAPI regression run: `Failed: 0, Passed: 42, Skipped: 0`.
- Final Release real-SQL Tier 1: `Failed: 0, Passed: 782, Skipped: 0`, duration `9m48s`.
- Tier 1 attestation: `mes/ingest/csharp/.artifacts/ticket11-tier1-final/run-20260824T001552Z/runtime-feedback-tier1-attestation.json`.

The updated ticket's existing actual-plan entry was run with exactly two fixed samples:

| Sample | Raw observations | Response bytes | Logical reads | Raw-object logical reads | Max grant KB | Spills | Actual plans | Gate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Baseline | 600 | 256,826 | 365 | 105 | 0 | 0 | 25 | passed |
| Representative | 240,600 | 259,232 | 525 | 175 | 0 | 0 | 25 | passed |

The representative per-surface logical-read bound was 565, so 525 passed; response size stayed below the explicit 2 MiB PollTrace limit. Evidence is under `mes/ingest/csharp/.artifacts/ticket11-polltrace-scale/scale-20260824T002932Z-66bed05a/` and `scale-20260824T003009Z-c9be0c83/`. Both fixed samples passed with no spill, grant, response-size, or identity risk signal, so no larger sample was run.
