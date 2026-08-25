# 28 — 通过加速并发稳定性门禁

**What to build:** 在 1536 MB SQL Server 常态配置下用 30–45 分钟高强度并发压力和加速的 24 小时逻辑周期验证完整新包，并只在资源趋势异常或用户明确要求时升级长时间真实 soak。

**Blocked by:** 27 — 通过快速容量预测门禁.

**Status:** ready-for-human

- [x] 生产默认仍为 60 秒 start-to-start、60/120/300 秒退避、Watch 30/60 秒刷新和每小时清理；验证专用加速 profile 只增加测试操作次数，不改变发布配置。
- [x] 复用 Tickets 02、12、16、21、27 的数据、并发、清理和客户端夹具，不新建 soak 平台；在固定小样本下运行 30–45 分钟高强度并发压力。
- [x] 使用可控时间跨越 24 小时逻辑边界，验证调度、退避、每小时清理、历史过期和重启状态，而不以真实等待替代确定性断言。
- [ ] 常用 Watch API P95 小于 2 秒、P99 小于 5 秒；运行期间没有 Error 701、持续 RESOURCE_SEMAPHORE、不可接受 spill、无界锁等待、重叠轮询或补跑突发。
- [x] 当前态查询逻辑读不随代表性 RawObservation 历史增长，冻结读取保持提交一致且不阻塞投影。
- [x] 持续采集数据库、LDF、tempdb、版本存储、进程内存、句柄、清理进度、earliest available、StoragePressurePause 和失败重试，并计算资源与延迟趋势。
- [x] 出现持续内存/文件/日志斜率、RESOURCE_SEMAPHORE、Error 701、spill、清理积压、延迟恶化或证据缺失时，快速门禁失败并升级 4 小时或 24 小时真实 soak；用户也可在正式现场切换前明确要求升级。
- [ ] 正常快速路径连同一次真实 SQL Server Tier 1 的目标总时长在 60 分钟内，并以 Failed: 0、Skipped: 0 关闭。
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
