# 07 — 实现按 WorkType 隔离的 TaskTypeProtection

**What to build:** 作为运维工程师，我希望某一 WorkType 从健康非零基线骤降为零时只保护该类型的 Demand，不让可疑空结果批量制造 GONE，同时其它类型继续正常对账，并能从正式 API 看见保护进入、恢复进度和权威恢复，以便异常源结果不会扩大成全局业务误判。

**Blocked by:** 02 — 固化轮次证据、幂等冲突与非成功隔离；05 — 实现 RestartBarrier、GONE 与归档前重现世代

**Status:** ready-for-agent

- [ ] 每个 WorkType 独立维护健康非零基线；某类型从健康非零结果骤降为零时进入 TaskTypeProtection/PausedZeroDrop，该轮及保护期间的成功空轮不能把该类型 Demand 标为 GONE 或推进归档。
- [ ] 一个 WorkType 受保护时，其它 WorkType 仍按各自观测和缺席权威正常创建、更新或标记 GONE；保护状态、计数和恢复进度不得跨类型串扰。
- [ ] 受保护类型连续两轮获得健康非零结果后才解除保护；第二轮只完成解除，下一轮完整结果才恢复该类型的缺席权威，不能在解除同轮自相矛盾地确认 GONE。
- [ ] FAILURE、INCOMPLETE、幂等重放和内容冲突不建立健康基线、不推进连续恢复计数，也不解除保护；RestartBarrier 与类型保护同时存在时，只有两者都允许的轮次才具有缺席权威。
- [ ] 保护进入、每步恢复进度、解除和权威恢复都产生稳定事件，并作为当前 CurrentIngestAttention 与轮次证据由正式 API 查询；结束后不保留为当前项，但历史事实仍可追溯。
- [ ] 保护状态和恢复进度在 Host 重启后保持，不能因进程重启提前获得缺席权威或丢失保护证据。
- [ ] 真实 SQL Server → 正式 API 验收同时驱动至少两个 WorkType，证明目标类型进入保护、保护空轮不 GONE、其它类型继续对账、两轮非零恢复以及随后权威空轮才 GONE。

