# 第 4 票 MES 字段边界证据

本票使用仓库中已封存的客户 MES 运行
`mes/evidence/runs/run-20260724T065749Z-c9b74a48bb/results/MES_TASK_UNION-round-*.csv`
作为真实值分布证据。该运行含 10 个完整轮次、6720 行，逐字段最大字符数/UTF-8 字节数为：

| 字段 | 最大字符数 | 最大 UTF-8 字节数 |
| --- | ---: | ---: |
| TASK_TYPE | 19 | 19 |
| SUBLOT | 14 | 14 |
| AREA | 7 | 7 |
| EQP | 8 | 8 |
| STEP | 6 | 18 |
| DATES 原文 | 19 | 19 |
| PACKAGE | 48 | 48 |

源数据库字典证据
`mes/evidence/legacy/schema-introspection-before-2026-07-16/查询MES字段类型与长度result.csv`
还声明 LOT 40 byte、AREA 30 byte、EQP 50 byte、STEP 最大 255 byte。历史说明明确要求 STEP
不能只按短样本设计。

因此 V2 schema 对 WorkType 保持 128 字符、Sublot 保持 256 字符；AREA、EQP、STEP、PACKAGE
统一采用 512 字符上限，覆盖已知源声明和客户实测并留有至少约 2 倍于最大已声明 STEP 的字符包络；
DATES 原文采用 128 字符。上限在 SQL 参数创建前验证，超界轮次以具名
`ArgumentOutOfRangeException` 失败；测试同时证明 512 字符 Unicode 原文逐字符往返且 513 字符不建库、
不写 PollTrace，因此不存在 SQL 截断、回填或任选。
