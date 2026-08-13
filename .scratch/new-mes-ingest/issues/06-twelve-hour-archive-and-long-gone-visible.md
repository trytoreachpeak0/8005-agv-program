# 06 — 实现十二小时归档与 LongGoneButVisible

**What to build:** 作为运维工程师和外部消费者，我希望连续 GONE 满十二小时的 Series 只在下一次可信成功轮次中不可逆归档，而归档后再次出现的真实 MES 数据仍可在运维读取中追踪、却永远不会重新成为外部可读候选，以便长期结束的生命周期既不丢证据也不被错误复活。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间；05 — 实现 RestartBarrier、GONE 与归档前重现世代

**Status:** ready-for-human

- [x] 十二小时连续 GONE 从 GoneConfirmedAt 的 Host UTC 证据计算，不使用 MesSourceDate、Watch 本机时间或单纯墙钟定时器；边界前的成功轮次不归档，达到边界后的下一轮具有缺席权威的完整 SUCCESS 才归档。
- [x] FAILURE、INCOMPLETE、RestartBarrier 或受保护而没有缺席权威的轮次既不归档，也不被当作推进归档的业务证据；Host 重启后仍按持久化的 GoneConfirmedAt 正确计算。
- [x] 归档转换不可逆并产生带 PollTrace、ProjectionCommit 和严格 SeriesSequence 的生命周期事件；正式 API 清楚区分 Tracking、GONE 与 Archived，而不是从当前行是否存在推断状态。
- [x] 归档后同键重现时保留原 SeriesId，创建新的 DemandId 和世代并连接 predecessor；新 Demand 在 WatchDemandProjection 中可见，状态明确为 LongGoneButVisible，原归档事实不被撤销。
- [x] 归档后重现形成 LONG_GONE_BUT_VISIBLE 当前错误、历史期间和稳定不可读原因；即使后续观测唯一且全部字段有效，该 Demand 也永久不能进入外部可读目录。
- [x] 达到边界、尚未达到边界、无权威轮次、归档、归档后重现和再次重启均通过真实 SQL Server → 正式 API seam 验收，且生命周期、世代、错误和不可读结论来自同一冻结投影提交。

## Comments

- 2026-08-13：新版 tracer/空库 schema 升至 6，并持久化 `DemandSeries.ArchivedAt`。归档只在拥有缺席权威的完整 SUCCESS 投影事务中执行，以 `GoneConfirmedAt` 和当前轮次 `CompletedAt` 的 Host UTC 证据判定包含式 12 小时边界；先处理本轮真实观测，再执行缺席与归档扫描，因此临界点同键重现会创建归档前世代而不会误归档。
- 归档以不可逆 `ARCHIVED` 生命周期和 `GONE_TIMEOUT_ARCHIVED` 事件记录，事件绑定同一 PollTrace/ProjectionCommit/SeriesSequence，正式 API 同时返回 `ArchivedAt`。归档后重现保留 SeriesId，创建带 predecessor 的新 VISIBLE Demand 世代，把 Series 当前态标为 `LONG_GONE_BUT_VISIBLE`，并开启 Series 作用域的 `LONG_GONE_BUT_VISIBLE` / `ARCHIVED_SERIES_VISIBILITY` 错误期间；结构化 `SERIES_ARCHIVED` 与 `LONG_GONE_BUT_VISIBLE` 阻断保证后续合法唯一观测也不能恢复外部可读资格。
- 双轴审查后补齐三条状态机边：恰好 12 小时且同轮观测时先按归档前重现处理；旧归档 PollTrace 在后继 Demand 已创建后重放仍返回原归档 DemandId；归档后可见 Demand 再次权威缺席时转回 GONE、结束当前错误期间，后续再出现创建下一代和新的期间。Demand 自身正式状态也固定为 `LONG_GONE_BUT_VISIBLE`，稳定词汇集中到领域契约。
- SQL Server `16.0.1190.2`（major 16、compatibility 160）Ticket 06 正式 Host/API 门禁为 `5 passed / 0 skipped`；Ticket 01-06 联合回归为 `23 passed / 0 skipped`，纯策略边界测试为 `6 passed / 0 skipped`，非增量 Release build 为 `0 warnings / 0 errors`。完整 solution 测试为核心 `509 passed / 46 environment-gated skipped / 2 unrelated failed`、Watch UI `82 passed / 27 golden-machine skipped`；两个核心失败分别是已知固定墙钟 telemetry 日期漂移，以及当前非黄金桌面的标题栏双击 UIA 环境失败，均与 Ticket06 后端改动无关。
