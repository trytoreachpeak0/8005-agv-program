# 16 — 运行 Host 每小时有预算清理

**What to build:** 让 MesIngest Host 自己按小时以有预算的小事务清理到期 RawObservation 和 Series 历史，轮询始终优先，失败可以续跑且可被运维观察。

**Blocked by:** 15 — 原子清理 Series 并永久保留墓碑.

**Status:** ready-for-human

- [x] 单实例 Host 后台流程默认每小时检查一次，不依赖 SQLSERVERAGENT 或外部 Windows 计划任务。
- [x] 每批具有明确行数和时间预算；真实基线选择并冻结安全默认值，但不得改变 30 天领域保留语义。
- [x] RawObservation 和 Series 清理均幂等、可取消、失败可续，单个 Series 的墓碑事务不能被批次预算拆开。
- [x] 轮询到期时清理让出资源，不与投影形成无界锁等待或并发清理实例。
- [x] 清理进度、最后成功、删除计数、earliest available、失败原因和下一次检查时间可观测。
- [x] 清理失败形成 Current Attention，但在未达到存储阈值时不自动暂停 MES 轮询。
- [x] 使用现有 TimeProvider 和最小到期批次加速跨越每小时间隔，不真实等待一小时、不生成规模历史，也不建立通用作业调度平台。
- [x] 只验证一个正常批次、一个预算中断续跑和一个失败恢复路径；其它边界由策略级确定性测试覆盖。
- [x] 开发期运行聚焦 cleanup/HostedService/Attention 测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。

## Comments

- Host 注册唯一 `HistoryCleanupHostedService`，用既有 `TimeProvider` 按固定小时边界运行且不补跑错过时隙；现场 `SQLSERVERAGENT` 为 `Stopped / Manual`，实现没有 SQL Agent、Windows Task Scheduler 或通用作业平台依赖。
- 冻结默认值为每小时 210,000 个 RawObservation、25 个完整 Series、15 秒 elapsed budget；600 行/14 秒真实摄取基线给行预算保留超过 30% 余量，真实 SQL 探针证明 25 个完整 Series 事务在 15 秒内提交。30×24 小时 Raw/Series 领域窗口未改变。
- 单个 PollTrace 在摄取验证和 schema check 中硬限制为 25,000 行；Raw 清理事务再限制 50 个 PollTrace，Series 始终沿用票 15 的单图原子墓碑事务。预算、时间或取消只在事务之间生效，失败/中断可自然续跑。
- 共享 poll-priority gate 保证轮询先行并阻止并发 cleanup；进度状态位于独立 `HistoryCleanupState` 单行表，避免 Begin/Complete/Fail 与投影的 `SchemaInfo` 热点竞争。终态 best-effort 持久化有 1 秒上限，不会把 Host shutdown 变成无界等待。
- Current Attention/API 持久公开 last attempt/success、per-run/cumulative counts、earliest available、next check、脱敏 failure reason 以及稳定的 failure time/run identity；失败后的真实 SQL 投影仍成功提交，`INTERRUPTED` 重试不会漂移原告警，真正成功后才清除。
- 聚焦真实 SQL/HostedService/Attention/schema/OpenAPI/contract 测试最终 31/31 通过，0 跳过；策略突变检查 3/3 被杀死。双轴复核最终均为 `No findings`。Ticket 20 仍按其既定边界负责最终 exact contractVersion/capability 整包切换；本票只把 exact schema identity/freeze 提升到 25。
- 首次完整门禁暴露一个旧 Watch 测试仍冻结四类 Attention（818 通过、1 失败、0 跳过）；测试契约更新为五类后，正式关闭门禁 `dotnet test MesIngest.Tests` 在真实 SQL Server ProductMajor 16 / compatibility 160 上 819 通过、0 失败、0 跳过，10 分 53 秒。未运行 Tier 2/3：本票未修改 WPF/XAML/布局/基线，且未请求 Golden Renderer。
