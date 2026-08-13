# Ticket 11 test status

## Current

- Ticket 11 implementation and requirement mapping complete.
- Public seams covered: normalized contract/token rules and production Host/real-SQL HTTP endpoint.
- Assertion/gap review complete: exact totals, own-dimension facets, DemandId evidence restriction, frozen high-water paging, and stable HTTP failures all assert observable outcomes.

## Validation log

- TDD red/green: contract/window and signed snapshot/cursor slices failed before their types existed, then passed after implementation.
- Focused compile/test: `ErrorSearchTests` builds; 3 non-SQL facts pass when the SQL opt-in is absent.
- Real SQL Server gate: SQL Server 16 / compatibility 160, exactly 8 passed, 0 skipped, 0 failed; TRX at `mes/ingest/csharp/.artifacts/ticket11-tests/ticket11-error-search-sqlserver.trx`.
- Release solution build: passed with 0 errors; NU1900 only because the NuGet vulnerability service index was unavailable.
- Full core suite: 601 passed, 19 skipped, 1 unrelated pre-existing failure in `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age`; isolated rerun reproduces it without Ticket 11 paths.
- Independent review: Spec axis found no ticket omissions. Standards findings for ingest-blocking range locks, nondeterministic IDENTITY row order, and non-canonical base64url signatures were fixed and the zero-skip SQL gate rerun green. Permanent-history exact facet aggregation remains a capacity-test follow-up.
