# 16 — 运行 Host 每小时有预算清理

**What to build:** 让 MesIngest Host 自己按小时以有预算的小事务清理到期 RawObservation 和 Series 历史，轮询始终优先，失败可以续跑且可被运维观察。

**Blocked by:** 15 — 原子清理 Series 并永久保留墓碑.

**Status:** ready-for-agent

- [ ] 单实例 Host 后台流程默认每小时检查一次，不依赖 SQLSERVERAGENT 或外部 Windows 计划任务。
- [ ] 每批具有明确行数和时间预算；真实基线选择并冻结安全默认值，但不得改变 30 天领域保留语义。
- [ ] RawObservation 和 Series 清理均幂等、可取消、失败可续，单个 Series 的墓碑事务不能被批次预算拆开。
- [ ] 轮询到期时清理让出资源，不与投影形成无界锁等待或并发清理实例。
- [ ] 清理进度、最后成功、删除计数、earliest available、失败原因和下一次检查时间可观测。
- [ ] 清理失败形成 Current Attention，但在未达到存储阈值时不自动暂停 MES 轮询。
- [ ] 使用现有 TimeProvider 和最小到期批次加速跨越每小时间隔，不真实等待一小时、不生成规模历史，也不建立通用作业调度平台。
- [ ] 只验证一个正常批次、一个预算中断续跑和一个失败恢复路径；其它边界由策略级确定性测试覆盖。
- [ ] 开发期运行聚焦 cleanup/HostedService/Attention 测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0。
