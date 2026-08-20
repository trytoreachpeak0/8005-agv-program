# 05 — 编辑器自动落盘

**What to build:** 用户在 AREA 内容编辑器里输入后不再需要按保存——停止输入约一秒后内容自动写入磁盘。切换选中配置、切换页面、关闭窗口前未落盘的内容被强制写入。`Ctrl+S` 保留为立即写盘的显式动作，给不放心自动保存的用户一个出口。页面底部的「保存」与「放弃修改」整行移除，编辑器因此获得更多纵向空间。

内部脏标记必须保留——本 ticket 删除的是按钮，不是状态机，03 与 06 的同步判定都依赖它。

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] 停止输入后内容自动写入磁盘，延迟对齐 VS Code 的自动保存默认值
- [ ] `Ctrl+S` 立即写盘
- [ ] 切换选中配置、切换页面、关闭窗口前强制落盘
- [ ] 「保存」与「放弃修改」按钮不复存在，引用它们的测试断言同步调整
- [ ] 内部脏标记保留且仍然正确反映未落盘状态
- [ ] 落盘写入沿用既有的原子写入与跨进程事务锁，不改写入方式
- [ ] 落盘延迟由注入时钟驱动，测试中**不出现真实等待**
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
