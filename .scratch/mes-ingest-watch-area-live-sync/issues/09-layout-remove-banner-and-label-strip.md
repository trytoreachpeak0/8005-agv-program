# 09 — 布局清理：删除横幅与 AREA 标签栏

**What to build:** 页面顶部重复陈述当前显示范围的横幅移除——当前应用的是哪个配置、有几个 AREA，左侧列表已经表达，应用时刻的信息价值不足以占据一整行。编辑器上方的「AREA（每行一个）」标签栏移除：有效 AREA 数量移到文件标题行右侧，格式要求并入文件路径那一行。

这两处合计腾出的纵向空间全部归编辑器。

**Blocked by:** 01

**Status:** ready-for-human

- [x] 顶部显示范围横幅不复存在
- [x] 「AREA（每行一个）」标签栏及其格式说明行不复存在
- [x] 有效 AREA 数量显示在文件标题行右侧
- [x] 格式要求与文件路径同行显示
- [x] 编辑器可视高度较改动前明显增加
- [x] 引用被删元素的测试断言同步调整
- [x] 符合 `docs/agents/fluent-ui.md` 的强制验收条款
- [x] tier 1 全绿

## Implementation evidence

- 删除 AREA 页恒驻的「当前显示范围」InfoBar；瞬态操作反馈仍按 Fluent 规则保留为可折叠 InfoBar，页面标题与主体之间只保留 12 epx 间距。
- `AreaProfileValidCountPill` 已移到文件标题行右侧；路径标题统一附带「每行一个 AREA，如 A1-1，# 开头忽略」，不再保留独立字段标签或格式说明行。
- 编辑器工作区删去两个冗余头部行，`AreaProfileEditorFrame` 直接取得释放的星号高度；组合测试在 1440×900 固定窗口下确认编辑器可视高度至少 500 epx。
- `Area_filter_layout_gives_redundant_banner_and_field_strip_space_to_the_editor` 覆盖横幅/标签条消失、标题行对齐、路径格式提示和编辑器高度；既有 golden UI 契约中的旧控件与网格行号断言已同步。
- 聚焦 `WatchAreaProfile*` 回归：64 passed、0 failed、0 skipped。Tier 1 `dotnet test MesIngest.Tests --verbosity minimal`：561 passed、82 skipped、0 failed；SQL Server fixture 因无 LocalDB 按 Tier 1 规则跳过。

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
