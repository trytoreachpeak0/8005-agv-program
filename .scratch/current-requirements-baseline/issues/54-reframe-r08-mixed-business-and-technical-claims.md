# 拆分 R08 业务义务与技术机制混合声明

Type: task
Status: resolved
Blocked by: 48

## Question

如何将 [R08 原子候选分类账](../evidence/atomic-candidates/R08-atomic-candidates.tsv) 中 29 条 `needs-atomic-reframing-before-approval` 记录所包含的业务义务、领域不变量和技术机制分别改写为可独立判断的候选，在不丢失原文上下文、不虚构业务含义、不提前批准技术设计的前提下，保留来源定位、指纹、决定/冲突指针和各自的批准缺口，并使 R08 在进入跨批次去重前不再存在混合声明路由？

## Answer

已把 [R08 原子候选分类账](../evidence/atomic-candidates/R08-atomic-candidates.tsv) 首轮隔离的 29 条混合声明机械拆为 72 条单一判断候选，并把拆分计划、重建和失败式核验固化在 [R08 重建器](../evidence/atomic-candidates/build_and_verify_r08_atomic_candidates.py)；可重建统计见 [R08 原子候选摘要](../evidence/atomic-candidates/R08-atomic-candidates-summary.json)，分类与复核约定见 [原子候选分类说明](../evidence/atomic-candidates/README.md)。

- 29 个原候选逐一覆盖为 24 条业务规则、12 条领域定义/不变量、3 条操作员产品行为和 33 条技术机制，共 72 条；`needs-atomic-reframing-before-approval` 已从 29 降为 0。纯技术机制进入 `exclude-from-requirement-approval`，其余候选分别保留业务、领域或操作产品负责人的明确批准缺口。
- 每个拆分候选沿用原记录的 `source_record_id`、路径、来源 SHA-256、精确位置、章节、完整 `source_context`、来源声明状态和决定/冲突指针；`duplicate_or_derivation` 新增原候选 ID、原声明指纹及 `business` / `domain` / `product` / `technical` 拆分面向，新声明另生成自己的规范化指纹。因此既能独立判断，又能无损回到原文混合声明。
- 拆分只发生在候选分类账的可重建派生层，没有修改制图时 `CONTEXT.md` 快照、当前根 `CONTEXT.md` 或任何 ADR，也没有把技术设计改写成业务含义。总账从 1,174 条变为 1,217 条，仍全部为 `not-approved`、零永久 `REQ-NNNN`、零批准升级。
- 拆分后路线统计为：`evidence-only=238`、技术设计隔离 `291`、业务批准候选 `248`、领域闭环候选 `268`、硬件证据候选 `35`、操作产品候选 `48`、身份/授权候选 `89`。49 条精确重复仍只保留指针，不合并或删除。
- 本次机械拆分没有裁定任何业务冲突，也没有暴露足以在跨批次去重前单独毕业的新 HITL 问题；既有 `CF-R01-001/002`、`RES-R08-001/002/003` 与 `EVID-R08-001` 指针全部保留。后续可直接进入“合并并语义去重 R01–R13 原子候选”。

独立 `--verify-only` 通过：`total=1217`、`sources=19`、`excluded_not_extracted=38`、`context_terms=130`、`glossary_table_rows=109`、`exact_duplicate_rows=49`、`reframed=29->72`、`mixed_route_remaining=0`、`approval_upgrades=0`；另核验 72 条拆分记录覆盖 29 个不同原候选，且每条均保存原指纹来源链。
