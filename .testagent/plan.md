# Ticket 10 test implementation plan

## Vertical red -> green slices

1. **Stable blocker vocabulary and qualification checks**
   - Red: all seven immutable codes exist once, stable diagnostic-first priority selects one lead while preserving all blockers, AREA vocabulary validation is exact.
   - Green: `ReadabilityBlockerCatalog` and shared audit contracts.

2. **Independent signed audit identity and cursor**
   - Red: round-trip includes ProjectionCommit plus CatalogRevision and cursor includes normalized filters/AREA/order/page/anchor; tampering and cross-condition reuse fail.
   - Green: audit-specific HMAC token codec over the existing persisted signing key.

3. **Frozen list, exact facets, filter/AREA/order/page**
   - Red: production SQL/Host lists every Demand generation, applies OR-within/AND-across filters and trusted AREA before exact counts, orders by the fixed contract, and pages at 1..200.
   - Green: one serializable as-of query with bounded result rows and exact server-side aggregates.

4. **Same-snapshot detail and evidence**
   - Red: detail returns all seven checks, all matched blocker evidence, unique fields or the conflicting raw multiset, Series summary, latest PollTrace/value provenance, ProjectionCommit and CatalogRevision.
   - Green: one demand-at-snapshot read through `IMesIngestProjection` and formal HTTP endpoint.

5. **Refresh and error semantics**
   - Red: an always-unreadable Demand changes blocker while `CatalogRevision` stays fixed; old pages/detail remain fixed and a refresh gets the new commit. Invalid/tampered/mismatched/unretained credentials return stable structured errors.
   - Green: snapshot resolution/error mapping and explicit refresh-by-omission semantics.

6. **Validation and review**
   - focused green run after each slice;
   - formal real-SQL ticket gate with no skips;
   - Release non-incremental solution build;
   - complete core suite once;
   - assertion/gap audit, then `/code-review` Standards + Spec and fixes.

## Requirement-to-test targets

| Requirement | Planned executable evidence |
| --- | --- |
| 1 | `Audit_lists_every_demand_generation_with_readability_separate_from_lifecycle` |
| 2 | `Blocker_catalog_is_complete_and_lead_priority_never_discards_other_reasons`; complex audit/detail tracer |
| 3 | `Audit_filters_use_or_within_and_across_dimensions_with_domain_identifier_matching` |
| 4 | `Area_scope_is_exact_and_excludes_untrusted_current_area_before_counts_and_pages` |
| 5 | `Audit_order_and_bounded_pages_are_stable_with_an_exact_total` |
| 6 | `Audit_facets_exclude_their_own_dimension_and_overlap_without_inflating_total` |
| 7 | `Audit_snapshot_stays_frozen_when_a_new_commit_changes_blockers_without_changing_catalog_revision` |
| 8 | `Audit_detail_uses_the_list_snapshot_and_returns_complete_checks_raw_evidence_and_provenance` |
| 9 | `Audit_tokens_bind_snapshot_filters_area_order_contract_and_reject_tampering_or_reuse` plus HTTP credential assertions |

## Completion conditions

- Every checklist row maps to at least one concrete passing assertion at the confirmed seam.
- New tests are discovered by the existing `MesIngest.sln` harness.
- `.testagent/status.md` records the exact clean build/test/gate/review evidence.
