# Ticket 11 test research — ErrorSearchAsOf list, windows, and facets

## Scope and confirmed seams

Ticket: `.scratch/new-mes-ingest/issues/11-error-search-as-of-list-window-facets.md`.

Confirmed public seams from the feature spec:

1. `IMesIngestProjection.ListErrorSearchAsync` for dense contract/token/interval rules.
2. Scripted `MesTaskUnionRound` → production `RoundIngestor`/Host → real SQL Server → `GET /api/v2/error-search` for acceptance behavior.

Tests observe only those public seams. Time is a system boundary and is controlled with the existing `AdjustableTimeProvider`. The real-SQL tests use `Ticket01SqlServerDatabase` and reject LocalDB as release evidence.

Ticket 11 does not change Watch/XAML/UI Automation/DPI/visual baselines, so the golden WPF renderer rules do not apply.

## Existing conventions

- Test project: `mes/ingest/csharp/MesIngest.Tests/MesIngest.Tests.csproj`.
- Framework/platform: xUnit 2.4.2 on VSTest (`Microsoft.NET.Test.Sdk`; no MTP signals).
- Host harness: `WebApplicationFactory<Program>` in Production with the V2 SQL projection enabled.
- SQL gate attribute: `[Ticket01SqlServerFact]` plus `[Collection("Ticket01SqlServer")]`.
- Neighboring model: `ReadabilityAuditTests.cs`, `ReadabilityAuditContract.cs`, `ReadabilityAuditTokenCodec.cs`, `SqlServerMesIngestProjection.ReadabilityAudit.cs`, and `NewMesIngestEndpoints.cs`.
- Error envelope: the existing V2 `NewMesIngestErrorDto { code, error }` contract.
- Snapshot signing key: persistent `mesingest.SchemaInfo.SnapshotTokenSigningKey`, with a distinct token purpose per read model.
- V2 endpoints remain excluded from the legacy v1 OpenAPI until ticket 17.

## Bounded target inventory

| Target | Responsibility |
| --- | --- |
| `ErrorSearchContract.cs` | normalized filter/window/query, interval overlap, DTO snapshots, stable errors |
| `ErrorSearchTokenCodec.cs` | signed snapshot+query binding and keyset cursor binding |
| `IMesIngestProjection.cs` | public list seam |
| `SqlServerMesIngestProjection.ErrorSearch.cs` | as-of/high-water reconstruction, exact filtering/facets/order/paging |
| `SqlServerMesIngestProjection.cs` / `Program.cs` | injectable Host `TimeProvider` |
| `NewMesIngestEndpoints.cs` | `/api/v2/error-search`, parsing, response DTOs, stable errors |
| `SqlServerMesIngestSchema.cs` | permanent-history query indexes and exact schema contract |
| `ErrorSearchTests.cs` | unit and production Host/SQL/API tracer bullets |
| `Invoke-Ticket11SqlServerGate.ps1` | zero-skip real SQL Server gate |

## Acceptance checklist (verbatim from ticket 11)

- [ ] 首次查询由 Host 冻结 `ErrorSearchAsOf`；默认窗口是截至该时点最近精确 7×24 小时，并可选择最近 24 小时、30×24 小时和全部历史，不按本地午夜或自然日取整。
- [ ] 错误期间与查询窗口统一采用 UTC 半开区间 `[from, to)`；边界相接不算命中，未显式给出 `to` 时以 `ErrorSearchAsOf` 为排他上界，显式非法区间得到明确失败而非静默改写。
- [ ] 查询支持主分类、SeriesErrorCode、`ACTIVE`/`ENDED`、时间、SeriesId、DemandId 与 SUBLOT；不同维度取交集、同维度多值取并集，默认同时包含活动和已结束，矛盾的分类与错误码组合明确失败。
- [ ] SeriesId、DemandId 与错误码采用去首尾空白后的不区分大小写精确匹配，SUBLOT 采用不区分大小写包含匹配；DemandId 命中时返回所属 Series，但只汇总满足全部条件的期间与证据。
- [ ] 列表按 DemandSeries 去重，并依次按匹配范围内 ACTIVE 优先、最近匹配证据时间降序、SeriesId 升序稳定排列；默认每页 100、最多 200，返回精确 totalSeriesCount，第一版不提供任意列排序或导出。
- [ ] 分类与状态分面按排除自身维度后的去重 DemandSeries 精确计算；一个 Series 可命中多个主分类，因此系统不会把分类数量机械相加解释为总数。
- [ ] 游标绑定完整规范化筛选、固定顺序、`ErrorSearchAsOf` 与契约版本；篡改、跨筛选复用或不匹配时返回稳定的明确错误，不自动冒充第一页。
- [ ] 在可控时间下，查询后追加、改变或关闭错误期间不会改变既有快照的列表、状态、分面和页序；刷新后才可观察到新的 `ErrorSearchAsOf` 与对应结果。
- [ ] 只有查询成功且零命中时才返回“该条件下没有错误历史”的空结果；加载失败、取消或零个活动错误都不会被报告为系统健康，AreaFilterProfile 也不会静默过滤错误检索。

## Risk notes

- `DemandSeriesErrorPeriods.EndedAt` is updated in place. Reads must reconstruct closure through the closed event's commit fence, not trust the current column alone.
- Evidence can be appended to an existing period after page one. Every evidence row must be fenced by ProjectionSequence.
- `ProjectionCommits.CommittedAt` is the round's business completion time, not a physical DB commit time. It cannot replace the frozen high-water sequence.
- Period overlap, not evidence timestamp containment, determines a match. A long-running period can match even when its latest evidence predates the window.
- Category facets intentionally overlap at Series level; their sum is not the exact total.
- `AreaFilterProfile`, arbitrary sorting, export, severity filtering, and ticket-12 detail/raw evidence are out of scope.
