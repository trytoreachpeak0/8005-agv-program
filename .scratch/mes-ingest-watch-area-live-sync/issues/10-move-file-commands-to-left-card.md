# 10 — 文件命令迁移到左栏右键菜单

**What to build:** 针对单个配置文件的命令不再散落在右侧编辑器标题行。另存为、重命名、删除移到左侧筛选配置列表的项右键菜单——这些命令本来就是对某一项的操作，右键的作用对象更明确。「打开配置文件夹」移到左栏卡片标题行。

左栏宽度固定，不足以平铺全部文件命令，因此走右键菜单而非按钮并排。重命名与删除沿用既有的确认流程，只是触发入口与确认面板位置改变。

**Blocked by:** 09

**Status:** ready-for-agent

- [ ] 另存为、重命名、删除通过左侧列表项的右键菜单触发
- [ ] 右侧编辑器标题行不再有文件命令按钮
- [ ] 「打开配置文件夹」位于左栏卡片标题行
- [ ] 重命名与删除的确认流程行为不变，仅入口与面板位置改变
- [ ] 右键菜单项的启用状态与既有规则一致
- [ ] 引用原按钮的测试断言同步调整
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
