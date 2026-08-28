# Ticket 11 test research

## Scope and confirmed seam

- Ticket: `.scratch/mes-ingest-bounded-storage-low-memory/issues/11-cut-over-polltrace-raw-evidence-reads.md`.
- Confirmed acceptance seam: scripted `MesTaskUnionRound` -> production `RoundIngestor` / `IMesIngestProjection` -> real SQL Server -> the sole V2 HTTP surface.
- This is a test-only TDD pass. Production code, schema, OpenAPI, contracts, Watch UI, and existing dirty files are out of scope.
- Tier 2 and Tier 3 are out of scope. SQL integration tests use `[Ticket01SqlServerFact]` and therefore require the repository's three real-SQL environment variables.
- The repository-wide `find-untested-sources` command was invoked once as required by the broad workflow, but it is not installed in this environment. The bounded inventory below was produced with `rg` instead.

## Bounded target inventory

- Domain seam: `MesIngest.Core/SeriesProjection/IMesIngestProjection.cs` and `ProjectionModels.cs` (`GetPollTraceAsync`, `PollTraceSnapshot`, `DemandRawObservationSnapshot`).
- SQL seam: `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestProjection.cs` (`GetPollTraceAsync`) and `SqlServerMesIngestSchema.cs` (`PollTraces`, `ProjectionCommits`, `DemandRawObservations`).
- V2 HTTP seam: `MesIngest.Host/NewMesIngestEndpoints.cs` (`GET /api/v2/poll-traces/{pollTraceId}`, `PollTraceDto`, `NewMesIngestErrorDto`).
- Scale proof seam: `pack/validation/Invoke-ScaleAndQueryEvidence.ps1` and `MesIngest.Tests/ScaleAndQueryEvidenceGateTests.cs`.
- Representative xUnit conventions: `Ticket15RoundEvidenceTests.cs`, `OracleMesTaskUnionProductionEntryTests.cs`, `DemandSeriesFrozenSnapshotTests.cs`, and `ScaleAndQueryEvidenceGateTests.cs`.

## Current behavior and confirmed gaps

- `GetPollTraceAsync` seeks the PollTrace row by exact `PollTraceId`, but reads raw observations with only `o.PollTraceId = @identity`; it does not bind the raw set to the PollTrace's `ProjectionCommitId`.
- The read opens a `Serializable` transaction and returns `PollTraceSnapshot?`. `null` is used only for not found, so there is no typed distinction between available, previously existent but unavailable, and never existent.
- `PollTraceSnapshot` / `PollTraceDto` do not expose `HistoryEpoch` or a shared earliest available Host UTC boundary.
- A retained PollTrace whose expected raw rows have been removed is currently returned as HTTP 200 with an empty observation collection. That can make expired evidence look like a valid empty source round.
- The raw table clustered key `(PollTraceId, Ordinal)` supports an exact object seek. The object query must additionally bind `ProjectionCommitId` so a legally referential but misbound row cannot leak into the object.
- The existing scale gate captures actual SQL plans, logical reads, grants, spills, and HTTP response bytes, but `PollTrace` is not a selectable surface and no PollTrace-specific response-size failure is declared.
- `DemandRawObservations` already preserves nulls, invalid raw dates, and duplicates. The regression must assert the returned multiset rather than merely checking a non-empty array.

## Acceptance checklist

1. **PollTrace 读取按稳定 PollTraceId 定位，不扫描其它轮次或 WatchRefreshTrace。**
   - Real-SQL/V2 regression creates a target round plus an unrelated round and injects a foreign-commit row under the target PollTraceId; the response must return only the target object's exact ordinals.
2. **原始证据只能按明确 PollTrace、ProjectionCommit、Series/Demand 或 evidence 身份有界展开。**
   - The same regression asserts every returned raw row carries the target ProjectionCommit and excludes the injected cross-commit row. Existing ErrorSearch raw-evidence tests remain the evidence-ID boundary canary; later phases must extend scale coverage for every supported bounded object kind.
3. **保留期内返回原始多重集合，不任选、补值、截断或用当前投影替换历史证据。**
   - The target round contains duplicate invalid rows plus an unassigned all-null identity row. Exact duplicate count, nulls, invalid raw date, ordinals, and original commit are asserted through V2.
4. **读取内部绑定 HistoryEpoch 与 ProjectionCommit，并能区分当前存在、曾存在但不可用和从未存在。**
   - Successful response asserts database HistoryEpoch and target ProjectionCommit. A retained PollTrace with deleted raw rows must return 410 `MES_INGEST_HISTORY_EXPIRED`; an unknown ID must remain 404 `POLL_TRACE_NOT_FOUND`.
5. **所有历史读取共享一个可查询的 earliest available Host UTC 边界来源。**
   - Available, expired, and never-existing PollTrace responses must publish the same `earliestAvailableHostUtc`, derived from PollTrace `CompletedAt` in Host UTC.
6. **复用 Ticket 10 的 historical read context、两个固定小样本和执行计划入口，不新建原始证据专用分页/身份框架。**
   - Reuse the established `ReadCommitted` historical transaction, `HistoryEpoch`, exact `ProjectionCommit` fence, and existing actual-plan runner. Do not add a raw paging token, cursor, or snapshot codec.
7. **真实 SQL Server 证明 PollTrace 与原始证据只按稳定对象键 seek，逻辑读、内存授予和响应大小具有与总历史规模无关的明确上限。**
   - Compare fixed 600-row and 240,600-row samples, capturing actual plans/runtime IO/grants/spills/response bytes and failing closed on the configured bounds.
8. **正常实现只运行聚焦 PollTrace/raw evidence/契约测试和一次最终真实 SQL Server Tier 1，验证部分目标在 30 分钟内完成并保持 Failed: 0、Skipped: 0。**
   - Focused runs cover the object and contract seams; the sole final successful Tier 1 attestation must report zero failures and skips.
9. **只有实际计划扫描无关轮次、对象响应失去上限或 earliest available 身份不一致时，才升级更大样本。**
   - Do not materialize 7/30 days unless either fixed sample raises one of those signals.

## Test conventions

- SDK: .NET 8; test platform: VSTest; framework: xUnit v2.
- SQL tests are serialized through `[Collection("Ticket01SqlServer")]` and use the shared disposable `Ticket01SqlServerDatabase` fixture.
- Production HTTP is hosted with `WebApplicationFactory<Program>` in Production and continuous polling disabled.
- Assertions use exact status, error code, identity, ordinals, field values, and multiset cardinality; no weak non-null-only assertions are used.
