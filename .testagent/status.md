# Ticket 16 test status

## Current

- Ticket/spec/ADR research complete; public seams were pre-confirmed by the spec.
- Worktree started clean at `89b6dca`.
- The production commit now exposes six transaction checkpoints; DemandSeries,
  catalog and CurrentIngestAttention expose their selected read fence through a
  production no-op observer.
- The deterministic catalog boundary test reproduced a real SQL deadlock. The
  green fix takes the shared side of the commit-order application lock before
  catalog table locks, so catalog readers are wholly before or after a writer.
- The strict real-SQL gate and five public-seam tests are green. Independent
  Standards/Spec review completed and every finding was fixed and revalidated.
- The Ticket 16 issue is complete and handed off as `ready-for-human`.

## Validation log

- Baseline probe:
  `NewSuccessRoundTracerSpineTests.First_success_round_is_read_back_with_atomic_series_demand_and_round_evidence`
  — 1 passed, 0 failed, 0 skipped.
- Release test-project build: 0 warnings, 0 errors.
- Focused Ticket 16 real-SQL tests: 5 passed, 0 failed, 0 skipped.
- Formal gate: PASSED on SQL Server `16.0.1190.2`, engine edition 3,
  compatibility 160; six checkpoints, 8 writers, 2 readers, one retry, replay
  and conflict. Reports were generated under ignored
  `.artifacts/ticket16-tests/`.
- Dependency real-SQL regression (idempotency, conflict/multi-WorkType,
  restart/GONE, archive/LGBV, protection, catalog, attention, overview and
  frozen DemandSeries): 57 passed, 0 failed, 0 skipped.
- Final Release solution build: 0 warnings, 0 errors.
- Final strict gate after review fixes: 5 passed, 0 failed, 0 skipped on SQL
  Server `16.0.1190.2`, engine edition 3, compatibility 160; six checkpoints,
  8 writers, 2 readers, one retry/replay/conflict.
- Full-suite observation: `MesIngest.Watch.UiTests` passed 82 with 27 skipped;
  `MesIngest.Tests` passed 683 with 2 failures and 19 skipped. Both failures are
  outside the Ticket 16 diff: the date-sensitive latency retention case, and a
  mouse-drag UI automation case that passed on focused retry.

## Review closure

- Standards: removed silent AREA normalization, reduced the gate to one
  canonical report schema, and completed the issue-tracker handoff.
- Spec: concurrent writers now directly prove RestartBarrier and protected
  WorkType behavior; restart compares SeriesSequence and commit identities; the
  failpoint fingerprint includes the active error series and open error period.
- All eight ticket checklist items map to the five real-SQL facts or the strict
  gate artifact; no in-memory or LocalDB result is accepted as release evidence.
