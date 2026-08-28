# 扩大 Demand 与 Alert 列表并折叠筛选栏

Type: task
Status: wontfix
Blocked by: 01

## Question

如何让 Demand 和 Alert 页面把列表作为主要视觉区域，同时让各自筛选栏可独立折叠/展开，并保持查询草稿、提交查询、失败保留结果、键盘导航和 UIA 语义完整？

默认筛选栏展开，折叠状态只在当前运行期间记忆；页面默认约 70% 高度给列表、30% 给详情，分隔条仍可调整并双击恢复。Demand 继续按 `TASK_TYPE` 过滤，Alert 明确以 `Code` 作为告警类型过滤，现有 Severity 和时间范围能力不得丢失。

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
