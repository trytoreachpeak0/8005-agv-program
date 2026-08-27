# 07 — 迁移双语 AREA 筛选工作区

**What to build:** 让使用者在中文或英文中管理本机 AREA 筛选配置，并在语言切换期间无损保留所选配置、未保存编辑、光标、滚动、验证结果和并发写入冲突。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** ready-for-agent

- [ ] 配置列表、搜索、编辑器状态、目录与文件动作、验证、自动保存、应用状态、空态、失败态和帮助完整双语化。
- [ ] 保留已批准的 Variant A master-detail 编辑器层级，不重新采用已拒绝的变体或改变 AREA 配置业务语义。
- [ ] AREA、配置名、文件内容、路径和诊断技术值保持原样；用户说明、按钮、状态和验证含义使用当前语言。
- [ ] 并发写入冲突的说明、选项、焦点和无障碍文本即时切换，但语言变化不解决冲突、不触发保存或改变磁盘版本。
- [ ] 切换语言保留当前配置、未保存草稿、光标位置、选择范围、编辑器滚动、文件身份和冲突状态。
- [ ] 切换不触发目录写入、配置应用、Host 请求或自动保存计时重置。
- [ ] 中文、英文、720 epx、高 DPI、主题和高对比状态下列表、编辑器、行号、命令和对话框均可达且不重叠。
- [ ] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

