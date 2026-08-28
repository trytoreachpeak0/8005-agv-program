# 07 — Watch Load more 在刷新后保留，两表排序/分页下推服务端

**What to build:** MesIngest.Watch 自动刷新不得清空用户已“Load more”追加的 Demand 行；Demand/Alerts 允许排序的列必须对服务端完整结果集排序/分页，禁止仅排序当前首页或把不可排序列假装可排。

**Blocked by:** 03 — Demand 降序 keyset 不因主排序并列丢行

**Status:** done

## Parent / References

- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（Watch 分页浏览）
- Issues:
  - `.scratch/mes-ingest-watch-operations/issues/07-watch-paged-demand-browsing-and-sorting.md`
  - `.scratch/mes-ingest-watch-operations/issues/05-paginated-indexed-demand-api.md`
- Handoff findings: MainWindow `resetPage: true`；两表排序/分页不完整

不重新定义筛选/cursor 契约；本票修复 Watch 对已实现 API 的使用方式。

## Repro

1. Demand 表滚动/Load more 追加第二页后等待自动刷新（约 2s）。
2. 对 Alerts：在仅首页数据下点击列头排序，对比仅本地页排序与全量服务端顺序。
3. 点击 Demand 上标明不可排序的列（若 UI 仍可点）。

期望失败态（现状）：刷新 `resetPage: true` 丢掉已加载行；Alerts 只拉默认首页再本地排序；部分 Demand 列未真正服务端排序。

## Regression tests

- [x] ViewModel/UI 测试：已有 `nextCursor`/已加载多页时，定时刷新保持页累积（或等价：刷新当前已请求区间），不无故回到仅第一页
- [x] 筛选变化时仍清页重查（既有 ticket 07 行为保留）
- [x] Alerts 排序变化触发带 sort 参数的服务端请求，而非只 `OrderBy` 当前内存页
- [x] 不可排序列在 UI 上不可启动排序，或启动后有明确拒绝；可排序列与 Host allow-list 一致
- [x] 依赖 ticket 03 的并列 DemandId 场景下，Watch 连续 Load more 仍无漏行

## Acceptance criteria

- [x] Load more 结果在自动刷新后仍然可见（筛选未变时）
- [x] 两表允许的排序/分页均下推 Host 完整结果集
- [x] 与 ticket 07/05 验收对齐的集成或契约测试通过

## Comments

- 2026-08-01: Extracted `WatchBrowseSession` with Reset / PreserveWindow / Append. Timer uses PreserveWindow. Alerts sort goes through `WatchAlertBrowseQuery` to Host allow-list; UI columns aligned (Severity/AlertId/first seen/last seen sortable; TASK_TYPE/SUBLOT/DemandId/Message not). Covered by `WatchBrowseSessionTests` + live Host tied-dates Load more.
