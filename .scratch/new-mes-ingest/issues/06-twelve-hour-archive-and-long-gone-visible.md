# 06 — 实现十二小时归档与 LongGoneButVisible

**What to build:** 作为运维工程师和外部消费者，我希望连续 GONE 满十二小时的 Series 只在下一次可信成功轮次中不可逆归档，而归档后再次出现的真实 MES 数据仍可在运维读取中追踪、却永远不会重新成为外部可读候选，以便长期结束的生命周期既不丢证据也不被错误复活。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；05 — 实现 RestartBarrier、GONE 与归档前重现世代

**Status:** ready-for-agent

- [ ] 十二小时连续 GONE 从 GoneConfirmedAt 的 Host UTC 证据计算，不使用 MesSourceDate、Watch 本机时间或单纯墙钟定时器；边界前的成功轮次不归档，达到边界后的下一轮具有缺席权威的完整 SUCCESS 才归档。
- [ ] FAILURE、INCOMPLETE、RestartBarrier 或受保护而没有缺席权威的轮次既不归档，也不被当作推进归档的业务证据；Host 重启后仍按持久化的 GoneConfirmedAt 正确计算。
- [ ] 归档转换不可逆并产生带 PollTrace、ProjectionCommit 和严格 SeriesSequence 的生命周期事件；正式 API 清楚区分 Tracking、GONE 与 Archived，而不是从当前行是否存在推断状态。
- [ ] 归档后同键重现时保留原 SeriesId，创建新的 DemandId 和世代并连接 predecessor；新 Demand 在 WatchDemandProjection 中可见，状态明确为 LongGoneButVisible，原归档事实不被撤销。
- [ ] 归档后重现形成 LONG_GONE_BUT_VISIBLE 当前错误、历史期间和稳定不可读原因；即使后续观测唯一且全部字段有效，该 Demand 也永久不能进入外部可读目录。
- [ ] 达到边界、尚未达到边界、无权威轮次、归档、归档后重现和再次重启均通过真实 SQL Server → 正式 API seam 验收，且生命周期、世代、错误和不可读结论来自同一冻结投影提交。

