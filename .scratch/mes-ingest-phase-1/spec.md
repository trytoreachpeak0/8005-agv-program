# MesIngest Phase 1

Status: ready-for-agent

Seams (confirmed): B — core `TransportDemandReconciler` + read-only HTTP API; snapshot source replaceable internally (Oracle / file / fake) for factory-copy workflow.

## Problem Statement

现场需要先稳定拿到 MES 运输候选并盯盘核验，但不能等完整派车/装载/运送状态机做完。开发机连不上工厂 MES Oracle，只能把程序拷到工厂机验证；因此必须能在本地用已核验快照推进接入逻辑，并在工厂机做真实连通与人工核验。当前若把对账与调度绑在同一模块，会阻塞第一期交付。

## Solution

交付独立的 **MesIngest（MES 任务接入）**：Windows Service 常驻轮询只读 `MES_TASK_UNION`，对账并投影为带稳定 `DemandId` 的 **TransportDemand**（`VISIBLE` / `GONE`），写入 SQL Server；经本机 Kestrel **只读 HTTP** 供 WPF 盯盘与外部程序共用读取。关闭 WPF 不停 Service。一期不做派车、装载、运送与人工永久抑制。

## User Stories

1. As a factory operator, I want a always-on service that keeps polling MES without me opening a window, so that transport demands stay current even when the watch UI is closed.
2. As a factory operator, I want a WPF watch screen showing current VISIBLE TransportDemands, so that I can see what MES currently implies without waiting for dispatch.
3. As a factory operator, I want the watch screen to show GONE demands and recent disappearals, so that I can understand what left the MES snapshot.
4. As a factory operator, I want to see the last poll start/end time, duration, row count, and success/failure, so that I know whether ingest is healthy.
5. As a factory operator, I want alerts for query failure, field drift, duplicate keys, zero-drop pause, and reappear-after-GONE, so that I can intervene or escalate to IT.
6. As a factory operator, I want poll delay to be configurable (default wait after each completed poll), so that load on MES can be tuned without rebuilding.
7. As a dispatch developer, I want each TransportDemand to have a stable DemandId, so that a future dispatch system can attach its own state without reusing TASK_TYPE+SUBLOT as the external primary key.
8. As a dispatch developer, I want TASK_TYPE+SUBLOT used only as the reconcile key with at most one VISIBLE instance at a time, so that identity across rare process rollbacks stays unambiguous via new DemandIds.
9. As a system, I want a new VISIBLE demand when a reconcile key first appears, freezing TASK_TYPE, SUBLOT, EQP, AREA, STEP, DATES, PACKAGE and other projected fields at first sight, so that later MES churn does not rewrite the demand.
10. As a system, I want field drift on a still-VISIBLE demand to raise an alert without overwriting frozen fields, so that operators see MES inconsistency without changing the projected demand.
11. As a system, I want mes_last_seen_at refreshed and disappear count reset when a VISIBLE demand still appears in a successful full snapshot, so that presence tracking stays accurate.
12. As a system, I want disappear counts to increment only after complete successful polls, so that timeouts and failures never fake disappearances.
13. As a system, I want a VISIBLE demand to become GONE after the configured consecutive successful absences (default 2), so that human carry-away and MES clearance are reflected in the projection.
14. As a system, I want phase-1 GONE transitions without loading/dispatch protection rules, so that ingest stays free of thick task-state coupling.
15. As a system, I want a same reconcile key that reappears after GONE to get a new DemandId plus an alert, so that rare process rollbacks do not revive the old instance silently.
16. As a system, I want duplicate rows for the same TASK_TYPE+SUBLOT in one successful snapshot to block creating/updating that key and raise an alert, so that ambiguous MES data never becomes a demand.
17. As a system, I want PAUSED_ZERO_DROP per TASK_TYPE when a type’s previous successful non-zero count is at/above a configurable threshold (default 10) and the next successful count is 0, so that sudden empty results do not mass-mark GONE.
18. As a system, I want PAUSED_ZERO_DROP to suspend disappear counting and GONE for that type only, so that other task types keep reconciling.
19. As a system, I want PAUSED_ZERO_DROP to clear automatically after two consecutive successful polls with count > 0 for that type, with no manual clear UI, so that recovery is automatic and auditable.
20. As a system, I want per-type last healthy non-zero count, recovery streak, and pause state persisted across restarts, so that zero-drop protection survives service recycle.
21. As a system, I want disappear counts persisted across restarts, so that a restart mid-absence does not reset the GONE sequence incorrectly.
22. As a system, I want a restart recovery barrier: the first successful full poll after start may create new VISIBLEs and refresh seen-at for returning keys, but must not increment disappear counts or mark GONE, so that cold-start instability does not wipe the board.
23. As a system, I want normal disappear/GONE and zero-drop logic to resume from the second successful full poll after restart, including the documented interactions with persisted zero-drop state, so that restart semantics match the business model.
24. As a system, I want go-live baseline filtering in the application layer (fixed baseline timestamp, default 2026-08-01 00:00:00) without editing customer SQL, so that historical backlog does not flood VISIBLE demands.
25. As a system, I want all six TASK_TYPEs from MES_TASK_UNION (including WIRE_TO_NITROGEN) projected with the same reconcile rules, so that nitrogen-cabinet candidates appear alongside the other five types.
26. As an operator, I want AREA emptiness or unparseable AREA to still create a TransportDemand that is visible for watch/API, with a clear projection/alert signal that site mapping is unresolved, so that ingest does not wait for dispatch mapping tables.
27. As a developer on a machine without MES Oracle, I want to run MesIngest against recorded snapshot files from factory evidence, so that I can develop and test without copying every change to the plant PC first.
28. As a developer, I want a fake/in-memory snapshot source for automated tests, so that reconcile and API behavior can be driven with crafted rows.
29. As a plant engineer, I want Oracle mode configurable as Thin by default with Thick+Instant Client switchable, so that 11g connectivity can be fixed by config after a probe without rewriting business code.
30. As a plant engineer, I want MES credentials and connection settings in local config outside the repo, so that secrets are never committed.
31. As a plant engineer, I want the official MES_TASK_UNION SQL copied from the repo query manuscript into the install-side queries folder at build/publish time, so that production does not maintain a drifting SQL fork.
32. As an external program, I want a read-only HTTP API on the local Kestrel host to list TransportDemands filtered by status (VISIBLE/GONE) and optionally TASK_TYPE/SUBLOT/DemandId, so that other systems can consume the projection.
33. As an external program, I want API responses to include DemandId, reconcile key fields, frozen MES fields, status, seen/disappear metadata, and relevant alerts, so that callers do not need SQL Server access.
34. As an external program, I want poll health and recent alert endpoints (or equivalent read resources), so that monitoring can detect ingest failure without scraping logs.
35. As an external program and the WPF client, I want to share the same read-only HTTP contract, so that UI and integrations cannot diverge.
36. As a WPF user, I want to filter/sort the demand list by TASK_TYPE, SUBLOT, status, and last seen time, so that large snapshots (~hundreds of rows) remain usable.
37. As a WPF user, I want a prominent failed-poll / PAUSED_ZERO_DROP banner, so that silent empty boards are not mistaken for “no work”.
38. As an operator, I want closing the WPF window to leave the Windows Service polling and serving API, so that watching is optional.
39. As an operator, I want starting WPF later to reconnect to the running service API and show current projection, so that the UI is a thin client.
40. As a maintainer, I want Service, config, queries, and optional WPF packaged as a self-contained install directory, so that factory copy/deploy is straightforward.
41. As a maintainer, I want Python meslab to remain factory lab tooling only, so that production ingest is not hosted by the experiment runner.
42. As a QA engineer, I want reconcile behavior testable from prior projection state + snapshot result without Oracle or SQL Server, so that business rules have a fast feedback loop.
43. As a QA engineer, I want HTTP contract tests against the read API with a replaceable store/source, so that WPF and external callers have a stable surface.
44. As a plant engineer, I want a small factory connectivity probe path for Oracle Thin/Thick, so that first-boot on the plant PC can prove query success before relying on continuous poll.
45. As a system, I want incomplete or failed MES polls to create no new VISIBLEs, increment no disappear counts, and raise interface alerts, so that bad rounds never mutate presence wrongly.
46. As a system, I want only one poll in flight at a time with post-completion delay (not overlapping fixed-rate ticks), so that MES load stays bounded and rounds stay ordered.
47. As a future dispatch owner, I want permanent suppress of TASK_TYPE+SUBLOT out of MesIngest entirely, so that suppress cannot erase MES visibility from the projection.
48. As a future dispatch owner, I want VISIBLE lists to remain the source of “currently implied by MES”, so that dispatch can choose to ignore a key without MesIngest cooperating.
49. As an auditor, I want DemandId allocation and GONE/reappear events retained in the projection store, so that instance history can be inspected after the fact.
50. As an operator, I want unmatched PACKAGE kinds to remain visible as frozen PACKAGE values without blocking phase-1 ingest, so that package-universe discovery can continue offline without gating TransportDemand creation.

## Implementation Decisions

### Boundary and phases
- Product boundary follows ADR-mes-0006: MesIngest only; dispatch thick states are out of this delivery.
- Tech stack follows ADR-mes-0007: C# Windows Service + optional WPF client + SQL Server projection store + Kestrel read-only API.
- Domain vocabulary: MesIngest, TransportDemand, DemandId (CONTEXT.md).

### Modules (logical)
- **MesSnapshotSource** (internal replaceable adapter): reads a full MES_TASK_UNION round result — success rows, failure, or incomplete. Production adapter uses Oracle (Thin default, Thick switchable). Dev/lab adapters read recorded factory snapshots or fakes. Not a public product contract; exists so development machines without MES can still run the pipeline.
- **TransportDemandReconciler** (core seam): pure projection step — prior persisted projection state + this round’s snapshot outcome → updated TransportDemands, per-type pause state, and alerts. Owns freeze, drift alert, VISIBLE uniqueness on TASK_TYPE+SUBLOT, disappear counting rules, GONE, reappear-new-DemandId, PAUSED_ZERO_DROP, restart barrier semantics, and go-live baseline filtering.
- **TransportDemandStore** (internal persistence adapter): SQL Server persistence for demands, per-type pause counters, poll health, and alerts needed after restart. Swappable with in-memory for tests; not elevated to a second public testing contract beyond smoke/integration.
- **PollHost** (Windows Service): single-flight poll loop, configurable post-success/failure delay, wires source → reconciler → store, hosts Kestrel.
- **ReadApi** (external seam): read-only HTTP surface shared by WPF and external programs.
- **WatchUi** (WPF): thin HTTP client; never hosts poll or owns projection truth.

### Reconcile / projection semantics
- External primary key: DemandId. Reconcile key: TASK_TYPE + SUBLOT; at most one VISIBLE per key.
- First VISIBLE freezes projected MES fields; later differences alert as drift and do not overwrite.
- Disappear increments only on complete successful polls; default GONE after 2 consecutive successful absences while not in PAUSED_ZERO_DROP for that type.
- Phase-1 has no loading/session/“start transport” protection; those belong to later dispatch.
- Reappear after GONE → new DemandId + alert.
- Same-key multi-row in one successful snapshot → alert + block that key for the round.
- PAUSED_ZERO_DROP: per TASK_TYPE; enter when previous healthy count ≥ threshold (default 10) and this successful count is 0; auto-clear after 2 consecutive successful counts > 0; no manual clear.
- Restart barrier: first successful poll after process start does not increment disappear / GONE; from second successful poll, normal rules apply; persist pause and disappear state across restarts as specified in the business model’s recovery snapshot rules (ingest-applicable subset only).
- Go-live baseline: configurable fixed timestamp filtered in application layer; default 2026-08-01 00:00:00; do not edit customer SQL.
- Unresolved AREA: still emit TransportDemand for watch/API with an explicit unresolved-mapping / location-risk signal in projection or alerts; do not implement AREA→station_name tables or RIoT map sync in phase 1.
- PACKAGE freeze is required; package-universe / basket-capacity enrichment is not required to create demands.

### Read-only HTTP contract (shared)
- Serves current projection and health from the service process.
- Minimum resources (names flexible, semantics fixed):
  - list/get TransportDemands (filter by status, TASK_TYPE, SUBLOT, DemandId);
  - list recent/active alerts;
  - get latest poll health (timestamps, duration, row count, success/failure, per-type counts if cheap).
- No write/command endpoints in phase 1 (no suppress, no force GONE, no clear pause, no manual create).
- Auth: local-machine first; if bound beyond localhost, require a simple configurable shared secret or equivalent — exact scheme may be chosen at implement time but must be documented in the install config. Prefer localhost binding by default.
- WPF and external callers must use this same contract; WPF must not read SQL Server directly.

### SQL / Oracle / deploy
- Query manuscript: official MES_TASK_UNION under the repo queries tree; publish copies beside the install as `queries/`; no divergent embedded production SQL fork.
- Expected columns: TASK_TYPE, SUBLOT, AREA, EQP, STEP, DATES, PACKAGE.
- Oracle: default Thin; Thick+Instant Client selectable by config; factory probe validates connectivity on plant PC.
- Pool sizes, command timeouts, and exact NuGet driver package pins are implementer defaults subject to plant probe; must be configurable without code change for mode switch.
- Credentials only in local config; never commit.
- Deploy unit: self-contained install directory (Service, config, queries, optional WPF).
- Python meslab remains lab/evidence tooling only.

### Schema (logical, not physical DDL mandate)
- Persist TransportDemand rows with DemandId, reconcile key, frozen fields, status VISIBLE|GONE, seen/disappear metadata, created/gone timestamps.
- Persist per-TASK_TYPE zero-drop / last healthy count / recovery streak.
- Persist recent poll runs and alerts needed for API/UI and restart.
- Physical SQL Server schema is an implementation detail behind the store adapter.

### Defaults (tunable)
- Post-poll delay: 10s after round completion.
- Query timeout: 30s (config).
- Disappear threshold: 2 successful absences.
- Zero-drop enter threshold: 10.
- Zero-drop clear: 2 consecutive successful non-zero rounds.
- Go-live baseline: 2026-08-01 00:00:00.

## Testing Decisions

### What makes a good test
- Assert observable outcomes of a round or an HTTP response: resulting TransportDemand set, alerts, pause flags, status codes/payloads.
- Do not assert internal private helpers, SQL text assembly, or WPF control trees as the primary suite.
- Prefer highest seams; avoid testing past them into adapter internals except for thin integration smokes.

### Formal seams (scheme B)
1. **TransportDemandReconciler** — primary business suite: freeze, drift, VISIBLE uniqueness, disappear/GONE, reappear DemandId, multi-row block, PAUSED_ZERO_DROP, restart barrier, baseline filter, failed/incomplete round no-ops.
2. **Read-only HTTP API** — contract suite: demand list/get filters, alert/health resources, shared semantics for WPF and external clients, no write verbs.

### Supporting (not elevated to equal product seams)
- In-memory or file MesSnapshotSource and in-memory store used behind tests of the above.
- Few plant/integration smokes: real Oracle probe on factory PC; real SQL Server persistence round-trip on a lab SQL instance when available.
- WPF: manual acceptance against the live API (filters, banners, close-window-service-keeps-running); optional light ViewModel tests if cheap — not a third formal seam.

### Prior art
- Factory evidence and meslab validation runs under mes evidence/samples for MES_TASK_UNION shape and performance expectations; use recorded snapshots as fixtures for file-source and reconciler tests.
- No existing C# MesIngest test suite in-repo; greenfield tests should follow the two formal seams above rather than inventing per-layer mock theatres.

## Out of Scope

- Dispatch, appoint vehicle, loading, delivering, multi-bin occupancy, start-transport protections.
- Permanent suppress set and any MesIngest write API that hides a reconcile key from projection.
- Full thick local task state machine (PENDING/DISPATCHED/LOADING/…).
- AREA→station_name tables, RIoT map sync, station_id persistence.
- Concrete nitrogen cabinet station_name / AREA field mapping (config later; type still ingested).
- package-universe-discovery completion; basket-capacity-driven loading UX.
- Web UI (WPF first per ADR).
- Editing or forking customer MES SQL business predicates.
- Using Python meslab as the production ingest host.
- Composite multi-SUBLOT vehicle missions.
- Mock production tasks mixed into MES reconcile (if mocks appear later, they must be a separate source and id space).

## Further Notes

- Business model doc thick chapters still describe target dispatch behavior; phase-1 reading guide is §1.1 plus ADR-mes-0006/0007. Implement ingest-applicable reconcile/recovery/zero-drop rules; do not implement loading-protection cancellation gates.
- Development constraint: MES Oracle is typically only reachable on a plant PC via copy-deploy. File/fake snapshot sources are first-class for local progress; human verification of live SQL results remains a plant activity and is not replaced by fakes.
- Performance context from factory re-validation (order-of-magnitude): successful union rounds ~3s average / sub-5s typical on plant evidence; treat as ops expectation, not a hard gate inside unit tests.
- Next skill after acceptance of this spec: `/to-tickets` to split tracer-bullet issues under `.scratch/mes-ingest-phase-1/issues/`.
