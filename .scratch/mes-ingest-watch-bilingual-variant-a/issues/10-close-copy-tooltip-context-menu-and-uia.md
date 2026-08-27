# 10 — 收口复制、Tooltip、上下文菜单与 UIA

**What to build:** 让键盘、屏幕阅读器和复制工作流与已经迁移的全部页面使用同一语言，同时保证技术值、规范代码和原始证据在复制与无障碍投影中不被翻译或重新格式化。

**Blocked by:** 02 — 按 Variant A 交付完整资格审计工作台; 03 — 迁移双语概览与统计语义; 04 — 迁移双语需求系列调查页; 05 — 同步双语 DemandSeries Inspector; 06 — 迁移双语错误检索; 07 — 迁移双语 AREA 筛选工作区; 08 — 迁移双语接入告警; 09 — 统一通知、对话框与运行反馈.

**Status:** implemented-awaiting-visual-validation

- [x] 单元格复制保持标识、代码、原始值和带偏移时间的机器可对照格式。
- [x] 整行和“含列头”复制的说明性列头跟随当前语言，值和规范码逐字不变；JSON、日志和原始证据不本地化。
- [x] Tooltip 和上下文菜单完整双语化，但 Tooltip 只补充帮助或完整截断值，不承担唯一字段标签。
- [x] Automation Name、HelpText、状态和 live region 使用当前语言并包含必要字段语义与原始值；AutomationId 保持稳定。
- [x] 语言切换后复制命令、菜单、键盘选择、焦点和 Tab 顺序保持可用，不产生重复 live-region 播报。
- [ ] 选中、通过、阻断、未知和失败均有文字或图标语义，主题和高对比状态下不依赖颜色。
- [x] 生产窗口六个页面、设置、Inspector、通知和对话框不存在遗漏的单语言辅助文本。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
