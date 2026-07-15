# 04-functional-requirements 功能需求

本目录存放功能需求（Functional Requirement）文档，编号格式为 `FR-001`、`FR-002` ...

- 新建功能需求时，套用 `_templates/template-functional-requirement.md` 模板（已通过 Templater 插件按目录自动关联）。
- 写作规范与章节含义见 [[fr-template-guide|FR 模板说明]]；黄金样例见 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]]、[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]]。
- 每条功能需求的 frontmatter 中通过 `related_br`、`related_uc`、`related_fr`、`related_nfr`、`related_tc` 字段登记追溯关系，配合 `06-traceability/traceability-matrix.md` 的 Dataview 查询自动汇总。
- 命名规范、ID 规则、跨文档引用方式见 `../README.md`。
- 非功能需求（质量属性）不放在本目录，见 `../08-non-functional-requirements/`。
- 2026-07-14 起，本目录下按 `03-use-cases/` 同名的 11 个业务领域拆成子文件夹（如 `01-site-operations/`、`02-slot-and-hardware/`），新建 FR 时应放入其主要派生自的 UC 所属领域子文件夹，具体规则与映射表见 [[classification-rules|FR/NFR/TC 分类规则]]；`fr-template-guide.md` 与本 `README.md` 仍保留在根目录。
