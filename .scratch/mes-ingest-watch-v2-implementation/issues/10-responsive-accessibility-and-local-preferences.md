# 10 — 完成响应式布局、可访问性与本机偏好

**What to build:** 让 MesIngestWatch V2 在工厂常用 Windows 视口和缩放下保持清晰、可键盘与 UI Automation 操作，并只跨重启保存安全、明确获准的本机配置和布局偏好。

**Blocked by:** 03 — 完成概览健康结论与业务摘要; 06 — 完成 TransportDemand 详情、选择与复制; 08 — 完成 IngestAlert 到 TransportDemand 的精确定位; 09 — 统一四视图自动刷新、取消与陈旧错误表达

**Status:** ready-for-agent

- [ ] `1440×900` 下导航、页面状态、刷新/取消、查询摘要和详情保持可用；宽表允许水平滚动，错误和最后成功时间不能只藏在 tooltip。
- [ ] `2560×1440` 利用额外空间扩展表格和详情，但不改变信息层级、导航或主要操作位置；125%/150% DPI 下无关键控件裁切。
- [ ] 使用统一浅色工业运维视觉 token；健康、警告、错误、陈旧和取消状态同时使用文字或图标，不能只依赖颜色。
- [ ] 所有导航、按钮、标签、筛选、表头、行、详情和关联操作具有稳定、语义化的 UI Automation 名称，并能通过键盘完成关键旅程。
- [ ] 允许保存 Host 基址、安全凭据引用、全局超时、四视图自动刷新偏好、窗口大小和详情分隔位置，并提供“恢复默认布局”。
- [ ] 禁止跨重启保存业务列表、查询、cursor、页码、选择、详情、最后成功业务时间或 Host 错误；损坏、越界或版本不兼容偏好安全回退默认值。

## Comments

- 2026-08-09：补齐黄金机真实窗口 DPI smoke。首次 125% 运行发现详情虽然可见，但布局 `Grid` 不发布稳定 UIA peer，导致 `DemandDetailsPanel` 在两条 journey 中不可定位；修复为在可访问的详情标题上发布稳定 AutomationId，并为 Demand/Alert 筛选侧栏增加纵向滚动，避免缩放后底部查询操作不可达。最终 125%（120 DPI）与 150%（144 DPI）均为环境探针 1 passed、FlaUI/UIA journeys 5 passed / 0 skipped / 0 failed；证据见 `mes/ingest/csharp/TestResults/ticket10-dpi-smoke-20260809/README.md`。本记录不批准 Ticket 11/12 视觉基线，也不自动改变本票状态。
