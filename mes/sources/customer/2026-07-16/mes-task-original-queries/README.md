# MES 五类任务客户原始查询

## 来源状态

本目录是 2026-07-16 从仓库现有五个 `original_queries` 文件归档的客户原始 SQL 快照，保留各分支当时的字段顺序、大小写和格式，用于追溯客户输入及与合并查询对比。

对应正式查询为 [`../../../../queries/mes-task-union/query.sql`](../../../../queries/mes-task-union/query.sql)，`QUERY_ID` 为 `MES_TASK_UNION`。

## 使用边界

- 仅用于差异比较、需求研究和实验基线。
- 不保证单独执行时与合并查询具有同一时刻快照。
- 不得由生产应用、工具或部署流程直接加载。
- 不得作为正式 SQL 的回退副本；运行时只能解析 `MES_TASK_UNION` 的正式查询包。
- 如客户后续更新原稿，应新建日期目录归档，不覆盖本快照。

同名 `.toml` 仅是实验打包清单。只有
[`mes-task-union-validation`](../../../../experiments/definitions/mes-task-union-validation/plan.md)
会通过这些清单把 SQL 快照复制到一次性的工厂 bundle；这些来源查询不进入正式
查询 catalog，也不构成应用运行时依赖。
