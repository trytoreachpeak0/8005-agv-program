# Ticket 12 TDD and implementation plan

## Vertical tracer bullets

1. Frozen detail: list -> signed snapshot -> detail; append/close after the snapshot and prove old detail is unchanged while refresh sees it.
2. Exact scope and overlap: prove category/code/window matching, true crossing boundaries, active null end, and distinct clear/gone reasons.
3. Structured evidence: prove open/change/close facts, subject/rule/Demand/WorkType/time/PollTrace, no per-round duplicates or OccurrenceCount.
4. Generation boundaries: prove Demand-scoped periods do not merge and Series-scoped periods preserve per-generation evidence; reconcile list counts.
5. Authorized raw: prove duplicate observations, missing values, invalid AREA, multi WorkType, fixed whitelist, redaction, item/total limit metadata, and no default raw.
6. Stable rejection: unauthorized, out-of-snapshot, unknown fields, and excessive limits return non-leaking stable errors and do not mutate any projection.
7. Release gate: contract/schema 12, focused real-SQL test run, solution build, one full test-suite run, independent standards/spec review.

## Requirement-to-test evidence

| Ticket requirement | Test evidence |
| --- | --- |
| Frozen as-of/filter/contract; later events only after refresh | `Frozen_detail_uses_the_list_snapshot_and_excludes_later_or_unmatched_periods` |
| Detail returns only matched periods/evidence | `Frozen_detail_uses_the_list_snapshot_and_excludes_later_or_unmatched_periods` |
| True crossing boundaries, distinct clear/gone, no fake active end | `Detail_marks_window_overlap_preserves_clear_and_gone_reasons_and_deduplicates_unchanged_evidence` |
| Structured open/change/end evidence without per-round duplication | overlap/dedup test; `Default_detail_summarizes_duplicate_missing_invalid_area_and_multi_worktype_diagnostics_without_raw_rows` |
| Demand/Series generation semantics and list/detail count reconciliation | `Detail_separates_demand_generations_and_reconciles_series_generation_evidence_with_list_counts` |
| Authorized allowlisted, redacted, bounded raw expansion; no default raw | `Raw_evidence_requires_explicit_authorization_and_returns_only_whitelisted_redacted_bounded_fields`; default-summary test |
| Stable non-leaking rejection with no mutation | `Raw_evidence_rejections_are_stable_non_leaking_and_leave_the_snapshot_unchanged` |
| Duplicate/missing/invalid AREA/multi WorkType/cross-window/concurrent fixtures | all six `ErrorSearchDetailTests` tracer bullets |
