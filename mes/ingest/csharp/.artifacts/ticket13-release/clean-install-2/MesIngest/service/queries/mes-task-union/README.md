# MES_TASK_UNION

一次执行六类 MES 运输任务查询，并在同一 Oracle 语句级一致性快照中返回统一列。正式 SQL 见 [`query.sql`](query.sql)，机器可读契约见 [`query.toml`](query.toml)。

## 契约

- 参数：无。
- 输出顺序：`TASK_TYPE`、`SUBLOT`、`AREA`、`EQP`、`STEP`、`DATES`、`PACKAGE`。
- `TASK_TYPE` 取值：`DIE_TO_WIRE_STAGING`、`DIE_TO_OVEN`、`WIRE_TO_GATE`、`WIRE_TO_OPTICAL`、`STAGING_TO_WIRE`、`WIRE_TO_NITROGEN`。
- 使用 `UNION ALL`，不得用 `UNION` 静默去重；应用层以 `TASK_TYPE + SUBLOT` 为幂等键，单次结果中该键多行视为硬失败（阻断冲突键、其余继续）。
- 查询只读，不在 SQL 中增加上线时间过滤；上线时间及异常骤降保护由应用层处理。

## 实验与证据关系

实验应通过 `MES_TASK_UNION` 定位本包，不复制 SQL。每轮实验记录查询版本、执行环境、时间和结论到 `experiments/` 与 `evidence/`；可公开结果须脱敏后放入 `samples/`。客户原始查询仅作为分支对比基线：

- 前五类：[`../../sources/customer/2026-07-16/mes-task-original-queries/`](../../sources/customer/2026-07-16/mes-task-original-queries/)
- 第六类：[`../../sources/customer/2026-07-24/mes-task-original-queries/`](../../sources/customer/2026-07-24/mes-task-original-queries/)

不得作为运行时依赖。
