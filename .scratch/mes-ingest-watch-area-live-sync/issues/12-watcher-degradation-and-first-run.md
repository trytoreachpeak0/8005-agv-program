# 12 — 目录降级与首次创建

**What to build:** 配置目录被删除、改名或因其他原因无法监视时，界面明确告知用户列表可能不是最新的，并在目录恢复后自动重新开始监视——用户不该在毫不知情的情况下看着一份过期的列表。首次使用 Watch 时配置目录自动创建，用户不需要手工准备。

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] 监视失效时界面显示明确的降级提示
- [ ] 目录恢复后自动重建监视并刷新列表
- [ ] 文件系统事件缓冲区溢出时触发全量重扫，目录状态不丢失
- [ ] 首次使用时配置目录自动创建
- [ ] 目录不存在时列表呈现为空而非报错
- [ ] 页面切走与窗口关闭时监视资源被释放
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
