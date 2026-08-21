# 03 — 呈现再现原因与完整 MES 边界证据

**What to build:** 在世代分析中完整呈现归档前再现、归档后再现和未来未知原因，让调查人员能够沿真实形成事实追溯边界，并在证据可信时比较全部 MES 原生字段；遇到缺失或重复时明确停用标量 diff、保留全部原始证据。

**Blocked by:** 02 — 切换为单实例 Inspector 并贯通首次观察。

**Status:** ready-for-human

**UI authority:** [Fluent UI guidance](../../../docs/agents/fluent-ui.md) · [Golden Renderer workflow](../../../docs/agents/golden-renderer.md)

- [x] `PREARCHIVE_REAPPEARANCE` 以“归档前消失后再现”呈现，并在证据存在时显示 predecessor、最后匹配观测、权威 absence/GONE 和 successor 首次匹配观测。
- [x] `POSTARCHIVE_REAPPEARANCE` 以“归档后再次出现”呈现，保留生产 `LONG_GONE_BUT_VISIBLE` 语义，并在证据存在时额外显示 archive fact。
- [x] 未知或畸形原因使用中性中文说明和次要原始码，布局不崩溃，也不合成不受证据支持的生命周期解释。
- [x] 每项形成事实暴露真实 PollTrace 和 projection evidence，缺失事实明确缺失，不用占位值冒充已提交事实。
- [x] 唯一可信边界行时，对齐显示 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES（MesSourceDate）和 PACKAGE，并区分“已变化”与“保持不变”。
- [x] 画面明确说明 MES 字段差异是观察证据，不是 TransportDemand/DemandId 形成原因。
- [x] 任一边界为零行时显示明确 absence fact，不渲染全空字段行。
- [x] 任一边界为多行时显示冲突状态和全部原始行，保持 ordinal 顺序，不生成标量 diff 或 canonical row。
- [x] 许多世代时导航继续虚拟化、滚动并保留当前/选中世代的独立标记。
- [x] 公开 presentation 和窗口交互测试覆盖归档前、归档后、未知原因、唯一 diff、零行、多行冲突及多世代滚动。
- [x] 自动化名称覆盖形成事实、MES 对比、absence、conflict 和完整原始行网格。
- [x] 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。
- [x] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-21 — implementation ready for golden-machine review

- Implemented truthful available/unavailable formation facts, visible and UIA
  PollTrace/ProjectionCommit evidence, global ordinal raw-row rendering, complete
  assignment/identity/native-field raw grids, and loaded-window focused-generation
  scrolling.
- Inspector-focused suite: 29 passed, 0 failed, 0 skipped.
- Final post-review Tier 1 `dotnet test MesIngest.Tests`: 606 passed, 0 failed,
  82 skipped, 688 total in 1m24s. Every skip is the named `Ticket01SqlServerFact` environment
  gate; the full list is recorded in
  `.testagent/demand-series-inspector-e-03/status.md`.
- Four ticket-specific pseudo-mutations were injected one at a time and all were
  killed by the new tests; every mutation was reverted and the final narrow suite
  was green.
- Golden-machine execution, final preview approval, evidence directory, and VM
  cleanup remain unchecked because Tier 2/3 requires explicit user authorization.
