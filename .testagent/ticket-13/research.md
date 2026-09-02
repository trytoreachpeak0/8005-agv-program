# Ticket 13 test research

## Target inventory

- `IMesIngestProjection` is the production seam used by the Host and the real SQL Server implementation.
- `SqlServerMesIngestProjection.CommitRoundAsync` is the only production transaction that changes Series lifecycle, conditions, events, and raw observations.
- `SqlServerMesIngestProjection.GetPollTraceAsync` plus `/api/v2/poll-traces/{id}` is the existing public 200/404/410 historical-evidence seam.
- `SqlServerMesIngestSchema` bootstraps and validates the exact database contract.
- Tests use xUnit v2 on VSTest and `Ticket01SqlServerFact` for real SQL Server 16 / compatibility 160.

## Existing conventions

- Drive state with `RoundIngestor` and production Host DI, never by mocking projection internals.
- Use `AdjustableTimeProvider` for exact UTC boundaries; do not wait in real time.
- Use a minimal scripted set of `MesTaskUnionRound` values and inspect behavior through HTTP or the projection maintenance seam.
- Database queries in tests are reserved for schema/retention-state evidence that is not exposed by the read-only HTTP contract.

## Acceptance checklist

- Raw observations use PollTrace `CompletedAt` and expire as one complete multiset at exactly 30 x 24 hours.
- The tick before the boundary remains readable; the boundary and later are expired.
- Expired PollTrace reads return 410 `MES_INGEST_HISTORY_EXPIRED` with the earliest available Host UTC; never-existing identity remains 404.
- Raw expiry does not delete or mutate current materialized state or the active Series structural graph.
- Only archived, non-visible/non-long-gone, condition-free and open-error-free Series receive `EligibilityAt`.
- Eligibility begins at the first qualifying Host UTC, has an exact 30 x 24 hour due boundary, is canceled atomically by new observations/conditions/events, and is recreated from the later qualifying Host UTC.
- MES `DATES`, archive time, creation time, local midnight, and calendar-month arithmetic do not determine either retention clock.
- Development validation stays on focused retention/410/eligibility tests; handoff runs Tier 1 once with a real SQL Server and zero skips.
