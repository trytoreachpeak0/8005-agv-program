# Ticket 16 vertical TDD test plan

Work one tracer bullet at a time: add one failing public-seam test, run only
that test, make the smallest production change, and repeat. Do not batch-write
all tests before implementation and do not refactor during red/green. Ticket 15
remains the authority for the atomic contents of one Series cleanup
transaction.

## Exact candidate test files and names

### `MesIngest.Tests/HistoryCleanupPolicyTests.cs`

1. `Cleanup_defaults_freeze_hourly_row_and_time_budgets_without_changing_thirty_day_retention`
   - Assert production defaults selected by the real SQL baseline: one-hour
     interval, positive bounded raw-row/Series limits and positive bounded time
     budget.
   - Assert both existing retention windows remain exactly 30 days.
   - Assert published `appsettings.json` matches the option defaults.
2. `Cleanup_options_reject_non_positive_or_unbounded_operational_budgets`
   - A compact theory over interval/row/Series/time invalid values; assert
     startup validation rejects the configuration before a loop starts.
3. `Cleanup_batch_stops_at_each_configured_budget_boundary`
   - A deterministic theory over raw-row limit, Series limit and elapsed-time
     limit using a recording `IMesIngestProjection` and controllable
     `TimeProvider`.
   - Assert exact calls/committed receipt counts and that empty/no-op results do
     not invent deletion progress.
4. `Pending_poll_prevents_another_cleanup_transaction_and_cleanup_never_overlaps_itself`
   - Gate a running cleanup call, mark poll due through the production
     coordination seam and concurrently request another cleanup run.
   - Assert max cleanup concurrency is one, no next cleanup transaction starts,
     poll gets the next acquisition, and the cleanup attempt returns/cancels
     within its configured bound.

### `MesIngest.Tests/HistoryCleanupHostedServiceTests.cs`

5. `History_cleanup_host_checks_once_per_hour_and_stops_with_the_Host`
   - Start the production cleanup `IHostedService` with
     `ManualTimerTimeProvider`; assert no call one tick before the first hour,
     one call at the boundary, no duplicate call before the next boundary and
     one second call at hour two.
   - Stop the Host and advance another hour; assert no further call.
   - Resolve hosted services from production DI and assert exactly one cleanup
     service is registered whenever projection is enabled, even with Oracle
     polling disabled.
6. `Budget_interruption_finishes_the_started_series_then_the_next_batch_resumes_at_the_next_series`
   - Configure the smallest two-Series sequence. Advance controlled time so the
     time budget expires while the first public one-Series transaction is in
     flight.
   - Assert its committed receipt is counted, the second Series is not started
     in that batch, cancellation is observed at the projection boundary, next
     run starts at the second Series, and no Series transaction overlaps.
   - This is the ticket's single budget-interruption/resume scenario; row-limit
     variants remain in the policy theory rather than another integration path.

### `MesIngest.Tests/HistoryCleanupSqlServerTests.cs`

7. `Normal_hourly_batch_deletes_only_the_budgeted_due_history_and_publishes_complete_progress`
   - `[Ticket01SqlServerFact]`, minimum fixture: only enough PollTraces/Series to
     put one item inside and one just outside the configured batch limit.
   - Drive the production Host cleanup service across one hour with
     `ManualTimerTimeProvider`; do not invoke direct deletion SQL.
   - Assert exact raw and Series committed counts, remaining continuation,
     tombstone/whole-graph result, non-regressing earliest available boundary,
     last-success UTC, progress/phase and exact next-check UTC through the
     production status seam. Assert a repeated no-op check is idempotent.
   - This is the ticket's single normal-batch integration scenario.
8. `Cleanup_failure_is_current_attention_then_recovery_clears_it_without_stopping_polls`
   - `[Ticket01SqlServerFact]`; inject one sanitized cleanup failure at an
     existing production checkpoint/public operation boundary, not inside a
     private helper.
   - Run the production cleanup and poll services together with deterministic
     gates. Through `/api/v2/current-ingest-attention`, assert the cleanup kind,
     ERROR severity, stable identity, occurred time and sanitized failure
     evidence; exact kind facets/order must include the new fifth source.
   - Assert another MES round begins/commits after the cleanup failure and no
     storage-pressure pause/automatic polling cancellation is observed.
   - Disarm the failure, advance to the next check and assert cleanup resumes,
     status records success/counts/next check, cleanup attention clears and
     polling continues. This is the ticket's single failure/recovery scenario.

### Neighbouring tests to update, not duplicate

- `CurrentIngestAttentionTests.Four_sources_are_stable_and_only_complete_success_clears_current_items_while_history_remains`
  should be renamed/generalized only as needed so exact all-kind/facet
  assertions include the cleanup kind at zero when healthy. Keep its existing
  four-source behavioral matrix intact.
- `MesTaskUnionPollRunnerTests.RecordingProjection` must implement any evolved
  public cleanup/status members without adding behavior unrelated to its poll
  tests.
- `EmptyDatabaseBootstrapTests` should add schema-contract assertions for the
  single durable cleanup-status row/table if that is the chosen observable
  persistence contract; do not inspect SQL command strings.
- Contract/OpenAPI freeze tests change only if cleanup observability adds fields
  to the public V2 DTO. A cleanup-attention item that reuses the existing DTO
  still requires the exact kind catalog/version updates demanded by the
  contract tests.

## Red-green tracer order

1. **Defaults and validation**: add test 1 (red), introduce only the cleanup
   options/defaults and retain 30-day constants (green); add test 2 and minimal
   startup validation.
2. **One deterministic batch**: add the relevant case of test 3 (red), add the
   public purpose-built cleanup batch coordinator and bounded raw projection
   request/result (green). Add remaining theory rows one by one.
3. **Hourly Host ownership**: add test 5 (red), register one production
   `HistoryCleanupHostedService` using `TimeProvider` (green). No generic job
   scheduler and no external trigger.
4. **Resume without split**: add test 6 (red), make the coordinator re-check
   time/cancellation only between projection transactions and preserve the
   continuation naturally in durable SQL state (green).
5. **Poll priority/single flight**: add test 4 (red), add the smallest shared
   production coordination boundary needed for pending-poll priority and one
   cleanup owner; bound SQL lock acquisition/cancellation rather than waiting
   indefinitely (green).
6. **Normal real-SQL batch**: add test 7 (red), persist/update cleanup run state
   atomically around committed receipts and expose the public status read
   (green). Reuse Ticket 13/15 seed helpers or extract only neutral fixture
   helpers; do not copy their complete matrices.
7. **Failure attention/recovery**: add test 8 (red), persist sanitized current
   cleanup failure, include it in Current Attention, clear it only after a
   successful retry and leave polling enabled (green).
8. **Contract/schema fallout**: update only affected exact schema, attention
   catalogs, DTO/OpenAPI and fake projection compile surfaces, each led by the
   narrow failing existing test.

## Requirement-to-test audit

| Verbatim requirement | Concrete test or non-test evidence |
| --- | --- |
| 单实例 Host 后台流程默认每小时检查一次，不依赖 SQLSERVERAGENT 或外部 Windows 计划任务。 | `History_cleanup_host_checks_once_per_hour_and_stops_with_the_Host`; production DI/appsettings plus repository inspection for absence of external deletion ownership. |
| 每批具有明确行数和时间预算；真实基线选择并冻结安全默认值，但不得改变 30 天领域保留语义。 | `Cleanup_defaults_freeze_hourly_row_and_time_budgets_without_changing_thirty_day_retention`, `Cleanup_batch_stops_at_each_configured_budget_boundary`, and ticket comment citing the real-SQL baseline measurements/default selection. |
| RawObservation 和 Series 清理均幂等、可取消、失败可续，单个 Series 的墓碑事务不能被批次预算拆开。 | `Normal_hourly_batch_deletes_only_the_budgeted_due_history_and_publishes_complete_progress`, `Budget_interruption_finishes_the_started_series_then_the_next_batch_resumes_at_the_next_series`, and existing Ticket 15 failpoint test. |
| 轮询到期时清理让出资源，不与投影形成无界锁等待或并发清理实例。 | `Pending_poll_prevents_another_cleanup_transaction_and_cleanup_never_overlaps_itself`; normal SQL scenario supplies bounded real lock/elapsed evidence. |
| 清理进度、最后成功、删除计数、earliest available、失败原因和下一次检查时间可观测。 | Normal SQL test asserts success/progress/count/boundary/next check; failure/recovery test asserts failure reason then cleared recovery state. |
| 清理失败形成 Current Attention，但在未达到存储阈值时不自动暂停 MES 轮询。 | `Cleanup_failure_is_current_attention_then_recovery_clears_it_without_stopping_polls`. |
| 使用现有 TimeProvider 和最小到期批次加速跨越每小时间隔，不真实等待一小时、不生成规模历史，也不建立通用作业调度平台。 | Hosted-service tests use `ManualTimerTimeProvider`; both SQL tests document their minimal fixture sizes; standards review confirms purpose-built service only. |
| 只验证一个正常批次、一个预算中断续跑和一个失败恢复路径；其它边界由策略级确定性测试覆盖。 | Exactly tests 7, 6 and 8 are the three scenario tests; tests 1-5 are deterministic policy/lifecycle tests. |
| 开发期运行聚焦 cleanup/HostedService/Attention 测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。 | Focused filters below during red/green; final real-SQL Tier 1 transcript/report with elapsed `< 45m`, `Failed: 0`, `Skipped: 0`. |

## Narrow validation progression

- During each loop, run one exact test with VSTest
  `--filter "FullyQualifiedName=MesIngest.Tests.<Class>.<Method>"` after obtaining
  the precise command/argument ordering from the `run-tests` skill.
- After each file is green, run only:
  `FullyQualifiedName~HistoryCleanupPolicyTests`, then
  `FullyQualifiedName~HistoryCleanupHostedServiceTests`, then
  `FullyQualifiedName~HistoryCleanupSqlServerTests|FullyQualifiedName~CurrentIngestAttentionTests`.
- After implementation, re-open every test and audit each assertion against the
  mapping above. Run `test-gap-analysis` and assertion-quality review if
  available, recording findings/fixes in `.testagent/status.md` as required by
  `code-testing-agent`.
- Run the required Spec and Standards code-review axes to a fixed point, then
  repeat only affected focused tests.
- At close, run Tier 1 exactly once from `mes/ingest/csharp` against the approved
  real SQL Server with all three `MES_INGEST_TICKET01_*` variables. Require exit
  0, elapsed under 45 minutes, `Failed: 0`, `Skipped: 0`. Do not enter Tier 2 or
  Tier 3 because no Watch UI is in scope.
- Update Ticket 16 status/comments with baseline defaults, focused and Tier 1
  evidence, two-axis review result and commit identity; then commit the complete
  implementation on the current branch.
## Ticket 02 addendum (toast Variant A)

1. Verify first/repeated/recovered/reoccurring continuing-fault cycles and background summaries.
2. Verify refresh selection loss produces one 3-second notification and leaves detail unselected.
3. Verify page notifications clear on navigation while global Host faults remain.
4. Verify all-AREA confirm/cancel and AREA conflict overwrite/reload/later through real `ContentDialog` instances.
5. Run only focused classes during development, then one repository tier 1 after production freeze.
