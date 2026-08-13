# Ticket 07 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/07-work-type-task-type-protection.md`.
- Confirmed production seam: scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> versioned HTTP API.
- Production modules: `MesIngest.Core/SeriesProjection`, `MesIngest.Infrastructure/SqlServer`, V2 Host composition, and the formal V2 read DTOs.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- Tickets 02 and 05 are done. Ticket 06 implementation is present and supplies the archive path that Ticket 07 must suppress per WorkType.
- Ticket 13 will compose the unified `CurrentIngestAttention` endpoint and Ticket 14 will compose `WatchOverviewSnapshot`. Ticket 07 must publish an attention-ready protection projection and immutable events through a focused V2 resource; it must not invert those dependencies by implementing the later aggregate APIs.
- No WPF/UI files are in scope, so the golden-renderer workflow does not apply.

## Inherited and resolved domain semantics

- Entry inherits the approved configurable `ZeroDropEnterThreshold` rule (default 10): when the most recent accepted non-zero count is at least the threshold and the next accepted complete SUCCESS count is zero, that WorkType enters `PAUSED_ZERO_DROP` in that round.
- A healthy count is the number of distinct recognizable `TransportDemandKey` values for the exact WorkType in the accepted round. Duplicate raw rows for one key count once; identifiable rows with non-key data errors still count; missing SUBLOT or WorkType does not count; V2 has no go-live date filter.
- Every accepted non-zero count replaces `LastHealthyNonZeroCount`, including recovery rounds; zero never overwrites it.
- Recovery requires exactly two consecutive accepted non-zero SUCCESS rounds. The first records 1/2 progress; the second records 2/2 and clears protection but remains `AUTHORITY_PENDING`. The following accepted SUCCESS restores type authority. A zero while recovering resets progress to zero and remains protected.
- Effective absence authority is the intersection of RestartBarrier authority and the per-WorkType protection decision. Callers still cannot supply authority.
- Current attention remains true through `PAUSED_ZERO_DROP`, `RECOVERING`, and `AUTHORITY_PENDING`; it becomes false only after the authority-restored event. Historical events remain queryable.
- Stable WorkType-scoped facts are separate from `DemandSeriesEvent`: entered, each recovery-progress step, cleared, and type absence-authority restored. Each event binds PollTrace, ProjectionCommit, Host UTC time, episode identity, stable WorkType sequence, thresholds, counts, and phases.

## Existing behavior and gaps

- `SqlServerMesIngestProjection.CommitRoundAsync` already rejects replay conflicts and isolates FAILURE/INCOMPLETE before any SUCCESS projection mutation. Ticket 07 state advancement must remain after those gates and in the same SERIALIZABLE transaction.
- `ProjectionCommit.AbsenceAuthority` currently records the global RestartBarrier decision and should retain that meaning. Per-type decisions need separate round evidence.
- GONE and twelve-hour archive sweeps currently accept one global boolean. Both must load candidate WorkType and apply the per-type authority decision.
- The V2 schema/API currently has no protection state, protection events, or focused protection endpoint.
- Legacy `TransportDemandReconciler` is only a semantic reference. Its old tables, DTOs, and `IngestAlert` incident lifecycle are forbidden by ADR-mes-0017.
- `find-untested-sources` is unavailable; deterministic pairing is bounded to the files below.

## Target inventory

| Target | Role |
| --- | --- |
| `MesIngest.Core/SeriesProjection/TaskTypeProtection.cs` | pure transition policy, phases, and stable event codes |
| `MesIngest.Core/SeriesProjection/ProjectionModels.cs` | protection state/event and per-round decision snapshots |
| `MesIngest.Core/SeriesProjection/IMesIngestProjection.cs` | focused read seam |
| `MesIngest.Core/SeriesProjection/NewMesIngestContract.cs` | exact empty-database contract/schema bump |
| `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestSchema.cs` | persistent protection state/events and exact schema validation |
| `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestProjection.cs` | count/transition state, effective authority, per-type GONE/archive, reads |
| `MesIngest.Host/Program.cs` / `MesIngestHostOptions.cs` | inject configurable entry threshold into V2 projection |
| `MesIngest.Host/NewMesIngestEndpoints.cs` | formal focused protection resource and round evidence DTOs |
| `MesIngest.Tests/TaskTypeProtectionTests.cs` | real SQL/Production Host/API tracer bullets |
| `Invoke-Ticket07SqlServerGate.ps1` | repeatable zero-skip real-SQL acceptance gate |

## Environment and commands

- SDK: .NET SDK 10.0.302; no MTP signals; VSTest + xUnit v2 syntax is required.
- Real SQL Server gate: `MES_INGEST_TICKET01_SQLSERVER`, `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR=16`, and `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL=160`; LocalDB is rejected.
- Narrow test: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~TaskTypeProtectionTests"`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Final core suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.

## Acceptance checklist (verbatim)

1. `每个 WorkType 独立维护健康非零基线；某类型从健康非零结果骤降为零时进入 TaskTypeProtection/PausedZeroDrop，该轮及保护期间的成功空轮不能把该类型 Demand 标为 GONE 或推进归档。`
2. `一个 WorkType 受保护时，其它 WorkType 仍按各自观测和缺席权威正常创建、更新或标记 GONE；保护状态、计数和恢复进度不得跨类型串扰。`
3. `受保护类型连续两轮获得健康非零结果后才解除保护；第二轮只完成解除，下一轮完整结果才恢复该类型的缺席权威，不能在解除同轮自相矛盾地确认 GONE。`
4. `FAILURE、INCOMPLETE、幂等重放和内容冲突不建立健康基线、不推进连续恢复计数，也不解除保护；RestartBarrier 与类型保护同时存在时，只有两者都允许的轮次才具有缺席权威。`
5. `保护进入、每步恢复进度、解除和权威恢复都产生稳定事件，并作为当前 CurrentIngestAttention 与轮次证据由正式 API 查询；结束后不保留为当前项，但历史事实仍可追溯。`
6. `保护状态和恢复进度在 Host 重启后保持，不能因进程重启提前获得缺席权威或丢失保护证据。`
7. `真实 SQL Server → 正式 API 验收同时驱动至少两个 WorkType，证明目标类型进入保护、保护空轮不 GONE、其它类型继续对账、两轮非零恢复以及随后权威空轮才 GONE。`
