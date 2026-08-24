# 11 — 切换 PollTrace 与原始证据读取

**What to build:** 让 PollTrace 和 DemandRawObservation 通过明确对象边界读取，并为后续历史过期提供统一的最早可用边界与存在性判断。

**Blocked by:** 10 — 切换 ErrorSearch 历史读取.

**Status:** ready-for-agent

- [ ] PollTrace 读取按稳定 PollTraceId 定位，不扫描其它轮次或 WatchRefreshTrace。
- [ ] 原始证据只能按明确 PollTrace、ProjectionCommit、Series/Demand 或 evidence 身份有界展开。
- [ ] 保留期内返回原始多重集合，不任选、补值、截断或用当前投影替换历史证据。
- [ ] 读取内部绑定 HistoryEpoch 与 ProjectionCommit，并能区分当前存在、曾存在但不可用和从未存在。
- [ ] 所有历史读取共享一个可查询的 earliest available Host UTC 边界来源。
- [ ] 复用 Ticket 10 的 historical read context、两个固定小样本和执行计划入口，不新建原始证据专用分页/身份框架。
- [ ] 真实 SQL Server 证明 PollTrace 与原始证据只按稳定对象键 seek，逻辑读、内存授予和响应大小具有与总历史规模无关的明确上限。
- [ ] 正常实现只运行聚焦 PollTrace/raw evidence/契约测试和一次最终真实 SQL Server Tier 1，验证部分目标在 30 分钟内完成并保持 Failed: 0、Skipped: 0。
- [ ] 只有实际计划扫描无关轮次、对象响应失去上限或 earliest available 身份不一致时，才升级更大样本。
