# Ticket 22 test plan

Work in vertical red-green slices at the specification-confirmed production
seam.

1. Add Error Search query-helper tests for default latest first page, all
   filters/windows/page sizes, frozen previous/next/direct page requests and
   explicit attention drill conditions; implement the minimum query helpers.
2. Add Error Search presenter tests for exact facets/totals/order, normalized
   condition/UTC window facts, successful-empty vs loading/failure retention,
   matched period boundaries, cross-generation evidence and bounded raw states;
   implement the minimum presenter.
3. Add Current Attention presenter/query tests for all four current kinds,
   stable Series identity/drill, structured global evidence, facets/paging and
   explicit non-incident semantics; implement the minimum helpers.
4. Add production ScriptedFakeHost tests for initial loads, filters/windows,
   frozen paging/direct jump, selection/detail, failure retention, raw evidence
   expansion/error isolation and attention-to-error drill-down.
5. Replace both placeholders with production Fluent pages and wire event
   handling through the existing client/session/auto-refresh interfaces. Do not
   add a page-only Host or test bypass.
6. Add tests proving AREA application never changes/refetches either Ticket 22
   query and that Overview explicit intents open both pages on page one.
7. Add semantic WPF tests for the Variant A equal-height three-column layout,
   responsive stack, stable UIA names/ids, keyboard reachability and non-color
   statuses. Pixel and real-window claims remain deferred until the shared run.
8. Re-open every generated assertion against the checklist, then perform
   `test-gap-analysis` with empirically verified pseudo-mutations and close any
   substantive survivors.
9. Run focused presenter/query/session/page suites and a non-incremental Release
   solution build, then the full solution test suite exactly once. Record every
   environment skip and unrelated pre-existing failure.
10. Run the required two-axis `/code-review`, fix findings, and repeat only the
    affected focused gates.
11. Freeze Ticket 22 with an implementation commit, then run the single shared
    tickets 19-22 interactive targeted-suite and real-window preview train.
    Pause for explicit user approval; do not generate candidates, promote
    baselines or create DPI clones because Ticket 23 owns those gates.
12. Record shared evidence/approval/cleanup in tickets 19-22, set Ticket 22's
    final tracker state, and commit the evidence closure.

## Requirement mapping

| Checklist | Planned evidence |
| --- | --- |
| 1, 2, 3, 4 | `WatchErrorSearchPresentationTests`, `WatchErrorSearchQueryTests`, and production integration |
| 5 | Error raw-evidence presenter tests and ScriptedFakeHost production interaction |
| 6, 7 | `WatchCurrentIngestAttentionPresentationTests` plus attention production integration |
| 8 | AREA-isolation request timeline and visible state assertions |
| 9 | Ticket 22 responsive/UIA semantic integration tests |
| 10 | Shared golden preview directory, targeted-suite results, explicit approval, named skips and cleanup logs |
