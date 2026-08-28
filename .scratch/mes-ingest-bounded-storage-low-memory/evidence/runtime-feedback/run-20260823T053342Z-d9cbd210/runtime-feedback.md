# MesIngest runtime feedback

- Run: `run-20260823T053342Z-d9cbd210`
- Captured: `2026-08-23T05:34:18.8290331+00:00`
- Primary state: **SQL_UNAVAILABLE**
- Observations: HOST_LISTENING, CONTRACT_OK, SQL_UNAVAILABLE, QUERY_TIMEOUT
- Read only: `true`; credentials/connection strings written: `false`

## Host and contract

| Check | Result |
| --- | --- |
| Service | Running, PID 12144 |
| Listener | 127.0.0.1:5088 |
| Contract | SUCCESS; `2026.08.new-mes-ingest.v2.0` / schema `17` |
| Deployment source | `93dd1dc75f9791cc8226f223929ab61885be8770`; dirty at package build: `True` |

## Current read probes

| Endpoint | HTTP | ms | Classification | Code |
| --- | ---: | ---: | --- | --- |
| `/api/v2/contract` | 200 | 64 | SUCCESS |  |
| `/openapi/v2.json` | 200 | 51 | SUCCESS |  |
| `/api/v2/watch-overview` | 0 | 3019 | QUERY_TIMEOUT | REQUEST_TIMEOUT |
| `/api/v2/current-ingest-attention?pageNumber=1&pageSize=1` | 0 | 3008 | QUERY_TIMEOUT | REQUEST_TIMEOUT |
| `/api/v2/externally-readable-demand-catalog` | 0 | 3016 | QUERY_TIMEOUT | REQUEST_TIMEOUT |
| `/api/v2/demand-series?presence=VISIBLE&page=1&pageSize=1` | 0 | 3007 | QUERY_TIMEOUT | REQUEST_TIMEOUT |

## SQL Server

- Service: MSSQLSERVER / Stopped
- Target identity (no credential): `localhost` / `MesIngest_V2` / integrated
- Connection: **SQL_UNAVAILABLE** (SQL_CONNECTION_FAILED_2, 4110 ms)
- Current configuration/recovery/files available: False / False / False
- SQL query evidence objects: 0; Windows SQL signal lookback: 168 hours
  - 701: count=22, first=2026-08-18T08:48:37.5101942Z, last=2026-08-22T01:33:33.0335019Z
  - 17300: count=12, first=2026-08-18T14:20:40.9094267Z, last=2026-08-22T01:33:32.9400037Z
  - 17312: count=7, first=2026-08-18T14:20:40.9108916Z, last=2026-08-22T01:33:32.9522568Z
  - RESOURCE_SEMAPHORE: count=0, first=, last=
  - spill: count=0, first=, last=

## Tier 1 SQL test evidence

- Command: `dotnet test MesIngest.Tests --configuration Release --results-directory <path> --logger "trx;LogFileName=runtime-feedback-tier1.trx"`
- Failed: **0**; Passed: **643**; Skipped: **82**; Total: **725**
- Real SQL Tier 1 proven: **False** (REAL_SQL_TIER1_TRX_NOT_FULL_SUITE)

## Dirty worktree

- Inventory available: True; entries: 67. All entries remain unattributed and preserved.
