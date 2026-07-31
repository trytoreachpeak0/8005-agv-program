# 10 — 结构化 IngestAlert 问题实例、去重与解除

**What to build:** 把当前每轮追加的通用 Alert Message 改成 SQL Server 持久化的问题实例，提供 Details JSON、首次/最后发现、累计次数、活动/解除和统一严重等级。

**Blocked by:** 01 — 时间契约; 04 — 增量投影事务边界

**Status:** ready-for-agent

- [ ] 模型/表/API字段包含 AlertId、Code、Severity、业务键、Message、Details、FirstSeenAt、LastSeenAt、OccurrenceCount、IsActive、ResolvedAt
- [ ] 相同 Code + 业务身份 + details fingerprint 持续时只更新 last/count，不每轮新增
- [ ] fingerprint 改变时解除旧实例并建立新实例；条件消失时写 ResolvedAt
- [ ] Severity：POLL_FAILURE/POLL_INCOMPLETE/DUPLICATE_RECONCILE_KEY/PAUSED_ZERO_DROP/FIELD_DRIFT=ERROR；REAPPEAR_AFTER_GONE=WARNING
- [ ] PausedZeroDrop 进入与解除属于同一个 ERROR 实例；解除后不计当前 ERROR
- [ ] FIELD_DRIFT 对所有冻结属性一视同仁，Details 列出 field/frozen/observed
- [ ] DUPLICATE、POLL、REAPPEAR、PAUSE 各自填充 spec 规定的结构化详情，并清理敏感信息
- [ ] 活动实例永不清理；resolved 默认保留 365 天、可配置、0=永久
- [ ] Alert API 支持 active/time/code/severity 筛选、稳定排序和游标分页
- [ ] 迁移现有 IngestAlerts 时不伪造旧详情；旧行以 legacy summary 安全保留或按迁移方案归档

## Comments

- This ticket is the backend prerequisite for meaningful alert detail and reliable current banners.

