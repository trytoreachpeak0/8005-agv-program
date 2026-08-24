# 拆分并分类跨域词汇、业务与物理事实的原子候选

Type: task
Status: resolved
Blocked by: 29, 34

## Question

依据总账 [R08 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 19 份候选文档，如何将词汇、领域事实、业务规则、物理约束和设计决定拆成可独立判断的原子条目，记录来源、范围、冲突与批准缺口，并确保任何后续获批词汇只经根 `CONTEXT.md` 的固定闭环进入运行时语言？

## Answer

已完成总账固定的 19/19 份 R08 候选材料的原子拆分与证据分类，规范主数据为 [R08 原子候选分类账](../evidence/atomic-candidates/R08-atomic-candidates.tsv)，可重建汇总为 [R08 原子候选摘要](../evidence/atomic-candidates/R08-atomic-candidates-summary.json)，来源恢复、字段边界、冲突/证据指针和处置路线见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fcaa9-3ac9-7e72-ad9a-e4405b0fb64c/R08-atomic-candidates.xlsx)。

- R08 批次的 57 份材料边界已失败式固定：只提取 19 份候选，其余 38 份纯技术决定或已替代历史材料保持文档级路由。每份候选都有记录，来源记录 ID 和路径零漏项。
- 根 `CONTEXT.md` 按 130 个词汇块拆分，每个定义中的独立声明分开，130 组 `_Avoid_` 同时作为规范名称/禁用同义词候选。由于该文件已被后续已批准决定写回，本批严格从地图固定 Git 基点 `1469d6309d00b0abb792f6cd686aed68286e638e` 恢复制图时语义内容，并保留初始快照工作树字节 SHA-256 `221b4e6942ba0fb0c12277a2e7c3311414b979b2ac90280d6400a805a0f937de`；没有把当前新内容倒灌进历史 R08 证据。
- 17 份混合 ADR 的正文、列表和结果均分开提取；`Status: accepted`、来源自述、取舍理由和形成关系只作证据，不当作业务批准。旧术语表的 109 个完整表格行和 11 条范围/治理/变更自述均保持 `evidence-only`，没有恢复为平行词汇入口。
- 最终形成 1,174 条记录：238 条证据、258 条嵌入技术设计、224 条业务规则、256 条领域定义/标准名称、35 条物理/硬件候选、45 条操作产品行为和 89 条身份/角色/授权候选。另有 29 条原文仍把业务义务与技术机制绑在同一声明中；为避免自行改写原意，已隔离到 `needs-atomic-reframing-before-approval`，并新建 [拆分 R08 业务义务与技术机制混合声明](54-reframe-r08-mixed-business-and-technical-claims.md) 在后续进入跨批次去重前完成人工可复核拆分。
- `RES-R08-001` 保留“决定操作员上下文的清除时点”对 ADR 0018/0055 冲突的解决，`RES-R08-002` 保留“决定装货待整批确认阶段是否存在”对旧阶段的排除，`RES-R08-003` 将两个词汇载体全部路由到“确定领域词汇唯一入口与旧术语表关系”。`EVID-R08-001` 连接 8005 物理主张与“补齐 8005 仓位硬件身份与现场信号证据”；`CF-R01-001/002` 继续保留 TransportDemandKey 和 MES 只读/回写的跨批次冲突线索。
- 1,174 条记录全部 `not-approved`、零永久 `REQ-NNNN`；49 条后出现记录只按规范化声明指纹标记精确重复，未合并语义近似项。本票没有批准新词汇或修改根 `CONTEXT.md`；后续只有经 `grilling` / `domain-modeling` 澄清并由用户明确批准的名称和定义，才能即时写回原路径。

独立失败式 `--verify-only` 通过：`total=1174`、`sources=19`、`excluded_not_extracted=38`、`context_terms=130`、`glossary_table_rows=109`、`exact_duplicate_rows=49`、`approval_upgrades=0`；指针命中为 `CF-R01-001=49`、`CF-R01-002=4`、`EVID-R08-001=82`、`RES-R08-001=43`、`RES-R08-002=6`、`RES-R08-003=577`。XLSX 的 19 份来源对账均为 `OK`，汇总公式与指针计数已对账，公式错误扫描为零，并完成四张工作表的视觉检查。
