# 15 — 工厂 DATES 语义与跨地点延迟人工验证

**What to verify:** 在可访问 MES Oracle、Host、SQL Server 和远程 Watch 的现场环境，验证六类 DATES 的业务解释及 timeout 根因证据；只读取/采集，不优化或修改客户 MES SQL。

**Blocked by:** 01 — 时间契约; 03 — 耗时遥测; 12 — Swagger; 14 — 可部署升级包

**Status:** ready-for-human

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

