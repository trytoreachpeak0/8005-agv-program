# 验证六区域 WPF 交互原型

Type: prototype
Status: resolved
Blocked by: 01

## Question

使用代表性假数据覆盖健康、活动异常、慢链路、离线、空状态和分页浏览时，怎样的六区域导航、信息层级、Demand/Alert 下钻及按页刷新交互，能让现场实施与运维工程师快速判断并定位问题，同时保持 WPF 流畅？

## Comments

- 2026-08-04：已建立可运行的 throwaway WPF 假数据原型 [`MesIngest.Watch.Prototype`](../../../mes/ingest/csharp/MesIngest.Watch.Prototype/README.md)，提供 A“全局态势看板”、B“事件处置优先”、C“证据时间线优先”三种结构方案，以及健康、活动异常、慢链路、Host 离线、空状态、分页浏览六种场景。固定底部栏/左右键切换方案；六区域导航、Demand/Alert 下钻、当前页手动/自动刷新、单飞取消与最后成功窗口均可交互评审。截图资产：[`A`](../prototype/variant-a.png)、[`B`](../prototype/variant-b.png)、[`C`](../prototype/variant-c.png)。本票等待用户实际评审，尚未形成 Answer 或关闭。

## Answer

用户于 2026-08-04 确认采用组合方案：以 A“全局态势看板”为全局产品壳和默认概览；吸收 C 的证据时间线，但仅作为“诊断”和“性能分析”中的上下文面板，不永久占用所有页面；吸收 B 的事件队列，但仅放在“告警分析”页，不作为全局常驻栏。

由此固定以下原型级决定：

- 六个一级区域保持左侧导航：概览、运输需求、告警分析、性能分析、诊断、设置；默认浅色工业运维风格。
- 概览首先平衡展示接入健康、活动异常数量、VISIBLE Demand 数量和最新链路耗时，并在同屏提供当前需定位问题与最近一轮四阶段链路，使现场人员能在约 10 秒内完成首轮判断。
- Demand 与 Alert 下钻保留来源列表/筛选上下文；Alert 始终只读，不增加确认、指派、备注或手工关闭动作。
- 连接事件、IngestAlert 与 poll trace 在证据时间线中分轨呈现；`DATES` 的 MES 数据年龄与四阶段链路耗时继续明确分离。
- 所有数据页默认手动刷新，可按当前页启用自动刷新；刷新单飞、可取消、不排队，切页或新请求使旧响应失效，失败/取消继续保留最后成功窗口。精确状态机与游标规则留给“定义流畅刷新、游标分页与取消模型”。
- 健康、活动异常、慢链路、Host 离线、成功空结果和分页浏览均已用假数据走查；页面 token、密度、列宽和最终状态文案留给“锁定页面交互与视觉行为”。

评审资产保留在 [`MesIngest.Watch.Prototype`](../../../mes/ingest/csharp/MesIngest.Watch.Prototype/README.md) 及 [`A`](../prototype/variant-a.png)、[`B`](../prototype/variant-b.png)、[`C`](../prototype/variant-c.png) 截图中；它们是规格决策的原始证据，不是生产实现。
