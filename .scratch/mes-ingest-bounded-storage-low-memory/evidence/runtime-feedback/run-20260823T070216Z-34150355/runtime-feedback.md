# MesIngest runtime feedback

- Run: `run-20260823T070216Z-34150355`
- Captured: `2026-08-23T07:02:59.4297195+00:00`
- Primary state: **QUERY_TIMEOUT**
- Observations: HOST_LISTENING, CONTRACT_OK, SQL_CONNECTED, QUERY_TIMEOUT
- Read only: `true`; credentials/connection strings written: `false`

## Host and contract

| Check | Result |
| --- | --- |
| Service | Running, PID 29420 |
| Listener | 127.0.0.1:5088 |
| Contract | SUCCESS; `2026.08.new-mes-ingest.v2.0` / schema `17` |
| Deployment source | `93dd1dc75f9791cc8226f223929ab61885be8770`; dirty at package build: `True` |

## Current read probes

| Endpoint | HTTP | ms | Classification | Code |
| --- | ---: | ---: | --- | --- |
| `/api/v2/contract` | 200 | 48 | SUCCESS |  |
| `/openapi/v2.json` | 200 | 63 | SUCCESS |  |
| `/api/v2/watch-overview` | 0 | 10020 | QUERY_TIMEOUT | REQUEST_TIMEOUT |
| `/api/v2/current-ingest-attention?pageNumber=1&pageSize=1` | 200 | 586 | SUCCESS |  |
| `/api/v2/externally-readable-demand-catalog` | 200 | 19 | SUCCESS |  |
| `/api/v2/demand-series?presence=VISIBLE&page=1&pageSize=1` | 0 | 10016 | QUERY_TIMEOUT | REQUEST_TIMEOUT |

## SQL Server

- Service: MSSQLSERVER / Running
- Target identity (no credential): `localhost` / `MesIngest_V2` / integrated
- Connection: **SUCCESS** (, 107 ms)
- Current configuration/recovery/files available: True / True / True
- SQL query evidence objects: 13; Windows SQL signal lookback: 168 hours
  - 701: count=26, first=2026-08-18T08:48:37.5101942Z, last=2026-08-23T06:22:35.7985796Z
  - 17300: count=12, first=2026-08-18T14:20:40.9094267Z, last=2026-08-22T01:33:32.9400037Z
  - 17312: count=7, first=2026-08-18T14:20:40.9108916Z, last=2026-08-22T01:33:32.9522568Z
  - RESOURCE_SEMAPHORE: count=0, first=, last=
  - spill: count=0, first=, last=

## Tier 1 SQL test evidence

- Command: `dotnet test MesIngest.Tests --configuration Release --results-directory <path> --logger "trx;LogFileName=runtime-feedback-tier1.trx"`
- Failed: **0**; Passed: **725**; Skipped: **0**; Total: **725**
- Real SQL Tier 1 proven: **True** ()

## Dirty worktree

- Inventory available: True; entries: 101. All entries remain unattributed and preserved.
