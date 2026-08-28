# MES 资料与查询目录

本目录按“业务说明、可执行查询、来源材料、验证证据”分层，避免正式 SQL、客户原稿和实验脚本互相引用而形成多份真源。

## 目录分层

- `docs/`：面向业务、接口和设计的说明文档，不存放正式可执行 SQL。
- `queries/`：正式查询包。每个包包含 `query.sql`、`query.toml` 和不复制 SQL 正文的 `README.md`。
- `sources/`：客户原始 SQL、需求摘录等来源快照，只用于追溯和差异研究。
- `experiments/`：查询实验方案与临时验证，不作为生产运行入口。
- `evidence/`：带日期的执行记录、结果摘要和结论。
- `samples/`：脱敏样本及样本说明。
- `reference/`：稳定的字段、容量、枚举等参考资料。
- `tools/`：校验、测试和辅助脚本；工具只能通过查询目录解析正式查询。

部分目录可能由后续重构阶段补齐；本文件先定义统一边界。

## QUERY_ID

`QUERY_ID` 是查询的稳定标识，不随目录名、中文标题或 SQL 修订变化。目录清单见 [`catalog/queries.md`](catalog/queries.md)，机器可读元数据见各查询包的 `query.toml`。

应用、工具、实验和证据应记录 `QUERY_ID`，再由清单或元数据定位查询包；不得把旧路径或客户来源路径当作运行时查询标识。当前登记：

- `MES_TASK_UNION`
- `SUBLOT_BOX_COUNT`
- `OP_OPERATOR_IDENTITY`
- `MES_SCHEMA_INTROSPECTION`

## 正式 SQL 唯一源

每个查询包中的 `queries/<package>/query.sql` 是该查询的正式 SQL 唯一源（SSOT）。生产代码、测试工具和后续文档只应引用它，不得在 README、脚本或样本中复制一份可执行 SQL。

`sources/customer/` 保存客户提供或从需求确认文档形成的来源快照。来源内容可以与正式查询比较，但不得被应用或生产部署作为运行时依赖；只有明确实验可以把来源快照复制进一次性 bundle。旧 `mes/sql/` 已退出维护，历史产物位于 `evidence/legacy/`。

`sources/legacy-program-sql/` 保存旧程序访问代码的哈希快照，其中既有未验证 SELECT
也有写操作；必须按
[`legacy-program-sql-research`](experiments/definitions/legacy-program-sql-research/plan.md)
研究，禁止直接执行。

工厂首次验证按
[`docs/工厂首轮执行与回传清单.md`](docs/工厂首轮执行与回传清单.md)
执行；未完成回传导入前，不得把本机检查结果写成 MES 现场通过。

## 新增查询流程

1. 分配唯一且稳定的 `QUERY_ID`，确定小写短横线包目录名。
2. 在 `queries/<package>/` 创建 `query.sql`、`query.toml` 和 `README.md`。
3. 在 `query.toml` 声明 `id`、`title`、`sql`、`readonly`、`parameters` 和 `expected_columns`，并用 Python `tomllib` 校验。
4. README 只描述输入、输出、只读边界、失败语义及实验关系，不复制 SQL 正文。
5. 将客户原稿或需求摘录按日期归档到 `sources/customer/YYYY-MM-DD/`，注明来源状态和禁止运行时依赖。
6. 在 `catalog/queries.md` 登记正式查询、参数、输出、来源、最后证据及样本状态。
7. 在只读环境中完成实验，保存脱敏样本与证据后，再允许运行方按 `QUERY_ID` 接入。
