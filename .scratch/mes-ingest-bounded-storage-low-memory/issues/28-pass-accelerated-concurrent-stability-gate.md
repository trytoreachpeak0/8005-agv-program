# 28 — 通过加速并发稳定性门禁

**What to build:** 在 1536 MB SQL Server 常态配置下用 30–45 分钟高强度并发压力和加速的 24 小时逻辑周期验证完整新包，并只在资源趋势异常或用户明确要求时升级长时间真实 soak。

**Blocked by:** none. Ticket 27 is done under the accepted 15-day hard-limit policy.

**Status:** done

- [x] 生产默认仍为 60 秒 start-to-start、60/120/300 秒退避、Watch 30/60 秒刷新和每小时清理；验证专用加速 profile 只增加测试操作次数，不改变发布配置。
- [x] 复用 Tickets 02、12、16、21、27 的数据、并发、清理和客户端夹具，不新建 soak 平台；在固定小样本下运行 30–45 分钟高强度并发压力。
- [x] 使用可控时间跨越 24 小时逻辑边界，验证调度、退避、每小时清理、历史过期和重启状态，而不以真实等待替代确定性断言。
- [x] 常用 Watch API P95 小于 2 秒、P99 小于 5 秒；运行期间没有 Error 701、持续 RESOURCE_SEMAPHORE、不可接受 spill、无界锁等待、重叠轮询或补跑突发。
- [x] 当前态查询逻辑读不随代表性 RawObservation 历史增长，冻结读取保持提交一致且不阻塞投影。
- [x] 持续采集数据库、LDF、tempdb、版本存储、进程内存、句柄、清理进度、earliest available、StoragePressurePause 和失败重试，并计算资源与延迟趋势。
- [x] 出现持续内存/文件/日志斜率、RESOURCE_SEMAPHORE、Error 701、spill、清理积压、延迟恶化或证据缺失时，快速门禁失败并升级 4 小时或 24 小时真实 soak；用户也可在正式现场切换前明确要求升级。
- [x] 正常快速路径连同一次真实 SQL Server Tier 1 的目标总时长在 60 分钟内，并以 Failed: 0、Skipped: 0 关闭。
- [x] 最终证据记录构建身份、contract/schema、HistoryEpoch、配置、数据规模、加速倍率、操作次数、持续时间、分位数、资源趋势和清理结果。
- [x] 本票不主动运行 Tier 3，也不推广视觉基线；任何未完成的已批准 UI 验证保持独立阻塞项。

## Comments

### 2026-08-25 — accelerated gate completed fail closed

The clean `f84fee2e4140ab16f8bdec77c7a8d762c557fa84` package completed a real
`1801.367s` accelerated run on the SQL Server 16 default instance at compatibility `160` and
`max server memory=1536 MB`. The fixed sample was 600 Series, 100 historical rounds, 60,600
initial RawObservation rows (60x poll and 60x cleanup operation multipliers), eight concurrent
clients, and one midpoint Host restart. The run produced 1,701 successful polls, 38,784 API
latency samples, 24,580 successful frozen detail reads, 1,767 catalog reads, 30 cleanup checks,
and 32 resource snapshots.

The ordinary P95/P99 SLO passed at `876.335/1196.112 ms`; current logical-read growth, frozen
commit consistency/non-blocking projection, cleanup, earliest-available advancement,
StoragePressure, retry/day-boundary, restart, Error 701, lock waits, memory envelopes, database
growth, and tempdb trends also passed. The gate nevertheless failed closed on seven signals:
`STABILITY_CATCH_UP_BURST` (1), `STABILITY_HTTP_ERROR` (69),
`STABILITY_LATENCY_DEGRADATION` (first/last quartile P95 `278.361/1063.180 ms`),
`STABILITY_RESOURCE_SEMAPHORE` (conservative cumulative counter above the first sample in 18
snapshots; 2 increase intervals / 11 new waiting tasks, active pending grants peak 0),
`STABILITY_SPILL` (2,881),
`STABILITY_LDF_TREND` (`2.139 MB/min`), and `STABILITY_HANDLE_TREND`
(`5.449 handles/min`). The required next validation is therefore a 4-hour or 24-hour real soak
after those named signals are resolved; this ticket cannot be marked complete from the fast run.

Ticket 27 remains independently release-blocking: 30-day +30% logical `21094.459486 MB`,
physical `21128 MB`, and nonlinearity `2.427779815`. Ticket 28 did not overwrite, weaken, or
clear it. See `evidence/ticket28-accelerated-stability-2026-08-25/` for the compact record and
`mes/ingest/csharp/.artifacts/ticket28-stability-f84fee2e/scale-20260824T233620Z-99e32a86/`
for the local raw bundle.

Post-stress review completed before Tier 1: final Spec and Standards axes both reported P0/P1
`0`; the standards review's cleanup finding was fixed in `7e768cae` without changing the captured
stress result. The one and only real-SQL Tier 1 then passed `890/890`, failed `0`, skipped `0`,
exit code `0`, in `13m37s` on the default SQL Server 16 instance at compatibility `160`. Tier 1
does not clear the seven stability failures, the required soak escalation, or Ticket 27.

### 2026-08-26 — v2.2 superseding gate passed

Ticket 27 was synchronized in order without reset or merge: upstream `8013b049`, `48c3d650`,
and `cdcf5620` are present here as `0703207e`, `d02227a3`, and `cf0163bd`. It is now `done` on
contract/schema `2026.08.new-mes-ingest.v2.2/29` under the accepted 15-day +30% hard-limit
policy. Logical `10548.651 MB`, physical `10568 MB`, and LDF `343.190 MB` are below
`12288/16384/2048 MB`; nonlinearity `2.427779815` and the 70% signal remain advisory warnings.
The old 30-day and pre-policy red evidence above is preserved as historical fact and is not
reintroduced as a current blocker.

The v2.2 platform first completed a historical 4-hour real run (`14403.077s`) that failed closed
on P95/P99, latency degradation, and LDF trend. It exposed two evidence-attribution defects:
ordinary request timers inherited the slowest concurrent sibling, and unrelated short
`ACTIVE_TRANSACTION` samples were accumulated without transaction identity. The final fixes stop
each surface timer when its task completes, select the database's actual oldest transaction,
record session/application/age, and reject missing, negative, nonnumeric, or regressing evidence.
The other five prior signals were fixed without lowering thresholds: RESOURCE_SEMAPHORE uses
attributed deltas/consecutive active grants; LDF uses physical/used/autogrowth/stable-tail evidence;
Host memory/handles and catch-up are process-generation scoped; frozen HTTP expiry is a separate
structured 410; and the attributed spill queries/sorts/grants were removed or bounded.

The clean `94cc7b07873528b358038a8d283146dba617264a` package (1,372 files) then completed the
superseding real quick gate for `1801.701s` on the SQL Server 16 default instance, compatibility
`160`, `SIMPLE`, max memory `1536 MB`, using the healthy F-volume database root. The fixed sample
was 600 Series, 100 historical rounds, initial/max RawObservation rows `60,600/60,607`, eight
clients, one midpoint restart, and 60x poll/cleanup operation multipliers. It produced
`1,777/1,777` successful polls, 13,475 Watch API reads, 24,176 frozen reads, 1,925 catalog reads,
30 cleanup checks, 39,576 latency samples, and 32 resource snapshots.

Overall P95/P99 were `171.746/857.611 ms`; maximum per-surface P95/P99 were
`1151.575/1716.177 ms`, stable-stage degradation count zero, and first/last quartile P95 improved
`218.071 -> 156.726 ms`. HTTP errors/unexpected/frozen errors were `0/0/0`; one intentional
`410 MES_INGEST_HISTORY_EXPIRED` was separately classified. Spill, 701, XEvent drops, semaphore
active/pending samples, pending grants, max lock wait, unbounded lock waits, catch-up bursts, and
frozen mismatches/windows without projection were all zero. Current logical-read growth passed;
292 projection commits occurred during frozen reads.

The stable generation-2 Host WS/handle slopes were `-0.0531 MB/min` and `0.9803 handles/min`;
Host/SQL peaks were `276.648/1367.445 MB`. Logical DB/physical data/tempdb slopes were
`-0.0713/0/0.1270 MB/min`; version-store peaks were `30.000/35.688 MB`. LDF physical/used peaks
were `136/63.910 MB`, with one early autogrowth, zero stable/late growth, stable used slope
`-2.0829 MB/min`, and persistent reuse-wait count one. Cleanup succeeded with backlog/failure
zero, expired polls 101, 60,600 initial rows deleted, 3,558 final rows; earliest available advanced,
StoragePressurePause stayed zero/`HEALTHY`, and retry/day-boundary/restart/HistoryEpoch checks
passed. The quick result is green and `soakEscalationRequired=false`; the historical 4-hour red is
retained, and no 24-hour run was performed merely for form.

Focused gate tests passed `51/51`, deterministic contract `15/15`, both with failed/skipped zero.
After all code and evidence review findings were fixed, Spec and Standards axes each reported
P0/P1/P2 zero. The superseding v2.2 closing cycle's sole real-SQL Tier 1 then ran from
`mes/ingest/csharp` through the exact `dotnet test MesIngest.Tests` wrapper, explicitly
expected/observed SQL major `16` and compatibility `160`, and passed `921/921`, failed `0`,
skipped `0`, exit `0`, in `861.951s`; no Tier 1 rerun occurred after the v2.2 inputs stabilized.
No Tier 2/3 or visual baseline was run because there was no UI/XAML change.

Superseding compact evidence is in
`evidence/ticket28-v22-concurrency-stability-2026-08-26/`; full local raw evidence is in
`mes/ingest/csharp/.artifacts/ticket28-v22-94cc7b07/`. Post-Tier-1 audit found zero owned scale
databases, both Scale/Stability XEvent sessions, Host processes, and F-volume files. Six unrelated
Ticket01 databases and one Host process predating the run were preserved. No manual action remains
for Ticket 28; a 24-hour soak is optional only if explicitly requested before field cutover.
