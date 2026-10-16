# MES 第七类任务客户原始查询（2026-10-16）

## 来源状态

本目录归档客户新增的第 7 类运输任务原始 SQL：`WIRE_TO_FULL_INSPECTION`（焊线/键合机台 → 全检区）。
原稿由用户 2026-10-16 提供，客户已在 MES 上实际跑过。需求与决定见追踪 issue
[trytoreachpeak0/8005-agv-program#195](https://github.com/trytoreachpeak0/8005-agv-program/issues/195)，
归档票为 [#196](https://github.com/trytoreachpeak0/8005-agv-program/issues/196)。

**第一行由用户同意改为新类型名**：原稿第一行输出的任务类型常量改为 `'WIRE_TO_FULL_INSPECTION' AS TASK_TYPE`，
其余逐字照抄，未调整格式、大小写与空白。

与此前各快照不同，这份原稿自带 `TASK_TYPE` 列，所以同名 `.toml` 的 `expected_columns` 以 `TASK_TYPE` 开头。

此前五类快照见 [`../../2026-07-16/mes-task-original-queries/`](../../2026-07-16/mes-task-original-queries/)，
第六类见 [`../../2026-07-24/mes-task-original-queries/`](../../2026-07-24/mes-task-original-queries/)，均不覆盖。

对应正式查询的 `QUERY_ID` 为 `MES_TASK_UNION`。它与实验定义已于 `b2d8d643` 随构建依赖迁往 `8005-mes-ingest`，
本仓不再有 `mes/queries/` 与 `mes/experiments/`；正式查询何时并入第七类由 MesIngest 那一侧的票决定，不由本快照决定。

## 使用边界

- 仅用于差异比较、需求研究和实验基线。
- 不保证单独执行时与合并查询具有同一时刻快照。
- 不得由生产应用、工具或部署流程直接加载。
- 不得作为正式 SQL 的回退副本；运行时只能解析 `MES_TASK_UNION` 的正式查询包。
- 如客户后续更新原稿，应再建新日期目录归档，不覆盖本快照。

同名 `.toml` 仅是实验打包清单。实验定义 `mes-task-union-validation`
会通过清单把 SQL 快照复制到一次性的工厂 bundle；这些来源查询不进入正式
查询 catalog，也不构成应用运行时依赖。
