# 09 — ExternallyReadableDemandCatalog 与 reference consumer

**What to build:** 让外部消费者能够通过 MesIngest 的当前完整 `ExternallyReadableDemandCatalog` 安全发现可读取的运输需求，并以一个最小 reference consumer 证明这是一份可随时丢弃、无需 ChangeFeed 或 Cursor 恢复的当前目录。目录集中执行 `ExternallyReadableDemand` 资格规则，发布全范围事实和单调 `CatalogRevision`；reference consumer 在执行承诺点最终重读候选并保存不可变 `AcceptedDemandSnapshot` 与可靠 `OrderIntent`，但不把 Dispatch 的筛选、取消或派车状态带回 MesIngest。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；04 — 处理重复键与同 SUBLOT 多 WorkType 冲突；06 — 实现十二小时归档与 LongGoneButVisible

**Status:** ready-for-human

- [x] 经正式 Host 和持久化投影读取时，目录只包含同时满足 `VISIBLE`、唯一原始观测、全部必填字段有效、无当前数据异常且所属 Series 未归档的 Demand；不合格 Demand 仍可从 Watch 运维投影追查。
- [x] 目录项可观察到稳定的 DemandId、SeriesId、TransportDemandKey、世代、DemandRevision、时间与当前可信 MES 字段，并按 DemandId 稳定输出；目录拒绝 WorkType、AREA、车辆、地图或站点等 Dispatch 范围参数。
- [x] 首次读取返回完整目录及 `CatalogRevision`；成员进入、退出或成员业务值变化才使修订递增，无变化轮次不递增，同一轮多个成员变化也只递增一次。
- [x] 以已有修订进行条件读取时，未变化目录返回 `304 Not Modified` 且不传输正文；变化后返回同一已提交修订对应的完整正文，不出现新修订配旧成员或旧字段。
- [x] reference consumer 清空缓存或重启后只靠完整目录即可恢复当前视图，不读取或持久化 DemandChangeFeed、Feed Sequence、bootstrap high-watermark 或同步 Cursor。
- [x] reference consumer 在执行承诺点最终重读 Demand：资格、Revision 或值已变化时可观察到明确拒绝或重新决策；接受成功时保存的 `AcceptedDemandSnapshot` 不会被后续目录刷新改写，`OrderIntent` 以稳定幂等身份处理结果未知。
- [x] 端到端契约证据覆盖唯一行、字段异常与恢复、重复键、多 WorkType、归档后可见、实时字段变化和无变化轮次，并证明 MesIngest 不读取或修改消费者的取消抑制与派车状态。

## Implementation evidence

- 已实现 `tracer.9` / schema 9 的持久化完整目录、集中资格判定、按业务变化单调递增的 `CatalogRevision` / `DemandRevision`、同一事务条件读取，以及正式 Host 的全局无筛选 API、弱 ETag 与无正文 `304`。
- 已新增独立 `MesIngest.ReferenceConsumer` 边界：缓存可丢弃，承诺点无条件最终重读，原子持久化不可变 `AcceptedDemandSnapshot` 与 `OrderIntent`，UNKNOWN 结果只复用同一稳定幂等键收敛；消费者状态不被 MesIngest 引用。
- ticket09 全边界聚焦运行结果为 33 passed、0 failed、0 skipped；消费者与 HTTP adapter 的 18 项以及正式 SQL/Host 的 15 项全部通过。
- 正式 SQL Server 2022 / compatibility 160 门禁 `Invoke-Ticket09SqlServerGate.ps1 -ExpectedProductMajor 16 -ExpectedCompatibilityLevel 160`：15 passed、0 failed、0 skipped；TRX 为 `.artifacts/ticket09-tests/ticket09-externally-readable-catalog-sqlserver.trx`，测试隔离库已清理。
- 两轴 code review 以 `30864c8` 为固定点完成复核：Spec 与 Standards 均无剩余 actionable finding；未改 WPF/UI 文件。
- Release solution build 0 errors；全量测试 586 passed、19 个既有 SQL fixture 环境 skip、1 个既有 `LatencyTelemetryTests` 墙钟保留测试失败，均不在 ticket09 变更面。
