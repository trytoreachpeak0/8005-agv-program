# 08 — 删除当前应用配置后保留快照

**What to build:** 用户删除了正在生效的那个 AREA 配置——无论是在 Watch 里删还是在资源管理器里删——显示范围都保持不变，不会突然从筛选后的少数 AREA 放开到全厂数据。列表里保留一个提示项，显示配置名与「文件已删除 · 范围仍生效」，并提供以同名另存为的恢复入口。要放开筛选必须显式应用「全部 AREA」。

> 这是本特性唯一一处改变既有业务语义的地方：现有实现中通过界面删除会清空活动标记并回退到全部 AREA，而外部删除不走该路径、快照会保留，两者不一致。统一为保留快照，已经用户确认。

**Blocked by:** 07, 04

**Status:** ready-for-human

- [x] 通过界面删除当前应用的配置后，显示范围保持不变
- [x] 外部删除当前应用的配置后，显示范围保持不变
- [x] 两条删除路径的行为一致
- [x] 列表保留提示项，标明文件已删除且范围仍生效
- [x] 提示项提供以同名另存为的恢复入口
- [x] 放开筛选只能通过显式应用「全部 AREA」
- [x] 删除非当前应用的配置行为不变
- [x] tier 1 全绿

## Implementation evidence

- `WatchAreaFilterProfileStore.Delete` 删除 TXT 时不再改写活动标记；返回值与重启后读取都保留原配置名、AREA 快照和应用时间。
- `EnumerateProfiles` 为已应用但 TXT 缺失的配置保留 `IsMissing` 摘要；界面将其投影为「文件已删除 · 范围仍生效」，继续显示快照 AREA 数并禁用重新应用、重命名和再次删除。
- 界面内删除和外部删除都保留同一 `AreaContext`；「另存为」在缺失行上默认填入原配置名，恢复后重新成为普通已应用行。
- `Selecting_an_unselected_missing_applied_row_restores_from_its_snapshot_not_the_other_editor` 固定从其它编辑器切回缺失行时只使用已应用快照，避免把另一配置的内容按缺失配置名恢复。
- `Only_applying_all_areas_releases_the_scope_after_its_profile_file_is_deleted` 固定只有显式「应用全部 AREA」才放开范围；`Delete_of_a_non_applied_profile_leaves_the_current_snapshot_untouched` 固定非当前配置删除语义不变。
- 聚焦 AREA 回归：134 passed、0 failed、0 skipped。Tier 1 `dotnet test MesIngest.Tests --verbosity minimal`：560 passed、82 skipped、0 failed；SQL Server 测试因无 LocalDB 按 Tier 1 规则跳过。

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
