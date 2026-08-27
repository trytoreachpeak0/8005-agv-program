# 08 — 迁移双语接入告警

**What to build:** 让使用者能在中文或英文中理解当前接入异常、任务类型保护、结构化证据和恢复状态，并使用保持规范条件的动作下钻到错误检索或需求系列。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** ready-for-agent

- [x] 页面标题、当前范围、筛选、分面、列表、证据、保护状态、恢复状态、分页、空态、失败态和下钻动作全部双语化。
- [x] 已知关注类型、保护状态、错误类别和操作结果显示当前语言含义及不变的规范代码。
- [x] 未知动态码使用中性本地化回退并保留原值，不继承任何已知类型的严重度或处置建议。
- [x] PollTrace、SeriesId、DemandId、WorkType、原始证据和绝对时间保持技术事实；字段和值由可见标签或表头解释。
- [x] 活动异常、恢复事实、加载、成功零结果、读取失败和保留旧结果保持不同语义。
- [x] 语言切换保留筛选、页码、选择、证据上下文、滚动和焦点，不新建告警、不改变活动状态、不增加 Host 请求。
- [ ] 中文、英文、720 epx、主题和高对比状态下状态不依赖颜色，分页和下钻操作均可达。
- [ ] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

