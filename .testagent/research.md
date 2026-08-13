# Ticket 09 test-generation research

## Scope and confirmed seams

Ticket: `.scratch/new-mes-ingest/issues/09-externally-readable-demand-catalog-reference-consumer.md`.

Confirmed public seams from the parent specification:

- scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> formal versioned HTTP catalog;
- persisted catalog projection read, including a conditional read at one committed revision;
- isolated reference-consumer API at cache refresh, execution commitment, consumer-owned durable intent, and remote-order idempotency boundaries.

No WPF/UI file is in scope; Fluent/golden-renderer rules do not apply. `find-untested-sources`
is unavailable, so source/test pairing is bounded to this ticket's seams.

## Existing architecture and gaps

- V2 uses C#/.NET 8, xUnit v2 on VSTest, ASP.NET Core minimal APIs, and a strict empty-database SQL Server schema.
- `SqlServerMesIngestProjection.CommitRoundAsync` already applies a whole SUCCESS under one
  SERIALIZABLE transaction. FAILURE/INCOMPLETE and idempotent replays do not mutate projection state.
- Current DemandSeries reads derive readability blockers, but there is no persisted catalog,
  `CatalogRevision`, or `DemandRevision`. `ProjectionSequence` and `LatestProjectionCommitId` advance
  on unchanged SUCCESS rounds and therefore cannot substitute for either domain revision.
- `DemandLastSeenAt` also advances on unchanged observations, so it cannot be a catalog-visible member
  value unless every poll creates revision noise. Catalog time fields must be stable/value-semantic:
  Demand `CreatedAt`, current `MesSourceDate`, and the commit/value evidence that produced the member.
- A catalog read must be one full-range resource, sorted by DemandId. It rejects query parameters;
  Minimal APIs otherwise silently ignore unknown parameters.
- The reference consumer belongs in a separate class library. Its cache is disposable. Durable state
  begins only at `AcceptedDemandSnapshot` + `OrderIntent`; it never writes cancellation/dispatch state
  to MesIngest.

## Target inventory

| Target | Role |
| --- | --- |
| `MesIngest.Core/SeriesProjection/ExternallyReadableDemandCatalog.cs` | central eligibility/value contract and catalog read models |
| `ProjectionModels.cs`, `IMesIngestProjection.cs`, `NewMesIngestContract.cs` | Demand revision, persisted read seam, contract/schema v9 |
| `SqlServerMesIngestSchema.cs` | singleton catalog state, current member rows, commit-to-revision evidence |
| `SqlServerMesIngestProjection.cs` / new partial | reconcile catalog once at the end of each SUCCESS and conditional atomic reads |
| `NewMesIngestEndpoints.cs` | full catalog GET, ETag/If-None-Match, 304, query rejection |
| `MesIngest.ReferenceConsumer` | disposable cache, final reread, immutable acceptance and idempotent intent workflow |
| `ExternallyReadableDemandCatalogTests.cs` | real-SQL production Host/API tracer bullets |
| `ReferenceConsumerTests.cs` | consumer boundary behavior and HTTP mapping |
| `Invoke-Ticket09SqlServerGate.ps1` | repeatable zero-skip SQL Server acceptance gate |

## Platform and commands

- SDK 10.0.302; project has no MTP signal. Test platform is VSTest, framework xUnit v2.
- Focused test: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~ExternallyReadableDemandCatalogTests|FullyQualifiedName~ReferenceConsumerTests"`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Full tests: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.
- Real SQL gate uses `MES_INGEST_TICKET01_SQLSERVER`, explicit product major, and compatibility level;
  LocalDB is rejected.

## Acceptance checklist (verbatim)

1. `经正式 Host 和持久化投影读取时，目录只包含同时满足 VISIBLE、唯一原始观测、全部必填字段有效、无当前数据异常且所属 Series 未归档的 Demand；不合格 Demand 仍可从 Watch 运维投影追查。`
2. `目录项可观察到稳定的 DemandId、SeriesId、TransportDemandKey、世代、DemandRevision、时间与当前可信 MES 字段，并按 DemandId 稳定输出；目录拒绝 WorkType、AREA、车辆、地图或站点等 Dispatch 范围参数。`
3. `首次读取返回完整目录及 CatalogRevision；成员进入、退出或成员业务值变化才使修订递增，无变化轮次不递增，同一轮多个成员变化也只递增一次。`
4. `以已有修订进行条件读取时，未变化目录返回 304 Not Modified 且不传输正文；变化后返回同一已提交修订对应的完整正文，不出现新修订配旧成员或旧字段。`
5. `reference consumer 清空缓存或重启后只靠完整目录即可恢复当前视图，不读取或持久化 DemandChangeFeed、Feed Sequence、bootstrap high-watermark 或同步 Cursor。`
6. `reference consumer 在执行承诺点最终重读 Demand：资格、Revision 或值已变化时可观察到明确拒绝或重新决策；接受成功时保存的 AcceptedDemandSnapshot 不会被后续目录刷新改写，OrderIntent 以稳定幂等身份处理结果未知。`
7. `端到端契约证据覆盖唯一行、字段异常与恢复、重复键、多 WorkType、归档后可见、实时字段变化和无变化轮次，并证明 MesIngest 不读取或修改消费者的取消抑制与派车状态。`
