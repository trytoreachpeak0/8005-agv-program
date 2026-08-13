# Ticket 11 test and implementation plan

## Vertical TDD slices

1. **Contract/window tracer**
   - Test `Error_search_query_normalizes_filters_and_resolves_exact_utc_windows`.
   - Add normalized filters, exact rolling windows, UTC offset parsing contract, half-open overlap, vocabulary/conflict/page validation.

2. **Credential tracer**
   - Test `Error_search_tokens_bind_asof_high_water_filter_window_order_and_page_size`.
   - Add a signed snapshot payload containing identity + normalized filter + resolved window + fixed order, and a separate keyset cursor purpose.

3. **Default search tracer**
   - Test `Rolling_and_custom_windows_use_utc_half_open_period_overlap` through the production HTTP/SQL seam.
   - Add projection high-water/as-of resolution and period reconstruction.

4. **Filter/facet tracer**
   - Test `Filters_facets_series_dedup_and_all_four_categories_share_one_snapshot`.
   - Add category/code/state/time/object intersection, same-dimension union, CI exact/contains semantics, exact category/state facets.

5. **Demand-generation tracer**
   - Test `Demand_id_filter_keeps_only_the_matching_generation_period_and_evidence`.
   - Add exact DemandId evidence restriction without losing the owning Series.

6. **Frozen-history, ordering, and paging tracer**
   - Test `Frozen_high_water_keeps_pages_state_facets_and_order_stable_after_backdated_commit`.
   - Fence opens/closes/evidence and summary state by frozen ProjectionSequence as well as ErrorSearchAsOf; prove fixed order and keyset paging.

7. **Failure/empty tracer**
   - Test `Http_failures_invalid_queries_and_successful_empty_results_remain_distinct`.
   - Add stable 400/409/410 mapping, cancellation propagation, unsupported parameter rejection, and successful empty response without health claims.

8. **Contract/release checks**
   - Keep `/api/v2/error-search` out of legacy v1 OpenAPI until ticket 17.
   - Add `Invoke-Ticket11SqlServerGate.ps1`, schema index self-check, contract/schema 11, ticket evidence.

## Requirement-to-test map

| Ticket requirement | Planned evidence |
| --- | --- |
| 首次查询由 Host 冻结…7×24…24 小时、30×24、全部历史 | `Rolling_and_custom_windows_use_utc_half_open_period_overlap` |
| UTC 半开区间 `[from,to)`…非法区间明确失败 | `Error_search_query_normalizes_filters_and_resolves_exact_utc_windows`; default-window HTTP test |
| 分类/code/state/time/SeriesId/DemandId/SUBLOT；OR/AND；矛盾失败 | `Filters_facets_series_dedup_and_all_four_categories_share_one_snapshot`; vocabulary contract test |
| 标识 exact/CI、SUBLOT contains/CI、DemandId only matching evidence | filter/facet test; `Demand_id_filter_keeps_only_the_matching_generation_period_and_evidence` |
| Series 去重、固定排序、100/200、精确总数、无任意排序/导出 | frozen high-water/paging test; failure test |
| 排除自身维度的分类/状态分面 | filter/facet HTTP test |
| cursor 绑定完整查询/asOf/version；篡改/复用失败 | token test; paging HTTP test |
| 后续追加/改变/关闭不改变旧快照 | `Frozen_high_water_keeps_pages_state_facets_and_order_stable_after_backdated_commit` |
| 成功空集与失败/取消/零 active/AREA 隐式过滤不同 | failure/empty HTTP test |

## Commands

- First red / narrow cycles: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --filter "FullyQualifiedName~ErrorSearchTests"`.
- Compile checks: `dotnet build MesIngest.Tests/MesIngest.Tests.csproj --configuration Release --no-restore`.
- Real SQL gate: `./Invoke-Ticket11SqlServerGate.ps1 -ExpectedProductMajor 16 -ExpectedCompatibilityLevel 160` (when the approved env is present).
- Final full core suite: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj --configuration Release`.
- Final solution build: `dotnet build MesIngest.sln --configuration Release --no-incremental`.
