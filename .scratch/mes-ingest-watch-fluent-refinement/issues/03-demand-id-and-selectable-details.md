# 将 DemandId 前置并让详情文本可选择复制

Type: task
Status: wontfix
Blocked by: 01

## Question

如何把 DemandId 作为 Demand 表格最左侧常驻主键列，并让用户选中 Demand 或 Alert 后能够在下方详情区域用鼠标选择、复制完整文字，同时保留详情分组、时间完整值、自动化名称以及既有单元格/整行复制行为？

DemandId 不再只在点击后显示于详情或隐藏列中；长值允许合理截断显示，但可通过水平滚动、详情选择和既有复制动作取得完整值。详情仍为只读，不引入可编辑输入控件的视觉误导。

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
