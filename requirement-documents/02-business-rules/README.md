# 02-business-rules 业务规则

本目录存放业务规则（Business Rule）文档，编号格式为 `BR-001`、`BR-002` ...

- 新建业务规则时，建议在 Obsidian 中对本目录使用 `Ctrl/Cmd + N` 新建笔记后，套用 `_templates/template-business-rule.md` 模板（已通过 Templater 插件按目录自动关联，新建笔记时会自动应用该模板并弹窗询问编号与标题）。
- 每条业务规则的 frontmatter 中通过 `related_uc` 字段登记被哪些 Use Case 引用，配合 `06-traceability/traceability-matrix.md` 的 Dataview 查询即可自动汇总追溯矩阵，无需手工维护表格。
- 命名规范、ID 规则、跨文档引用方式见 `../README.md`。

- [[br-001-dispatch-task-range|BR-001 派车任务范围定义]]：定义"本次派车任务范围"的判定标准，供 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-003-agv-arrives-at-designated-station|UC-003]] 引用。
