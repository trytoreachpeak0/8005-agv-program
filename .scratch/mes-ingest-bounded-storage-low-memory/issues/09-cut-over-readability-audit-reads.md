# 09 — 切换 ReadabilityAudit 当前与冻结读取

**What to build:** 让 ExternalReadabilityAudit 的当前结论与冻结调查走分离且有界的物理路径，同时保持列表、分面、计数和详情属于同一审计快照。

**Blocked by:** 07 — 切换目录、关注与概览当前读取.

**Status:** ready-for-agent

- [ ] 当前资格结论从当前 Demand、Series、条件和资格投影读取，不通过完整历史重算。
- [ ] 冻结列表、精确总数、原因分面、稳定分页与详情绑定同一 HistoryEpoch 和 ProjectionCommit。
- [ ] 详情保持完整 ReadabilityBlocker 集合、可信字段或冲突证据、Series、PollTrace 与 CatalogRevision。
- [ ] snapshot/cursor 跨纪元、提交、筛选、AREA、顺序或页大小复用时被明确拒绝。
- [ ] 并发投影不能让列表结论与详情理由来自不同提交。
- [ ] 复用 Tickets 06–07 的 current/historical read context、snapshot identity 和两个固定小样本，不新建审计专用读取框架或规模生成器。
- [ ] 真实 SQL Server 实际计划证明当前资格路径不访问 DemandRawObservation 历史；冻结详情只按 Demand/Series 对象键有界读取。
- [ ] 正常实现只运行聚焦 ReadabilityAudit 测试和一次最终真实 SQL Server Tier 1，验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。
- [ ] 只有计划扫描/排名历史、逻辑读随小样本增长、出现异常 grant/spill 或快照不一致时，才升级更大样本或额外并发运行。
