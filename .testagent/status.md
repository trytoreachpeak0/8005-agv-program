# Ticket 02 test-generation status

## Outcome

- Five vertical real-SQL acceptance tests are implemented in `MesIngest.Tests/RoundEvidenceIdempotencyTests.cs`; the canonical multiset rule also has a focused unit test in `MesIngest.Tests/MesTaskUnionRoundDigestTests.cs`.
- The formal SQL Server gate ran on product version `16.0.1190.2`, major `16`, compatibility level `160`: ticket 01 regression + ticket 02 + digest produced **9 passed, 0 skipped, 0 failed**.
- Each real-SQL test owns one GUID-suffixed `MesIngest_Ticket01_` database and removes only that validated database during disposal.
- A non-incremental Release solution build passed with **0 warnings and 0 errors**. Solution-level discovery found all nine ticket 01/02 tests.
- Full `MesIngest.Tests` regression, with the already-documented unrelated retention test and one known desktop-interaction flake excluded, produced **508 passed, 19 environment-gated skips, 0 failed**. The retention test derives a file timestamp from the real wall clock but evaluates retention against a fixed 2026-07-31 clock. `MainWindowUiAutomationTests.Fluent_title_bar_supports_uia_keyboard_double_click_and_mouse_drag` failed once in the broad run and passed immediately in isolation. Ticket 02 changes neither telemetry nor Watch UI.

## Requirement-to-test evidence

| Requirement | Test evidence |
| --- | --- |
| `SUCCESS、FAILURE 和 INCOMPLETE 都留下可查询的 PollTraceId、查询版本、结果类型、Host UTC 时间、行数和规范化内容摘要；原始行按稳定规范化多重集合计算，返回顺序变化不会改变摘要，重复行数量变化会改变摘要。` | `All_outcomes_expose_canonical_utc_round_evidence_without_projecting_unsuccessful_results` reads all three outcomes through `/api/v2`, including UTC times, counts and digests. `Canonical_digest_treats_raw_rows_as_an_order_insensitive_multiset` proves order and offset invariance plus duplicate multiplicity sensitivity. The replay/conflict tests exercise the same digest against SQL. |
| `使用相同 PollTraceId 和相同规范化内容重放时，正式 API 返回同一已接受结果，且不会重复创建 PollTrace、ProjectionCommit、Series、Demand 或事件。` | `Same_poll_trace_and_canonical_content_replays_the_original_accepted_result_without_duplicates` changes row order, source-date offset and attempt timestamps, then asserts the original receipt/API JSON and exact table counts `(1,1,2,2,2,4)`. The all-outcomes test also proves FAILURE/INCOMPLETE replay. |
| `使用相同 PollTraceId 绑定不同内容时，整轮以明确、版本化的契约冲突失败；真实 SQL Server 中的轮次账本和全部业务投影均无部分写入。` | `Same_poll_trace_with_different_content_returns_versioned_conflict_without_partial_writes` checks duplicate multiplicity, outcome and query-version conflicts, the stable `POLL_TRACE_CONTENT_CONFLICT` code/contract version/id, unchanged SQL counts and byte-equivalent API state. |
| `FAILURE 和 INCOMPLETE 只追加各自的可追溯轮次证据，不创建、更新、标记 GONE 或归档任何 Series/Demand，也不改变上一成功 ProjectionCommit 的正式 API 读取结果。` | `All_outcomes_expose_canonical_utc_round_evidence_without_projecting_unsuccessful_results` starts with SUCCESS, appends FAILURE and INCOMPLETE, and proves both have nullable commits/zero raw projection rows while the prior Series API JSON and latest commit remain unchanged. |
| `缺列、列类型或结果结构不满足契约时归为 INCOMPLETE；结构完整但字段值为空、非法或互相冲突的原始行仍归为 SUCCESS 数据证据，不得借 INCOMPLETE 隐藏局部坏数据。` | The all-outcomes test sends structurally incomplete evidence through the production `MesTaskUnionRound` classification boundary and observes INCOMPLETE isolation. `Success_preserves_unassigned_rows_while_projecting_every_assignable_key` keeps null/blank/invalid/conflicting values in SUCCESS and projects two distinct WorkTypes for one SUBLOT. Oracle column/type detection remains owned by ticket 15. |
| `SUCCESS 中缺少 SUBLOT 或 TASK_TYPE 的行以 UnassignedMesObservation 原样归入该轮证据且不猜测 DemandSeries；同轮其它可识别业务键仍正常投影。` | `Success_preserves_unassigned_rows_while_projecting_every_assignable_key` asserts explicit `UNASSIGNED` observations with null identities and original values, negative no-guess API reads, two `ASSIGNED` observations, and exact Series/Demand/raw/event SQL counts. |
| `通过真实 SQL Server 和正式 API 连续验证成功、同内容重放、内容冲突、FAILURE、INCOMPLETE 及 Host 重启，证明业务投影隔离、轮次证据和幂等结论在持久化后保持一致。` | `Restarted_host_preserves_round_evidence_replay_and_projection_isolation` uses one owned SQL database across two production Host/DI graphs and compares SUCCESS/FAILURE/INCOMPLETE trace JSON, Series JSON, replay receipt, post-restart conflict and table counts. |

## TDD and gap analysis

- Each of the five vertical slices failed for the missing production behavior before its implementation and passed after the minimal slice was added.
- Empirically killed mutation 1: returning `IsReplay = false` for an unsuccessful replay failed the all-outcomes test.
- Empirically killed mutation 2: removing outcome from the immutable PollTrace fingerprint failed the conflict test.
- Empirically killed mutation 3: reporting unassigned raw rows as assigned failed the unassigned-evidence test.
- Required Standards review found and resolved two consistency defects: MES source-date offset equality now shares one domain rule between canonical evidence and projection comparison, and initial/replay receipts share one stable identity aggregation rule. The source-date regression test failed before the fix and passed after it.
- No mutation remains applied. Transaction fault injection and concurrent commit/read stress remain deliberately assigned to ticket 16.
