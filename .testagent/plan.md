# Ticket 18 test plan

Work in vertical red-green slices at the confirmed `ScriptedFakeHost ->
production MesIngest.Watch` seam.

1. Add a scripted HTTP scenario and a failing contract/capability test; implement
   the strict V2 client factory, shared query URI canonicalization, wire mapping,
   Bearer/correlation/redaction, and all six Watch capability reads.
2. Add a failing Host replacement test; implement the V2 workspace Host
   generation, synchronous business-state reset, connection gate, and exact
   contract failure state.
3. Add slow/cancel/late/query-change tests one at a time; implement the generic
   per-view request gate and success/failure state with separate pending and
   committed canonical queries.
4. Add retained failure/cursor tests; implement structured server-query errors,
   success/failure timestamps, stale state, and no cursor fallback.
5. Add selection tests for SeriesId and DemandId; implement atomic relocation or
   detail clearing after successful snapshots.
6. Add always-on refresh tests; implement five interval-only view schedules.
7. Re-open every assertion against the ticket matrix, run narrow projects, then
   run the full solution once and record any environment-only exclusions.
