# 07 — 完成 IngestAlert 浏览与非模态详情

**What to build:** 让操作员以固定 100 行的服务端窗口查看活动和已解除 IngestAlert，按生产字段筛选、排序和分页，并在不中断主窗口刷新的情况下打开完整只读详情。

**Blocked by:** 01 — 建立 V2 四页产品壳与单 Host 会话闭环; 02 — 建立正式 Watch UI 测试宿主与 fake Host

**Status:** ready-for-agent

- [ ] 默认查询只取活动告警、limit 100 且不显式指定 sortBy，保留 Host 的 ERROR→WARNING、同级 LastSeenAt 倒序优先级。
- [ ] 支持活动/已解除、六类生产 code、ERROR/WARNING severity 和 LastSeenAt 起止筛选；FirstSeenAt 只显示和排序，不作为筛选条件。
- [ ] 草稿—查询—成功提交、服务端 allow-list 排序、重置、前后 cursor 翻页、当前页重取和 cursor 一次恢复遵循与 Demand 相同的原子窗口语义。
- [ ] 列表只把六类生产 code 作为 IngestAlert；HOST_UNREACHABLE 等 Watch 连接问题不得混入告警列表。
- [ ] 双击、Enter 或右键“查看详情”打开可调整大小的非模态窗口，完整显示告警生命周期、业务身份、结构化 details 和创建时间，主窗口继续可刷新。
- [ ] 当前页刷新时已打开详情按 AlertId 更新或明确显示历史快照；列表和详情均不提供确认、指派、备注、手工关闭或工单操作。
