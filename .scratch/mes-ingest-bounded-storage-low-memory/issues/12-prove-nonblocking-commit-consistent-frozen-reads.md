# 12 — 快速验证冻结读取并发一致性

**What to build:** 在全部读取面迁移后复用 Tickets 06、09、10、11 已建立的提交一致机制，集中证明一次冻结响应完整属于一个 HistoryEpoch 和 ProjectionCommit；默认只补跨面验证证据，不再新建第二套读取架构。

**Blocked by:** 11 — 切换 PollTrace 与原始证据读取.

**Status:** ready-for-agent

- [ ] DemandSeries、ReadabilityAudit、ErrorSearch、Overview 和原始证据在并发提交栅栏下只能读到完整旧提交或完整新提交。
- [ ] 实现不得默认使用覆盖整个用户调查的长 Serializable 事务。
- [ ] 若使用 Snapshot Isolation，真实负载证据必须记录 tempdb 版本存储、锁等待、内存和数据库文件影响。
- [ ] 若使用不可变快照读模型，提交、回收和读取身份必须原子且有界。
- [ ] 慢冻结读取不能阻塞固定轮询，取消读取不能留下事务、连接或版本资源泄漏。
- [ ] 直接复用前序票据已有 failpoint、read fence、snapshot 和取消夹具；除非测试先证明缺口，不新增通用并发基础设施。
- [ ] 正常路径只运行一个覆盖全部读取面的聚焦并发矩阵和一次真实 SQL Server Tier 1，验证部分目标在 30 分钟内完成并保持 Failed: 0、Skipped: 0。
- [ ] 若验证发现某个读取面缺口，失败并回到拥有该读取面的前序 ticket 做最小修复，不在本票扩张成跨模块重构。
