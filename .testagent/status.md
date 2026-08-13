# Ticket 12 test status

## Current

- Contract/API/domain implementation complete at production seams.
- Six production Host/real-SQL HTTP acceptance tests cover all eight ticket requirements.
- Contract/schema advanced to tracer 12 / schema 12.
- Test-gap analysis complete; the confirmed half-open boundary survivor was closed and re-verified.

## Validation log

- Focused Release build: passed; NU1900 only because the vulnerability service index was unavailable.
- Real SQL Server gate: SQL Server 16 / compatibility 160, exactly 6 passed, 0 skipped, 0 failed; TRX at `mes/ingest/csharp/.artifacts/ticket12-tests/ticket12-error-detail-sqlserver.trx`.
- Ticket 11 regression: 8 passed, 0 skipped, 0 failed.
- Pseudo-mutation: `endedAt > window.ToUtc` -> `>=` initially survived; after adding the equal-boundary assertion it failed the focused test and was reverted; focused baseline is green.
- Release solution build: passed with 0 errors; NU1900 only because the NuGet vulnerability service index was unavailable.
- Full core suite: 606 passed, 19 skipped, and 2 failures outside Ticket 12 paths. The UI Automation title-bar failure passed in isolation; the pre-existing latency-retention test remains reproducible and compares a real 2026 file timestamp with a fixed July 2026 test clock.
- Independent Standards/Spec review: passed after fixing whole-value `Authorization: Bearer` redaction and active-period `endsAfterWindow` semantics. The initial generic V2 raw concern was withdrawn because those payloads are an explicit Ticket 08 contract outside Ticket 12's Error Search boundary.
