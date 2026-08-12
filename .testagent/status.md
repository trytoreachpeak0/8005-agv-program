# Ticket 01 test-generation status

## Outcome

- Three vertical acceptance tests are implemented in `MesIngest.Tests/NewSuccessRoundTracerSpineTests.cs`.
- All three pass against an explicitly opted-in, non-LocalDB SQL Server instance (`16.0.1190.2`, product major `16`, compatibility level `160`).
- Each test owns a new `MesIngest_Ticket01_<guid>` database and removes only that strictly validated database in `DisposeAsync`; no owned databases remain after the run.
- Release non-incremental solution build passes with 0 warnings and 0 errors.
- Full `MesIngest.Tests` result after the final build: 499 passed, 22 SQL tests skipped because their explicit connection variables were absent (including the three ticket-01 tests covered separately by the zero-skip formal gate), and 2 failed. The UI Automation failure passed on immediate isolated rerun. The remaining stable failure is the pre-existing `LatencyTelemetryTests.Watch_latency_file_telemetry_enforces_log_retention_by_age`: current HEAD sets the old file from real wall-clock time but evaluates retention against fixed 2026-07-31, so on 2026-08-12 it is only 28 days old relative to the injected clock. Ticket 01 does not modify that test or telemetry code.

## Requirement-to-test evidence

| Requirement | Test evidence |
| --- | --- |
| `在空的新数据库中提交包含一条唯一且字段有效的完整 SUCCESS 后，正式 API 能读到一个由 SUBLOT + WorkType 唯一确定的 DemandSeries、一个 VISIBLE 的第一代 TransportDemand、稳定的 SeriesId/DemandId，以及该轮完整原始观测和当前 MES 字段。` | `First_success_round_is_read_back_with_atomic_series_demand_and_round_evidence` asserts the v2 contract and key rule, Series/Demand IDs and generation, TRACKING/VISIBLE state, every live MES field, every raw field, and both by-key/by-id reads. |
| `首次成功轮次产生可追溯的 PollTrace、ProjectionCommit 和按 SeriesSequence 排序的首次事实事件；API 返回的 Series、Demand、事件和轮次证据都指向同一次原子投影提交，不会呈现半轮状态。` | The same test asserts trace/commit linkage across Series, Demand, raw observation and initial SERIES/DEMAND facts, plus consecutive SeriesSequence ordering. |
| `再提交内容等价但 PollTraceId 不同的完整 SUCCESS 时，SeriesId、DemandId、世代和当前字段保持不变，且不会因无意义的重复观测追加业务变化事件。` | `Equivalent_success_round_preserves_identity_and_does_not_append_business_events` asserts stable identity/generation/fields/event IDs, a new commit, and two independently linked raw observations/traces. |
| `Host 重启后，从正式 API 读到的标识、当前状态、原始证据和事件顺序与重启前一致，新历史不会依赖内存状态重建。` | `Restarted_host_reads_the_same_persisted_projection` disposes the first factory, constructs a new production Host/DI graph over the same SQL database, and compares IDs, state, raw links, event IDs/order and trace commit through HTTP only. |
| `新主干只发布新版 schema 和版本化契约，不迁移或重新解释旧 TransportDemand、冻结字段、IngestAlert、DemandChangeFeed 或旧 DTO，也不提供新旧契约混跑的兼容路径。` | The first test starts with an empty dedicated database, asserts the separate `/api/v2/contract`, proves legacy API/OpenAPI and legacy store DI are absent in Production V2, and exercises only the isolated `mesingest` schema/DTO path. Production also fails closed when the V2 database is omitted. Existing databases are validated against an exact schema manifest and are never patched or stamped. |
| `自动验收以脚本化 MesTaskUnionRound → 生产 Host/领域入口 → 现场兼容的真实 SQL Server → 正式版本化 HTTP API 为门禁；内存存储或 LocalDB 结果只能提供开发反馈，不能替代该证据。` | All three tests resolve production `SuccessRoundIngestor` from `WebApplicationFactory<Program>`, use only `MES_INGEST_TICKET01_SQLSERVER`, reject LocalDB/cloud engines, require an explicitly approved product major and compatibility level, and read via v2 HTTP. The gate completed with 3 passed and 0 skipped. A wrong-major mutation failed all three tests before database creation. |

## Gap analysis

- Empirically killed mutation 1: changing key-token inputs to uppercase made the case-variant 404 assertion fail.
- Empirically killed mutation 2: reversing event SQL ordering made the consecutive SeriesSequence assertion fail.
- High-risk ticket-01 behaviors are covered. Transaction fault injection and concurrent torn-read gates are intentionally owned by ticket 16 rather than expanded here.
- No mutation remains applied; the three-test baseline is green after restoration.
