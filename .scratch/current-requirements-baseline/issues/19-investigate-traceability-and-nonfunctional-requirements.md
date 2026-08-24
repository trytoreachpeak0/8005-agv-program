# 调查追溯规则与非功能需求

Type: research
Status: resolved
Blocked by: 11

## Question

对无损清单 R07 批次中的追溯规则、追溯矩阵、非功能需求与索引，逐份核实来源、历史、具名批准证据、批准范围和当前适用性；如何区分可独立批准的非功能要求、派生追溯记录与空白分类占位？

## Answer

完整调查见 [R07 追溯规则与非功能需求调查](../evidence/investigations/R07-traceability-and-nonfunctional-requirements.md)。固定清单中的 15/15 份材料均已核实且 SHA-256 零漂移。只有 NFR-001 与 NFR-002 表达可独立判断的内部派生 NFR 候选，共 5 个 FC；两者均为 `draft` 且缺少批准四要素，99.5%/15 分钟与 180 天/5 分钟等数值也都明确标为 TBD，不能作为已承诺 SLA、恢复或合规指标。

`traceability-matrix.md` 是动态 Dataview 查询定义，不是固定结果快照；`classification-rules.md` 是内部归档规则且已遗漏后续 FR-031；模板指南、根索引和 9 个分类 README 只提供记录/导航结构或空白占位。后续须将 NFR 度量、适用时窗、排除项、外部依赖归因与测量方法逐项批准，并把“有链接、来源已批准、派生转换已核对、验证已通过”保存为不同状态，不能由可渲染追溯链反推权威性。
