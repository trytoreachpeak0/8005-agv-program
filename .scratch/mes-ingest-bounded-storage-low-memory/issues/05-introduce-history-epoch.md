# 05 — 引入 HistoryEpoch 内部身份

**What to build:** 在不一次性打破全部调用方的前提下扩展 MesIngest，使一段连续可追溯数据库历史拥有稳定 HistoryEpoch，并为后续各读取面逐步迁移提供统一身份。

**Blocked by:** 04 — 建立新空库的存储默认值.

**Status:** ready-for-agent

- [ ] 新空库创建不可为空且稳定的 HistoryEpoch，并与 schema 身份一起原子持久化。
- [ ] 普通 Host 停止、重启、故障恢复和新 HostSession 不改变既有 HistoryEpoch。
- [ ] 计划空库创建和明确的不可恢复重建能够请求新 HistoryEpoch，但本票不实现风险确认或切换删除。
- [ ] 投影提交与读取栅栏在内部携带 HistoryEpoch，使后续读取面不需要各自发明纪元来源。
- [ ] 旧数据库缺少新纪元结构时严格拒绝，不把应用版本、HostSessionId、ProjectionCommit 或 CatalogRevision 当作纪元。
- [ ] expand 阶段保持现有生产读取行为可运行，新增测试证明纪元持久性、重启稳定性与空库唯一性。
