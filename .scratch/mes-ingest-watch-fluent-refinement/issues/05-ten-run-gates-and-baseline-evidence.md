# 将最终 UI 稳定性门禁统一为连续 10 次

Type: task
Status: wontfix
Blocked by: 04

## Question

如何把规格、测试入口和验收证据中的旧 50 次完整门禁永久调整为：日常相关套件各运行 1 次，最终批准候选的 Verify.Xaml、FlaUI 关键旅程和真实窗口视觉套件分别连续通过 10 次，并确保失败不会被成功重跑掩盖？

必须同步所有仍声称 50 次的权威规格、票据、脚本或说明；用户批准后的新候选连续 10 次通过后，才可生成 before/after/diff、晋升明确批准的基线并再次证明 `0 received`。出现失败或抖动时从第 1 次重新计数，并按红证据增加诊断运行。

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
