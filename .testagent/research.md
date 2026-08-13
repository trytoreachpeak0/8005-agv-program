# Ticket 04 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/04-duplicate-key-and-multiple-work-types.md`.
- Confirmed production seam: scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> versioned HTTP API.
- Production modules: `MesIngest.Core/SeriesProjection`, `MesIngest.Infrastructure/SqlServer`, and the V2 Host read contract.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- Tickets 01-03 are complete at `da0cc4a`, `0c17773`, and `913dc77`; Ticket 03 supplies durable error periods, current conditions, readability, and API evidence.
- GONE/archive/reappearance, TaskTypeProtection, catalog/audit/search APIs, Watch UI, and final OpenAPI freezing are later tickets and out of scope.

## Existing behavior and gaps

- `PrepareRound` preserves every assignable observation, but `EnsureSupportedNewRound` rejects any repeated `TransportDemandKey` before the SUCCESS transaction is accepted.
- The commit path currently projects one row at a time. It must instead group a SUCCESS round by exact `SUBLOT + WorkType`, create or advance one Series/Demand per group, and attach every group row to that identity.
- `DemandRawObservations` already preserves multiplicity, source values, PollTrace, ProjectionCommit, SeriesId, and DemandId. The Series and PollTrace APIs already expose those rows.
- Ticket 03's durable condition model already has the required stable identity (`SeriesId + code + target + subject`), permanent periods, evidence-change semantics, and SUCCESS-only closure. Ticket 04 should deepen that model, not create another incident/seam.
- A duplicate group has no trustworthy `LiveMesFieldSet`; the API must distinguish that from one unique row whose individual live fields are null.
- Duplicate evidence must be a stable canonical representation of the normalized row multiset: input order changes nothing, while content or multiplicity changes append evidence to the same period.
- Multi-WorkType evidence must be the complete ordinally sorted WorkType set for a SUBLOT. Every currently observed key gets its own Series/Demand and Demand-scoped condition.
- When a WorkType is absent from a later round, the absence is not yet authoritative in Ticket 04. Only an observed key whose complete SUCCESS membership set is now unique has explicit `CONDITION_CLEARED` counterevidence. Absent related Demands retain their current conflict/readability blocker until Ticket 05 can establish absence authority, transition them to `GONE`, and close with `DEMAND_GONE`; otherwise the current scaffold would expose stale `VISIBLE` Demands as readable.
- `find-untested-sources` is not installed in this environment; deterministic source/test pairing was therefore bounded manually to the files listed below.

## Target inventory

| Target | Role |
| --- | --- |
| `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestProjection.cs` | group observations, project conflicts, preserve identities, synchronize durable conditions |
| `MesIngest.Core/SeriesProjection/ProjectionModels.cs` | express absence of a trustworthy live field set |
| `MesIngest.Host/NewMesIngestEndpoints.cs` | publish nullable live field set through the formal V2 DTO |
| `MesIngest.Tests/DuplicateKeyAndMultipleWorkTypesTests.cs` | four real-SQL/HTTP tracer bullets, composition coverage, and restart proof |

No schema shape change is required: current error evidence is lossless `nvarchar(max)`, and current-round multiplicity can be derived from rows linked to the Demand's latest observation commit.

## Environment and commands

- SDK: .NET SDK 10.0.302; no MTP signals; VSTest syntax is required.
- Real SQL Server: default local instance, ProductVersion `16.0.1190.2`, EngineEdition `3`, `CREATE ANY DATABASE = 1`, created-database compatibility `160`; LocalDB is rejected by the fixture.
- Process-only gate variables: `MES_INGEST_TICKET01_SQLSERVER`, `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR=16`, `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL=160`.
- Narrow test: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~DuplicateKeyAndMultipleWorkTypesTests"`.
- Prerequisite regression: filter `FullyQualifiedName~LiveMesFieldsAndErrorPeriodsTests|FullyQualifiedName~RoundEvidenceIdempotencyTests|FullyQualifiedName~NewSuccessRoundTracerSpineTests`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Final suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.

## Acceptance checklist (verbatim)

1. `一个成功轮次中同一 SUBLOT + WorkType 出现两条或更多原始行时，只保留一个 Series 和一个当前 Demand 世代，完整保存规范化后的所有行，不选主行、不拼接字段，也不生成虚假的 LiveMesFieldSet。`
2. `重复行形成 DUPLICATE_TRANSPORT_DEMAND_KEY 当前错误和不可读结论；正式 API 能从受影响 Demand 追到全部观测、错误期间、证据值、PollTrace 和 ProjectionCommit。`
3. `将相同重复行从 A/B 调换为 B/A 不产生新的业务变化或新错误期间；行内容或数量真正变化时在原期间追加证据，而不是改变冲突身份。`
4. `重复观测恢复为唯一行时，继续使用原 SeriesId、DemandId 和世代，恢复实时字段，并由完整 SUCCESS 明确结束错误期间，不以恢复为由制造新 Demand。`
5. `同一 SUBLOT 在同轮出现多个 WorkType 时，每个 SUBLOT + WorkType 分别形成独立 Series/Demand，同时所有受影响当前 Demand 都形成 SUBLOT_MULTIPLE_WORK_TYPES 冲突及完整 WorkType 集合证据。`
6. `多 WorkType 冲突恢复后，各 Series 不合并、不换键；仍可见的相关 Demand 结束当前冲突，历史错误期间和逐世代证据永久保留。`
7. `真实 SQL Server → 正式 API 验收覆盖重复行、换序、证据变化、恢复唯一、同 SUBLOT 多 WorkType 及恢复，并证明标识、错误期间和原始多重集合在 Host 重启后保持一致。`
