# Ticket 15 test research — formal single-statement Oracle round source

## Confirmed production gaps

- Production V2 registers `RoundIngestor` and the host-session service, but the
  Oracle source and legacy poll service are registered only on the legacy path.
- The legacy `OracleMesSnapshotSource` trims text, treats blank identity and bad
  `DATES` values as `INCOMPLETE`, and exposes neither provider column types nor
  the configured command timeout to its fake executor.
- `OdpNetOracleQueryExecutor` currently sends `SET TRANSACTION READ ONLY` before
  the SELECT, so one round results in two Oracle commands.
- The published query is copied twice into a release package and is checked only
  for existence/non-empty content. The canonical raw-byte SHA-256 is
  `54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae`.
- The old `Thick` mode only prepends Instant Client to `PATH` while still using
  managed ODP.NET Core. Ticket 15 therefore needs a distinct OCI-backed adapter
  (Oracle ODBC + Instant Client) and must never silently fall back to Thin.

## Agreed public seams

1. `IMesTaskUnionRoundSource.ReadRoundAsync` owns artifact verification, exactly
   one statement request, structural metadata validation, raw-value mapping,
   `QueryVersion`, timing, and safe `FAILURE` / `INCOMPLETE` diagnostics.
2. The internal executor request exposes the exact SQL and command timeout; its
   result exposes provider column names/types and raw rows.
3. `MesTaskUnionPollRunner.RunOnceAsync` is the production source-to-`RoundIngestor`
   seam. A hosted service runs it independently of any Watch process.
4. `CanonicalMesTaskUnionQuery` is the single content-addressed artifact authority.

## Framework and gate

- .NET SDK 10.0.302, xUnit 2.4.2, VSTest.
- Focused syntax uses `dotnet test ... -c Release --filter "FullyQualifiedName~..."`.
- The formal Host/SQL proof reuses `MES_INGEST_TICKET01_SQLSERVER`, SQL Server 2022
  product major 16, compatibility 160, and must report zero skipped tests.
- Real Oracle is not a CI substitute: the factory probe records `NOT_EXECUTED`
  when no approved Oracle 11g endpoint is available.
