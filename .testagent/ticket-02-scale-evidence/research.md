# Ticket 02 test research

## Public seams

- Operator entry: packaged `validation/Invoke-ScaleAndQueryEvidence.ps1`.
- Database boundary: an explicitly named, newly-created real SQL Server database carrying a run-owned marker; system, existing, LocalDB, production-like, and unverifiable targets are rejected.
- Query boundary: the packaged production Host is launched against that database and the unique V2 HTTP endpoints are exercised.
- Evidence boundary: one immutable run directory contains the replay manifest, query measurements/actual plans, storage breakdown, gate result, and SHA-256 inventory.

## Existing conventions

- `RuntimeFeedbackLoopTests` tests packaged PowerShell entry points through both static contract checks and offline process execution.
- Ticket 01 uses `MES_INGEST_TICKET01_SQLSERVER` aimed at `master`, rejects LocalDB, and attests real SQL test counts.
- Publishing copies all files under `pack/validation`, so the new gate belongs there and must be documented in `pack/INSTALL.md`.
- SQL behavior is xUnit v2 on VSTest; repository Tier 1 is `dotnet test MesIngest.Tests` from `mes/ingest/csharp`.

## Acceptance checklist

1. Deterministic 0/7/30-day profiles retain key duplication, active/archive ratios, and error periods.
2. Explicit isolated target, strong identity rejection, owned cleanup.
3. DemandSeries, catalog, attention, overview, readability, error search, and raw evidence capture actual plan, IO/time, grants, spill, latency.
4. Logical used, physical data, LDF, table, clustered/nonclustered index, and compression reporting.
5. Replay identity includes build, configuration, seed, query parameters, schema/contract, SQL identity, and data scale.
6. Missing plan, skipped SQL tests, or empty data cannot pass.
