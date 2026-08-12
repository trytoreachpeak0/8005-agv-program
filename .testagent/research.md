# Ticket 01 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/01-new-success-round-tracer-spine.md`.
- Production seam (already confirmed by the spec): scripted `MesTaskUnionRound` -> production Host/domain interface -> real SQL Server -> versioned read-only HTTP API.
- Source projects: `MesIngest.Core`, new `MesIngest.Infrastructure`, and `MesIngest.Host`.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- Existing Watch/UI files are out of scope and already contain user changes.

## Environment and commands

- SDK: .NET SDK 10.0.302, with no MTP runner configuration.
- Narrow test command: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~NewSuccessRoundTracerSpineTests"`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Final suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.
- Real SQL Server available locally: SQL Server 2022 `16.0.1190.2` on `localhost` with integrated authentication.
- Tests must create and own a GUID-suffixed `MesIngest_Ticket01_` database. They must never use the populated local `MesIngest` database or the legacy destructive `SqlServerTestEnv.WipeProjection` helper.

## Existing conventions

- HTTP tests use `WebApplicationFactory<Program>` and JSON assertions through public routes.
- SQL tests use xUnit facts/traits and serialize destructive legacy tests, but Ticket 01 will use a unique database per test instead of sharing one.
- API JSON uses camelCase, string enums, and `DateTimeOffset`.
- Existing Core/Host files are clean; only new files and narrow composition changes are safe to edit.

## Acceptance checklist (verbatim ticket requirements)

1. `在空的新数据库中提交包含一条唯一且字段有效的完整 SUCCESS 后，正式 API 能读到一个由 SUBLOT + WorkType 唯一确定的 DemandSeries、一个 VISIBLE 的第一代 TransportDemand、稳定的 SeriesId/DemandId，以及该轮完整原始观测和当前 MES 字段。`
2. `首次成功轮次产生可追溯的 PollTrace、ProjectionCommit 和按 SeriesSequence 排序的首次事实事件；API 返回的 Series、Demand、事件和轮次证据都指向同一次原子投影提交，不会呈现半轮状态。`
3. `再提交内容等价但 PollTraceId 不同的完整 SUCCESS 时，SeriesId、DemandId、世代和当前字段保持不变，且不会因无意义的重复观测追加业务变化事件。`
4. `Host 重启后，从正式 API 读到的标识、当前状态、原始证据和事件顺序与重启前一致，新历史不会依赖内存状态重建。`
5. `新主干只发布新版 schema 和版本化契约，不迁移或重新解释旧 TransportDemand、冻结字段、IngestAlert、DemandChangeFeed 或旧 DTO，也不提供新旧契约混跑的兼容路径。`
6. `自动验收以脚本化 MesTaskUnionRound → 生产 Host/领域入口 → 现场兼容的真实 SQL Server → 正式版本化 HTTP API 为门禁；内存存储或 LocalDB 结果只能提供开发反馈，不能替代该证据。`

## Design constraints discovered

- The full URI and API contract are frozen by later ticket 17. Ticket 01 therefore introduces a small, explicitly versioned tracer contract under `/api/v2` without claiming the later complete contract.
- TransportDemandKey comparison was not chosen by the spec. Ticket 01 must choose and publish one rule consistently. The implementation uses ordinal, case-sensitive, whitespace-preserving strings and one length-framed SHA-256 identity token for SQL uniqueness.
- Ticket 02 owns same-PollTrace replay/conflict and FAILURE/INCOMPLETE behavior; ticket 03 owns field changes and data errors; tickets 05-07 own lifecycle protection/GONE/archive; ticket 08 owns full frozen list/detail paging.
- Legacy endpoints may remain development-only until tickets 17/25, but the new path uses a separate connection option and schema and never reads, writes, or adapts legacy tables/DTOs.
