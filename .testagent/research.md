# Ticket 08 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/08-demand-series-frozen-snapshot-list-and-detail.md`.
- Confirmed public seam: scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> formal `/api/v2` HTTP.
- Production modules: `MesIngest.Core/SeriesProjection`, `MesIngest.Infrastructure/SqlServer`, and `MesIngest.Host/NewMesIngestEndpoints.cs`.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- No WPF/UI files are in scope; the Fluent/golden-renderer workflow does not apply.
- `find-untested-sources` is unavailable; source/test pairing was determined from the bounded ticket seam.

## Required semantics and current gaps

- A first list request must bind to one persisted `ProjectionCommit`; all pages, exact totals, facets, list rows, and detail reads must use that same point.
- `ProjectionCommitId` is a random GUID and `CommittedAt` may tie, so a persisted monotonic projection sequence is required for `<= snapshot` reconstruction.
- Current Series/Demand/error-condition tables are mutable. A historical read must reconstruct state from immutable events, raw observations, and error evidence; a later close must not leak into an older snapshot.
- Lifecycle and presence are orthogonal: TRACKING/ARCHIVED versus VISIBLE/GONE/LONG_GONE_BUT_VISIBLE.
- Default stable order is fixed to `StartedAt DESC, SeriesId ASC`; bounded pages default to 100 and max at 200.
- Filters are server-side and exact under the contract: lifecycle, presence, exact ordinal WorkType, ordinal SUBLOT search, exact SeriesId/DemandId, and trusted current AREA.
- Snapshot and page credentials persist across Host restart, are HMAC-protected with a database-persisted key, and bind contract version, projection sequence/id, canonical filters, order, page, and page size.
- No commit exists for FAILURE/INCOMPLETE, so latest remains the last SUCCESS. Before any SUCCESS, list/detail return structured `PROJECTION_NOT_AVAILABLE`.
- Snapshot history is not assigned a TTL in ticket08; a structurally valid reference to a retained commit remains addressable.
- Full single-Series history is returned for this ticket. Ticket12 remains the later bounded evidence API; list reads are always bounded.

## Target inventory

| Target | Role |
| --- | --- |
| `MesIngest.Core/SeriesProjection/DemandSeriesBrowseContract.cs` | public query/result/error and signed credential contract |
| `ProjectionModels.cs`, `IMesIngestProjection.cs`, `NewMesIngestContract.cs` | provenance additions, frozen reads, schema/contract v8 |
| `SqlServerMesIngestSchema.cs` | monotonic commit sequence and persistent signing key |
| `SqlServerMesIngestProjection.cs` | latest/as-of resolution, reconstruction, exact list/facets/page/detail |
| `NewMesIngestEndpoints.cs` | formal frozen list/detail HTTP resources and structured errors |
| `DemandSeriesFrozenSnapshotTests.cs` | real-SQL Production Host tracer bullets plus credential tests |
| `Invoke-Ticket08SqlServerGate.ps1` | zero-skip real SQL acceptance gate |

## Environment and commands

- SDK: .NET SDK 10.0.302; no MTP signals; use VSTest + xUnit v2 syntax.
- Real SQL gate environment: `MES_INGEST_TICKET01_SQLSERVER`, `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR=16`, and `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL=160`.
- Focused: `dotnet test mes/ingest/csharp/MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~DemandSeriesFrozenSnapshotTests"`.
- Final build: `dotnet build mes/ingest/csharp/MesIngest.sln --configuration Release --no-incremental`.
- Full tests: `dotnet test mes/ingest/csharp/MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.

## Acceptance checklist (verbatim)

1. `首次列表请求冻结到一个明确的 ProjectionCommit；响应必须带快照身份/commit 元数据。该快照的 exact total、lifecycle facets、每行 lifecycle/currentPresence/currentDemand/generation/lastSeriesSequence，以及随后页面和详情都按同一 commit 计算。`
2. `列表不按外部可读资格隐藏坏数据，覆盖 TRACKING+VISIBLE、TRACKING+GONE、ARCHIVED+GONE、ARCHIVED+LONG_GONE_BUT_VISIBLE，并稳定返回 SeriesId、SUBLOT、WorkType、StartedAt、Lifecycle、CurrentPresence、当前 Demand/Generation、LastSeriesSequence。`
3. `详情返回全部 Demand 世代与 predecessor、当前和历史 MES 事实、规范化原始多重集合、duplicate/多 WorkType 冲突、当前条件、永久错误期间、生命周期节点和每代不可读结论。`
4. `详情事实可追溯 DemandId、PollTraceId、Host UTC、ProjectionCommitId；事件严格按 SeriesSequence 升序且保留 payloadVersion，归档、恢复及错误历史不得遗漏。`
5. `Host 在快照内先筛选，再 exact count/facets，再稳定排序和有界分页；cursor/locator 绑定 snapshot、规范化 filter、固定 order、contract version，并校验完整性。`
6. `取得旧列表后提交改变字段或生命周期的新 SUCCESS，旧 snapshot 的页面和详情仍属于旧 commit；latest 才看到新 commit；未知、失效、篡改或跨 filter/version 引用结构化失败，不能静默返回第一页/最新态。`
7. `脚本化 MesTaskUnionRound -> production Host/domain -> real SQL Server -> formal versioned HTTP API 覆盖字段异常及恢复、duplicate、多 WorkType、GONE、归档前重现、archive、LongGoneButVisible、重启，以及旧快照读取期间的新提交。`
