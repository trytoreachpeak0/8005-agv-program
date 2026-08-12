# 10 — ReadabilityAuditSnapshot 查询与详情

**What to build:** 让运维工程师通过一个冻结的 `ReadabilityAuditSnapshot` 核对每个已生成 TransportDemand 世代当前是否属于 `ExternallyReadableDemand`，并从列表、精确统计和详情追到完整资格检查证据。资格审计必须把生命周期与可读资格分开，展示全部稳定 `ReadabilityBlocker`，在 Host 端完成 AREA 范围、筛选、计数、排序和有界分页，且整个查询过程始终绑定同一个 ProjectionCommit，而不是把 `CatalogRevision` 冒充审计快照。

**Blocked by:** 08 — 提供 DemandSeries 冻结快照列表与详情；09 — ExternallyReadableDemandCatalog 与 reference consumer

**Status:** ready-for-agent

- [ ] 审计可观察到每个已生成 Demand 世代，包括 VISIBLE、GONE、所属 Series 已归档及 LongGoneButVisible；每项独立给出 `READABLE` 或 `NOT_READABLE`，不会把资格状态等同于生命周期状态。
- [ ] 第一版稳定阻断目录覆盖 `DEMAND_GONE`、`SERIES_ARCHIVED`、`LONG_GONE_BUT_VISIBLE`、`DUPLICATE_TRANSPORT_DEMAND_KEY`、`SUBLOT_MULTIPLE_WORK_TYPES`、`REQUIRED_MES_FIELD_MISSING` 与 `INVALID_MES_FIELD_FORMAT`；一个 Demand 的全部命中原因均可见，列表主要原因由 Host 的稳定优先级选择。
- [ ] 列表支持资格、WorkType、阻断原因、DemandId 和 SUBLOT 条件；不同维度取交集、同维度多值取并集，默认同时包含可读与不可读，标识匹配规则与领域契约一致。
- [ ] 当前 AreaFilterProfile 的合法 MesArea 集合由 Host 在计数和分页前精确应用；不可信当前 AREA 不借历史值命中配置，只在“全部 AREA”范围内出现，AREA 条件不改变资格或 `CatalogRevision`。
- [ ] 列表默认先显示不可读项，再按主要原因优先级、DemandLastSeenAt 降序和 DemandId 升序稳定排列；默认每页 100、最多 200，并返回当前完整筛选下的精确 Demand 总数。
- [ ] 资格与原因分面按去重 Demand 精确计算且排除自身维度；同一 Demand 可计入多个原因分面，但原因数量之和不会被报告为不可读总数。
- [ ] 首次查询冻结独立的 `ReadabilityAuditSnapshot`，列表、分面、精确总数、后续页和详情共享其 ProjectionCommit 身份并携带当时的 `CatalogRevision`；并发产生的新提交只在显式刷新后的新快照出现。
- [ ] 详情从同一审计快照返回全部资格检查、完整阻断集合、可信字段或原始观测冲突、所属 Series、PollTrace、ProjectionCommit 与 `CatalogRevision`；主要原因不能替代完整推导。
- [ ] 游标绑定审计快照、规范化筛选、AREA 值集合、固定顺序与契约版本；无效、过期、篡改或跨条件复用均明确失败，不静默返回第一页或另一快照的数据。
