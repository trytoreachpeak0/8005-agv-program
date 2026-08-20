# 04 — 删除延迟确认与改名跟随

**What to build:** 主流编辑器保存文件的方式是「写临时文件再替换或改名」，在文件系统层面表现为删除紧接着新建——本项目自身的原子写入也是如此。因此用户在别处保存配置文件时，这个配置不应该在列表里闪烁或短暂消失。文件被改名时，正在编辑它的界面跟随到新名字，而不是弹出「文件已删除」的误报。

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] 外部编辑器保存导致的「删除后立即重现」不被判定为删除，列表无闪烁
- [ ] 延迟确认窗口过后文件仍不存在，才判定为真删除
- [ ] 判定为内容更新时按 03 的同步规则处理
- [ ] 文件被改名时列表项改名并重排
- [ ] 正在编辑的文件被改名时界面跟随到新名字，不提示已删除
- [ ] 上述时序全部由 `FakeTimeProvider` 驱动，测试中**不出现真实等待**
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
