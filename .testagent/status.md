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
