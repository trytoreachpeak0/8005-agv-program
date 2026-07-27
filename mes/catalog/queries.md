# MES 查询目录

本表以 `QUERY_ID` 为稳定索引。正式 SQL 仅指向 `mes/queries/**/query.sql`；来源、证据和样本均不是运行时依赖。

| QUERY_ID | 正式查询 | 参数 | 输出 | 客户来源 | 最后证据 | 样本状态 |
| --- | --- | --- | --- | --- | --- | --- |
| `MES_TASK_UNION` | [SQL](../queries/mes-task-union/query.sql) · [元数据](../queries/mes-task-union/query.toml) · [契约](../queries/mes-task-union/README.md) | 无 | `TASK_TYPE`, `SUBLOT`, `AREA`, `EQP`, `STEP`, `DATES`, `PACKAGE` | [2026-07-16 五类原始查询](../sources/customer/2026-07-16/mes-task-original-queries/README.md)；[2026-07-24 第六类](../sources/customer/2026-07-24/mes-task-original-queries/README.md) | 尚未迁入 `evidence/` | 待迁入/脱敏 |
| `SUBLOT_BOX_COUNT` | [SQL](../queries/sublot-box-count/query.sql) · [元数据](../queries/sublot-box-count/query.toml) · [契约](../queries/sublot-box-count/README.md) | `:sublot` | `MAX_BOX_COUNT` | [来源说明与快照](../sources/customer/2026-07-16/sublot-box-count/README.md) | 尚未迁入 `evidence/` | 无独立脱敏样本 |
| `OP_OPERATOR_IDENTITY` | [SQL](../queries/operator-identity/query.sql) · [元数据](../queries/operator-identity/query.toml) · [契约](../queries/operator-identity/README.md) | `:user_id` | `OPERATOR_NAME` | [来源说明与快照](../sources/customer/2026-07-16/operator-identity/README.md) | 尚未迁入 `evidence/` | 无独立脱敏样本 |
| `MES_SCHEMA_INTROSPECTION` | [SQL](../queries/schema-introspection/query.sql) · [元数据](../queries/schema-introspection/query.toml) · [契约](../queries/schema-introspection/README.md) | 无 | 单一字段字典结果集，含 `FOUND` | 当前仓库内部为核验运输任务字段而编制，无独立客户 SQL 原稿 | 尚未迁入 `evidence/` | 不适用（元数据核验） |

“尚未迁入”只表示本次查询结构/SSOT 重构未改动旧证据和样本路径，不表示查询已经或尚未通过现场验证。
