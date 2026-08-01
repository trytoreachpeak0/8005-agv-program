# 17 — 用 TransportDemandKey 值对象收敛业务键 seam

**What to build:** 将 MesIngest 内部以 TASK_TYPE + SUBLOT 表示的运输需求业务键收敛为 `TransportDemandKey` 值对象，使 reappear 历史查询、Reconciler 与 store 接口直接表达领域身份，避免继续扩散成对字符串参数，同时不改变外部 API、SQL schema 或既有匹配语义。

**Blocked by:** None — can start immediately

**Status:** ready-for-human

- [x] `TransportDemandKey` 明确定义 TASK_TYPE + SUBLOT 的相等性、大小写与空值约束，并与现有生产语义一致
- [x] reappear 历史查询、Reconciler callback、内存/SQL store 与 telemetry decorator 使用该值对象，不再传递新的 taskType/sublot 参数对
- [x] Oracle/CSV 输入、HTTP DTO、OpenAPI 与 SQL 表结构保持兼容，不为内部重构改变外部契约
- [x] 首次出现、VISIBLE、GONE、跨 GONE 再现及同 SUBLOT 不同 TASK_TYPE 的行为保持不变
- [x] 单元测试锁定值对象相等性和边界；现有 Reconciler、store、API 与完整 Release 测试全绿

## Comments

- 2026-08-01: Added an immutable `TransportDemandKey` with ordinal, case-sensitive value equality, non-blank component validation, and no normalization. Reconciler key sets/grouping and GONE-history callback, both stores, telemetry decorator, and store test doubles now use the value object. Oracle/CSV, HTTP/OpenAPI, and SQL schema contracts are unchanged. Targeted Release tests passed 125/125; full `MesIngest.sln` Release suite passed 423/423.
