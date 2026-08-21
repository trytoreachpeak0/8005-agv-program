# 04 — 交付真实事件调查与相关事件跳转

**What to build:** 让调查人员从世代分析进入一个全宽、可审计的事件工作区，在同一冻结事件集合上切换全部 Series 事件与当前 Demand 相关事件，不重新查询、不改变顺序，也不发明生产模型中不存在的事件。

**Blocked by:** 02 — 切换为单实例 Inspector 并贯通首次观察。

**Status:** ready-for-human

**UI authority:** [Fluent UI guidance](../../../docs/agents/fluent-ui.md) · [Golden Renderer workflow](../../../docs/agents/golden-renderer.md)

- [x] “事件”作为与“世代分析”平级的一级 Tab，全宽显示冻结快照中的真实 `DemandSeriesEvent` 字段和 payload evidence。
- [x] 事件始终按 `SeriesSequence` 的提交顺序稳定呈现，不因过滤、渲染或刷新重新排序。
- [x] 过滤器提供“全部 Series 事件”和“当前 Demand 相关事件”，并明确当前过滤上下文。
- [x] “相关事件”从选中世代原子切换到事件 Tab 并按该 DemandId 过滤；返回全部事件无需 Host 请求。
- [x] 过滤只操作同一不可变事件集合，不修改、重新获取、复制或合成领域事实。
- [x] 切换选中世代后，相关事件过滤上下文与新 DemandId 一致；切换 Series 时清除旧 Series 的过滤状态。
- [x] 不显示原型便利事件；生产事件字段、subject、PollTrace、projection commit、payload version 和 payload 均可追溯。
- [x] 公开 presentation/交互测试覆盖全部事件、相关事件、过滤往返、稳定顺序、无额外请求和 Series 切换清理。
- [x] 自动化名称和键盘操作覆盖事件 Tab、相关事件动作、过滤器和事件证据网格。
- [x] 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。
- [x] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-21 — implementation ready for golden-machine review

- Production now follows accepted E commit `5ef7e367`: the event count is in
  the first-level event Tab header, and the event task owns the full content
  width with exact all-Series/current-Demand filters.
- The grid exposes all real immutable fields: `SeriesSequence`, `EventId`,
  `SeriesId`, `OccurredAt`, `EventType`, `SubjectKind`, `SubjectId`,
  `PollTraceId`, `ProjectionCommitId`, `PayloadVersion`, and `PayloadJson`.
- Related/all filtering preserves the original event objects and committed
  order, emits no outward request, tracks focused-generation changes, and
  resets on Series changes.
- Focused Inspector tests: 29 passed, 0 failed, 0 skipped. Six empirical
  pseudo-mutations were killed and reverted.
- Final Tier 1: 611 passed, 0 failed, 82 skipped, 693 total in 1m03s. Every skip
  is the expected SQL Server environment gate; Ticket 04 changes no SQL.
- Final Standards review has no hard finding; final Spec review has no finding.
  `MesIngest.Watch.UiTests` builds with zero warnings/errors and the production
  journey now captures `03c-demand-series-related-events`.
- Tier 2 `watch-ui-journeys`, final preview approval, evidence recording, and
  VM cleanup remain unchecked because they require explicit user authorization.

### 2026-08-21 — first golden preview retained as red visual evidence

- User authorized Tier 2 `watch-ui-journeys`. The run used clean commit
  `f855ccf4` on `gpt_win11` at 1920×1080 / 96 DPI and passed 1/1 with zero
  failures, skips, or not-run tests.
- Evidence is preserved at
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-04/run-20260821-203205-watch-ui-journeys`.
- Human comparison with accepted E prototype commit `5ef7e367` rejected the
  candidate: `SeriesSequence`, `SubjectKind`, `ProjectionCommitId`, and
  `PayloadVersion` headers were visibly clipped, so field identity was not
  directly readable even though automation found all eleven bindings.
- Event columns now reserve enough width for every technical header and use the
  shared `DataGridTextCell` style. Focused tests remain 29/29, and
  `MesIngest.Watch.UiTests` builds with zero warnings/errors. A fresh Tier 2 run
  is required; the passing rerun must not replace this red evidence.

### 2026-08-21 — second golden preview exposed runtime column compression

- Clean commit `fefafd52` again passed `watch-ui-journeys` 1/1 with zero skips;
  cleanup left no scheduled task or residual process and restored the 96 DPI
  environment.
- Evidence is preserved at
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-04/run-20260821-204023-watch-ui-journeys`.
- The shared cell style improved value separation, but visual inspection still
  found long technical headers compressed. A real-window regression confirms
  the declared `ActualWidth`; explicit per-column `MinWidth` is now required so
  the golden renderer must use horizontal scrolling instead of shrinking field
  identity.
- Focused tests remain 29/29 and now assert both actual and minimum widths for
  all eleven fields. A third clean Tier 2 run is required; both prior visual
  rejections remain preserved.
