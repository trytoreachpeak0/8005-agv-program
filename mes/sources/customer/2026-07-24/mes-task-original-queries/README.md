# MES 第六类任务客户原始查询（2026-07-24）

## 来源状态

本目录归档客户新增的第 6 类运输任务原始 SQL：`WIRE_TO_NITROGEN`（焊线1 → 氮气柜）。

此前五类快照仍见 [`../../2026-07-16/mes-task-original-queries/`](../../2026-07-16/mes-task-original-queries/)，不覆盖。

对应正式查询为 [`../../../../queries/mes-task-union/query.sql`](../../../../queries/mes-task-union/query.sql)，`QUERY_ID` 为 `MES_TASK_UNION`。

## 使用边界

- 仅用于差异比较、需求研究和实验基线。
- 不保证单独执行时与合并查询具有同一时刻快照。
- 不得由生产应用、工具或部署流程直接加载。
- 不得作为正式 SQL 的回退副本；运行时只能解析 `MES_TASK_UNION` 的正式查询包。
- 如客户后续更新原稿，应再建新日期目录归档，不覆盖本快照。

同名 `.toml` 仅是实验打包清单。
[`mes-task-union-validation`](../../../../experiments/definitions/mes-task-union-validation/plan.md)
会通过清单把 SQL 快照复制到一次性的工厂 bundle；这些来源查询不进入正式
查询 catalog，也不构成应用运行时依赖。
