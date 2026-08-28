# 04 — 处理重复键与同 SUBLOT 多 WorkType 冲突

**What to build:** 作为运维工程师，我希望重复业务键和同一 SUBLOT 同时落入多个 WorkType 时，系统保留全部原始事实、绝不任选或拼接一行，并通过正式 API 展示每个受影响 Series 的冲突与恢复过程，以便我能诊断源数据而不会得到伪造的单值 Demand。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间

**Status:** done

- [x] 一个成功轮次中同一 SUBLOT + WorkType 出现两条或更多原始行时，只保留一个 Series 和一个当前 Demand 世代，完整保存规范化后的所有行，不选主行、不拼接字段，也不生成虚假的 LiveMesFieldSet。
- [x] 重复行形成 DUPLICATE_TRANSPORT_DEMAND_KEY 当前错误和不可读结论；正式 API 能从受影响 Demand 追到全部观测、错误期间、证据值、PollTrace 和 ProjectionCommit。
- [x] 将相同重复行从 A/B 调换为 B/A 不产生新的业务变化或新错误期间；行内容或数量真正变化时在原期间追加证据，而不是改变冲突身份。
- [x] 重复观测恢复为唯一行时，继续使用原 SeriesId、DemandId 和世代，恢复实时字段，并由完整 SUCCESS 明确结束错误期间，不以恢复为由制造新 Demand。
- [x] 同一 SUBLOT 在同轮出现多个 WorkType 时，每个 SUBLOT + WorkType 分别形成独立 Series/Demand，同时所有受影响当前 Demand 都形成 SUBLOT_MULTIPLE_WORK_TYPES 冲突及完整 WorkType 集合证据。
- [x] 多 WorkType 冲突恢复后，各 Series 不合并、不换键；仍可见的相关 Demand 结束当前冲突，历史错误期间和逐世代证据永久保留。
- [x] 真实 SQL Server → 正式 API 验收覆盖重复行、换序、证据变化、恢复唯一、同 SUBLOT 多 WorkType 及恢复，并证明标识、错误期间和原始多重集合在 Host 重启后保持一致。

## Comments

- 2026-08-13：V2 tracer 契约/空库 schema 升至 4。SUCCESS 在单个 SERIALIZABLE `ProjectionCommit` 中按精确 `SUBLOT + WorkType` 分组；重复组保留完整规范化多重集合并共享一个 Series/Demand 身份，正式 API 以 `liveMesFields: null` 表达“没有可信单值”，同时发布目录所有者定义的重复/多 WorkType 条件、永久期间、证据、原始行、PollTrace 与提交链接。
- 重复多重集合以 UTC 规范化后的完整行稳定排序：A/B 与 B/A、等价时区表示及同 PollTrace 重放不制造业务噪声；内容或数量变化只向同一期间追加证据。恢复唯一继续原 SeriesId、DemandId 与 generation，并以完整 SUCCESS 的 `CONDITION_CLEARED` 恢复实时字段。完全相同的重复行仍按 multiplicity 保存。
- 多 WorkType 每个复合键保持独立 Series/Demand，所有本轮受影响 Demand 获得完整排序 WorkType 集合；重复键与多 WorkType 条件可在同一 Demand 上共存。A/B/C → A 时，重新观测到的 A 有明确反证并关闭当前冲突；缺席 B/C 不是恢复证据，继续阻断读取，直到 Ticket 05 通过缺席权威转为 GONE 并以 `DEMAND_GONE` 结束，避免把陈旧的 `VISIBLE` Demand 误报为可读。
- 真实 SQL Server `16.0.1190.2`（major 16、compatibility 160）Ticket 04 正式 Host/API 门禁为 `4 passed / 0 skipped`；Ticket 01-04 关键回归为 `16 passed / 0 skipped`；非增量 Release build 为 `0 warnings / 0 errors`。完整测试项目执行结果为 `519 passed / 19 environment-gated skipped / 2 unrelated failed`：固定墙钟 telemetry 用例存在日期漂移，WPF 标题栏拖拽首次波动后单独通过；后续并发 WPF package-stream 波动也单独通过。双轴审查为 `Spec: 0 findings`、`Standards: 0 hard violations`，仅记录两个非阻断后续重构建议。
