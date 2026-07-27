# 13 — DemandDto 嵌入相关告警

**What to build:** 只读需求 API 的 `DemandDto`（列表与单条）带上与该 DemandId / 对账键相关的告警，满足 Story 33「relevant alerts」，调用方不必再按 demandId 自行 join `/api/alerts`。

**Blocked by:** None — can start immediately（01 / 03 已完成；本票为 review Spec A1 跟进）

**Status:** done

- [x] `GET /api/demands` 与 `GET /api/demands/{id}` 的每条需求包含相关告警集合（至少覆盖带 DemandId 的活跃/近期告警；键级告警若可关联到该需求亦应纳入）
- [x] 无相关告警时返回空集合，不改变既有需求字段语义
- [x] `/api/alerts` 仍可独立列出全局告警（本票不删除该端点）
- [x] HTTP 契约测试覆盖：有/无相关告警时的 DTO 形状；Watch 若消费新字段则同步或保持向后兼容

## Comments

- 2026-07-27: From `/code-review ffe1f49` Spec A1 (light) / Story 33. Evidence: `DemandDto` in `Program.cs` has no alerts; clients must join `GET /api/alerts` by demandId.
- 2026-07-27: Implemented — `DemandDto.Alerts` embeds alerts matched by DemandId or TASK_TYPE+SUBLOT; empty array when none; `/api/alerts` unchanged. Watch keeps separate `/api/alerts` fetch (JSON extra props ignored). Contract: `Demand_dto_embeds_relevant_alerts_by_demand_id_or_reconcile_key`.
