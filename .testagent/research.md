# Ticket 03 test-generation research

## Bounded scope

- Ticket: `.scratch/new-mes-ingest/issues/03-live-fields-validation-and-error-periods.md`.
- Confirmed production seam: scripted `MesTaskUnionRound` -> production `RoundIngestor`/Host -> real SQL Server -> versioned HTTP API.
- Production modules: `MesIngest.Core/SeriesProjection`, `MesIngest.Infrastructure/SqlServer`, and the V2 Host composition/read contract.
- Test project: `MesIngest.Tests` (`net8.0-windows`, xUnit 2.4.2, VSTest).
- Tickets 01 and 02 are complete at commits `da0cc4a` and `0c17773`; they provide the stable round, idempotency, unsuccessful isolation, persistence and HTTP seam.
- WPF/Watch UI, duplicate and multi-WorkType observations (ticket 04), GONE/archive/reappearance (tickets 05-06), catalog/audit/search APIs (tickets 09-12), and final OpenAPI freezing (ticket 17) are out of scope.

## Existing behavior and gaps

- A first unique SUCCESS stores all five live MES fields and produces `DEMAND_SERIES_STARTED` plus `TRANSPORT_DEMAND_CREATED`; an identical later SUCCESS advances last-seen/commit without a business event.
- Any later AREA/EQP/STEP/DATES/PACKAGE change currently throws a ticket-03 `NotSupportedException`; live values cannot yet change.
- The isolated new schema has no current-condition, error-period or error-evidence persistence. The series DTO has no current conditions, permanent error history or readability conclusion.
- Five fields are required: AREA, EQP, STEP, DATES and PACKAGE. String null/empty/whitespace remains exact raw/live evidence but is missing. Nonblank AREA must match `^[A-Z][1-9][0-9]?-[1-9][0-9]?$`; invalid source values are never normalized.
- Field error identity is `SeriesId + SeriesErrorCode + Target + SubjectKind`, with demand target `DEMAND:<DemandId>` and the field name as subject. Evidence changes extend one period; exact repeats add no noise; explicit later SUCCESS closes it with `CONDITION_CLEARED`.
- The first complete SUCCESS against an empty new database opens already-present errors at Host UTC using `BOOTSTRAPPED_CURRENT_CONDITION`; FAILURE/INCOMPLETE neither consume this bootstrap nor alter conditions.
- The contract-owned v1 catalog publishes five stable codes across four stable categories; ticket 03 produces only missing/invalid-field errors but publishes the complete catalog for later tickets.

## Environment and commands

- SDK: .NET SDK 10.0.302; no MTP runner configuration; tests use VSTest syntax.
- Narrow integration command: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~LiveMesFieldsAndErrorPeriodsTests"`.
- Focused rule command: filter `FullyQualifiedName~MesFieldValidationAndSeriesErrorCatalogTests`.
- Prerequisite regression: filter `FullyQualifiedName~NewSuccessRoundTracerSpineTests|FullyQualifiedName~RoundEvidenceIdempotencyTests|FullyQualifiedName~MesTaskUnionRoundDigestTests`.
- Final build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
- Final suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-build`.
- Formal SQL gate uses explicit process-only `MES_INGEST_TICKET01_SQLSERVER` plus expected product major/compatibility. It rejects LocalDB and creates only GUID-suffixed owned databases.
- Available approved local server: SQL Server `16.0.1190.2`, product major `16`, compatibility `160`.

## Existing conventions

- `WebApplicationFactory<Program>` starts the production composition; tests resolve the production round ingestor and observe state exclusively through `/api/v2` reads.
- JSON assertions use camel-case properties, exact stable contract codes, string outcomes, and UTC `DateTimeOffset` values.
- Each SQL test owns and removes one validated temporary database; tests never wipe or reuse a populated database.

## Acceptance checklist (verbatim)

1. `对同一唯一原始观测连续提交成功轮次时，AREA、EQP、STEP、DATES 和 PACKAGE 的有意义变化更新同一 Demand 世代的 LiveMesFieldSet，不创建新的 Series 或 Demand；MesSourceDate 保持源字段语义，不被当作 Host 观测时间或生命周期时间。`
2. `每次真实字段变化都产生含 before/after、PollTrace、Host UTC 时间和 ProjectionCommit 身份的事件；相同观测不追加噪声事件，SeriesSequence 始终严格单调。`
3. `必填字段变为 NULL 或空白时保存真实空值并形成 REQUIRED_MES_FIELD_MISSING；AREA 只有符合领域格式的值才有效，非法值形成 INVALID_MES_FIELD_FORMAT，任何场景都不得用历史值或客户端正规化掩盖错误。`
4. `字段异常不会阻止 Series、Demand、全部原始观测和 WatchDemandProjection 生成；正式 API 同时返回当前真实值、当前条件、稳定错误码/主分类和不可读结论，使坏数据保持可见但不能被误当作安全外读事实。`
5. `同一错误身份持续存在且证据值变化时只扩充同一错误期间的证据，不按轮询创建新期间；后续完整 SUCCESS 给出明确反证时以 CONDITION_CLEARED 结束该期间，并保留全部历史。`
6. `空库首轮已存在的字段错误以 BOOTSTRAPPED_CURRENT_CONDITION 建立最早可证明起点，不回扫或伪造旧系统中的开始时间；错误目录中的已发布代码、分类、作用域和含义在契约中稳定。`
7. `真实 SQL Server → 正式 API 的验收覆盖有效值、实时变化、必填字段缺失与恢复、非法 AREA 与恢复、无变化轮次及 Host 重启，证明当前投影和错误历史在同一提交中持久一致。`
