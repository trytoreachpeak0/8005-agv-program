# 拆分并分类用例与流程的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R03 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 46 份候选文档，如何按流程和可独立判断的行为拆分原子条目，将业务用例候选与内部设计推演分开，并记录上游、适用范围、重复/派生关系、冲突和批准缺口？

## Answer

已完成 46/46 份 R03 候选用例的原子拆分与证据分类，规范主数据为 [R03 原子候选分类账](../evidence/atomic-candidates/R03-atomic-candidates.tsv)，字段、拆分边界、冲突登记和复核方式见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fca27-ded6-78d1-8185-64aa0e20dcbc/R03-atomic-candidates.xlsx)。

- 共形成 3,095 条可独立审查声明；每条固定来源记录、路径、原 SHA-256、Markdown 行号、章节、声明、完整上下文、适用范围、候选类别、自述来源状态、处置路线、重复/派生关系、冲突指针和批准缺口。
- 46 份来源逐份有记录、候选 ID 零重复。按总账保留 22 份 `R03-C` 业务用例候选与 24 份 `R03-I` 内部设计推演的文档身份；167 条后出现记录只按规范化声明指纹标为精确重复，没有擅自合并语义近似项。
- 在 `R03-C` 内进一步把 874 条可独立审查的业务行为与 138 条嵌入式内部技术细化分开；明确的 API、SQL、字段、持久化、状态机、轮询、快照、事务和幂等实现不能随整份 UC 一起批准。`R03-I` 中的流程、接口、安全、权限和审计推演分别保留类别，但不从自身进入需求批准路线。
- 处置结果为：872 条 `needs-source-and-explicit-approval`、2 条 `hold-for-conflict-decision`、50 条 `needs-question-resolution`、638 条 `evidence-only` 和 1,533 条 `exclude-from-requirement-approval`。
- 所有 3,095 条记录的 `approval_state` 都是 `not-approved`，没有把 `draft`、Notes 中的“用户确认”、关联 BR/UC、Git 历史、ADR 或当前实现当作批准，也没有分配永久 `REQ-NNNN`。
- 复用既有冲突/版本指针：`CF-R01-001` 命中 5 条业务键/幂等口径，`CF-R01-002` 命中 3 条 MES 只读/回写边界，`CF-R01-003` 命中 41 条 AREA 映射模型，`AD-R01-001` 命中 3 条五类/六类任务版本差异。本批补足了 R03 侧证据，但没有暴露需要在跨批次去重前提前新增的独立冲突票。
- XLSX 的 Summary、Source Coverage、Conflict Register 与 Candidates 四张表已从最终导出文件重新导入核验并逐张完成视觉检查；46 个来源对账全为 `OK`，公式错误和 `MISMATCH` 扫描均为零。

失败式 `--verify-only` 已独立通过：`total=3095`、`sources=46`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=167`、`conflict_rows=49`；46 个来源当前 SHA-256 与固定值一致，重建结果与主账逐字段一致。

本票只分类现有证据，没有批准新的领域词汇或业务决定，因此未修改根 `CONTEXT.md`。
