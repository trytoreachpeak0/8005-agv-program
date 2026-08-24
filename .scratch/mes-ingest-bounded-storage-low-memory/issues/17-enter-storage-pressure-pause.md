# 17 — 实施 StoragePressurePause 与本地恢复

**What to build:** 实现 StoragePressurePause 的完整端到端状态机：数据库卷接近耗尽时在查询 MES 前暂停，并只允许数据库主机上的授权人员通过 MesIngestLocalAdministration 明确恢复。

**Blocked by:** 16 — 运行 Host 每小时有预算清理.

**Status:** ready-for-agent

- [ ] 从实际数据库文件解析并验证受监控卷，不允许用未解析环境变量、通配路径或错误磁盘代替。
- [ ] 剩余空间低于 15% 时产生严重存储告警，低于 10% 时在调用 MES 查询之前原子进入 StoragePressurePause。
- [ ] 暂停期间不调用 MES、不取得新 PollTrace、不推进缺席、GONE、归档或 TaskTypeProtection 恢复。
- [ ] Watch 诊断、最后成功投影和仍在窗口内的历史继续可读。
- [ ] ExternallyReadableDemandCatalog 与执行承诺读取返回 503 INGEST_NOT_CURRENT，不返回陈旧目录或空集合。
- [ ] 空间回升、清理成功、Host 重启或连续成功健康检查都不能自动恢复轮询。
- [ ] 本地恢复命令验证授权身份、精确目标数据库、当前暂停状态、安全空间和数据库可读写健康。
- [ ] 成功恢复审计执行身份、原因、HistoryEpoch、前后状态和 Host UTC；未授权、错误纪元/数据库或健康失败时保持暂停。
- [ ] Watch 不增加恢复按钮，远程 Host API 不暴露恢复写操作，直接修改 SQL 状态不构成合法确认。
- [ ] 可控卷空间与脚本化轮次端到端覆盖 15%/10% 边界、查询前门禁、重启、恢复、幂等和失败后不开放外部读取。
- [ ] 恢复后的下一轮遵守正常调度而非补跑，真实 SQL Server Tier 1 最终 Failed: 0、Skipped: 0。
- [ ] 使用可注入的卷空间读取 seam 和最小真实数据库健康检查，不实际填满磁盘、不等待空间变化，也不建设跨平台存储监控框架。
- [ ] 所有阈值、暂停、恢复、错误身份和审计分支先用确定性策略测试覆盖；真实 SQL Server 只运行一个暂停/恢复成功路径和一个代表性拒绝路径。
- [ ] 开发期运行聚焦状态机/CLI/HTTP 测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 60 分钟内完成并保持 Failed: 0、Skipped: 0。
