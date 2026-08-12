# 05 — 实现 RestartBarrier、GONE 与归档前重现世代

**What to build:** 作为运维工程师，我希望 Host 重启和完整快照中的真实缺席具有可解释且不同的语义：重启保护期不误报消失，获得缺席权威后才把 Demand 标为 GONE，而归档前再次出现时在原 Series 中建立可追溯的新世代，以便生命周期不会因冷启动或短暂消失被破坏。

**Blocked by:** 01 — 建立新版成功轮次端到端骨架；02 — 固化轮次证据、幂等冲突与非成功隔离

**Status:** ready-for-agent

- [ ] 持久化一条 VISIBLE Demand 后重启 Host，系统自动进入 RestartBarrier；调用方没有能够绕过保护或直接指定缺席权威的输入。
- [ ] 重启后的第一轮完整 SUCCESS 只建立基线，第二轮只结束保护，前两轮即使缺少原业务键也不推进 GONE；第三轮完整 SUCCESS 仍缺少该键时才拥有缺席权威并确认 GONE。
- [ ] RestartBarrier 的进入、基线完成和权威恢复都有可查询的稳定事件与轮次证据；FAILURE、INCOMPLETE 和内容冲突不会推进保护阶段或获得缺席权威。
- [ ] 不处于保护状态时，首个具有缺席权威的完整 SUCCESS 未包含当前业务键，便把其 VISIBLE Demand 转为 GONE；DemandLastSeenAt 保持最后真实看见时间，GoneConfirmedAt 单独记录确认缺席的 Host UTC 时间。
- [ ] 保护期间仍可创建新 VISIBLE Demand、更新已观测 Demand 的实时字段并保留正常事件，只禁止由缺席推进 GONE 或归档。
- [ ] Series 尚未归档时，同键在后续完整 SUCCESS 中重现会保留 SeriesId，创建更高世代和新 DemandId，并以 predecessor 关系连接永久保留的上一代；旧代不被静默复活或改写。
- [ ] 真实 SQL Server → 正式 API 的持久化重启验收依次证明第一、第二、第三轮边界、直接权威缺席、归档前重现和前后世代关系，且 API 展示的生命周期事件均绑定对应 PollTrace/ProjectionCommit。

