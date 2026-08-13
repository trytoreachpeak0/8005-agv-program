# Ticket 05 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/05-restart-barrier-gone-and-prearchive-reappearance.md`.
- Confirmed production seam: scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> versioned HTTP API.
- Production modules: `MesIngest.Core/SeriesProjection`, `MesIngest.Infrastructure/SqlServer`, the V2 Host composition root, and the formal V2 read DTOs.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- Tickets 01-04 are complete and supply the durable PollTrace/ProjectionCommit ledger, exact replay/conflict isolation, live fields, durable error periods, raw observation multisets, and the real SQL/API fixture.
- Twelve-hour archive, post-archive visibility, per-WorkType TaskTypeProtection, catalogs, frozen/paged Series reads, Watch UI, and final OpenAPI freezing are later tickets and out of scope.

## Existing behavior and gaps

- `RoundIngestor` exposes only `MesTaskUnionRound + CancellationToken`; `MesTaskUnionRound` has no caller-provided absence-authority or restart input. Preserve that deep seam.
- `SqlServerMesIngestProjection.CommitRoundAsync` rejects replay conflicts before any mutation and records FAILURE/INCOMPLETE without ProjectionCommit. Restart phase advancement must remain after those gates and inside the SUCCESS transaction.
- SUCCESS currently projects only keys present in the round. There is no authoritative-absence sweep, `GoneConfirmedAt`, Host session, restart phase, or authority event storage.
- Existing schema already reserves `Generation` and `PredecessorDemandId`, but observation advancement rejects any non-VISIBLE current Demand.
- The current Series API exposes only `CurrentDemand`; Ticket 05 needs durable read-back of both predecessor and current generations. A `Demands` collection ordered by generation is the smallest formal API addition; Ticket 08 remains responsible for frozen list/paging semantics.
- Existing error periods close only as `CONDITION_CLEARED`. Authoritative GONE must close every current Demand-scoped condition as `DEMAND_GONE`, with evidence and Series events bound to the absence PollTrace/ProjectionCommit.
- External readability currently depends only on current conditions. GONE must independently publish `NOT_READABLE` + `DEMAND_GONE` even after its data-error conditions close.
- Host restart must be internal. A process-stable HostSession identity is created by the SQL projection; a V2 startup hosted service initializes it before requests. The commit path calls the same idempotent initialization as a defensive fallback.
- Every Host session, including the initial empty-database session, starts in `BARRIER` and records `RESTART_BARRIER_ENTERED` as a startup fact. SUCCESS #1 records `RESTART_BASELINE_COMPLETED` and moves to `POST_BARRIER`; SUCCESS #2 records `RESTART_ABSENCE_AUTHORITY_RESTORED` and moves to `NORMAL`; only rounds that begin in `NORMAL` have restart absence authority.
- Authority state/events remain queryable by HostSessionId after a later Host takes over. The current-state endpoint remains the convenience read.
- A Demand persists `LatestObservationProjectionCommitId` so equal round timestamps cannot make PollTrace lexical order select stale raw multiplicity. Positive observations advance it; authoritative GONE preserves it.
- `find-untested-sources` is unavailable; deterministic pairing is bounded to the files below.

## Target inventory

| Target | Role |
| --- | --- |
| `MesIngest.Core/SeriesProjection/ProjectionModels.cs` | expose HostSession/authority evidence, GoneConfirmedAt, and all Demand generations |
| `MesIngest.Core/SeriesProjection/RestartBarrier.cs` | centralize restart phase transitions and stable event codes |
| `MesIngest.Core/SeriesProjection/IMesIngestProjection.cs` | internal startup initialization/read seam without authority input |
| `MesIngest.Core/SeriesProjection/NewMesIngestContract.cs` | bump exact empty-database contract identity |
| `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestSchema.cs` | persist host sessions, authority events, GoneConfirmedAt, and exact schema validation |
| `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestProjection.cs` | compute restart authority, sweep authoritative absences, close conditions as GONE, create reappearance generations |
| `MesIngest.Host/Program.cs` | initialize the V2 Host session on startup |
| `MesIngest.Host/NewMesIngestEndpoints.cs` | publish authority state/events and generation history |
| `MesIngest.Tests/RestartBarrierGoneAndPrearchiveReappearanceTests.cs` | real SQL/Production Host/API tracer bullets |
| `Invoke-Ticket05SqlServerGate.ps1` | repeatable zero-skip real-SQL acceptance gate |

## Environment and commands

- SDK: .NET SDK 10.0.302; no MTP signals; VSTest + xUnit v2 syntax is required.
- Real SQL Server gate: `MES_INGEST_TICKET01_SQLSERVER`, `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR=16`, and `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL=160`; LocalDB is rejected.
- Narrow test: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~RestartBarrierGoneAndPrearchiveReappearanceTests"`.
- Prerequisite regression: Ticket 01-04 test classes plus Ticket 05.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Final suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.

## Acceptance checklist (verbatim)

1. `持久化一条 VISIBLE Demand 后重启 Host，系统自动进入 RestartBarrier；调用方没有能够绕过保护或直接指定缺席权威的输入。`
2. `重启后的第一轮完整 SUCCESS 只建立基线，第二轮只结束保护，前两轮即使缺少原业务键也不推进 GONE；第三轮完整 SUCCESS 仍缺少该键时才拥有缺席权威并确认 GONE。`
3. `RestartBarrier 的进入、基线完成和权威恢复都有可查询的稳定事件与轮次证据；FAILURE、INCOMPLETE 和内容冲突不会推进保护阶段或获得缺席权威。`
4. `不处于保护状态时，首个具有缺席权威的完整 SUCCESS 未包含当前业务键，便把其 VISIBLE Demand 转为 GONE；DemandLastSeenAt 保持最后真实看见时间，GoneConfirmedAt 单独记录确认缺席的 Host UTC 时间。`
5. `保护期间仍可创建新 VISIBLE Demand、更新已观测 Demand 的实时字段并保留正常事件，只禁止由缺席推进 GONE 或归档。`
6. `Series 尚未归档时，同键在后续完整 SUCCESS 中重现会保留 SeriesId，创建更高世代和新 DemandId，并以 predecessor 关系连接永久保留的上一代；旧代不被静默复活或改写。`
7. `真实 SQL Server → 正式 API 的持久化重启验收依次证明第一、第二、第三轮边界、直接权威缺席、归档前重现和前后世代关系，且 API 展示的生命周期事件均绑定对应 PollTrace/ProjectionCommit。`
