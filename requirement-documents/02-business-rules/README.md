# 02-business-rules 业务规则

本目录存放业务规则（Business Rule）文档，编号格式为 `BR-001`、`BR-002` ...

- 新建业务规则时，建议在 Obsidian 中对本目录使用 `Ctrl/Cmd + N` 新建笔记后，套用 `_templates/template-business-rule.md` 模板（已通过 Templater 插件按目录自动关联，新建笔记时会自动应用该模板并弹窗询问编号与标题）。
- 每条业务规则的 frontmatter 中通过 `related_uc` 字段登记被哪些 Use Case 引用，配合 `06-traceability/traceability-matrix.md` 的 Dataview 查询即可自动汇总追溯矩阵，无需手工维护表格。
- 命名规范、ID 规则、跨文档引用方式见 `../README.md`。

- [[br-001-dispatch-task-range|BR-001 派车任务范围定义]]：定义"本次派车任务范围"的判定标准，供 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-003-agv-arrives-at-designated-station|UC-003]] 引用。
- [[br-012-mes-task-idempotency-and-reconciliation|BR-012 MES任务幂等与轮询对账]]：MES 合并查询、去重、消失对账与只读约束。
- [[br-013-multi-basket-loading|BR-013 多花篮装载]]：任务与装载明细两层模型及重复扫码新增一篮。
- [[br-014-transport-task-types-and-fixed-stations|BR-014 五类任务与固定站点]]：五类搬运类型与四个固定区域站点配置。
- [[br-015-path-cost-and-dispatch-ranking|BR-015 路径成本与派车排序权衡]]：基于 RIOT 路网最短路径成本参与派车排序；与紧急度等时间指标一并权衡；不替代 RIOT 导航。
