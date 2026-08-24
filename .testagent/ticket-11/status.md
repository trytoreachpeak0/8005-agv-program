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

The first updated-ticket actual-plan pass exposed scan operators during code review. That evidence
was retained as red evidence and was not treated as approval. The implementation now persists the
shared `HistoryEpoch` + `EarliestAvailableHostUtc` boundary in `SchemaInfo`, and the plan gate fails
closed unless PollTrace/raw evidence use their stable object-key seeks with zero related-table scans.

The second spec review then found that the RawEvidence endpoint still entered ErrorSearch page
matching before reading the exact evidence. That path read the Series/Demand raw history to derive
list-only MES area fields, and the old ShowPlan parser hid it by mixing statement events with
duplicated parent-operator counters. The final implementation removes that list path, validates the
snapshot filter using the exact evidence/period/series identities, counts only actual access
operators, and includes raw-object logical reads in the growth gate.

The final committed build passed real-SQL Tier 1: `Failed: 0, Passed: 784, Skipped: 0`, duration
`9m25s`. Attestation:
`mes/ingest/csharp/.artifacts/ticket11-tier1-final-exact-raw/run-20260824T013535Z/runtime-feedback-tier1-attestation.json`.

The corrected build then ran the same two fixed samples for both historical object surfaces:

| Surface/sample | Raw observations | Response bytes | Access reads | Raw reads | Max grant KB | Spills | PollTrace PK seeks | Raw PK seeks | Related scans | Gate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| PollTrace baseline | 600 | 256,826 | 65 | 25 | 0 | 0 | 5 | 5 | 0 | passed |
| PollTrace representative | 240,600 | 259,232 | 75 | 35 | 0 | 0 | 5 | 5 | 0 | passed |
| RawEvidence baseline | 600 | 1,749 | 215 | 20 | 1,024 | 0 | 5 | 5 | 0 | passed |
| RawEvidence representative | 240,600 | 1,754 | 225 | 30 | 1,024 | 0 | 5 | 5 | 0 | passed |

Evidence is under `mes/ingest/csharp/.artifacts/ticket11-final-scale-exact-raw/`, runs
`scale-20260824T014540Z-a4166d6c`, `scale-20260824T014614Z-b0bd8ff3`,
`scale-20260824T014657Z-5239af9d`, and `scale-20260824T014723Z-6e8d774e`.
Every run recorded `objectKeySeekComplete=true`, `unrelatedHistoryScanCount=0`, and a passing
gate; both PollTrace runs also recorded `earliestIdentityComplete=true`. From 600 to 240,600 raw
rows, PollTrace access/raw reads changed only 65/25 to 75/35 (limits 85/45), while RawEvidence
changed only 215/20 to 225/30 (limits 237/40). No escalation condition remained, so no larger
sample ran.
