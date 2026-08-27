# 02 — 按 Variant A 交付完整资格审计工作台

**What to build:** 让资格审计使用者在生产页面中获得已批准的 Variant A 语义分层工作台：从带标签的 TransportDemand 主列表选择一项后，先看到当前外部可读结论，再通过唯一 MES 观测、当前阻断条件、外部可读资格、缺值与查询语义四个稳定区域核对完整证据。

**Blocked by:** 01 — 建立可持久化的生产语言切换基础.

**Status:** implemented-awaiting-visual-validation

- [x] 桌面态保留约 330 epx 主列表、12 epx 间距和弹性详情；1440×900 下结构与已选 Variant A 信息层级一致且不包含评审 chrome。
- [x] 无表头列表逐行显示 DemandId、WorkType、SUBLOT、本地化资格结论及规范主要阻断码，选择状态不只依赖颜色。
- [x] 详情结论条同时呈现本地化结论、主要原因、规范码和相关原始字段；全部阻断原因仍可在结构化证据中检查。
- [x] 可信唯一观测呈现 AREA、EQP、STEP、DATES、PACKAGE 和最近观测的可见标签；重复观测不任选单值，来源 NULL 不以通用破折号代替。
- [x] 来源未提供、系统未知、不适用、尚未加载、查询成功但无结果和读取失败进入不同强类型状态；失败保留旧值时同时显示最后成功时点。
- [x] READABLE、NOT_READABLE、GONE、Series 已归档、LongGoneButVisible、重复业务键、SUBLOT 多 WorkType 和缺字段数据都保持同一信息层级。
- [x] 资格、WorkType、原因和标识筛选显示本地化含义与规范代码，但提交和保存的始终是规范代码。
- [x] 语言切换保留已提交筛选、页码、选中 Demand、主/详情滚动位置和跳转需求系列所需的审计上下文，且不触发读取。
- [ ] 720 epx、英文长文案及高 DPI 下采用生产响应式重排，不出现水平裁剪、覆盖或不可达操作。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

