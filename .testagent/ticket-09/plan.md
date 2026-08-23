# Ticket 09 TDD plan

Work in vertical red -> green slices. This delegated test task writes only the first red batch; production implementation remains with the parent agent.

## Requirement mapping

| Ticket requirement | Planned test evidence | Phase |
| --- | --- | --- |
| "当前资格结论从当前 Demand、Series、条件和资格投影读取，不通过完整历史重算。" | `Current_audit_list_does_not_wait_for_raw_history`; later add a current-result fixture that deletes retained raw rows and still returns the same blockers, trusted fields, count, and facets. | Red batch 1 / implementation slice 1 |
| "冻结列表、精确总数、原因分面、稳定分页与详情绑定同一 HistoryEpoch 和 ProjectionCommit。" | `Audit_snapshot_exposes_the_database_history_epoch`; existing `Audit_filters_facets_area_order_and_detail_share_one_exact_snapshot` and `Audit_order_and_bounded_pages_are_stable_and_credentials_fail_explicitly`; strengthen them after the identity compiles to assert epoch equality on every page/detail. | Red batch 1 / slice 2 |
| "详情保持完整 ReadabilityBlocker 集合、可信字段或冲突证据、Series、PollTrace 与 CatalogRevision。" | Existing `Audit_filters_facets_area_order_and_detail_share_one_exact_snapshot`; add a Ticket 09 frozen-detail assertion covering the complete multi-blocker evidence payload at the selected commit after the frozen model is implemented. | Slice 3 |
| "snapshot/cursor 跨纪元、提交、筛选、AREA、顺序或页大小复用时被明确拒绝。" | Existing token test covers commit-bound cursor identity, filter/AREA/order/page-size mechanics and tampering. Add `Audit_snapshot_and_cursor_are_rejected_when_history_epoch_does_not_match` after `ReadabilityAuditSnapshotIdentity` gains `HistoryEpoch`, following Ticket 06 prior art. | Slice 2 |
| "并发投影不能让列表结论与详情理由来自不同提交。" | `Audit_list_and_detail_are_wholly_old_or_new_at_a_concurrent_commit_fence`; gate list and detail at commit A, require commit B to finish before releasing either frozen reader, then assert both old responses remain at commit A. | Red batch 1 / slice 3 |
| "0、7、30 天真实 SQL Server 门禁证明当前逻辑读有界，全部 SQL 测试实际运行。" | Extend `ScaleAndQueryEvidenceGateTests` fail-closed fixtures for ReadabilityAudit and the scale script's 0/7/30 profiles; final evidence must show real SQL `Failed: 0, Skipped: 0` plus saved logic-read/plan/grant/spill artifacts. | Slice 4 / final validation |

## Sequence

1. Add the three first-batch real Host/SQL tests above and run only the Ticket 09 class, recording the expected red causes.
2. Parent implementation: create a current ReadabilityAudit read model/path and preserve frozen historical semantics.
3. Bind snapshot/cursor/Host DTO/OpenAPI/Watch wire identity to `HistoryEpoch`; add exact cross-epoch negative tests.
4. Extend `ProjectionReadSurface` / `IProjectionReadBoundaryObserver` to ReadabilityAudit and implement a nonblocking commit-consistent frozen view. Do not reuse a current-read locking pattern that holds the projection writer behind the observer gate.
5. Complete detail payload and concurrency assertions, then add ReadabilityAudit fail-closed scale fixtures and 0/7/30 evidence.
6. Re-open every generated assertion against the public seam, run scoped tests, real-SQL Tier 1 with zero skips, and the required scale gate. Record gap/assertion review in `status.md` only when green implementation is available.
