# MES五类任务合并查询测试脚本说明（Python 3.14.6）

## 1. 适用环境

- 操作系统：Windows
- Python：**必须是 3.14.x，目标版本 3.14.6**
- 依赖：`oracledb`（MES 若为 Oracle 11g，必须用 Thick 模式 + Instant Client）
- 权限：仅 SELECT，脚本会拒绝非只读 SQL

## 2. 拷贝到远程机

把整个文件夹拷过去，至少包含：

```text
MES五类任务合并查询/
  MES五类任务合并查询.sql
  run_mes_query_test.py
  requirements.txt
  config.example.ini
  README_测试脚本.md
  sql/original_queries/*.sql
```

不要把含真实密码的 `config.ini` 提交到公共仓库。

## 3. 安装

在远程机打开命令行，进入本目录后执行：

```bat
python --version
python -m pip install -r requirements.txt
python -c "import oracledb; print(oracledb.__version__)"
```

期望：

- `python --version` 显示 `Python 3.14.6`
- `oracledb` 能正常 import，版本建议 `3.4.2+`（推荐 `4.0.1+`）

如果 `python` 不是 3.14，可改用：

```bat
py -3.14 --version
py -3.14 -m pip install -r requirements.txt
py -3.14 run_mes_query_test.py
```

### 3.1 若报 DPY-3010（必须装 Instant Client）

报错含义：当前 MES Oracle 版本偏旧（常见 11.2），`oracledb` 默认 Thin 模式不支持，需要 Thick 模式。

1. 下载 Oracle Instant Client（Windows x64，建议 **19c Basic** 或 Basic Light）
2. 解压到固定目录，例如：`C:\oracle\instantclient_19_26`
3. 确认目录里有 `oci.dll`
4. 在 `config.ini` 配置：

```ini
mode = thick
instant_client_dir = C:\oracle\instantclient_19_26
```

也可把该目录加入系统 PATH，然后只保留 `mode=thick`。

验证 Thick 模式：

```bat
python -c "import oracledb; oracledb.init_oracle_client(lib_dir=r'C:\oracle\instantclient_19_26'); print('thin=', oracledb.is_thin_mode())"
```

期望输出：`thin= False`

## 4. 配置连接

```bat
copy config.example.ini config.ini
```

编辑 `config.ini`：

```ini
[oracle]
host = 172.19.1.152
port = 1521
service_name = SQMES
user = fwmes
password = fwmes
timeout_seconds = 30
mode = thick
instant_client_dir = C:\oracle\instantclient_19_26
```

## 5. 运行

一键跑完全部阶段（约：1次合并 + 5次独立 + 10轮合并，中间每轮等待10秒）：

```bat
python run_mes_query_test.py
```

可选参数：

```bat
python run_mes_query_test.py --phase all
python run_mes_query_test.py --phase 1
python run_mes_query_test.py --phase 2
python run_mes_query_test.py --phase 3
python run_mes_query_test.py --rounds 10 --wait-seconds 10 --timeout-seconds 30
```

## 6. 输出文件

运行后生成 `output/`：

| 文件 | 内容 |
| --- | --- |
| `MES五类任务合并查询result.csv` | 阶段1完整结果 |
| `MES五类任务合并查询测试记录.md` | 开始/完成时间、耗时、行数、错误 |
| `phase2_original_counts.csv` | 5组独立SQL行数与耗时对比 |
| `phase3_perf_rounds.csv` | 10轮性能测试 |
| `test_summary.md` | 质量检查与验收汇总 |

把整个 `output/` 拷回本机即可继续分析。

## 7. 安全提醒

- 严禁对 MES 执行 INSERT / UPDATE / DELETE / DDL
- 本脚本启动时会检查 SQL 是否只读
- 当前账号可能有写权限，但仍必须只读使用
- 不要在公共聊天或公共仓库中传播 `config.ini` 明文密码
