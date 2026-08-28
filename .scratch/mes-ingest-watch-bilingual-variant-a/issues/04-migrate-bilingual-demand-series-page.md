# 04 — 迁移双语需求系列调查页

**What to build:** 让需求系列使用者能够在中文或英文中浏览 Tracking、GONE、Archived 和归档后仍可见状态，使用规范筛选和稳定分页选择一个 Series，并从同一调查上下文进入 DemandSeries Inspector。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** done

- [x] 页面标题、刷新状态、AREA 范围、筛选、分面、列表、生命周期、详情、分页、空态、失败态和 Inspector 动作全部双语化。
- [x] 生命周期、当前出现状态和 WorkType 等筛选显示本地化含义及规范代码；ViewState 与 Host 请求始终保存规范代码。
- [x] 列表和详情中的 SeriesId、DemandId、SUBLOT、WorkType、协议码、原始 MES 值及绝对时间保持可机器对照。
- [x] 多值身份摘要使用完整字段标签并按字段换行；必要截断同时提供完整 Tooltip 和复制操作。
- [x] 加载、成功零结果、读取失败和保留旧快照不会共享同一个空态或占位符。
- [x] 语言切换保留全部已提交筛选、页码、选中 Series/Demand、主/详情滚动位置和焦点，且不增加 Host 请求。
- [x] 打开 Inspector 时携带同一 Series、Demand 和调查上下文；页面语言变化不改变 Inspector 生命周期。
- [x] 中文、英文和 720 epx 下命令、分页及详情证据可达，不出现水平裁剪或仅凭位置解释的值。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

