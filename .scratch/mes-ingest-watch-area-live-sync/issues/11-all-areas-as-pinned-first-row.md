# 11 — 「全部 AREA（不筛选）」常驻首项

**What to build:** 「全部 AREA（不筛选）」成为左侧列表的常驻首项，与其他配置共用同一套选中与应用操作。原本独立的「应用全部 AREA」按钮移除，左栏底部只保留一个应用主按钮，07 定义的五态逻辑对该首项同样成立。

**Blocked by:** 07, 10

**Status:** done

- [x] 列表首项为「全部 AREA（不筛选）」且常驻，搜索与目录变化都不使其消失
- [x] 选中它并应用，等价于原「应用全部 AREA」的效果
- [x] 原独立按钮不复存在，引用它的测试断言同步调整
- [x] 左栏底部只有一个应用主按钮
- [x] 该首项被应用时按钮呈现「已应用」态
- [x] 该首项不可另存为、重命名或删除
- [x] tier 1 全绿

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。

## Comments

- 2026-08-20：将「全部 AREA（不筛选）」建模为不对应 TXT 文件的常驻首项；搜索与目录刷新只改变后续文件行。首项复用 `AreaProfileApplyButton` 与既有 `ApplyAllAreas` 存储契约，当前生效时呈现「已应用」，且不提供另存为、重命名或删除菜单。
- 独立 `AreaApplyAllAreasButton` 已删除，通用应用按钮迁入左栏底部；执行型按钮按 `docs/agents/fluent-ui.md` 保持 `Secondary`，不使用表示持久选择的强调色。
- AREA 聚焦回归：70 passed、0 failed、0 skipped。Tier 1 `dotnet test MesIngest.Tests --verbosity minimal`：567 passed、82 skipped、0 failed；SQL Server fixture 因无 LocalDB 按 Tier 1 规则跳过。未运行 Tier 2/3，按本特性约定留待全部 ticket 完成后统一金机验证。
