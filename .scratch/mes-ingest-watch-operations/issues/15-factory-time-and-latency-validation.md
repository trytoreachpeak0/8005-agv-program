# 15 — 工厂 DATES 语义与跨地点延迟人工验证

**What to verify:** 在可访问 MES Oracle、Host、SQL Server 和远程 Watch 的现场环境，验证六类 DATES 的业务解释及 timeout 根因证据；只读取/采集，不优化或修改客户 MES SQL。

**Blocked by:** 01 — 时间契约; 03 — 耗时遥测; 12 — Swagger; 14 — 可部署升级包

**Status:** needs-info

- [ ] 每个 TASK_TYPE 至少抽样一条，与 MES 页面/客户 IT 对照：DATES=进入当前工序时间，STEP=下一工序
- [ ] 验证无 offset Oracle DATES 按 UTC+08:00 解释，Watch 在实际系统时区显示正确
- [ ] 在 A/B/C 地点链路分别采集 Oracle round、SQL Server read/write、Host endpoint、Watch total latency 和 correlation id
- [ ] 记录 `/api/demands` 首/后续页、DemandId exact/prefix、alerts、poll-health、ChangeFeed/Bootstrap 的响应时间和行数
- [ ] 验证 30 秒 Watch timeout 可配置且错误指出真实 endpoint/stage；不得只通过无限增大 timeout 判定通过
- [ ] 使用 Swagger + SharedSecret 完成人工 GET 测试，确认远程文档与鉴权可用
- [ ] 不执行 Oracle DDL、索引、视图或 SQL 重写；若 `stage=ORACLE_QUERY` 慢，将证据交客户 IT
- [ ] 将环境、样本、时间、结果和未决外部瓶颈追加到本票 Comments，不提交凭证/连接字符串

## Comments

- Human-only because factory MES and the A/B/C network topology are unavailable to automated agents and local CI.
- 2026-08-03: Implemented `pack/validation/Invoke-FactoryValidation.ps1` so an agent/operator can perform the mechanical portion instead of hand-copying results. Each A/B/C run is GET-only and captures paged demands/alerts, DemandId exact/prefix, poll-health, ChangeFeed/Bootstrap, Swagger/OpenAPI, elapsed time/row count/correlation id, DATES samples, Host Oracle/SQL/API telemetry, Watch total latency, redaction metadata, and SHA-256. Watch latency lines now carry `recordedAt` so a run can select its own observation window.
- 2026-08-03: Local File-source rehearsal passed: 17 requests, 671 VISIBLE rows, 6 TASK_TYPE DATES samples, 25 evidence files, GET-only manifest, and no injected-secret match. This proves the package flow only; it does **not** claim Oracle/SQL Server/A-B-C factory validation. Status moved to `needs-info` pending plant Oracle + SQL Server local configuration, A/B/C BaseUrl/access paths, SharedSecret availability, Host Event Log access, and Watch execution at each site.
- 2026-08-03: Used the supplied deployment configuration for an actual local Host/Watch check with remote Oracle and SQL Server; no credentials or connection strings were copied into the repo. Oracle Thin probe succeeded without Instant Client (about 3.8 s, 721 rows at probe time). A local Host Oracle poll also succeeded (about 3.9 s, 723 rows), exposed 658 VISIBLE demands with a subsequent page, returned all six TASK_TYPE values, and preserved sampled Oracle DATES as UTC+08:00 on a Windows `China Standard Time` machine. The actual WPF Watch process repeatedly completed `/api/contract`, `/api/demands`, `/api/alerts`, and `/api/poll-health` successfully with its configured 30 s timeout; the validation collector captured Watch total-latency records and complete request correlation ids.
- 2026-08-03: The supplied SQL Server connection string failed with SqlClient error 20 until a temporary, non-persisted `Encrypt=False` compatibility option was added; `TrustServerCertificate=True` alone did not make this legacy endpoint compatible with the current SqlClient default. With that temporary option, SQL open/read succeeded: the Host served 100 VISIBLE rows on the first page, reported a subsequent page, and read persisted `poll-health=SUCCESS`. The SQL-backed write/poll did not complete within the observation window after roughly 500 `SQL_QUERY` events, and emitted no completed `SQL_TRANSACTION`/`SQL_WRITE` evidence, so SQL write validation remains open. The original supplied configuration was not modified.
- 2026-08-03: This run validates one local Host/Watch topology only, per the supplied deployment description. It does not satisfy the required A/B/C distinct-site evidence, SharedSecret-authorized Swagger GET, intentional timeout-stage display, or the per-TASK_TYPE MES page/customer-IT confirmation that `DATES=current-step entry time` and `STEP=next process`. Those items remain `needs-info`; no factory sign-off is claimed.

