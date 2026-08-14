# Ticket 17 test status

## Current

- Ticket, spec, domain glossary, ADR-mes-0006..0017, and applicable skills read.
- Public HTTP/OpenAPI seam is pre-confirmed by the spec.
- Worktree started clean at `bd7181b`.
- Read-only API, test, cursor, package, and release-gap research completed in
  parallel; no implementation files changed during research.
- Baseline `OpenApiContractTests`: 7 passed, 0 failed, 0 skipped.
- Ticket 17 implementation and independent Standards/Spec review are complete;
  both review axes pass after follow-up fixes.

## Validation log

- Contract freeze red test failed on missing compatibility policy, capability
  inventory, OpenAPI path and exact-match helper; green now fixes version
  `2026.08.new-mes-ingest.v2.0`, schema 17, nine stable capability IDs and all
  17 GET operations.
- V2 OpenAPI red test failed because V2 remained excluded and `/openapi/v2.json`
  was absent; green publishes an independent Production document with exact
  paths, parameters, response matrices, schemas, stable values, time semantics,
  ETag/304 and raw-evidence limits. Non-SQL OpenAPI facts pass 7/7.
- ErrorSearch cursor binding mismatch now returns
  `ERROR_SEARCH_CURSOR_MISMATCH`; invalid/tampered remains the invalid-cursor
  code. Focused token fact passes.
- Reference consumer now discovers and exact-matches contract/schema/capability
  IDs and versions before every catalog read; 11/11 focused facts pass.
- Compatibility classifier distinguishes exact, documentation-only, additive
  and breaking changes, including the canonical V2 document; 6/6 facts pass.
- Real SQL Server 16 / compatibility 160 Round -> Host -> SQL -> HTTP contract
  fact passes 1/1, covering unavailable, empty, success, ETag/304, invalid page
  and valid-but-unretained snapshot responses.
- Canonical `pack/openapi/v2.json`, package/release gate, smoke, HTTP examples
  and operator docs are implemented. `ReleasePackageValidationTests`: 16/16
  pass; all three PowerShell scripts parse successfully.
- Post-review contract/auth/path checks pass 3/3; the compatibility remap check
  passes 1/1; the real SQL runtime contract fact passes 1/1.
- Pseudo-mutations for capability operations, stable query codes, key
  comparison, Production legacy probing, manifest hash, hidden writes, hidden
  query parameters, and previous-contract credentials were injected and killed;
  no mutation marker remains.
- `dotnet build MesIngest.sln -c Release --no-restore --verbosity minimal`
  succeeds with 0 warnings and 0 errors.
- The final full-suite command was started exactly once. Its terminal result was
  lost during desktop context compaction, so it is intentionally not claimed as
  passing evidence; all evidence above has an observed terminal result.
