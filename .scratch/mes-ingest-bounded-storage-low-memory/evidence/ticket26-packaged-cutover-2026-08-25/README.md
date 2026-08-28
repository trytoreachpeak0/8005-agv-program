# Ticket 26 packaged cutover rehearsal evidence

Date: 2026-08-25 (Asia/Shanghai)

## Isolation and final package

- Local default SQL Server `LAB-WIN-01\MSSQLSERVER`: ProductVersion `16.0.1190.2`, major `16`, EngineEdition `3`, compatibility `160`; not LocalDB and not production.
- All four databases were randomly named by this rehearsal, checked against its exact ownership pattern, and placed under `F:\MesIngestTicket26Cutover`.
- Final package: clean source commit `0373531ba90cf0f5b525d84af505e3bf17f52afb`, `Release`, `win-x64`, 1,372 declared files. Manifest SHA-256: `15cb4db5c4d07cb85f61b03c28192f728ed15b484e9a44252d31454c675643fa`.
- Shipped `Test-PackageIdentity` independently returned `Identical=true`, missing/mismatched/unexpected all zero. The cutover calls it at start and immediately before authorization.
- Contract/schema: `2026.08.new-mes-ingest.v2.1` / `28`; shared Service/Watch contract SHA-256 `c80b96c4df15cc2493c460b52d570cd9240647359c5a922ee40c1e37a6f80a66`; identical Service/Watch contract bytes.
- The installed MesIngest service was untouched. Each recognizable old database was created by the final packaged Host through an OS-owned, database-bound scheduled task. Before authorization and again post-elevation, the shipped cutover required the task to be `Disabled`, with zero triggers and zero restart attempts; parsed the Host connection argument and checked exact `Initial Catalog`; rechecked Task Scheduler last-run state, executable/action hashes, and absence of an exact-old-database Host process. Caller-authored JSON/PID proof is rejected.

## Representative failure

- RunId `8ff96d54-591e-460b-845b-3a9ea653d7aa`.
- Old `MesIngest_Ticket26_F_b8c64334d89240898faddc40f7563452_Old`; new `MesIngest_Ticket26_F_6967b605aa31461f8d0a53e2ecc50f6b_New`; new HistoryEpoch `5a6ce5bd-239f-46e4-9662-8dfb8026a19f`.
- Old-Host task `MesIngestCutoverOld_11644e4e9f464cb08854a7183b08e6fa`: `Disabled`, no trigger/restart, package Host SHA-256 `2a97b5bfb4e59278d5acd7ff2072135664c00dffe8b3743da25b6c4ca261e0de`, action SHA-256 `1aad85b049c668ebf402fbda2f4f594e74380a692568d2e57c67429ffce4ecde`.
- Deliberately unreachable API produced `CUTOVER_HTTP_GATE_UNREACHABLE`, exit 1, after `12,936.5 ms`. Before failure it proved exact old/new contract/schema, two tombstones, no base delete permission, and three post-seed rounds (driver `4,914.1 ms`, three PollTraces).
- Five seconds after exit both exact databases remained; child process count was zero; no retry or delete attempt occurred; the cutover principal was `NOT_GRANTED_AND_VERIFIED_ABSENT` with `VerifiedAbsent=true`.
- Only after these assertions did the harness clean the two test databases and task.

## Success

- RunId `83ef2385-a383-4777-a554-a519fcbfeac3`.
- Old `MesIngest_Ticket26_S_9502db75d61c4d808c3ac0c457ebf7dd_Old`; new `MesIngest_Ticket26_S_93174e1372f14dc2b916558a57e56436_New`; new HistoryEpoch `1e2dd82d-55ad-48dd-b622-4b48fd55cd23`.
- Old-Host task `MesIngestCutoverOld_d8a201803d1d438f890af91a871ab5c8`: `Disabled`, `Enabled=false`, `TriggerCount=0`, `RestartCount=0`, same Host SHA-256, action SHA-256 `8e188c94152108d24e037dc6d711046906065658a6a3ad34bc419721d0787ce8`.
- Recognizable old identity was schema/contract `27` / `2026.08.new-mes-ingest.v2.0-test-old` with two tombstones. Accelerated post-seed commits were `02c72d0edeec4a78820d0ab677ba7034`, `65df8e5bae4e4657b787116d66a16830`, and `00712f68a9da466dbfa1c0b55366ee1b`.
- All 11 old-host/session/identity/permission/tombstone/projection/five-Watch-API/catalog/packaged-reference-consumer/exclusion gates passed. Full cutover: `16,071.3 ms`.
- Only after final revalidation and immutable pre-delete evidence did it grant permission for the exact old database, delete only that database, close impersonation, revoke/drop the principal, and verify absence. The new database remained during the deletion assertion.
- Final harness cleanup removed the test new database, application login, and task. Direct checks found zero Ticket 26 databases, related logins, package/cutover processes, and scheduled tasks.

## Measured steps

| Step | Failure ms | Success ms |
| --- | ---: | ---: |
| Package byte identity | 2,315.2 | 2,262.4 |
| Evidence preflight and OS old-Host gate | 1,331.6 | 1,255.7 |
| Database identity | 172.7 | 132.8 |
| Tombstone seed/proof | 128.0 | 104.9 |
| Three projection rounds | 6,133.5 | 6,099.4 |
| Watch API/contract | 2,124.7 expected failure | 782.3 |
| Reference consumer/catalog | — | 398.9 |
| Final destructive revalidation | — | 2,480.3 |
| Pre-delete evidence/event | — | 46.5 |
| Exact delete/permission revocation | — | 2,054.0 |
| Final Windows event | — | 5.2 |

Final package publish took `20.6 s`. The harness, including four database creations, two actual packaged-Host task runs, success/failure cutovers, five-second retention observation, and cleanup, ran `48.801 s` (`04:39:44.8042507`–`04:40:33.6050513+08:00`). Controlled one-second Host rounds exercised persisted PollTrace/projection seams without waiting the production interval.

## Field-window extrapolation

Measured automation is seconds; conservative human-control budget is `40 minutes`:

| Field activity | Budget |
| --- | ---: |
| Confirm approved isolated target, change record, explicit no-backup acknowledgement, manifest | 8 min |
| Stop and independently verify actual old Host | 3 min |
| Recheck exact names/paths/credentials; create new DB/HistoryEpoch | 8 min |
| Tombstones plus accelerated projection/API/catalog/reference gates | 5 min |
| Human review of immutable pre-delete evidence and exact confirmation | 5 min |
| Verify deletion, revocation, new Host, Windows events | 4 min |
| Bounded pre-delete correction contingency | 7 min |
| **Total** | **40 min** |

This fits 30–60 minutes with 20 minutes before the upper bound. On failure, retain both databases/evidence, do not retry in the background, diagnose the named gate, and use a new RunId for a forward fix; otherwise reschedule. Evidence is not a backup or rollback path.

## Events, tests, review, and human actions

- Application Event ID `2300` records the failure before authorization, the successful pre-delete authorization, and final successful deletion/revocation for the exact identities above.
- `runs/` contains immutable failure JSON/Markdown, immutable success pre-delete/final JSON/Markdown, and aggregate summary. No business payload is included; evidence states `IsDatabaseBackup=false`, `HasRollbackPath=false`.
- Focused package/gate behavior: `8 passed / 0 failed / 0 skipped`.
- Final Tier 1, run exactly once from `mes/ingest/csharp` with the explicit non-LocalDB SQL Server 16 / compatibility 160 environment: `887 passed / 0 failed / 0 skipped`, test duration `4m44s`. TRX counters are total/executed/passed `887/887/887`, failed/notExecuted `0/0`; all 887 `UnitTestResult` nodes are Passed. TRX: `mes/ingest/csharp/.artifacts/ticket26-tier1/ticket26-tier1.trx`, SHA-256 `f7d069b44a2657a3da07b27131f422413dd1245b8fa02b682654cc1759506a20`.
- Final two-axis review: Standards `Pass`, 0 hard findings; Spec/Scope `Pass`, 0 functional findings, scope creep 0, Ticket 27 implementation 0. Findings about package-byte validation, behavior tests, failure permission absence, old-Host OS provenance, task state/trigger/restart policy, exact connection binding, and no-backup wording were fixed before these final passes.
- No Watch UI/XAML/UI Automation/DPI/baseline changed; Tier 2/3 do not apply.
- Field operators must verify the approved instance, identities/paths, change record and no-backup acknowledgement; fill local secrets; stop the actual old Host; review pre-delete evidence before confirmation; archive final evidence/events outside SQL Server; and make every failed attempt a new explicit forward-fix run.
