# 09 — ExternallyReadableDemandCatalog 与 reference consumer

**What to build:** 让外部消费者能够通过 MesIngest 的当前完整 `ExternallyReadableDemandCatalog` 安全发现可读取的运输需求，并以一个最小 reference consumer 证明这是一份可随时丢弃、无需 ChangeFeed 或 Cursor 恢复的当前目录。目录集中执行 `ExternallyReadableDemand` 资格规则，发布全范围事实和单调 `CatalogRevision`；reference consumer 在执行承诺点最终重读候选并保存不可变 `AcceptedDemandSnapshot` 与可靠 `OrderIntent`，但不把 Dispatch 的筛选、取消或派车状态带回 MesIngest。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible

**Status:** ready-for-agent

- [ ] 经正式 Host 和持久化投影读取时，目录只包含同时满足 `VISIBLE`、唯一原始观测、全部必填字段有效、无当前数据异常且所属 Series 未归档的 Demand；不合格 Demand 仍可从 Watch 运维投影追查。
- [ ] 目录项可观察到稳定的 DemandId、SeriesId、TransportDemandKey、世代、DemandRevision、时间与当前可信 MES 字段，并按 DemandId 稳定输出；目录拒绝 WorkType、AREA、车辆、地图或站点等 Dispatch 范围参数。
- [ ] 首次读取返回完整目录及 `CatalogRevision`；成员进入、退出或成员业务值变化才使修订递增，无变化轮次不递增，同一轮多个成员变化也只递增一次。
- [ ] 以已有修订进行条件读取时，未变化目录返回 `304 Not Modified` 且不传输正文；变化后返回同一已提交修订对应的完整正文，不出现新修订配旧成员或旧字段。
- [ ] reference consumer 清空缓存或重启后只靠完整目录即可恢复当前视图，不读取或持久化 DemandChangeFeed、Feed Sequence、bootstrap high-watermark 或同步 Cursor。
- [ ] reference consumer 在执行承诺点最终重读 Demand：资格、Revision 或值已变化时可观察到明确拒绝或重新决策；接受成功时保存的 `AcceptedDemandSnapshot` 不会被后续目录刷新改写，`OrderIntent` 以稳定幂等身份处理结果未知。
- [ ] 端到端契约证据覆盖唯一行、字段异常与恢复、重复键、多 WorkType、归档后可见、实时字段变化和无变化轮次，并证明 MesIngest 不读取或修改消费者的取消抑制与派车状态。
