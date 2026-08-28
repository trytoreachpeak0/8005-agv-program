# 05 — 同步双语 DemandSeries Inspector

**What to build:** 让独立 Inspector 窗口与主窗口共享同一显示语言，并在不重载业务快照的情况下以当前语言解释 Demand 形成原因、MES 边界差异和事件证据，同时始终保留内部原因码和原始事实。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** done

- [x] 标题栏、上下文、标签页、形成原因、证据标签、MES 差异、事件、空态、帮助和 UIA 全部使用共享双语目录。
- [x] `FIRST_OBSERVED`、`PREARCHIVE_REAPPEARANCE`、`POSTARCHIVE_REAPPEARANCE` 等已知原因分别显示原因特定事实和不变的原始码。
- [x] 未知或格式错误的形成原因使用中性本地化回退并保留原始码，不借用已知原因的严重度、证据模板或处置叙事。
- [x] 主窗口切换语言后，所有已打开 Inspector 同步更新；随后打开的窗口直接继承当前语言。
- [x] 切换保留窗口位置、当前 Series、当前 Demand、选中标签、事件过滤、焦点和滚动位置，不重新读取或伪造证据。
- [x] 标识、原始 MES 行、JSON、字段名、内部代码和带偏移绝对时间逐字保持不变。
- [x] 中文、英文、窄窗、高 DPI、主题和高对比状态下的层级、键盘路径及非颜色状态表达保持可用。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

