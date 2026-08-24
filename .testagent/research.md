# Ticket 16 test research

## Scope and authority

- Starting point is `e78486ab4e17af89b7b9a8ac4c07471094b33a34` on
  `codex/ticket-16-budgeted-hourly-cleanup`.
- Authority read for this pass: root `AGENTS.md`, `CONTEXT.md`, Ticket 16,
  `.scratch/mes-ingest-bounded-storage-low-memory/spec.md`, ADR-mes-0020,
  ADR-mes-0022, ADR-mes-0024, the repository `/tdd` skill and the
  `code-testing-agent` skill.
- Ticket 16 is a broad cleanup/HostedService/Attention change, so this
  Research -> Plan artifact pair is appropriate. The requested
  `find-untested-sources` helper is not installed in this environment; one
  bounded manual source/test pairing pass was performed instead.
- This research pass did not edit product or test code and did not run the full
  suite.

## Pre-agreed public seams

The specification already agrees the seams; tests must not call private loop
methods, assert SQL text, or expose implementation-only state.

1. **Host lifecycle and controllable time**: start/stop the production cleanup
   `IHostedService` and advance the existing `TimeProvider` through its public
   timer behavior. `MesTaskUnionPollHostedService.StartAsync/StopAsync` is the
   neighbouring convention; `ManualTimerTimeProvider` avoids real waits.
2. **Production cleanup policy operation**: invoke the production public batch
   coordinator (the narrow class that owns one check/batch) with an
   `IMesIngestProjection` test double. This seam may observe operation order,
   supplied cancellation tokens and completed receipts, but must not mock
   private helpers.
3. **Transactional projection seam**: use
   `IMesIngestProjection.AdvanceHistoryRetentionAsync` for a bounded raw
   expiration transaction and
   `CleanupNextRetentionEligibleSeriesAsync` for one indivisible Series
   tombstone/graph transaction. Ticket 16 may evolve the raw call to accept an
   explicit batch limit/result continuation, but it must preserve this public
   policy boundary rather than add direct deletion SQL in the Host.
4. **Operational read seam**: observe cleanup status through a production
   projection read/result and cleanup failure through the only V2
   `/api/v2/current-ingest-attention` endpoint. Persistent SQL may be queried
   only for integration evidence that the public operation committed the
   documented graph/boundary; it must not replace the public status/HTTP
   assertion.
5. **Poll-priority seam**: drive the production poll/cleanup coordination
   boundary with a pending poll and a running cleanup batch. Assert that no
   second cleanup transaction starts once polling is due and that no two
   cleanup batches overlap. Do not test a private semaphore or lock object.

These seams are fixed by the ticket/spec language: controllable
`TimeProvider`, production poll coordinator, transactional projection, V2
Current Attention, and real SQL Server. A general scheduler, SQL Server Agent,
Windows Task Scheduler, Watch-only state or direct test deletion are outside
scope.

## Current production inventory and gaps

- `MesIngest.Host/Program.cs` registers `TimeProvider.System`, one projection,
  `NewMesIngestHostSessionService`, and (only for Oracle runtime) one
  `MesTaskUnionPollHostedService`. It does not register a history-cleanup
  hosted service.
- `MesIngestHostOptions` currently has polling options only. `appsettings.json`
  freezes `ContinuousPollEnabled=true`, `PostPollDelaySeconds=10` and the
  Oracle timeout, but has no cleanup interval, row limit, time budget or enable
  switch.
- `AdvanceHistoryRetentionAsync` uses the commit-order application lock and one
  serializable transaction, but selects every expired PollTrace and can delete
  an unbounded number of raw observations. Its result already reports advance
  time, cutoff, expired traces, deleted observations and earliest available
  Host UTC.
- `CleanupNextRetentionEligibleSeriesAsync` selects at most one due Series and
  atomically writes the permanent tombstone before deleting the complete graph.
  Ticket 15 failpoint tests prove rollback/retry and indivisibility. Ticket 16
  should loop around this seam; it must never split or reproduce its internals.
- Both retention transactions currently wait on the same commit-order lock as
  projection with no Host-level poll-priority decision. There is no cleanup
  single-flight state or bounded lock-wait policy exposed at the production
  coordination seam.
- `SchemaInfo.EarliestAvailableHostUtc` is durable, but there is no durable
  cleanup-run state for last attempt/success, progress, counts, failure reason
  or next check.
- `CurrentIngestAttentionKinds` has four kinds only: Series error, poll failure,
  task-type protection and unassigned observation. Attention SQL has no cleanup
  source. Cleanup failure therefore cannot currently appear or clear through
  the V2 endpoint.
- Storage-pressure state/pause is owned by Ticket 17. Ticket 16 must prove only
  that an ordinary cleanup failure does not cancel, gate or pause MES polling;
  it must not implement a volume-space monitor early or equate cleanup failure
  with `StoragePressurePause`.

## Existing test conventions and reusable harnesses

- `MesIngest.Tests` targets `net8.0-windows`, xUnit 2.4.2 and VSTest. Tests use
  `Fact`/`Theory`, descriptive snake-case names and direct xUnit assertions; no
  mocking package is installed, so small recording/failing doubles are normal.
- Pure coordination tests live in `MesIngest.Tests`, construct the public
  production type, use `NullLogger<T>`, deterministic `TaskCompletionSource`
  gates and cancellation tokens, and assert secondary observations such as
  call order/max concurrency. See `SingleFlightPollLoopTests` and
  `MesTaskUnionPollRunnerTests`.
- `ManualTimerTimeProvider` drives `TimeProvider.CreateTimer`; use it for the
  hourly loop. Do not poll with arbitrary sleeps and do not wait an hour.
- Real SQL tests use `[Collection("Ticket01SqlServer")]`,
  `[Ticket01SqlServerFact]`, `Ticket01SqlServerDatabase.CreateAsync()`,
  `Ticket01ProcessEnvironmentScope`, production `WebApplicationFactory<Program>`
  and explicit SQL Server identity evidence. See `HistoryRetentionStateTests`,
  `ArchivedDemandKeyTombstoneTests` and `CurrentIngestAttentionTests`.
- Ticket 13 already proves exact 30-day raw/Series boundaries, earliest
  available history and eligibility reset. Ticket 15 already proves every
  intra-Series failpoint, one tombstone and whole-graph retry. Do not duplicate
  those matrices in Ticket 16.
- Current Attention assertions verify kind/severity/stable identity/evidence,
  exact facets, stable ordering and clearing after recovery through HTTP. Add
  cleanup as a fifth source and update exact kind/facet expectations instead of
  creating a parallel diagnostics endpoint just for failure.
- Tier 1 is `dotnet test MesIngest.Tests` from `mes/ingest/csharp`. For SQL work
  the three `MES_INGEST_TICKET01_*` environment values must target a real
  server; final evidence must say `Failed: 0, Skipped: 0`. Only the parent
  implementation run should obtain the exact command through `run-tests` and
  execute it once at close.

## Acceptance checklist mapped to evidence

| Ticket checklist item | Planned evidence |
| --- | --- |
| 单实例 Host 后台流程默认每小时检查一次，不依赖 SQLSERVERAGENT 或外部 Windows 计划任务。 | `History_cleanup_host_checks_once_per_hour_and_stops_with_the_Host` advances `ManualTimerTimeProvider` to one tick before/at two hourly boundaries, asserts one production service instance and one check per boundary. Production registration/appsettings and bounded repository inspection are non-test evidence that no external scheduler owns deletion. |
| 每批具有明确行数和时间预算；真实基线选择并冻结安全默认值，但不得改变 30 天领域保留语义。 | `Cleanup_defaults_freeze_hourly_row_and_time_budgets_without_changing_thirty_day_retention` asserts the real-baseline constants and exact 30-day policy. `Cleanup_batch_stops_at_each_configured_budget_boundary` is a deterministic policy theory for row/time boundaries. The ticket comment must cite the real SQL baseline used to select defaults. |
| RawObservation 和 Series 清理均幂等、可取消、失败可续，单个 Series 的墓碑事务不能被批次预算拆开。 | Normal and resume scenarios assert bounded raw/Series receipts and retry. `Budget_interruption_finishes_the_started_series_then_the_next_batch_resumes_at_the_next_series` asserts no next Series starts and cancellation reaches the projection. Existing `Series_cleanup_failpoints_roll_back_then_retry_writes_one_minimal_tombstone_and_deletes_graph_once` remains authoritative for intra-Series atomicity. |
| 轮询到期时清理让出资源，不与投影形成无界锁等待或并发清理实例。 | `Pending_poll_prevents_another_cleanup_transaction_and_cleanup_never_overlaps_itself` deterministically gates calls, asserts poll begins before another cleanup transaction, cleanup max concurrency is one, and the batch ends rather than waiting without bound. Real SQL normal path records bounded elapsed/lock behavior. |
| 清理进度、最后成功、删除计数、earliest available、失败原因和下一次检查时间可观测。 | The normal SQL scenario reads the production cleanup-status seam and asserts run phase/progress, last success, per-run and cumulative raw/Series counts, earliest available and exact next check. Failure scenario asserts sanitized reason; recovery asserts it clears while prior counts remain coherent. |
| 清理失败形成 Current Attention，但在未达到存储阈值时不自动暂停 MES 轮询。 | `Cleanup_failure_is_current_attention_then_recovery_clears_it_without_stopping_polls` reads V2 HTTP after failure/recovery and concurrently proves poll call count continues. It asserts no `StoragePressurePause` transition/stop is reported; Ticket 17 retains threshold behavior ownership. |
| 使用现有 TimeProvider 和最小到期批次加速跨越每小时间隔，不真实等待一小时、不生成规模历史，也不建立通用作业调度平台。 | All scheduling tests use `ManualTimerTimeProvider` and fixtures seed only the smallest expired raw trace/one or two due Series. Code review evidence confirms one purpose-built cleanup service/coordinator and no scheduler abstraction/platform. |
| 只验证一个正常批次、一个预算中断续跑和一个失败恢复路径；其它边界由策略级确定性测试覆盖。 | Exactly three integration scenarios are named below. Remaining interval/row/time/cancellation/poll-priority cases are deterministic coordinator/policy tests with doubles, not additional large SQL histories. |
| 开发期运行聚焦 cleanup/HostedService/Attention 测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。 | Focused filters run after each tracer slice; the final ticket evidence records one real-SQL `dotnet test MesIngest.Tests` run, wall time under 45 minutes, and `Failed: 0, Skipped: 0`. No Tier 2/3 is required because Ticket 16 does not touch Watch UI. |

## High-risk pseudo-mutations

- Change the interval from one hour or schedule the next check relative to
  completion rather than the fixed check boundary.
- Ignore one of the row/time limits, or count an attempted Series before its
  transaction commits.
- Cancel between tombstone and graph deletion, or start a second Series after
  the budget/cancellation is already exhausted.
- Start cleanup while a poll is pending, allow two cleanup loops, or wait
  indefinitely on the projection order lock.
- Record success before all committed receipts, erase cumulative counts on a
  no-op run, move earliest available backward, or compute next check from wall
  clock outside `TimeProvider`.
- Log a cleanup exception but fail to persist a sanitized failure attention;
  retain that attention after a successful retry; or stop MES polling merely
  because cleanup failed.
- Trigger cleanup from a Watch request, SQL Agent, external script or a generic
  scheduler instead of the one Host-owned lifecycle.
