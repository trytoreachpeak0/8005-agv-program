# 10 — 文件命令迁移到左栏右键菜单

**What to build:** 针对单个配置文件的命令不再散落在右侧编辑器标题行。另存为、重命名、删除移到左侧筛选配置列表的项右键菜单——这些命令本来就是对某一项的操作，右键的作用对象更明确。「打开配置文件夹」移到左栏卡片标题行。

左栏宽度固定，不足以平铺全部文件命令，因此走右键菜单而非按钮并排。重命名与删除沿用既有的确认流程，只是触发入口与确认面板位置改变。

**Blocked by:** 09

**Status:** done

- [x] 另存为、重命名、删除通过左侧列表项的右键菜单触发
- [x] 右侧编辑器标题行不再有文件命令按钮
- [x] 「打开配置文件夹」位于左栏卡片标题行
- [x] 重命名与删除的确认流程行为不变，仅入口与面板位置改变
- [x] 右键菜单项的启用状态与既有规则一致
- [x] 引用原按钮的测试断言同步调整
- [x] tier 1 全绿

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。2026-08-21 统一验收已完成，证据与结论记录在
> [`spec.md`](../spec.md) 的 Golden renderer acceptance 一节。

## Comments

- 2026-08-20：另存为、重命名、删除迁入每个 AREA 配置列表项的右键菜单，使用稳定 UI Automation ID；打开配置文件夹与新建并列于左栏卡片标题行，文件操作确认面板同步迁入左栏。编辑器标题只保留文件身份与有效 AREA 数量。
- 未命名草稿没有可承载右键菜单的文件行，因此仅在外部删除留下草稿时，于左栏底部显示「另存草稿」恢复入口；普通文件的另存为仍只从列表项右键菜单触发。
- 菜单启用状态沿用既有规则：当前缓冲非法时禁用另存为，脏缓冲或缺失文件禁用重命名/删除；已应用但文件缺失的快照行仍允许另存恢复。确认关闭后键盘焦点回到稳定的配置列表。
- 聚焦 AREA 回归：55 passed、0 failed、0 skipped。`MesIngest.Watch.UiTests` 编译通过（0 warnings / 0 errors），未执行 Tier 2。
- 更新黄金机 UI 断言时同时修正了该文件中由前置 ticket 遗留、已无法编译的 `StatusText` / `LastModifiedAt` 旧成员引用，使其对齐当前的应用徽标、有效性与注意状态模型；这不是本票新增状态语义。
- Tier 1 `dotnet test MesIngest.Tests --verbosity minimal`：563 passed、82 skipped、0 failed；SQL Server fixture 因无 LocalDB 按 Tier 1 规则跳过。
