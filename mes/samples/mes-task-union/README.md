# MES_TASK_UNION 样本

当前仅建立治理占位，不含已晋升 latest。

- 预期字段：`TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE`。
- 旧 6 字段历史结果位于 [`../../evidence/legacy/2026-07-10-mes-task-union/`](../../evidence/legacy/2026-07-10-mes-task-union/)，缺 `PACKAGE`，不得晋升为当前 latest。
- 只有 `import-run` 可从通过校验的 evidence 更新 `latest.csv`、`latest.md` 和 `latest.meta.json`。
- `latest.meta.json` 必须含源 run、`sourceEvidence` 相对路径和输出哈希。
- 导入时自动生成 `package-coverage/`；其中 `unmatched_packages.csv` 是反馈客户补充容量对照的当前清单。
