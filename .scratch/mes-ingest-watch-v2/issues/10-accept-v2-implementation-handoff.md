# 确认 V2 实现交接

Type: grilling
Status: resolved
Blocked by: 09

## Question

汇编后的《MesIngestWatch V2 产品与交互规格》是否完整、内部一致并通过用户最终评审，足以关闭决策地图并进入独立的生产实现规划？

## Comments

- 2026-08-07：用户确认长期 `MesIngestWatch` 产品概念仍可包含链路延迟能力，但 V2 是当前范围子集，明确不包含性能、trace、遥测和诊断功能；规格已改为用“MesIngestWatch V2”定义本期产品，并保留 `CONTEXT.md` 的长期领域定义。
- 2026-08-07：用户确认概览的一次刷新操作允许并发读取 PollHealth、活动 IngestAlert 与 VISIBLE TransportDemand；子请求共享取消、Host 会话和请求代次，并按资源独立原子提交。其它视图仍各自保持单一刷新操作。
- 2026-08-07：用户确认 V2 的 IngestAlert 时间筛选收缩为 `lastSeenAt` 范围，与现有 `/api/alerts?from=&to=` 契约一致；`firstSeenAt` 仅保留显示与服务端排序，不新增筛选或 Host API 版本变化。
- 2026-08-07：完成实现可行性复核。现有 `/api/contract`、`/api/poll-health`、`/api/demands`、`/api/demands/{demandId}`、`/api/alerts` 及其 OpenAPI/查询解析器可支撑收缩后的全部读取、筛选、排序、分页与 Alert → Demand 跳转；同时澄清 Demand 的 `locationRiskCode` 不可排序，以及点击“应用”即作废旧 Host 会话、验证失败也不得恢复旧业务数据。
- 2026-08-07：用户最终批准《MesIngestWatch V2 产品与交互规格》，授权将规格标记为已确认、完成交接检查表并关闭本决策地图。

## Answer

《MesIngestWatch V2 产品与交互规格》已通过最终人工评审，可以作为独立生产实现规划的权威输入。评审确认四页信息架构、字段与文案、只读范围、本机自动化验收和实现交接边界完整且内部一致。

最终评审消除了三处歧义：V2 是长期 MesIngestWatch 产品概念的当前范围子集，不包含性能、trace、遥测和诊断；概览以单一刷新操作协调可并发的 PollHealth、活动 IngestAlert 与 VISIBLE TransportDemand 子请求；IngestAlert 时间筛选仅使用现有 Host 契约支持的 `lastSeenAt` 范围。实现可行性复核同时固定了 Demand 可排序列与 Host 切换时旧会话立即作废的行为。

现有 Host 只读 API/OpenAPI 能支撑规格所需查询、分页、排序和 Alert → Demand 跳转，不需要在进入实现规划前新增或版本化业务契约。规格状态与最终交接检查表均已更新为通过；生产实现、实现票拆分、发布迁移和现场部署仍按地图边界留给独立后续规划。
