# 02 — 迁移反馈、故障生命周期与 AREA 阻塞选择

**What to build:** 让 Watch 使用者在所有主页面得到一致且安静的反馈语义：短暂操作结果进入窗口通知，持续故障收敛到页面标题或全局 Host 状态，稳定空态和详情仍留在内容区，需要明确选择的 AREA 操作使用真正覆盖内容的对话框。

**Blocked by:** 01 — 建立 Variant A 窗口级通知主链。Ticket 01 完成前不得开始本票。

**Status:** done

## Final Golden evidence

- 2026-08-27 Ticket 03 最终生产状态完整 `watch-ui-journeys`：96 DPI、120 DPI、144 DPI 均为 1 passed / 0 failed / 0 skipped。证据：`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/final-96-20260827-114310`、`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/dpi-120-final-20260827-112746`、`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/dpi-144-final-20260827-112746`。

规格依据：[Variant A 通知规格](../spec.md)。本票涉及 Watch UI、WPF UI 控件和 UIA，必须遵守 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)。

- [x] 审核主工作区现有反馈并按外部行为迁移：显式保存、应用、恢复默认设置及必要失败进入 toast；初始加载、自动刷新、查询、排序和分页成功保持静默，只更新固定进度、新鲜度或结果区域。
- [x] 刷新清除当前选择时只产生一次 3 秒信息通知，同时详情区进入稳定未选择状态且不自动选择另一项。
- [x] 空结果、未选择详情、字段校验、只读结论和目录监视降级继续使用稳定内容表面；迁移后正常轮询不得再通过开合 `Auto` 高度反馈行推动表格、分页或详情布局。
- [x] 用户操作失败显示面向操作员的短说明和真实下一步；凭据、完整 URL、调用栈和长异常不得进入 toast，只能进入既有受控详情或日志表面。
- [x] 以真实刷新提交和工作区状态识别持续故障周期：新故障首次出现时通知一次，持续刷新不新增也不重复播报，恢复时清除稳定状态并显示一次 3 秒恢复通知，同一来源的新故障周期能够再次通知。
- [x] 每个受影响主页面在标题同一布局行显示最高严重度、当前故障数量和可访问详情动作；关闭、过期或溢出首次 toast 不得清除该稳定状态。
- [x] Host 连接或契约故障继续由导航页脚表达全局状态，首次故障可显示全局 toast，动作进入连接设置或详情，并能跨页面保留。
- [x] 导航完成后立即结束离开页面的短暂通知，但不清除全局通知或真实持续故障；返回页面时只根据当前状态恢复稳定摘要，不回放旧成功或恢复结果。
- [x] 窗口最小化或后台期间不桥接 Windows 系统通知；过期成功、信息和恢复直接丢弃，返回前台时仅对仍活动的新故障最多摘要一次。
- [x] 将切换到全 AREA 范围的确认迁移为覆盖内容的 WPF UI `ContentDialog`；确认和取消复用既有查询语义，取消不得改变当前查询或选择。
- [x] 将 AREA 并发写入冲突迁移为提供“覆盖并保存”“重新载入文件”“稍后处理”的真实 `ContentDialog`；关闭或稍后处理必须保留草稿并保持自动保存暂停，只有既有解决语义完成后才恢复。
- [x] 对话框打开时通知和页面处于正确层级与禁用状态，焦点进入对话框；关闭后按既有窗口规则恢复到调用控件或合理后续控件。
- [x] 使用现有生产窗口、自动刷新、选择和 AREA 冲突测试 seam，只补充迁移后可观察行为；不重复测试 Host 查询、AREA 指纹或自动保存内部算法。
- [x] 实现期间按页面或行为运行最窄测试选择；全部生产改动完成后只运行一次 tier 1 `dotnet test MesIngest.Tests`，记录通过、失败、跳过数以及未配置 SQL Server 环境时的命名跳过。
- [x] 本票不得提前运行 tier 2 或 tier 3；最终 Golden 预览与用户批准统一由 Ticket 03 完成。

## Golden renderer checklist

- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

Ticket 03 完成最终 Golden 验证后，应把同一最终生产状态的证据引用回本票；在此之前不得声称本票已获得视觉批准。
