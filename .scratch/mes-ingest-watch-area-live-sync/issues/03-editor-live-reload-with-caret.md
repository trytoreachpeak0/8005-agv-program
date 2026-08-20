# 03 — 外部改文件时编辑器自动同步

**What to build:** 用户在 Watch 里查看某个 AREA 配置的同时，另一个程序（记事本、VS Code 等）修改并保存了同一个文件。编辑器内容自动更新为文件的新内容，而用户的光标位置、选中范围和滚动位置保持不动——每次外部保存都让光标跳回开头，比冲突提示还难用。「从磁盘加载」按钮随之移除。

本 ticket 只处理缓冲干净的情形。缓冲为脏时的并发冲突属于 06。

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] 外部修改并保存后编辑器内容自动更新
- [ ] 更新后光标位置、选中范围、滚动位置保持
- [ ] 磁盘内容与编辑器当前内容逐字节相同时不触发重载
- [ ] 本进程自身写盘产生的事件被抑制，不导致重载与光标跳动
- [ ] 文件正被外部写入而读取失败时按退避重试，重试耗尽才报错
- [ ] 事件回调切回 UI 线程后才更新界面
- [ ] 「从磁盘加载」按钮不复存在，引用它的测试断言同步调整
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
