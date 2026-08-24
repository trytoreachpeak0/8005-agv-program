# 12 — 错误详情与受限原始证据

**What to build:** 让运维工程师从错误检索结果打开与当前筛选真正匹配的错误期间和诊断证据，并保持详情与列表相同的 `ErrorSearchAsOf`。默认详情提供足以解释规则的结构化证据；完整 `DemandRawObservation` 只能经过受访问控制、敏感字段白名单和大小上限的按需读取获得，使现场能够深挖源数据而不会把错误页变成任意日志或无限数据出口。

**Blocked by:** 08 — 提供 DemandSeries 冻结快照列表与详情；11 — ErrorSearchAsOf 列表、窗口与分面

**Status:** ready-for-human

- [x] 从一个错误列表项打开详情时，响应绑定同一 `ErrorSearchAsOf`、规范化筛选与契约版本；查询后产生的新事件不会混入已打开详情，显式刷新后才能进入新快照。
- [x] 详情只返回满足当前分类、错误码和时间条件的 `DemandSeriesErrorPeriod` 及证据，不把所属 Series 的其它错误或完整事件历史冒充命中结果。
- [x] 与查询窗口相交但在窗口外开始或结束的期间会明确展示真实边界及交叠语义；`CONDITION_CLEARED` 与 `DEMAND_GONE` 保持不同结束原因，活动期间不会伪造结束时间。
- [x] 默认诊断证据可观察到错误主体、观测值、期望规则、相关 DemandId 或 WorkType、Host 证据时间、PollTrace，以及期间开启、证据变化和结束事实；相同内容不会按每轮重复或退化为 OccurrenceCount。
- [x] Demand 级错误不会跨 DemandId 拼接，Series 级错误可以跨世代展示但保留逐世代证据；列表摘要中的命中期间数和 Demand 世代数可由详情核对。
- [x] 完整原始观测默认不随列表或详情首屏返回，只能对已授权的具体证据按需展开；响应仅包含白名单字段，执行敏感字段脱敏，并对单条与总响应设置可验证的大小上限。
- [x] 无权限、对象不属于当前快照、请求超过上限或包含非白名单字段时得到稳定且不泄露内容的错误；单次拒绝不会改变错误历史、当前条件或其它业务投影。
- [x] 契约测试以重复原始行、字段缺失、非法 AREA、多 WorkType、跨窗口期间和并发新事件证明列表—详情一致性、边界标注、白名单、脱敏与大小限制均可从正式 API 观察。

## Implementation evidence

- Contract/schema: `2026.08.new-mes-ingest.tracer.12` / schema `12`.
- Runtime routes: frozen detail at `GET /api/v2/error-search/{seriesId}` and explicitly authorized raw expansion at `GET /api/v2/error-search/{seriesId}/evidence/{evidenceId}/raw-observations`.
- Raw policy: seven-field allowlist; 20 items; 2,048 UTF-8 bytes per item; 65,536 UTF-8 bytes total; secret-pattern redaction.
- Real SQL Server 16 / compatibility 160 gate: exactly 6 passed, 0 skipped; `mes/ingest/csharp/.artifacts/ticket12-tests/ticket12-error-detail-sqlserver.trx`.
- Ticket 11 Error Search regression: 8 passed, 0 skipped.
- Pseudo-mutation gap audit: the `EndedAt == window.ToUtc` boundary mutation survived initially, then was killed by the added exact-boundary assertion.
- Release solution build passed. Full core suite: 606 passed / 19 skipped / 2 failures outside Ticket 12; the UI Automation title-bar failure passed in isolation, while the pre-existing latency-retention clock mismatch remains reproducible.
- Independent Standards/Spec review passed after fixing whole-value Bearer credential redaction and active-period `endsAfterWindow` semantics.

## Comments

- 2026-08-13: Ticket 12 is complete and ready for human verification. Existing DemandSeries/PollTrace raw payloads remain unchanged because Ticket 08 explicitly owns that contract; Ticket 12 gates the new Error Search raw-evidence expansion without broadening scope into a breaking legacy API change.
