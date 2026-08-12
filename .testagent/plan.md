# Ticket 02 test implementation plan

## Interface decision

Deepen the existing projection module from a SUCCESS-only interface to one `RoundIngestor.IngestAsync(MesTaskUnionRound)` interface. The SQL adapter owns canonical preparation, replay lookup, conflict detection, and atomic persistence. Callers learn one operation and one receipt; SQL transaction ordering stays behind the seam.

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `All_outcomes_expose_canonical_utc_round_evidence_without_projecting_unsuccessful_results` | Requirements 1, 4, 5 |
| 2 | `Same_poll_trace_and_canonical_content_replays_the_original_accepted_result_without_duplicates` | Requirements 1, 2; order-insensitive multiset and UTC normalization |
| 3 | `Same_poll_trace_with_different_content_returns_versioned_conflict_without_partial_writes` | Requirement 3; duplicate multiplicity mutation |
| 4 | `Success_preserves_unassigned_rows_while_projecting_every_assignable_key` | Requirements 5, 6 |
| 5 | `Restarted_host_preserves_round_evidence_replay_and_projection_isolation` | Requirement 7 and persistent conclusions across restart |

## Production changes

- Core: unified round receipt/ingestor, nullable ProjectionCommit evidence, typed/versioned PollTrace conflict, UTC-normalized multiset digest.
- SQL adapter: one serializable transaction for all outcomes; lock/read idempotency ledger first; exact replay returns original receipt; mismatch throws conflict; FAILURE/INCOMPLETE insert only PollTrace; SUCCESS persists assigned and unassigned evidence atomically.
- SQL schema: bump isolated new-contract/schema version; preserve exact-manifest validation; allow SUCCESS raw evidence to represent explicitly unassigned rows.
- Host V2 DTO/read mapping: nullable ProjectionCommit and explicit unassigned observation shape; stable contract identity/error details where the production ingress interface exposes a conflict.
- Tests: add `RoundEvidenceIdempotencyTests.cs`, reusing the strictly-owned real SQL database fixture and production Host composition.

## Verification

- Demonstrate red before each production slice, then run the filtered class after green.
- Re-run ticket 01 regression after interface compatibility changes.
- Re-open every assertion and perform focused gap/assertion review.
- Run the formal real-SQL gate with zero skips, full non-incremental Release build, full Release test suite, and solution-level test discovery.
