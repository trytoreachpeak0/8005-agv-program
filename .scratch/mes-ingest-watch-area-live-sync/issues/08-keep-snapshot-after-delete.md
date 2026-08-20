# 08 — 删除当前应用配置后保留快照

**What to build:** 用户删除了正在生效的那个 AREA 配置——无论是在 Watch 里删还是在资源管理器里删——显示范围都保持不变，不会突然从筛选后的少数 AREA 放开到全厂数据。列表里保留一个提示项，显示配置名与「文件已删除 · 范围仍生效」，并提供以同名另存为的恢复入口。要放开筛选必须显式应用「全部 AREA」。

> 这是本特性唯一一处改变既有业务语义的地方：现有实现中通过界面删除会清空活动标记并回退到全部 AREA，而外部删除不走该路径、快照会保留，两者不一致。统一为保留快照，已经用户确认。

**Blocked by:** 07, 04

**Status:** ready-for-agent

- [ ] 通过界面删除当前应用的配置后，显示范围保持不变
- [ ] 外部删除当前应用的配置后，显示范围保持不变
- [ ] 两条删除路径的行为一致
- [ ] 列表保留提示项，标明文件已删除且范围仍生效
- [ ] 提示项提供以同名另存为的恢复入口
- [ ] 放开筛选只能通过显式应用「全部 AREA」
- [ ] 删除非当前应用的配置行为不变
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
