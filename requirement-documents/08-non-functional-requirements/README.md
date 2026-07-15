# 08-non-functional-requirements 非功能需求

本目录存放非功能需求 / 质量属性（Non-Functional Requirement）文档，编号格式为 `NFR-001`、`NFR-002` ...

- 新建非功能需求时，套用 `_templates/template-non-functional-requirement.md` 模板（已通过 Templater 插件按目录自动关联）。
- 写作规范与章节含义见 [[nfr-template-guide|NFR 模板说明]]；黄金样例见 [[nfr-001-service-availability|NFR-001]]、[[nfr-002-audit-completeness-and-retention|NFR-002]]。
- 每条 NFR 的 frontmatter 中通过 `related_uc`、`related_fr`、`related_tc` 及 `category` 登记追溯与分类，配合 `06-traceability/traceability-matrix.md` 的 Dataview 查询自动汇总。
- 命名规范、ID 规则、跨文档引用方式见 `../README.md`。
- 功能需求见 `../04-functional-requirements/`；NFR 横切约束 FR，不替代 FR。
- 2026-07-14 起，本目录下按 `category` 字段拆成 11 个质量属性子文件夹（如 `availability/`、`auditability/`），新建 NFR 时应放入对应质量属性子文件夹（不按 UC 业务领域分类），具体规则与分类表见 [[classification-rules|FR/NFR/TC 分类规则]]；`nfr-template-guide.md` 与本 `README.md` 仍保留在根目录。
