# 拆分并分类客户、项目协议与原始输入的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R01 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 13 份候选文档，如何按可独立判断的声明拆分原子条目，保留客户来源、讨论稿、内部推导和待确认的证据差异，并为每个条目记录来源、适用范围、重复/派生关系、冲突指针和批准缺口，而不把自称关闭或未签署协议当作批准？

## Answer

已完成 13/13 份 R01 候选文档的原子拆分与证据分类，规范主数据为 [R01 原子候选分类账](../evidence/atomic-candidates/R01-atomic-candidates.tsv)，字段、边界、冲突登记和复核方式见 [R01 原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fc822-5233-78a0-8de6-14b894bf1f11/R01-atomic-candidates.xlsx)。

- 共形成 3,091 条可独立审查声明；每条固定来源记录、路径、原 SHA-256、Markdown 行号或 DOCX 段落/表格行定位、声明文本、完整上下文、适用范围、候选类别、来源自述状态、处置路线、重复/派生关系、冲突指针和批准缺口。
- 13 份来源逐份有记录，候选 ID 零重复。通过规范化声明指纹识别 915 条后出现的精确重复并指向首条记录，但没有擅自合并语义近似项；跨 R01–R13 的语义去重继续等待其余批次拆分完成。
- 建议动作、内部设计、运行时组织、历史状态、来源说明和项目计划分别进入 `evidence-only` 或 `exclude-from-requirement-approval`，没有被提取成客户需求。172 条文档自述未决问题保持 `needs-question-resolution`。
- 58 条自称“已关闭”的结论单独标为 `self-asserted-closed-decision`，仍是 `not-approved`；技术协议中的 137 条项目特定或通用模板候选继续保持未签署/未生效隔离，不能由格式、标题或条款措辞升级。
- 所有 3,091 条记录的批准状态均为 `not-approved`，统一保留具名批准人、批准日期、批准范围和版本/哈希绑定四项缺口；本票没有分配永久 `REQ-NNNN`。
- 已登记三条冲突线索和一条版本差异：`CF-R01-001`（`TASK_TYPE + SUBLOT` 与旧稿幂等键口径）、`CF-R01-002`（当前阶段 MES 只读与旧稿回写职责）、`CF-R01-003`（AREA 自动派生与被引用的人工版本化模型，等待 R02/R03 复核）以及 `AD-R01-001`（2026-07-14 五类任务与当前六类任务）。按地图既定雾区规则，本票不在跨批次去重前提前生成 HITL 决策票。
- DOCX 使用只读 OOXML 结构抽取；当前环境缺少 LibreOffice，无法新增页面渲染复核，因此没有声称验证页码、版式或可见签章。该限制不改变既有调查中“未发现完整批准链”的结论，也没有修改原文档。
- XLSX 的 Summary、Source Coverage、Conflict Register 与 Candidates 四张表已完成公式读回和视觉检查；13 个来源对账全为 `OK`，摘要为 3,091 条、13 份来源、915 条精确重复、0 条批准升级，公式错误扫描为零。

失败式 `--verify-only` 已独立通过：`total=3091`、`sources=13`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=915`、`conflict_rows=82`，13 个来源当前 SHA-256 与固定值一致，重建结果与主账逐字段一致。

本票只分类现有证据，没有批准新的领域词汇或业务决定，因此未修改根 `CONTEXT.md`。
