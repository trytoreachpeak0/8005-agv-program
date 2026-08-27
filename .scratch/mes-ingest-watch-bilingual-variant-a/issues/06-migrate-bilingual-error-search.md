# 06 — 迁移双语错误检索

**What to build:** 让使用者能在中文或英文中按错误分类、代码、活动状态、时间和标识检索需求系列错误，阅读命中期间和诊断证据，并在需要时查看逐字保真的原始证据。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** implemented-awaiting-visual-validation

- [x] 分类导航、分面、筛选、结果、分页、期间、证据、失败状态、帮助和下钻动作全部使用共享双语目录。
- [x] 已知错误码同时显示当前语言含义和规范原码；未知码显示中性“未知代码”说明并保留原值。
- [x] 原始 JSON、日志正文、API 字段、证据值、SeriesId、DemandId 和错误码不翻译。
- [x] 活动、已结束、加载、成功零结果、读取失败和保留旧快照使用不同可见语义，不把翻页失败冒充第一页。
- [x] 时间窗口显示明确时区；绝对时间保留偏移，滚动窗口和相对说明使用当前语言。
- [x] 语言切换保留分类、错误码、活动状态、时间窗口、SeriesId、DemandId、页码、选择、滚动和冻结查询上下文。
- [x] 切换不增加 Host 请求、不重新解释筛选、不改变游标绑定或原始证据。
- [ ] 中文、英文、720 epx、主题和高对比状态下三列工作区保持统一上下边缘、可用高度和可达动作。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

