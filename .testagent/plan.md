# Ticket 09 test implementation plan

## Vertical slices

1. **Domain eligibility and catalog value identity**
   - Red: readable unique VISIBLE member versus missing/invalid/duplicate/multi-WorkType/GONE/archived.
   - Green: centralized `ExternallyReadableDemand` policy and immutable catalog item contract.

2. **Persisted catalog revision and Host conditional read**
   - Red: first full response; stable DemandId order; unchanged SUCCESS/replay/non-success keep revision;
     member enter/exit/value change bump once; same revision returns empty-body 304; query filters rejected.
   - Green: schema v9 catalog state/items/commit evidence, one reconciliation at SUCCESS transaction end,
     atomic projection read, Host ETag mapping.

3. **Lifecycle/error tracer scenarios**
   - Red/green in small public-seam scenarios for field error/recovery, duplicate/recovery,
     multiple WorkTypes/recovery, GONE and postarchive visibility, plus stable current Watch detail.

4. **Reference consumer**
   - Red: fresh/restarted cache reconstructs solely from full catalog; commitment always rereads;
     missing/changed candidate rejects or asks for re-decision; accepted snapshot stays immutable;
     timeout leaves the same stable intent UNKNOWN and reconciliation never changes its key.
   - Green: isolated class library with catalog client/store/order-gateway ports and an HTTP adapter.

5. **Validation**
   - focused tests after each slice;
   - real SQL ticket gate with no skips;
   - ticket01-08 regression slice;
   - Release non-incremental solution build;
   - complete core test suite once;
   - assertion/gap audit, then two-axis `/code-review` and fixes.

## Requirement-to-test targets

| Requirement | Planned executable evidence |
| --- | --- |
| 1 | `Catalog_only_contains_centrally_eligible_demands_while_operations_detail_keeps_every_rejected_demand` |
| 2 | `Catalog_returns_complete_stable_items_in_demand_id_order_and_rejects_dispatch_scope_queries` |
| 3 | `Catalog_revision_changes_once_only_for_member_or_member_value_changes` |
| 4 | `Conditional_catalog_read_returns_bodyless_304_or_one_atomically_committed_full_revision` |
| 5 | `Disposable_cache_rebuilds_after_restart_from_only_the_complete_catalog` |
| 6 | `Commitment_reread_rejects_changed_or_missing_candidate_and_preserves_accepted_snapshot`; `Unknown_order_result_reconciles_with_the_same_stable_intent_identity` |
| 7 | lifecycle/error catalog tests plus a consumer/Host isolation assertion and ticket09 SQL gate |

## Completion conditions

- Every checklist row maps to a concrete passing test/assertion.
- Generated tests are visible through the existing `MesIngest.sln` harness.
- `.testagent/status.md` records final exact test/build/review evidence.
