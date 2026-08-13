# Ticket 15 test status

## Current

- Research, implementation, focused validation, and the independent Standards /
  Spec review are complete.
- Production V2 owns the formal Oracle source and Service poll lifetime. Startup
  fails fast when polling is enabled with a non-Oracle source, and only the
  concrete provider-backed probe can attest a live Oracle attempt.

## Validation log

- Ticket 15 focused source/artifact/provider/runner/probe/package/evidence tests:
  exactly 84 passed / 0 failed / 0 skipped. TRX:
  `mes/ingest/csharp/.artifacts/ticket15-tests/ticket15-focused-final.trx`.
- Real SQL Server 16.0.1190.2 / EngineEdition 3 / compatibility 160 Ticket 15 gate:
  exactly 5 passed / 0 skipped. TRX:
  `mes/ingest/csharp/.artifacts/ticket15-tests/ticket15-oracle-round-source-sqlserver.trx`.
- Production V2 SQL-test configuration-isolation regression (duplicate keys,
  field/error periods, restart, round evidence, task-type protection, and archive):
  exactly 30 passed / 0 skipped. TRX:
  `mes/ingest/csharp/.artifacts/ticket15-tests/ticket15-production-v2-env-isolation.trx`.
- Self-contained `win-x64` Host publish and strict release validation passed:
  397 files, exactly one canonical SQL artifact, manifest schema v2.
- Release solution build passed with 0 warnings / 0 errors.
- Full Release suite after the final test-environment isolation change: 603 passed /
  93 skipped / 3 failed. None is in Ticket 15 code: the pre-existing
  `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age`
  still reproduces in isolation, while both
  `MainWindowStartupTests.MainWindow_drag_completed_converts_absolute_rows_back_to_stars`
  and
  `MainWindowUiAutomationTests.Fluent_title_bar_supports_uia_keyboard_double_click_and_mouse_drag`
  passed in isolation and failed only during the full local UI run. TRX:
  `mes/ingest/csharp/.artifacts/ticket15-tests/ticket15-full-post-audit.trx`.
- NuGet audit found no vulnerable packages in production projects. The unchanged
  xUnit 2.4.2 test dependency graph still brings two known high-severity transitive
  advisories (`System.Net.Http` 4.3.0 and `System.Text.RegularExpressions` 4.3.0).
- Independent Spec review found no gaps. Standards review found two issues
  (idle Production V2 startup and caller-forged live probe evidence); both were
  fixed and covered by regression tests before the final focused run. A final
  targeted post-fix review found no remaining high-confidence blocker.

## Deliberately not claimed

- No approved live Oracle 11g endpoint was available, so no factory log is
  represented as a live pass. The shipped probe records `NOT_EXECUTED` unless a
  real provider connection attempt can be attested.
- The packaged Production smoke requires an explicitly confirmed, dedicated empty
  SQL Server database. That destructive-safety precondition was not supplied, so
  the smoke was not run; the disposable-database SQL integration gate above was.
