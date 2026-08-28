# 02 — 固化轮次证据、幂等冲突与非成功隔离

**What to build:** 作为运维工程师，我希望每次 MES 轮询都有不可歧义的结果与内容证据，相同轮次能够安全重放、冲突重放会被整轮拒绝，而失败或结构不完整的轮次绝不会改变既有业务投影，以便我能解释每次读取发生了什么而不把采集故障误认为业务变化。

**Blocked by:** 01 — 建立新版成功轮次端到端骨架

**Status:** done

- [x] SUCCESS、FAILURE 和 INCOMPLETE 都留下可查询的 PollTraceId、查询版本、结果类型、Host UTC 时间、行数和规范化内容摘要；原始行按稳定规范化多重集合计算，返回顺序变化不会改变摘要，重复行数量变化会改变摘要。
- [x] 使用相同 PollTraceId 和相同规范化内容重放时，正式 API 返回同一已接受结果，且不会重复创建 PollTrace、ProjectionCommit、Series、Demand 或事件。
- [x] 使用相同 PollTraceId 绑定不同内容时，整轮以明确、版本化的契约冲突失败；真实 SQL Server 中的轮次账本和全部业务投影均无部分写入。
- [x] FAILURE 和 INCOMPLETE 只追加各自的可追溯轮次证据，不创建、更新、标记 GONE 或归档任何 Series/Demand，也不改变上一成功 ProjectionCommit 的正式 API 读取结果。
- [x] 缺列、列类型或结果结构不满足契约时归为 INCOMPLETE；结构完整但字段值为空、非法或互相冲突的原始行仍归为 SUCCESS 数据证据，不得借 INCOMPLETE 隐藏局部坏数据。
- [x] SUCCESS 中缺少 SUBLOT 或 TASK_TYPE 的行以 UnassignedMesObservation 原样归入该轮证据且不猜测 DemandSeries；同轮其它可识别业务键仍正常投影。
- [x] 通过真实 SQL Server 和正式 API 连续验证成功、同内容重放、内容冲突、FAILURE、INCOMPLETE 及 Host 重启，证明业务投影隔离、轮次证据和幂等结论在持久化后保持一致。

## Comments

- 2026-08-13：生产入口深化为统一 `RoundIngestor`，SQL 事务先锁定 PollTrace 幂等账本；相同 `Outcome + QueryVersion + RowCount + ContentDigest` 返回首次 receipt，不同指纹抛出携带稳定 code、contract version 与 PollTraceId 的契约冲突。
- FAILURE/INCOMPLETE 只写 PollTrace；SUCCESS 才创建 ProjectionCommit。正式 V2 PollTrace API 现可读取 nullable commit 的三态证据，并显式区分 `ASSIGNED` / `UNASSIGNED` 原始观测。Oracle 缺列/类型的识别仍由票 15 的正式 source 负责，本票在生产轮次边界固化 INCOMPLETE 的隔离与读取语义。
- 真实 SQL Server `16.0.1190.2`（major 16、compatibility 160）联合门禁为 `9 passed / 0 skipped`；非增量 Release build 为 `0 warnings / 0 errors`；排除仓库已知且与本票无关的 telemetry 保留期测试和一次已隔离复跑通过的 WPF 交互波动后，核心全量为 `508 passed / 19 environment-gated skipped / 0 failed`。
