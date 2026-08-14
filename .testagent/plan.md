# Ticket 19 test plan

Work in vertical red-green slices at the confirmed `ScriptedFakeHost ->
production V2 Watch window` seam.

1. Add a failing production-composition/shell semantic test; introduce the V2
   composition and one `FluentWindow` with integrated title bar,
   `NavigationView`, six primary pages, Host footer, and settings footer.
2. Add a real scripted-Host initial-load test; apply the exact contract, issue
   the explicit overview read, render all four summaries and no-activity state
   from the same `WatchOverviewSnapshot`, then activate overview auto-refresh.
3. Add success -> gated refresh -> failure tests; project refreshing, retained
   full snapshot, committed AREA scope, Host snapshot time, client success /
   failure time, stale reason, and current connection without a health claim.
4. Add Host replacement and settings persistence tests; prove the UI clears
   synchronously for a new Host, no old Host survives failure, credentials are
   never stored, and interval-only changes preserve Host generation.
5. Add local AREA-context and drill-down tests; keep local profile state separate
   from Host `Snapshot.MesAreas`, and route the complete Host-provided
   `OverviewNavigationIntent` with page one and null cursor.
6. Add deterministic auto-refresh notification tests and dispatcher projection;
   prove start/completion/failure are observable, busy ticks do not queue, and
   settings/AREA pages deactivate Host polling.
7. Add adaptive/accessibility semantic tests for 720 epx reflow, text+icon
   states, automation names, tab focus, and absence of forbidden manual refresh,
   cancel, and auto-refresh enabled controls.
8. Re-open every assertion against the ticket matrix, perform pseudo-mutation
   checks, run focused tests/builds, run the full solution exactly once, then run
   independent Standards and Spec reviews. Do not run or promote golden evidence
   in this ticket-local loop.
