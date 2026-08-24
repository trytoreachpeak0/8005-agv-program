# 拆分并分类现场操作验收场景的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R05 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 67 份候选文档，如何按场景级验收声明拆分原子条目，将业务验收候选与接口、安全及内部设计主张分开，并记录来源、适用范围、上游派生、证据/冲突指针和批准缺口？

## Answer

已完成总账固定的 67/67 份 R05 现场操作 TC 的原子拆分与证据分类，规范主数据为 [R05 原子候选分类账](../evidence/atomic-candidates/R05-atomic-candidates.tsv)，可重建汇总为 [R05 原子候选摘要](../evidence/atomic-candidates/R05-atomic-candidates-summary.json)，拆分边界、字段和冲突/追踪质量登记见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fca7f-d517-73a0-a52a-1790f66ff61e/R05-atomic-candidates.xlsx)。

- 38 份 `R05-C1` 上游镜像草稿与 29 份 `R05-C2` 内部设计显著草稿共形成 401 条记录；Preconditions、Test Steps、Expected Result、Verifies 分别拆为 101 条前置、87 条动作、146 条结果与 67 条追踪证据，每份来源都完整覆盖四种场景角色。
- 业务验收、身份/权限/即时认证、硬件与安全、车载—服务端/MES 接口、HMI/操作体验及内部状态机/架构主张已分开分类，并分别记录责任人、来源、接口/硬件版本、风险评审、适用范围和对象哈希等批准缺口。
- 处置路线为：112 条上游业务来源与明确批准、69 条身份/角色责任人批准、49 条安全/硬件责任人批准、28 条接口责任人及受控版本批准、20 条操作/产品责任人批准、51 条内部设计隔离、67 条仅作追踪证据；另有 5 条业务/接口候选保持既有冲突待裁决。
- `CF-R01-001` 命中 8 条 `TransportDemandKey`、同一 SUBLOT 的任务类型边界或取消抑制记录；其中 3 条本来就是内部设计主张而继续隔离，5 条进入 `hold-for-conflict-decision`。`TQ-R05-001` 固定 11 份来源、58 条记录的文件名/正文语义漂移，避免按路径名称误判当前声明。
- 所有 401 条记录的 `approval_state` 均为 `not-approved`，没有分配永久 `REQ-NNNN`；5 条后出现记录只按规范化声明指纹标为精确重复，没有合并语义近似项，也没有把 `draft`、ADR `accepted`、Git 历史或计划预期结果误作批准或实际执行证据。
- 本批只补足既有跨批次冲突与追踪质量证据，没有暴露需要在其余批次原子化、跨批次语义去重前新增的独立 HITL 票。

失败式 `--verify-only` 已独立通过：`total=401`、`sources=67`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=5`、`conflict_or_traceability_rows=66`；67 个来源当前 SHA-256 与固定值一致，重建结果与主账逐字段一致。XLSX 的 Summary、Source Coverage、Conflict Register 与 Candidates 四张表已核验：汇总公式为 401/67/5/0，67 个来源全部 `OK`，公式错误扫描为零，并完成四张表及 Candidates 首尾区域的视觉检查。

本票只分类现有证据，没有批准新的领域词汇或业务决定，因此未修改根 `CONTEXT.md`。
