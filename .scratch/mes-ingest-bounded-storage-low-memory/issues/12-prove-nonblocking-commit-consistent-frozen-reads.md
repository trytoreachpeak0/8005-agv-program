# 12 — 快速验证冻结读取并发一致性

**What to build:** 在全部读取面迁移后复用 Tickets 06、09、10、11 已建立的提交一致机制，集中证明一次冻结响应完整属于一个 HistoryEpoch 和 ProjectionCommit；默认只补跨面验证证据，不再新建第二套读取架构。

**Blocked by:** 11 — 切换 PollTrace 与原始证据读取.

**Status:** ready-for-human

- [x] DemandSeries、ReadabilityAudit、ErrorSearch、Overview 和原始证据在并发提交栅栏下只能读到完整旧提交或完整新提交。
- [x] 实现不得默认使用覆盖整个用户调查的长 Serializable 事务。
- [x] 若使用 Snapshot Isolation，真实负载证据必须记录 tempdb 版本存储、锁等待、内存和数据库文件影响。
- [x] 若使用不可变快照读模型，提交、回收和读取身份必须原子且有界。
- [x] 慢冻结读取不能阻塞固定轮询，取消读取不能留下事务、连接或版本资源泄漏。
- [x] 直接复用前序票据已有 failpoint、read fence、snapshot 和取消夹具；除非测试先证明缺口，不新增通用并发基础设施。
- [x] 正常路径只运行一个覆盖全部读取面的聚焦并发矩阵和一次真实 SQL Server Tier 1，验证部分目标在 30 分钟内完成并保持 Failed: 0、Skipped: 0。
- [x] 若验证发现某个读取面缺口，失败并回到拥有该读取面的前序 ticket 做最小修复，不在本票扩张成跨模块重构。

## Comments

- 2026-08-24：新增独立的 `FrozenReadCommitConsistencyMatrixTests`，通过生产 Host 的正式 V2 HTTP API 集中覆盖 DemandSeries 列表/详情/精确计数/facet、ReadabilityAudit 列表/详情/精确计数/facet、ErrorSearch 列表/详情/facet、受限 raw-observations、PollTrace 原始多重集以及 WatchOverview。矩阵在同一 HistoryEpoch 内同时冻结八个历史读取，延长 Overview 的短 current-read fence，释放 Overview 后证明写入在其余冻结读取仍挂起时完成；随后逐响应验证完整旧提交与完整新提交业务值。
- 首次红跑证明 ErrorSearch 和 PollEvidence 尚未接入既有 `IProjectionReadBoundaryObserver`；最小修复只为这两个前序读面补充现有 fence 观察点，没有新增事务模式、锁、快照框架或通用并发基础设施。Ticket 16 的五测试发布门禁通过独立 Ticket 12 测试入口保持不变。
- 取消路径连续执行 5 次，每次确认活动用户事务为 0；之后提交与读取继续成功，数据库用户会话数不高于取消前基线。数据库同时证明 `snapshot_isolation_state = 0` 且 `is_read_committed_snapshot_on = false`，因此 Snapshot Isolation 条件未成立，不采集 tempdb 版本存储；现有按 ProjectionSequence 有界的不可变历史事实继续作为冻结读模型。
- 聚焦真实 SQL Server 16 / compatibility 160 矩阵：1 passed、0 failed、0 skipped。最终 Tier 1 `dotnet test MesIngest.Tests --verbosity minimal`：785 passed、0 failed、0 skipped，耗时 10m21s，低于 30 分钟预算。
- 未运行 Tier 2、Tier 3、Golden WPF、额外规模样本或 soak；本票未改 Watch UI，且没有出现扫描、版本存储、锁等待、内存、数据库增长或一致性风险信号来触发升级。
- `$code-review` 双轴复核后补齐 raw-observations、逐 fence/逐响应 HistoryEpoch、新提交业务值和重复取消资源基线；Spec 轴无剩余 finding。Standards 轴仅保留一个判断性 Middle Man 意见：独立 xUnit 入口委托既有并发夹具，以避免复制真实 SQL/Host 栅栏基础设施并保持 Ticket 16 精确五测试门禁。
