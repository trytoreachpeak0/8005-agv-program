# Ticket 02 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/02-round-evidence-idempotency-and-unsuccessful-isolation.md`.
- Confirmed production seam: scripted `MesTaskUnionRound` -> production Host/domain entry -> real SQL Server -> versioned HTTP API.
- Production modules: `MesIngest.Core/SeriesProjection`, `MesIngest.Infrastructure/SqlServer`, and the V2 Host composition/read contract.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- Ticket 01 commit `da0cc4a` is the tracer-spine prerequisite; fixed implementation/review point for this work is checkpoint commit `acfaadd`.
- Watch/UI, Oracle execution/mapping (ticket 15), field-error periods (ticket 03), duplicate-key projection (ticket 04), and lifecycle/absence authority (tickets 05-07) are out of scope.

## Existing behavior and gaps

- `MesTaskUnionRoundDigest` already sorts length-framed row representations and preserves multiplicity, but source dates must be normalized to UTC so the same instant with another offset has the same canonical evidence.
- The production interface and `SuccessRoundIngestor` accept only SUCCESS. The SQL adapter rejects every existing PollTraceId and always creates a ProjectionCommit.
- `GetPollTraceAsync` inner-joins ProjectionCommit, so FAILURE and INCOMPLETE evidence cannot currently be read.
- SQL schema already permits all three outcome strings and nullable Series/Demand links on raw observations; the implementation rejects unassigned rows before the transaction.
- The idempotency identity must include `Outcome + QueryVersion + RowCount + ContentDigest`. Accepted timestamps are evidence returned from the first attempt, not mutable replay input.
- FAILURE/INCOMPLETE carry no trusted business observations: they persist count/digest evidence but no ProjectionCommit or business/raw-observation rows.

## Environment and commands

- SDK: .NET SDK 10.0.302; no MTP runner configuration; tests use VSTest syntax.
- Narrow command: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~RoundEvidenceIdempotencyTests"`.
- Prerequisite regression: filter `FullyQualifiedName~NewSuccessRoundTracerSpineTests`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Final suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.
- Formal SQL gate uses explicit opt-in `MES_INGEST_TICKET01_SQLSERVER` plus expected product major/compatibility. It rejects LocalDB and creates only GUID-suffixed `MesIngest_Ticket01_` databases.
- Baseline on SQL Server `16.0.1190.2`, product major `16`, compatibility `160`: ticket 01 tests `3 passed / 0 skipped`.

## Existing conventions

- `WebApplicationFactory<Program>` starts the production composition; tests resolve the production round ingestor and observe state exclusively through `/api/v2` reads.
- JSON assertions use camel-case properties, exact stable contract codes, string outcomes, and UTC `DateTimeOffset` values.
- Each SQL test owns and removes one validated temporary database; tests never wipe or reuse a populated database.

## Acceptance checklist (verbatim)

1. `SUCCESS、FAILURE 和 INCOMPLETE 都留下可查询的 PollTraceId、查询版本、结果类型、Host UTC 时间、行数和规范化内容摘要；原始行按稳定规范化多重集合计算，返回顺序变化不会改变摘要，重复行数量变化会改变摘要。`
2. `使用相同 PollTraceId 和相同规范化内容重放时，正式 API 返回同一已接受结果，且不会重复创建 PollTrace、ProjectionCommit、Series、Demand 或事件。`
3. `使用相同 PollTraceId 绑定不同内容时，整轮以明确、版本化的契约冲突失败；真实 SQL Server 中的轮次账本和全部业务投影均无部分写入。`
4. `FAILURE 和 INCOMPLETE 只追加各自的可追溯轮次证据，不创建、更新、标记 GONE 或归档任何 Series/Demand，也不改变上一成功 ProjectionCommit 的正式 API 读取结果。`
5. `缺列、列类型或结果结构不满足契约时归为 INCOMPLETE；结构完整但字段值为空、非法或互相冲突的原始行仍归为 SUCCESS 数据证据，不得借 INCOMPLETE 隐藏局部坏数据。`
6. `SUCCESS 中缺少 SUBLOT 或 TASK_TYPE 的行以 UnassignedMesObservation 原样归入该轮证据且不猜测 DemandSeries；同轮其它可识别业务键仍正常投影。`
7. `通过真实 SQL Server 和正式 API 连续验证成功、同内容重放、内容冲突、FAILURE、INCOMPLETE 及 Host 重启，证明业务投影隔离、轮次证据和幂等结论在持久化后保持一致。`
