# MES Lab 离线工具链

该工具链把“联网仓库准备查询、隔离工厂执行、结果回仓导入”拆成三个步骤。构建
bundle 和查看命令帮助均不需要安装 Oracle 驱动；只有 `run-factory` 真正连接时
才会导入 `oracledb`。

## 查询约定

每个查询放在 `mes/queries/<query-dir>/`：

```text
query.sql
query.toml
```

最小 `query.toml` 示例：

```toml
id = "MES_TASK_UNION"
title = "MES 五类任务合并查询"
sql = "query.sql"
readonly = true
parameters = ["FACTORY_CODE"]
expected_columns = ["TASK_ID", "SOURCE_TYPE"]
```

无参查询使用 `parameters = []`。工具只接受单条 `SELECT` 或 `WITH`；校验会先剥离
注释、字符串和引号标识符，再检查分号、入口语句和危险关键字。DML、DDL、PL/SQL、
事务控制、锁语句及 `DBMS_*` 调用均会被拒绝。

## 1. 构建 bundle

```powershell
python mes/tools/mes_lab.py build-bundle `
  --queries-root mes/queries `
  --query-id MES_TASK_UNION `
  --output C:\transfer\mes-bundle
```

不指定 `--query-id` 时打包目录中的全部正式查询。也可用
`--experiment experiment.toml`；除 `query_ids` 外，实验可通过
`source_manifests` 引用客户来源目录中的只读查询清单。来源 SQL 只会被复制进本次
传输 bundle，不会成为应用运行时查询。
输出目录必须不存在。工具先在临时目录生成文件，再放置最终 bundle，并写入
`bundle-manifest.json`、SQL/查询清单哈希，同时包含自带的 `runner/`、占位配置和
`requirements.txt`。bundle 是一次性传输产物，不是第二编辑源。

## 2. 工厂执行

进入 bundle 后安装依赖，再将配置复制到 bundle 外的受控目录：

```powershell
python -m pip install -r requirements.txt
copy config.example.ini C:\private\mes-config.ini
```

填写本地值后不要把配置带回仓库。当前 MES 若为 Oracle 11g，应保持 `mode=thick` 并配置
`instant_client_dir`（或环境变量 `ORACLE_CLIENT_LIB_DIR`）；`mode=thin` 只适用于
驱动支持的较新 Oracle 版本。

```powershell
python runner/mes_lab.py run-factory `
  --bundle . `
  --config C:\private\mes-config.ini `
  --output-root C:\transfer\runs `
  --query-id MES_TASK_UNION `
  --params-json '{"FACTORY_CODE":"<VALUE>"}' `
  --experiment-record '@C:\private\experiment-record.json'
```

参数也可写为 JSON 文件路径或 `@C:\private\params.json`。多查询需要不同参数时，
JSON 可按查询 ID 嵌套。`--experiment-record`（及废弃别名 `--approval-json`）为**可选**，
用于记录本次自跑实验（谁、何时、范围、备注），**不再要求客户批准**，也禁止写入凭据。
每次执行生成唯一 `run-...` 目录，内含 `run-manifest.json`、`execution-log.md` 和 `results/*.csv`。

可选实验能力：

```powershell
# MES_TASK_UNION phase1（固定单轮）
python runner/mes_lab.py run-factory ... --phase1

# 合并查询与六客户源对比（自动同时执行 MES_TASK_UNION）
python runner/mes_lab.py run-factory ... `
  --compare-sources `
  CUSTOMER_BASELINE_DIE_TO_WIRE_STAGING `
  CUSTOMER_BASELINE_DIE_TO_OVEN `
  CUSTOMER_BASELINE_WIRE_TO_GATE `
  CUSTOMER_BASELINE_WIRE_TO_OPTICAL `
  CUSTOMER_BASELINE_STAGING_TO_WIRE `
  CUSTOMER_BASELINE_WIRE_TO_NITROGEN

# 性能轮次
python runner/mes_lab.py run-factory ... --query-id MES_TASK_UNION `
  --rounds 3 --wait-seconds 10
```

配置值、密码和参数值不会写入 manifest 或日志。连接建立后工具声明 Oracle 只读
事务，并且仍会在执行前重新校验每个 SQL。

## 3. 导入运行结果

把原 bundle 和 run 目录带回仓库环境：

```powershell
python mes/tools/mes_lab.py import-run `
  --bundle C:\transfer\mes-bundle `
  --run-dir C:\transfer\runs\run-... `
  --mes-root mes
```

导入会验证 bundle manifest、SQL、query.toml 和所有 CSV 的 SHA-256。运行证据放到
`mes/evidence/runs/<run-id>`；已有同名 run 时拒绝覆盖。每个查询最后一轮结果会更新：

```text
mes/samples/<query-id>/latest.csv
mes/samples/<query-id>/latest.md
mes/samples/<query-id>/latest.meta.json
```

导入 `MES_TASK_UNION` 时还会使用当前
`mes/reference/package-basket-capacity.csv` 离线生成 `package-coverage/`，
其中包含未匹配 PACKAGE 清单、前缀命中清单、汇总和分析哈希。

## 依赖与测试

工具要求 Python 3.11 或更高。工厂执行环境另行安装：

```powershell
python -m pip install oracledb
```

本地单元测试不连接数据库：

```powershell
python -m unittest discover -s mes/tests -p "test_*.py"
```
