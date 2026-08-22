# 01 — 同步 E 架构决策并建立可信 Presentation

**What to build:** 以 [E 方案规格](../spec.md) 为权威，将 Inspector 的信息架构决策同步进现有 ADR，并建立不依赖窗口或 Session 的不可变 DemandSeries presentation。调查人员随后看到的形成原因、形成事实、MES 边界证据和事件输入，都必须来自冻结的生产快照，而不是 UI 推断或原型词汇。

**Blocked by:** None — can start immediately.

**Status:** done

- [x] 现有 Inspector ADR 明确改为 E 信息架构；窗口所有权、焦点、刷新、导航和持久化决策保持不变。
- [x] Presentation 从匹配 DemandId 的真实 `TRANSPORT_DEMAND_CREATED` 事件提取原因；第一代为 `FIRST_OBSERVED`，已知原因显示规定的中文，原始码保留为次要技术信息。
- [x] 未知或畸形原因得到中性中文回退和原始码，不崩溃、不借用其他原因的叙事。
- [x] 形成证据是按真实事件、PollTrace 和 projection evidence 构成的可变有序事实集合，能够区分首次观察、归档前再现和归档后再现。
- [x] Presentation 只使用生产状态和事件词汇，包括 `LONG_GONE_BUT_VISIBLE`；不引入原型专用状态或便利事件。
- [x] MES 边界按真实 PollTrace/commit 和 assignment 分组，重复原始行按 ordinal 保留，不被挑选、合并或覆盖。
- [x] 标量比较仅在每个适用侧恰有一条可信 assigned 原始行时成立；零行呈现缺失事实，多行呈现冲突和完整原始行集合。
- [x] MES 证据保留 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES（MesSourceDate）和 PACKAGE，并明确字段变化只是观察证据而非 DemandId 形成原因。
- [x] 事件输入只包含冻结快照中的真实不可变事件，并保持 `SeriesSequence` 顺序，能够支持按 DemandId 的本地过滤。
- [x] 使用生产形状快照覆盖形成原因、形成事实、MES diff 资格、缺失、冲突和事件输入；不测试私有方法。
- [x] 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。

## Comments

### 2026-08-22 — implementation and acceptance evidence reconciled

- Commit `5854b8b1` added the E information-architecture ADR, immutable
  `WatchDemandSeriesInspectorPresentation`, and its production-shape public
  behavior tests. The integrated implementation at clean source commit
  `7111f77c` retains the frozen snapshot identity, real creation reasons and
  facts, production status vocabulary, ordinal MES evidence, seven native MES
  fields, scalar-diff eligibility, explicit absence/conflict states, and
  stable real-event ordering required by this ticket.
- `WatchDemandSeriesInspectorPresentationTests` covers the frozen snapshot,
  known and malformed reasons, reason-specific formation facts,
  `LONG_GONE_BUT_VISIBLE`, missing facts, unique/zero/multiple assigned MES
  boundaries, all seven scalar fields, global ordinal raw evidence, immutable
  `SeriesSequence` ordering, and local DemandId filtering through the public
  projection surface rather than private methods.
- The final integrated Tier 1 run from `mes/ingest/csharp` at the validated
  source identity passed 641, failed 0, skipped 82, total 723. All 82 skips are
  the repository's SQL Server environment gate because
  `MES_INGEST_TICKET01_SQLSERVER`,
  `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`, and
  `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL` were not set; this ticket
  changed no SQL. Ticket 01 requires no visual acceptance and is complete.
