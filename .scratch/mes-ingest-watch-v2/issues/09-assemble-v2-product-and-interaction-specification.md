# 汇编 V2 产品与交互规格

Type: task
Status: resolved
Blocked by: 01, 02, 07, 08, 11, 13

## Question

如何把已确认的 MES 任务/IngestAlert 事实目录、简化信息架构与原型、刷新分页状态模型和自动化策略汇编为一份可追溯、无冲突、可直接交给实现阶段的《MesIngestWatch V2 产品与交互规格》？

## Answer

已汇编形成单一交接候选：[《MesIngestWatch V2 产品与交互规格》](../spec.md)。规格把已确认决定收口为四页 WPF 产品壳、领域事实目录、现有 Host 只读契约、按 Host 会话/视图隔离的浏览状态机、页面字段与跳转、错误/陈旧表达、本机持久化安全边界以及可直接验收的 UIA/视觉矩阵。

汇编时解决了一处契约冲突：现有列表响应只有 `items/nextCursor/hasMore`，没有总数，因此概览在 `hasMore=false` 时显示当前第一页的精确数量，在 `hasMore=true` 时显示 `100+`，不得用 `PollHealth.rowCount` 或第一页长度伪造 VISIBLE Demand/活动 IngestAlert 总量。其余筛选、排序、分页和 Alert → Demand 行为均可由现有 `/api/contract`、`/api/poll-health`、`/api/demands`、`/api/demands/{demandId}` 与 `/api/alerts` 契约实现，不要求扩大业务写边界。

规格状态为“待最终交接确认”；下一张[确认 V2 实现交接](10-accept-v2-implementation-handoff.md)只需对该单一规格做最终人工完整性与一致性评审。本票不创建生产实现或实现拆分。
