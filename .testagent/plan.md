# Ticket 07 test implementation plan

## Interface decision

Keep the confirmed round entry unchanged: callers submit only `MesTaskUnionRound` through `RoundIngestor.IngestAsync`. Publish focused read-only `/api/v2/task-type-protections` and `/api/v2/task-type-protections/{workType}` resources, with attention-ready current state and immutable events. Extend PollTrace evidence with per-type decisions/event references. Leave the multi-source CurrentIngestAttention and Overview aggregation to tickets 13 and 14.

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `Zero_drop_enters_protection_and_only_unprotected_work_type_marks_gone` | requirements 1, 2, and multi-type core of 7 |
| 2 | `Two_nonzero_rounds_clear_protection_but_following_round_restores_authority_before_absence_can_mark_gone` | requirement 3 and recovery half of 7 |
| 3 | `Failure_incomplete_replay_and_conflict_do_not_change_protection_recovery_or_events` | non-success/idempotency/conflict half of requirement 4 |
| 4 | `Protection_progress_survives_restart_and_both_gates_must_allow_absence_authority` | RestartBarrier intersection half of requirement 4 plus requirement 6 |
| 5 | `Distinct_recognizable_keys_define_healthy_count_without_raw_duplicate_inflation` | inherited count population and requirement 1 robustness |
| 6 | `Protected_gone_series_does_not_archive_while_other_work_type_can_archive` | archive half of requirements 1 and 2 |

## Production changes

- Centralize the pure per-WorkType transition policy and stable event vocabulary in Core.
- Persist one state row per exact WorkType and an immutable WorkType-sequenced event stream grouped by episode.
- On every newly accepted SUCCESS, count distinct recognizable keys per WorkType, load/lock all persisted states, evaluate transitions, and materialize a decision for every persisted or observed type.
- Keep global RestartBarrier evidence unchanged; compute effective type authority from both gates.
- Filter both current-visible GONE candidates and overdue-GONE archive candidates by WorkType decision.
- Return stable, exact WorkType-ordered focused state/detail resources; expose current-attention readiness until effective authority restoration and retain immutable event history afterward.
- Attach type decisions/event references to PollTrace read evidence.
- Wire `ZeroDropEnterThreshold` into the V2 projection and reject invalid values at construction/startup.
- Bump the empty-database schema/contract identity and update exact shape validation.

## Verification

- Run every tracer bullet red before its production slice.
- Run the focused test class against real SQL Server with zero skips.
- Run Ticket 01-07 key regressions.
- Run a non-incremental Release solution build and the complete test suites once at the end.
- Re-open every Ticket 07 assertion and map it to all seven verbatim requirements.
- Run two-axis review from fixed point `112590abce17a245f69de1c5d596ac5191d167c1`, fix findings, and repeat affected gates.
