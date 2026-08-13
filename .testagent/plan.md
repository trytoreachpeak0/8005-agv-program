# Ticket 05 test implementation plan

## Interface decision

Keep the confirmed round entry unchanged: callers submit only `MesTaskUnionRound` through `RoundIngestor.IngestAsync`. Host-session creation and absence authority remain internal. Add read-only V2 evidence for the current HostSession/RestartBarrier and all Demand generations so the real SQL/API seam can prove the lifecycle without private-table assertions.

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `Restarted_host_requires_two_successful_barrier_rounds_before_third_absence_marks_gone` | Requirements 1-3 and restart half of 7 |
| 2 | `Failure_incomplete_replay_and_conflict_never_advance_restart_barrier` | Requirement 3 and transaction/idempotency regression |
| 3 | `Restart_barrier_still_creates_and_updates_visible_demands_without_marking_absent_demands_gone` | Requirement 5 |
| 4 | `First_authoritative_absence_marks_visible_demand_gone_preserves_last_seen_and_closes_conditions_as_demand_gone` | Requirement 4 and Ticket 04 deferred condition closure |
| 5 | `Prearchive_reappearance_creates_persisted_successor_generation_without_rewriting_predecessor` | Requirement 6 and generation half of 7 |
| 6 | `Same_completed_at_uses_latest_accepted_success_instead_of_poll_trace_lexical_order_for_current_raw_multiplicity` | Exact latest-observation evidence and Ticket 03/04 readability regression |

## Production changes

- Generate one opaque HostSessionId per V2 Host/projection instance; initialize it idempotently through a startup hosted service and a commit fallback.
- Persist HostSessions and AbsenceAuthorityEvents. Every Host session begins in `BARRIER` with `RESTART_BARRIER_ENTERED`, including the initial empty-database session.
- On a new SUCCESS only, load/lock the session phase. Decide absence authority from the phase at round start, perform projection and absence sweep, then atomically advance BARRIER -> POST_BARRIER or POST_BARRIER -> NORMAL and append the corresponding bound authority event.
- Sweep current VISIBLE demands missing from the round only when the round began in NORMAL. Set status/presence GONE and GoneConfirmedAt, preserve DemandLastSeenAt, update latest commit, append a lifecycle event, and close current conditions with `DEMAND_GONE`.
- When an observed key's current Demand is GONE and the Series is still tracking, insert generation + 1 with predecessor, point CurrentDemandId to it, retain the old row, and continue ordinary field/error projection on the new generation.
- Return both `currentDemand` and generation-ordered `demands`; publish GoneConfirmedAt and explicit GONE readability.
- Persist the exact last-observation ProjectionCommit per Demand, update it on positive observations, and retain it when GONE changes only lifecycle state.
- Expose current and historical HostSession evidence through read-only `/api/v2/absence-authority` endpoints so events remain queryable after another restart.
- Bump the exact empty-database contract/schema identity and update schema-shape validation.

## Verification

- Run each tracer bullet red before its production slice.
- Run the focused test class against real SQL Server and require 6 passed / 0 skipped.
- Run Ticket 01-05 key regressions after green.
- Run a non-incremental Release solution build and the complete test suite.
- Re-open every Ticket 05 assertion and map it to all seven verbatim requirements.
