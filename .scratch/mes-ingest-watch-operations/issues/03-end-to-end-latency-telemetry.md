# 03 — Watch→Host→SQL Server→Oracle 分阶段耗时遥测

**What to build:** 为频繁 HTTP timeout 提供可归因证据，分别测量 Watch endpoint、Host request、SQL Server store 操作和 Oracle round，不再只显示笼统 `HTTP fetch failed`。

**Blocked by:** None — can start immediately

**Status:** done

- [x] 为一次 Watch refresh 和三个 HTTP 请求生成/传递 correlation id
- [x] 记录 endpoint、状态码、总耗时、超时/取消来源和 payload row count/bytes（不记录密钥）
- [x] 记录 SQL Server open/query/write/transaction 各阶段耗时和读取/写入行数
- [x] PollHealth/Alert 记录 Oracle 整轮耗时、返回行数及 `stage=ORACLE_QUERY` 失败阶段
- [x] 区分 Watch timeout、Host request abort、SQL timeout、Oracle query timeout 和 JSON parse failure
- [x] 日志输出可直接用于 A/B/C 三地现场对照，且不包含 SharedSecret、数据库密码或完整连接字符串
- [x] 测试稳定错误分类与 correlation id，不以真实网络延迟作为单元测试断言

## Comments

- MES SQL is immutable/read-only for this effort; telemetry may prove customer-side slowness but must not rewrite or DDL the Oracle query.
- 2026-07-31: Implemented staged latency telemetry (correlation id, Watch/Host/SQL/Oracle stages, PollHealth FailureStage+OracleDurationMs, secret-free logs). Review follow-ups: failure-path Watch telemetry, SQL_TIMEOUT wiring, SqlOpen timing on real SQL open, connection-string redaction.
