# 拆分并分类历史本地 spec 需求摘要的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R12 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 2 份混合 spec，如何按 story 和语义拆分原子需求摘要，追溯上游来源、核查当前适用性、分离设计与实施决定，并记录重复、冲突和批准缺口；其余 48 张实施、评审与修复票继续只作历史证据？

## Answer

已完成总账固定的 2/2 份 R12 混合 spec 的原子拆分与证据分类，规范主数据为 [R12 原子候选分类账](../evidence/atomic-candidates/R12-atomic-candidates.tsv)，可重建汇总为 [R12 原子候选摘要](../evidence/atomic-candidates/R12-atomic-candidates-summary.json)，拆分、分类、追溯和指针边界见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fcb14-fb41-72a1-bcac-265d5507b151/R12-atomic-candidates.xlsx)。

- R12 的 50 份材料边界已失败式固定：只提取 `MesIngest Phase 1` 和 `MesIngest Watch Operations and Scalable Read Model` 两份 spec；31 张实施/偏差修复票与 17 张 review remediation 票继续只作历史证据。
- 最终形成 300 条记录：Phase 1 spec 130 条，Watch spec 170 条；逐项覆盖 50 个 Phase 1 story、8 个 Watch `Confirmed Domain Semantics` 来源项和 65 个 Watch Functional Requirements 来源项。
- 已分开 TransportDemand 生命周期、MES 外部数据契约、Watch 用户/运维行为、读 API 与 ChangeFeed/Bootstrap 同步契约、Alert 事件语义、安全边界、可调默认值、产品范围与本地技术/测试决定。44 条纯技术/测试机制进入 `exclude-from-requirement-approval`，2 条混合语句保持待重新原子化。
- 每条均保留来源路径/哈希、精确位置、上下文、总账当前适用性、上游 `ADR-mes-0006/0007`、`MES_TASK_UNION`/查询材料、根 `CONTEXT.md` 闭环和 R11 工厂证据的显式指针。`ready-for-agent`、`Confirmed`、勾选完成和测试结果都不传递需求权威。
- `RES-R11-001`/`BOUND-R11-001` 将“客户批准 SQL”的历史自述限制为未满足四项批准证据；`EVID-R11-001` 继续限定工厂 run 和耗时观察；`CF-R01-001/002`、`AD-R01-001` 保留已知身份、只读/回写与五/六类版本线索。本批没有在跨批次语义去重前新增独立 HITL 真实冲突票。
- `RES-R08-003` 覆盖历史词汇/领域语义声明；本票没有新的用户词汇批准，因此不修改根 `CONTEXT.md`。
- 300 条记录全部为 `not-approved`、零永久 `REQ-NNNN`；唯一精确重复是两份 spec 的 `Status: ready-for-agent`，只保留后出现指针，不删除或合并记录。

独立失败式 `--verify-only` 通过：`total=300`、`sources=2`、`excluded_not_extracted=48`、`phase1_stories=50`、`watch_semantics=8`、`watch_fr_items=65`、`exact_duplicate_rows=1`、`approval_upgrades=0`；八类冲突/决定/证据指针全部命中。XLSX 的 2 份来源对账均为 `OK`，汇总公式与指针计数已对账，公式错误扫描为零，并完成四张工作表的视觉检查。
