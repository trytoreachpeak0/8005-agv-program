# 04 — 处理重复键与同 SUBLOT 多 WorkType 冲突

**What to build:** 作为运维工程师，我希望重复业务键和同一 SUBLOT 同时落入多个 WorkType 时，系统保留全部原始事实、绝不任选或拼接一行，并通过正式 API 展示每个受影响 Series 的冲突与恢复过程，以便我能诊断源数据而不会得到伪造的单值 Demand。

**Blocked by:** 03 — 投影实时字段、字段异常与错误期间

**Status:** ready-for-agent

- [ ] 一个成功轮次中同一 SUBLOT + WorkType 出现两条或更多原始行时，只保留一个 Series 和一个当前 Demand 世代，完整保存规范化后的所有行，不选主行、不拼接字段，也不生成虚假的 LiveMesFieldSet。
- [ ] 重复行形成 DUPLICATE_TRANSPORT_DEMAND_KEY 当前错误和不可读结论；正式 API 能从受影响 Demand 追到全部观测、错误期间、证据值、PollTrace 和 ProjectionCommit。
- [ ] 将相同重复行从 A/B 调换为 B/A 不产生新的业务变化或新错误期间；行内容或数量真正变化时在原期间追加证据，而不是改变冲突身份。
- [ ] 重复观测恢复为唯一行时，继续使用原 SeriesId、DemandId 和世代，恢复实时字段，并由完整 SUCCESS 明确结束错误期间，不以恢复为由制造新 Demand。
- [ ] 同一 SUBLOT 在同轮出现多个 WorkType 时，每个 SUBLOT + WorkType 分别形成独立 Series/Demand，同时所有受影响当前 Demand 都形成 SUBLOT_MULTIPLE_WORK_TYPES 冲突及完整 WorkType 集合证据。
- [ ] 多 WorkType 冲突恢复后，各 Series 不合并、不换键；仍可见的相关 Demand 结束当前冲突，历史错误期间和逐世代证据永久保留。
- [ ] 真实 SQL Server → 正式 API 验收覆盖重复行、换序、证据变化、恢复唯一、同 SUBLOT 多 WorkType 及恢复，并证明标识、错误期间和原始多重集合在 Host 重启后保持一致。

