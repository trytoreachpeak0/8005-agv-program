# 10 — 切换 ErrorSearch 历史读取

**What to build:** 让 ErrorSearch 的列表、分面、活动状态、分页和详情从按快照有界的历史路径读取，避免把当前行和事件历史拼成不一致结果。

**Blocked by:** 09 — 切换 ReadabilityAudit 当前与冻结读取.

**Status:** ready-for-agent

- [ ] ErrorSearchAsOf、时间窗口、筛选、稳定顺序和 cursor 绑定同一 HistoryEpoch 与 ProjectionCommit。
- [ ] 列表、分面、ACTIVE/ENDED 状态和详情解释同一冻结历史，不泄漏快照后的新开、变化或关闭。
- [ ] 查询先按服务端条件缩小对象和页，再读取匹配 Series 的有界证据，不下载或排名全部原始历史。
- [ ] 24 小时、7 天、30 天和全部可用历史继续使用 Host UTC 半开区间语义。
- [ ] 复用既有 historical read context、snapshot codec、cursor 和 Ticket 02 固定分布，只建立两个不超过 250,000 条 RawObservation 的确定性样本。
- [ ] 实际计划证明列表先分页缩小 Series、详情只按命中对象读取；不以完整 30 天物化、客户端去重或本地分面替代。
- [ ] 正常实现只运行聚焦 ErrorSearch 列表/详情/契约测试和一次最终真实 SQL Server Tier 1，验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。
- [ ] 只有页或对象读取不再有界、计划扫描全部历史、参数计划退化或证据不完整时，才升级更大样本。
