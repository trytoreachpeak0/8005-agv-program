# MES_SCHEMA_INTROSPECTION 样本

当前仅建立治理占位，不含已晋升 latest。

- 样本只保留批准的字段类型、长度、可空性和必要对象标识，不导出无关数据字典信息。
- 应用字段长度以数据库声明为准，不按样本值缩短。
- 只有 `import-run` 可晋升 latest。
- latest 使用 `latest.csv`、`latest.md` 和 `latest.meta.json`；meta 必须含 `sourceEvidence`，并记录查询与源 evidence 哈希。
