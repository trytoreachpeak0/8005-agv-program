# 14 — 一致 WatchOverviewSnapshot

**What to build:** 让现场运维工程师通过一个原子 `WatchOverviewSnapshot` 在十秒内判断需求系列、外部可读资格、活动错误、当前关注项和近期动态的整体态势。所有 Host 业务摘要必须来自同一个 ProjectionCommit 身份和时间；AREA 只限定需求系列与资格摘要，错误与当前关注保持全局，Watch 的本地配置名称和状态不得伪装成 Host 快照事实。

**Blocked by:** 08 — 提供 DemandSeries 冻结快照列表与详情；10 — ReadabilityAuditSnapshot 查询与详情；11 — ErrorSearchAsOf 列表、窗口与分面；13 — CurrentIngestAttention 当前关注读取

**Status:** ready-for-agent

- [ ] 单次读取原子返回一个可识别的 ProjectionCommit 与快照时间，需求系列、资格、错误、当前关注及动态摘要全部声明并实际使用该身份；并发新轮次提交不会造成卡片跨提交撕裂。
- [ ] Series 摘要在当前 MesArea 范围内返回精确去重 Series 总数、Tracking/Archived 等生命周期分面，并单列 GONE 与 LongGoneButVisible 关注数量；可能重叠的分面不会被机械相加。
- [ ] 资格摘要在同一提交及 AREA 范围内返回精确 Demand 总数、READABLE 与 NOT_READABLE 数，三者使用 `ReadabilityAuditSnapshot` 的 Demand 世代口径而不是 Series 或目录条目估算。
- [ ] 错误摘要不受 AreaFilterProfile 影响，返回当前 ACTIVE Series 精确数及截至概览快照最近 7×24 小时曾命中的去重 Series 数；当前关注摘要返回精确项数以及类型和严重度构成。
- [ ] 概览动态只来自 Series 生命周期、错误期间开闭、轮询失败/恢复和 TaskTypeProtection 等真实状态转换；仅返回最近 24 小时最新五条，并按发生时间降序及稳定事件标识排序，不以每轮观测或静态计数变化制造动态。
- [ ] 无近期动态时明确表达“近期无重点动态”而不宣称系统健康；零错误、零阻断或连接成功也不会单独被提升为整体健康结论。
- [ ] 各摘要和动态携带明确的下钻查询意图，进入目标读取时从第一页开始并显式表达 AREA、ACTIVE 或最近 7 天等条件，不依赖目标页默认值或沿用旧游标。
- [ ] AreaFilterProfile 名称、文件状态和本地更新时间不进入 Host 业务快照；改变 MesArea 范围只改变 Series 与资格相关摘要，不改变错误、当前关注、外部资格或 `CatalogRevision`。
- [ ] 在同一提交制造 Series、资格、错误、关注与动态变化，并在读取期间提交下一轮的集成测试，证明响应要么完整属于旧提交、要么刷新后完整属于新提交，不出现混合快照。
