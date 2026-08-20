# 09 — 布局清理：删除横幅与 AREA 标签栏

**What to build:** 页面顶部重复陈述当前显示范围的横幅移除——当前应用的是哪个配置、有几个 AREA，左侧列表已经表达，应用时刻的信息价值不足以占据一整行。编辑器上方的「AREA（每行一个）」标签栏移除：有效 AREA 数量移到文件标题行右侧，格式要求并入文件路径那一行。

这两处合计腾出的纵向空间全部归编辑器。

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] 顶部显示范围横幅不复存在
- [ ] 「AREA（每行一个）」标签栏及其格式说明行不复存在
- [ ] 有效 AREA 数量显示在文件标题行右侧
- [ ] 格式要求与文件路径同行显示
- [ ] 编辑器可视高度较改动前明显增加
- [ ] 引用被删元素的测试断言同步调整
- [ ] 符合 `docs/agents/fluent-ui.md` 的强制验收条款
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
