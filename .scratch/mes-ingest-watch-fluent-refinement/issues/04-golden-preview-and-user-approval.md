# 在黄金机验证完整 Fluent 交互并取得预览批准

Type: prototype
Status: wontfix
Blocked by: 02, 03

## Question

在正式 `MesIngest.Watch.exe`、假 Host 和校准的黄金渲染机上，新的 Fluent 标题栏、可折叠筛选、扩大列表、DemandId 前置以及可选择详情是否共同形成用户认可的 Win11 操作体验，并且没有破坏 Demand/Alert 关键旅程？

必须生成至少包含 Demand、Alert、筛选展开、筛选折叠和最大化窗口状态的真实黄金机预览；同时执行相关 FlaUI 旅程并保留失败证据。用户明确批准最终预览前，本票不得解决，后续基线票不得开始。

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
