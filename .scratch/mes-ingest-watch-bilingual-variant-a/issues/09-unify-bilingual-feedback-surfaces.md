# 09 — 统一通知、对话框与运行反馈

**What to build:** 让 toast、InfoBar、ContentDialog、字段校验和恢复说明在所有页面使用同一语言与术语，并让正在显示的反馈在语言切换后原地更新而不被当成新的业务或告警事件。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** ready-for-agent

- [ ] toast 的严重度、标题、说明、动作、计数、计时和关闭帮助均从共享双语目录投影。
- [ ] InfoBar、ContentDialog、字段校验、操作成功/失败和恢复说明使用同一术语与未知码回退规则。
- [ ] 切换语言更新当前通知和已打开对话框，但不重新登记事件、不重置消失期限、不重播进入动画、不改变 continuing fault 生命周期。
- [ ] live region 对新事件只播报一次；纯语言重投影不会制造重复告警或重复朗读。
- [ ] 通知动作、对话框选择、未完成输入、键盘焦点、暂停计时和页面范围在切换前后保持不变。
- [ ] 自动刷新开始/成功继续保持静默；新故障首次提示、持续故障收缩和恢复反馈不因本地化改变既有层级。
- [ ] 中文、英文、窄窗、减少动画、高对比和后台/非活动状态下反馈不抢焦点、含义不只依赖颜色。
- [ ] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

