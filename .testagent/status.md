# Ticket 08 test-generation status

## Current state

- Implementation and public-seam acceptance coverage are complete.
- Fixed review point: `b2efb21` (ticket07).
- Formal seam: scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> `/api/v2/demand-series` HTTP.
- Ticket08 SQL Server/API gate: 10 passed, 0 failed, 0 skipped on SQL Server product major 16 / compatibility level 160.
- Standards and Spec re-review both report no remaining actionable findings.

## Requirement evidence

| Verbatim requirement | Executed evidence |
| --- | --- |
| 首次列表请求冻结到一个明确的 ProjectionCommit；响应必须带快照身份/commit 元数据。该快照的 exact total、lifecycle facets、每行 lifecycle/currentPresence/currentDemand/generation/lastSeriesSequence，以及随后页面和详情都按同一 commit 计算。 | `Old_snapshot_detail_stays_at_commit_a_until_a_latest_refresh_reads_commit_b`; `Frozen_snapshot_combines_all_lifecycle_presence_states_with_exact_pages_and_provenance` |
| 列表不按外部可读资格隐藏坏数据，覆盖 TRACKING+VISIBLE、TRACKING+GONE、ARCHIVED+GONE、ARCHIVED+LONG_GONE_BUT_VISIBLE，并稳定返回 SeriesId、SUBLOT、WorkType、StartedAt、Lifecycle、CurrentPresence、当前 Demand/Generation、LastSeriesSequence。 | `Frozen_snapshot_combines_all_lifecycle_presence_states_with_exact_pages_and_provenance`; `Frozen_conflict_detail_keeps_duplicate_multiset_and_multi_work_type_evidence_after_recovery` |
| 详情返回全部 Demand 世代与 predecessor、当前和历史 MES 事实、规范化原始多重集合、duplicate/多 WorkType 冲突、当前条件、永久错误期间、生命周期节点和每代不可读结论。 | `Frozen_conflict_detail_keeps_duplicate_multiset_and_multi_work_type_evidence_after_recovery`; `Prearchive_reappearance_creates_a_frozen_successor_without_rewriting_the_gone_snapshot`; `Frozen_detail_retains_missing_field_period_after_recovery_without_leaking_its_future_close` |
| 详情事实可追溯 DemandId、PollTraceId、Host UTC、ProjectionCommitId；事件严格按 SeriesSequence 升序且保留 payloadVersion，归档、恢复及错误历史不得遗漏。 | `Frozen_snapshot_combines_all_lifecycle_presence_states_with_exact_pages_and_provenance`; `Prearchive_reappearance_creates_a_frozen_successor_without_rewriting_the_gone_snapshot`; conflict and error-period tests assert raw/event/evidence provenance. |
| Host 在快照内先筛选，再 exact count/facets，再稳定排序和有界分页；cursor/locator 绑定 snapshot、规范化 filter、固定 order、contract version，并校验完整性。 | `Frozen_pages_are_exact_stable_and_reject_tampered_or_mismatched_credentials`; three token tests cover full binding, purpose separation, tampering, and normalized-filter mismatch. Cursor pages execute keyset seek over `StartedAt DESC, SeriesId ASC`; direct page location remains bounded to page size 200. |
| 取得旧列表后提交改变字段或生命周期的新 SUCCESS，旧 snapshot 的页面和详情仍属于旧 commit；latest 才看到新 commit；未知、失效、篡改或跨 filter/version 引用结构化失败，不能静默返回第一页/最新态。 | `Old_snapshot_detail_stays_at_commit_a_until_a_latest_refresh_reads_commit_b`; `Frozen_pages_are_exact_stable_and_reject_tampered_or_mismatched_credentials`; both include same-Host-time commits and structured HTTP failures. |
| 脚本化 MesTaskUnionRound -> production Host/domain -> real SQL Server -> formal versioned HTTP API 覆盖字段异常及恢复、duplicate、多 WorkType、GONE、归档前重现、archive、LongGoneButVisible、重启，以及旧快照读取期间的新提交。 | Seven SQL/HTTP tests in `DemandSeriesFrozenSnapshotTests`; `Invoke-Ticket08SqlServerGate.ps1` enforces exactly 10 total tests passed and zero skipped. |

## Verification log

- `Invoke-Ticket08SqlServerGate.ps1 -Configuration Release -ExpectedProductMajor 16 -ExpectedCompatibilityLevel 160`: 10 passed, 0 failed, 0 skipped; marker `MESINGEST_TICKET08_SQLSERVER_API_GATE_PASSED`.
- Ticket01-07 production SQL regressions (`NewSuccessRoundTracerSpine`, field/error periods, duplicate/multi-WorkType, restart/GONE/prearchive, archive/LongGone, TaskType protection): 28 passed, 0 failed, 0 skipped.
- `dotnet build MesIngest.sln --configuration Release --no-incremental`: 0 warnings, 0 errors.
- Full solution: `MesIngest.Tests` 552 passed / 19 skipped / 2 unrelated existing environment failures; `MesIngest.Watch.UiTests` 82 passed / 27 environment-gated skips / 0 failed.
  - `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age` is the pre-existing fixed-clock/current-file-time failure already recorded under the Fluent refinement tracker.
  - `MainWindowUiAutomationTests.Fluent_title_bar_supports_uia_keyboard_double_click_and_mouse_drag` cannot inject mouse input in this non-interactive process (`Win32Exception: Access is denied`); no Watch/UI files changed in ticket08.
- Pseudo-mutation audit: lifecycle reconstruction mutation and WorkType predicate mutation were each killed by the new acceptance tests (2/2); both mutations were reverted before the final gate.
- Two-axis review from `b2efb21`: initial missing prearchive coverage and cursor-anchor findings were fixed; Standards and Spec re-review found no remaining actionable issue.
