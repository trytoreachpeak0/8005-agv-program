# Ticket 08 test implementation plan

## Interface decisions

- First `GET /api/v2/demand-series` without a snapshot freezes the latest SUCCESS commit and returns an opaque `snapshotReference` plus explicit commit metadata.
- Subsequent list pages may use the returned cursor; frozen detail uses `?snapshot=...`. A detail request without a snapshot explicitly freezes latest for compatibility, but always returns its selected identity.
- Stable order is `StartedAt DESC, SeriesId ASC`. Page size is 100 by default and 200 maximum.
- Exact facets are computed after filters and before pagination. Lifecycle and presence counts remain separate.
- Signed references survive restart because their key is stored in the exact schema contract.

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `Old_snapshot_detail_stays_at_commit_a_until_a_latest_refresh_reads_commit_b` | requirements 1 and 6, including equal Host time |
| 2 | `Frozen_snapshot_combines_all_lifecycle_presence_states_with_exact_pages_and_provenance` | requirements 2, 4, and 5 |
| 3 | three snapshot/cursor token tests plus `Frozen_pages_are_exact_stable_and_reject_tampered_or_mismatched_credentials` | credential half of requirements 5 and 6 |
| 4 | frozen missing-field and duplicate/multi-WorkType conflict detail tests | requirements 3 and 4 |
| 5 | `Old_snapshot_detail_remains_readable_after_the_production_host_restarts` | restart half of requirement 7 |
| 6 | `Prearchive_reappearance_creates_a_frozen_successor_without_rewriting_the_gone_snapshot` | prearchive generation/evidence half of requirement 7 |

## Production changes

- Add a database-assigned monotonic sequence to `ProjectionCommits` and a persistent credential signing key to `SchemaInfo`; bump exact schema/contract to v8.
- Add immutable Core frozen-read models and credential codec, keeping snapshot identity distinct from each Series' latest affected commit.
- Resolve latest/reference and reconstruct as-of state in one SERIALIZABLE read transaction.
- Rebuild current demand, lifecycle/presence, fields, conditions, error period close state, raw observations, and events using only evidence at or before the selected sequence.
- Query/filter/count/facet/order/page in Host storage; never download a current table to the client.
- Publish list and snapshot-bound detail via the existing versioned endpoint module with stable structured errors.

## Verification

- Run each tracer bullet red before implementing its production slice.
- Run credential unit tests locally and the SQL/API class through the real-SQL zero-skip gate when configured.
- Run key ticket01-07 regressions, non-incremental Release build, and the full test project.
- Invoke test-gap-analysis and map every ticket assertion to concrete test evidence.
- Run two-axis review from fixed point `b2efb21` and repeat affected gates after fixes.
