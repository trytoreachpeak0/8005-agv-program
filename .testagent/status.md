# Ticket 16 test completion status

## Pseudo-mutation verification

Targeted xUnit/VSTest mutation checks were applied one at a time to
`HistoryCleanupBatchRunner`, run with the narrowest covering test, and reverted
immediately.

| Mutation | Initial result | Final result |
| --- | --- | --- |
| Series time boundary `< deadline` → `<= deadline` | Survived the original `+16s` fixture | Closed by moving the fixture to the exact `+15s` deadline; the mutation then failed because `series-2` started in the first batch. |
| Raw row loop `< configured limit` → `<= configured limit` | Killed | `Cleanup_batch_stops_at_the_configured_raw_row_budget` observed an illegal third transaction with a zero remaining limit. |
| Sanitized `exception.GetType().Name` → `exception.Message` | Killed | Real-SQL failure/Attention test rejected the secret-bearing message and the wrong persisted failure reason. |

Observed injected mutations: 3; killed by the final tests: 3; surviving gaps: 0.
The substantive static candidates for fixed hourly boundaries, single-flight,
poll priority, failure clearing, cumulative counts, and exact next-check time
also have direct assertions in the focused suite. No production mutation remains
in the worktree.

## Assertion review

- Defaults use independent literals and also compare the published JSON values.
- Budget tests assert transaction inputs, committed counts, status and natural
  continuation, rather than private loop calls.
- SQL tests assert the public status/HTTP contracts and use direct SQL only for
  tombstone/raw-row commit evidence.
- Failure evidence asserts both the stable sanitized reason and absence of the
  injected secret.
- Cancellation evidence asserts the active operation receives cancellation,
  no failure is recorded, and the polling gate is immediately reacquirable.
- No test was skipped or weakened to obtain a green run.

## Review closure

- The post-review focused suite passed 31/31 with SQL Server 16 and database
  compatibility level 160; failed 0, skipped 0.
- Added direct evidence for the hard 25,000-row PollTrace ceiling, exact
  overrun scheduling, safe scheduler logging, poll-held yielding, graceful
  interruption, and post-failure polling continuation.
- The real-SQL default probe committed 25 whole-Series cleanup transactions
  inside the frozen 15-second elapsed budget.
- Final standards/code-quality and Ticket 16 specification reviews both
  reported no findings after the retry failure identity and restart-schema
  validation fixes.

## Final gate

`dotnet test MesIngest.Tests` passed against SQL Server ProductMajor 16 at
compatibility level 160: 819 passed, 0 failed, 0 skipped in 10m 53s. The first
attempt found one stale four-kind Watch presentation assertion; after updating
that contract test to all five kinds, the closing run was green.
## Ticket 02 addendum (toast Variant A)

- Focused tests cover the Ticket 01 toast spine, continuing overview failure cycles, DemandSeries selection loss, navigation scope, all-AREA confirmation, and AREA write-conflict resolution/later behavior.
- `First_fault_repeats_recovery_and_reoccurrence_form_distinct_notification_cycles` killed an injected mutation that removed same-cycle suppression; the mutation was reverted and the lifecycle class returned green (3/3).
- A missing global-vs-page navigation assertion was added to `Overlay_preserves_page_measure_focus_scope_and_independent_dismissal`: leaving Settings clears its page toast while an active global Host fault remains without replay.
- No Ticket 03 Golden, DPI, animation, baseline, or visual-approval work was run.
- Final Ticket 02 tier 1 (`dotnet test MesIngest.Tests`) passed: failed 0, passed 800, skipped 133, total 933; all three Ticket01 SQL Server environment variables were unset, so the named SQL-dependent tests were skipped.
