# 03 — 迁移双语概览与统计语义

**What to build:** 让使用者在中文或英文概览中独立理解需求系列、资格审计、错误检索、AREA 筛选和接入关注摘要，包括每个数量的对象、单位、范围、数据时点以及通往目标页面的明确查询含义。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** ready-for-agent

- [ ] 页面标题、摘要卡、统计单位、范围说明、更新时间、近期重点动态和下钻动作全部来自共享双语目录。
- [ ] 大号数量由卡片标题和当前语言单位解释，次要说明明确 AREA 范围、投影提交、CatalogRevision 或其它真实统计时点。
- [ ] 需求系列、资格、当前错误和接入关注项保持各自规范计数单位，不因翻译改变聚合或跳转条件。
- [ ] 绝对时间始终包含偏移，相对时间随语言变化且只作为次要说明；标识、版本和修订号不做文化相关转换。
- [ ] 刷新失败时保留上一份完整成功概览并明确显示其时点和当前失败，不能把新旧卡片拼成当前快照。
- [ ] 语言切换保留当前概览状态、滚动和焦点，不触发 Host 刷新；下钻仍携带相同规范条件并从第一页开始。
- [ ] 中文、英文、720 epx、浅色、深色、非活动和高对比状态下均无孤立值、遮挡或仅依赖颜色的含义。
- [ ] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

