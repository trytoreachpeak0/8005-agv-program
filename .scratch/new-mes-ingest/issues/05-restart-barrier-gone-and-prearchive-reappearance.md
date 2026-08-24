# 05 — 实现 RestartBarrier、GONE 与归档前重现世代

**What to build:** 作为运维工程师，我希望 Host 重启和完整快照中的真实缺席具有可解释且不同的语义：重启保护期不误报消失，获得缺席权威后才把 Demand 标为 GONE，而归档前再次出现时在原 Series 中建立可追溯的新世代，以便生命周期不会因冷启动或短暂消失被破坏。

**Blocked by:** 01 — 建立新版成功轮次端到端骨架；02 — 固化轮次证据、幂等冲突与非成功隔离

**Status:** done

- [x] 持久化一条 VISIBLE Demand 后重启 Host，系统自动进入 RestartBarrier；调用方没有能够绕过保护或直接指定缺席权威的输入。
- [x] 重启后的第一轮完整 SUCCESS 只建立基线，第二轮只结束保护，前两轮即使缺少原业务键也不推进 GONE；第三轮完整 SUCCESS 仍缺少该键时才拥有缺席权威并确认 GONE。
- [x] RestartBarrier 的进入、基线完成和权威恢复都有可查询的稳定事件与轮次证据；FAILURE、INCOMPLETE 和内容冲突不会推进保护阶段或获得缺席权威。
- [x] 不处于保护状态时，首个具有缺席权威的完整 SUCCESS 未包含当前业务键，便把其 VISIBLE Demand 转为 GONE；DemandLastSeenAt 保持最后真实看见时间，GoneConfirmedAt 单独记录确认缺席的 Host UTC 时间。
- [x] 保护期间仍可创建新 VISIBLE Demand、更新已观测 Demand 的实时字段并保留正常事件，只禁止由缺席推进 GONE 或归档。
- [x] Series 尚未归档时，同键在后续完整 SUCCESS 中重现会保留 SeriesId，创建更高世代和新 DemandId，并以 predecessor 关系连接永久保留的上一代；旧代不被静默复活或改写。
- [x] 真实 SQL Server → 正式 API 的持久化重启验收依次证明第一、第二、第三轮边界、直接权威缺席、归档前重现和前后世代关系，且 API 展示的生命周期事件均绑定对应 PollTrace/ProjectionCommit。

## Comments

- 2026-08-13：新版 tracer/空库 schema 升至 5。每个 HostSession 在启动服务中自动进入持久化 `BARRIER`；新接受的完整 SUCCESS 依次执行 `BARRIER → POST_BARRIER → NORMAL`，仅从 `NORMAL` 开始的轮次拥有缺席权威。进入、基线完成、权威恢复均有稳定事件；当前及历史 HostSession 可由正式 `/api/v2/absence-authority` API 查询，基线/恢复事件绑定对应 PollTrace/ProjectionCommit。调用方输入保持为 `MesTaskUnionRound + CancellationToken`，无缺席权威绕过参数。
- 权威缺席在同一 SERIALIZABLE 投影事务中把当前 VISIBLE Demand 置为 GONE，保留 `DemandLastSeenAt`，单独写 `GoneConfirmedAt`，以 `DEMAND_GONE` 结束 Demand 级当前错误期间并显式阻断读取。正向重现保持 SeriesId，以新 DemandId、递增 generation 和 predecessor 创建下一代；旧代及其时间/commit/字段永久不改写。重现时间不得早于前代 GoneConfirmedAt，乱序轮次整笔回滚。
- Demand 另存精确 `LatestObservationProjectionCommitId`：正向观测推进、GONE 保留，避免相同 CompletedAt 时按 PollTraceId 字典序误选旧原始多重集合。Series 正式 API 按 generation 返回全部 Demand 世代，并保留 currentDemand 兼容读取。
- SQL Server `16.0.1190.2`（major 16、compatibility 160）Ticket 05 正式 Host/API 门禁为 `6 passed / 0 skipped`；Ticket 01-05 联合回归为 `22 passed / 0 skipped`；非增量 Release build 为 `0 warnings / 0 errors`。完整核心测试为 `504 passed / 41 environment-gated skipped / 1 unrelated failed`，失败仍是已知固定墙钟 telemetry 保留日期漂移。最终双轴审查为 `Spec: 0 findings`；Standards 的 3 个代码问题与证据账本问题均已修复并复核。
