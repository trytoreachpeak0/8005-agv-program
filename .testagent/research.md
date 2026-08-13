# Ticket 10 test-generation research

## Scope and confirmed seam

Ticket: `.scratch/new-mes-ingest/issues/10-readability-audit-snapshot-query-detail.md`.

The parent specification already confirms the public acceptance seam:

- scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> formal versioned HTTP API;
- pure domain tests are limited to the stable blocker catalog/priority and signed-token binding that are expensive to exhaust through SQL.

This ticket does not change `MesIngest.Watch`, XAML, Wpf.Ui, UI Automation, DPI, or visual baselines, so the Fluent/golden-renderer workflow is not in scope.

## Existing architecture and bounded gaps

- C#/.NET 8, xUnit v2 on VSTest, ASP.NET Core minimal APIs, and a strict empty-database SQL Server contract.
- Ticket 08 already persists a monotonic `ProjectionSequence` plus a restart-stable 32-byte HMAC key and reconstructs DemandSeries reads as of a retained commit.
- Ticket 09 already records the committed `CatalogRevision` on every `ProjectionCommit`, including commits that do not change the catalog. This is the required correlation value, but it cannot identify an audit snapshot.
- Existing DemandSeries reads expose blockers only for the current Demand and return one row per Series. Ticket 10 needs one row per generated Demand generation, its own exact facets/order/filter semantics, and complete detail evidence.
- The first-version blocker vocabulary already exists implicitly across lifecycle constants and `SeriesErrorCatalog`; it needs one explicit immutable `ReadabilityBlockerCatalog` with stable priorities and checks.
- No new business table is required. The audit can rebuild latest observation, lifecycle events, active-as-of error periods, PollTrace provenance, and catalog revision from retained committed facts in one serializable read transaction.

## Target inventory

| Target | Role |
| --- | --- |
| `MesIngest.Core/SeriesProjection/ReadabilityAuditContract.cs` | blocker catalog, filter/query/result/detail/error contract |
| `MesIngest.Core/SeriesProjection/ReadabilityAuditTokenCodec.cs` | tamper-evident snapshot and cursor binding |
| `IMesIngestProjection.cs`, `NewMesIngestContract.cs` | public read seam and tracer/schema 10 identity |
| `SqlServerMesIngestProjection.ReadabilityAudit.cs` | as-of Demand-generation states, filters/facets/order/page/detail |
| `NewMesIngestEndpoints.cs` | list/detail HTTP resources, parsing, validation, structured status mapping |
| `ReadabilityAuditTests.cs` | domain token tests and real-SQL production Host/API tracer bullets |
| `Invoke-Ticket10SqlServerGate.ps1` | repeatable zero-skip real SQL Server acceptance gate |

## Platform and commands

- SDK 10.0.302; no MTP signal in `global.json`, project, `Directory.Build.props`, or `Directory.Packages.props`.
- Test platform: VSTest. Framework: xUnit v2.
- Existing `MesIngest.Tests.csproj` already references Core and Host; no new project/reference is needed.
- Focused: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~ReadabilityAuditTests"`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Full core suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.
- Formal SQL gate uses `MES_INGEST_TICKET01_SQLSERVER` with explicit product-major and compatibility assertions; LocalDB is rejected.

## Acceptance checklist (verbatim)

1. `审计可观察到每个已生成 Demand 世代，包括 VISIBLE、GONE、所属 Series 已归档及 LongGoneButVisible；每项独立给出 READABLE 或 NOT_READABLE，不会把资格状态等同于生命周期状态。`
2. `第一版稳定阻断目录覆盖 DEMAND_GONE、SERIES_ARCHIVED、LONG_GONE_BUT_VISIBLE、DUPLICATE_TRANSPORT_DEMAND_KEY、SUBLOT_MULTIPLE_WORK_TYPES、REQUIRED_MES_FIELD_MISSING 与 INVALID_MES_FIELD_FORMAT；一个 Demand 的全部命中原因均可见，列表主要原因由 Host 的稳定优先级选择。`
3. `列表支持资格、WorkType、阻断原因、DemandId 和 SUBLOT 条件；不同维度取交集、同维度多值取并集，默认同时包含可读与不可读，标识匹配规则与领域契约一致。`
4. `当前 AreaFilterProfile 的合法 MesArea 集合由 Host 在计数和分页前精确应用；不可信当前 AREA 不借历史值命中配置，只在“全部 AREA”范围内出现，AREA 条件不改变资格或 CatalogRevision。`
5. `列表默认先显示不可读项，再按主要原因优先级、DemandLastSeenAt 降序和 DemandId 升序稳定排列；默认每页 100、最多 200，并返回当前完整筛选下的精确 Demand 总数。`
6. `资格与原因分面按去重 Demand 精确计算且排除自身维度；同一 Demand 可计入多个原因分面，但原因数量之和不会被报告为不可读总数。`
7. `首次查询冻结独立的 ReadabilityAuditSnapshot，列表、分面、精确总数、后续页和详情共享其 ProjectionCommit 身份并携带当时的 CatalogRevision；并发产生的新提交只在显式刷新后的新快照出现。`
8. `详情从同一审计快照返回全部资格检查、完整阻断集合、可信字段或原始观测冲突、所属 Series、PollTrace、ProjectionCommit 与 CatalogRevision；主要原因不能替代完整推导。`
9. `游标绑定审计快照、规范化筛选、AREA 值集合、固定顺序与契约版本；无效、过期、篡改或跨条件复用均明确失败，不静默返回第一页或另一快照的数据。`
