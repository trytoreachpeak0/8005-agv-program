# 19 — 实施非计划历史重置确认

**What to build:** 当无备份数据库不可恢复丢失时，让系统建立新 HistoryEpoch、阻断外部当前读取，并要求授权运维人员明确接受旧历史与墓碑已丢失的风险后再开放。

**Blocked by:** 17 — 实施 StoragePressurePause 与本地恢复.

**Status:** ready-for-agent

- [ ] 系统区分普通 Host 重启、计划空库切换和非计划不可恢复重建；普通重启不换纪元。
- [ ] 非计划重建创建新 HistoryEpoch，并记录需要 HistoryResetAcknowledgement 的持久状态。
- [ ] 确认前 ExternallyReadableDemandCatalog 和执行承诺读取持续返回 503 INGEST_NOT_CURRENT，诊断与新纪元建立进度仍可读。
- [ ] RestartBarrier、成功轮次、磁盘恢复或服务重启都不能代替 HistoryResetAcknowledgement。
- [ ] 本地管理命令验证授权身份和目标 HistoryEpoch，并审计旧墓碑不可恢复的风险接受、前后状态与时间。
- [ ] 确认不声称恢复旧墓碑；确认后只在新纪元开放，旧 snapshot、cursor、cache 和条件身份全部被拒绝。
- [ ] 复用 Ticket 17 的 MesIngestLocalAdministration、审计、503 和空库 bootstrap seam，不新建第二套管理命令或恢复状态框架。
- [ ] 三种启动路径、错误纪元、重复确认和 reference consumer 行为先用最小空库与确定性状态测试覆盖；不删除真实业务库、不生成历史数据。
- [ ] 真实 SQL Server 只运行一个非计划重建/确认成功路径和一个错误纪元拒绝路径；开发期用聚焦测试，关闭时运行一次 Tier 1。
- [ ] 正常验证目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0；只有纪元持久化或 503 边界无法由最小空库证明时才扩大矩阵。
