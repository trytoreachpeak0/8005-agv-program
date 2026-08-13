# Ticket 04 test implementation plan

## Interface decision

Keep the confirmed public interface unchanged: submit a complete round through `RoundIngestor.IngestAsync`, then observe committed behavior only through `/api/v2/demand-series` and `/api/v2/poll-traces`. Deepen the SQL adapter so one transaction owns grouping, canonical conflict evidence, identity preservation, current conditions, permanent periods, and raw observations.

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `Duplicate_multiset_reorders_without_noise_changes_evidence_in_place_and_recovers_the_same_demand_after_restart` | Requirements 1-4 and duplicate half of 7 |
| 2 | `Exact_duplicate_observations_preserve_multiplicity_and_cannot_clear_a_field_error_without_unique_counterevidence` | Exact multiset multiplicity and Ticket 03 recovery authority regression |
| 3 | `Multiple_work_types_create_independent_series_update_complete_membership_evidence_and_clear_the_still_visible_demand_after_restart` | Requirements 5-7, including observed-key recovery and absent-key safety boundary |
| 4 | `Duplicate_key_and_multiple_work_type_conditions_coexist_with_complete_raw_assignments` | Composition of both Ticket 04 conflict types in one successful round |

## Production changes

- Group assigned rows by the exact existing `TransportDemandKey` comparison before projecting.
- Preserve all source rows with the group's single SeriesId/DemandId; never choose or merge a duplicate row.
- Store no current live-field values for a duplicate group and return `liveMesFields: null` whenever the Demand's latest observation commit contains other than exactly one row.
- Canonicalize duplicate multiset evidence and WorkType membership evidence so ordering is irrelevant and multiplicity/content remain significant.
- Reuse the durable Ticket 03 condition synchronizer for duplicate/membership start, evidence change, and `CONDITION_CLEARED` closure.
- Close membership conditions only for keys observed with explicit counterevidence. A WorkType absent from the round is not a recovery fact until Ticket 05 grants absence authority and transitions its Demand to `GONE`; retaining its blocker avoids exposing a stale `VISIBLE` Demand as readable.

## Verification

- Run each slice red before implementing its production behavior.
- Build the focused test project and run Ticket 01-03 regressions after green.
- Run all four Ticket 04 tests with the real SQL Server gate variables and require zero skips.
- Run a non-incremental solution build and the complete test suite.
- Re-open every assertion and map it to the seven verbatim ticket requirements before completion.
