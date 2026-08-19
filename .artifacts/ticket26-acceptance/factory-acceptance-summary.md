# MesIngest factory acceptance — PASSED_WITH_NAMED_SKIPS

Run factory-acceptance-20260819T175432Z-380c08a5 on LAB-WIN-01 at 2026-08-20T01:57:52.1588862+08:00.

Package source commit: 3286b04ed39ee1199ce67e9b3091062c2b4fc565.

| Check | Gate | Status | Detail |
| --- | --- | --- | --- |
| PACKAGE_IDENTITY_MATCHES_RELEASE_MANIFEST | FACTORY_PACKAGE_IDENTITY | PASSED | 914 files match RELEASE-MANIFEST.json (sourceCommit=3286b04ed39ee1199ce67e9b3091062c2b4fc565, manifest sha256=723e796e59aa79636dbde2db607b3d19f29147209e0973df5e242c6a1bfa1fd6). |
| TARGET_ENVIRONMENT_IDENTITY_RECORDED | FACTORY_PACKAGE_IDENTITY | PASSED | SQL Server LAB-WIN-01\MSSQLSERVER/MesIngest_Ticket26_Factory (major 16, compatibility 160, 0 user tables before bootstrap); Oracle mode Thin with commandTimeout=30s from the operator configuration; machine LAB-WIN-01, clock 2026-08-20T01:54:34.7237607+08:00. |
| CANONICAL_QUERY_READ_ONLY_BOUNDARY | FACTORY_ORACLE_ACCEPTANCE | PASSED | One statement, 6 TASK_TYPE branches, 5 UNION ALL, no write keyword, sha256=54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae. |
| LIVE_ORACLE_THIN_PROBE | FACTORY_ORACLE_ACCEPTANCE | PASSED | execution_scope=LIVE_ORACLE, connection_attempted=true, mode Thin->Thin via Oracle.ManagedDataAccess.Core, query MES_TASK_UNION/sha256:54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae, outcome=Success, rows=597, duration=3001ms, commandTimeout=30s. |
| LIVE_MES_TASK_UNION_ROUNDS | FACTORY_ORACLE_ACCEPTANCE | PASSED | 3 complete rounds, 3 SUCCESS. All on MES_TASK_UNION/sha256:54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae. outcome/rows: SUCCESS/602, SUCCESS/601, SUCCESS/602. Canonical digests recorded per round in rounds.json. |
| NON_SUCCESS_ROUNDS_PRESERVE_PROJECTION | FACTORY_ORACLE_ACCEPTANCE | PASSED | No non-SUCCESS round occurred in this window; every observed round committed normally. |
| CONTRACT_DISCOVERY_AND_AUTHORIZATION | FACTORY_API_ACCEPTANCE | PASSED | contractVersion=2026.08.new-mes-ingest.v2.0, schemaVersion=17, 9 capabilities, GET-only. Restricted raw evidence: no secret 403, wrong secret 403, correct secret 400. |
| EXTERNALLY_READABLE_CATALOG_FIRST_BODY_AND_304 | FACTORY_API_ACCEPTANCE | PASSED | First body carried 260 externally readable Demands at catalogRevision 2 with ETag W/"catalog-r2"; the same-revision read was 304 with no body. |
| PRIMARY_READ_SURFACES | FACTORY_API_ACCEPTANCE | PASSED | demandSeries=200/100 items; readabilityAudit=200/100 items; errorSearch=200/100 items; currentIngestAttention=200/100 items; watchOverview=200/-1 items. Every surface answered the frozen contract version with a correlation id. |
| REMOTE_BINDING_DATA_ACCESS_PROTECTION | FACTORY_API_ACCEPTANCE | PASSED | Startup validation refused the off-loopback binding before Kestrel bound (exit code -532462766), naming MesIngest:SharedSecret. |
| SQLSERVER_PROJECTION_COMMIT_PERSISTENCE | FACTORY_SQLSERVER_ACCEPTANCE | PASSED | 259 Demands at catalogRevision 3 (projectionCommitId 6585d5680e694508ac8ce4847ef4b715) read identically twice after an abrupt Service restart. |
| SQLSERVER_RESTART_BARRIER | FACTORY_SQLSERVER_ACCEPTANCE | PASSED | A new Host session (d541cef7372248a691e0e305c3a50bf9) replaced 638737fa195b4015a614c52c87573b12, entered the barrier (events RESTART_BARRIER_ENTERED), and is in phase BARRIER with absenceAuthorityAvailable=False. |
| TASK_TYPE_PROTECTION_READ | FACTORY_SQLSERVER_ACCEPTANCE | PASSED | 6 work types reported; 0 currently withhold absence authority. Phases recorded per work type in task-type-protections.json. |
| CATALOG_REVISION_MONOTONIC | FACTORY_SQLSERVER_ACCEPTANCE | PASSED | CatalogRevision across 3 observed rounds: 1 -> 2 -> 2. |
| SNAPSHOT_READ_NOT_TORN | FACTORY_SQLSERVER_ACCEPTANCE | PASSED | A page of 50 of 602 Demands re-read identically under the same snapshotReference after a later round committed. |
| WATCH_SIX_PAGE_LIVE_HOST_VERIFICATION | FACTORY_WATCH_ACCEPTANCE | PASSED | Startup to main window 1408.6 ms. Pages shown: 概览, 需求系列, 资格审计, 错误检索, AREA 筛选, 接入告警, 设置, Host 状态. Host state 'Host 已连接'. Auto-refresh advanced the Watch view 3 time(s) in 45 s. Paging, detail selection and cross-page drill: detail selection: exercised on 1 of 4 live rows; paging: not exercised (the live snapshot fits one page of 4 rows); cross-page drill: exercised from an attention item into error search. Window captures stay on this machine; only their hashes are published. |
| WATCH_CLOSED_SERVICE_CONTINUES | FACTORY_WATCH_ACCEPTANCE | PASSED | The Watch exited with code 0; the Service kept running, advanced the PollTrace high water 10 -> 11, wrote to SQL Server and still served the catalog at revision 7. |
| TICKET23_VISUAL_GATES_NOT_REPEATED | FACTORY_WATCH_ACCEPTANCE | PASSED | This run verifies final packaging and live-site connection only. The pixel candidate, ten-run stability, baseline promotion and DPI clone from ticket 23 stay valid because this ticket changed no XAML, UI Automation or DPI behaviour. If the plant observes a real UI, UI Automation or DPI regression, keep the red evidence and return the affected scenario to ticket 23's gates rather than re-approving here. |
| EVIDENCE_REDACTION_AND_HASHES | FACTORY_EVIDENCE_CLOSURE | PASSED | 18 evidence files hashed. Probe logs and provider messages are redacted; API response bodies and Watch window captures are not published — they carry customer rows. |
| LIVE_ORACLE_THICK_MODE_REVERIFICATION | FACTORY_ORACLE_ACCEPTANCE | SKIPPED | Not run. The ticket asks for Thick only when the plant actually needs it; the Thin probe and rounds passed, so no Thick fallback was exercised. |

## Named skips

- **LIVE_ORACLE_THICK_MODE_REVERIFICATION** — owner: plant IT / release owner; requires: Oracle Instant Client plus a registered Oracle ODBC driver, then rerun with -OracleMode Thick; gate left open: FACTORY_ORACLE_ACCEPTANCE.

## Residual risks

- Oracle Thick mode was not re-verified unless a separate -OracleMode Thick run recorded it.
- Plant business semantics (DATES/STEP per TASK_TYPE) remain a human confirmation in validation\execution-log.md.
- Response bodies and Watch captures stay on this machine, so an off-site reviewer sees counts and hashes rather than rows.

## Rollback readiness

Rollback stays the ticket 25 drill: stop the new Service, restore the separate legacy backup with scripts\cutover\Invoke-CutoverRollback.ps1, and run the legacy programs against the restored legacy database. No mixed-mode operation is supported.
