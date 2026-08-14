# Ticket 21 test plan

Work in vertical red-green slices at the confirmed production seam.

1. Add profile parser/store tests for comments/blanks, canonical MesArea,
   empty/duplicate/over-limit diagnostics, safe names, UTF-8 atomic save, active
   profile persistence, and selected/saved/applied state separation; implement
   the smallest local TXT module.
2. Add Readability query tests for latest first page, frozen previous/next and
   direct-page requests; add latest-current-page session refresh and route audit
   auto-refresh through it.
3. Add presenter tests for generation-vs-lifecycle semantics, Host exact facets,
   lead/all blockers, zero/loading/failure states, same-snapshot details, trusted
   fields/raw conflicts and evidence provenance; implement the presenter.
4. Add production ScriptedFakeHost tests proving immediate first-page load,
   filters, page size, frozen paging/direct jump, selection/detail, refresh
   reselection/clearing, and audit-to-Series navigation.
5. Replace the Audit placeholder with the production master-detail page and wire
   operations, auto-refresh arbitration, UIA, focus and non-color status.
6. Add profile-window tests proving editor selection is not application, invalid
   drafts cannot apply, save/apply state is clear, and AREA application refreshes
   only Overview, DemandSeries and Audit.
7. Replace the AREA placeholder with the Variant A master-detail editor and wire
   local profile storage, active context load, save/apply and All Areas.
8. Add semantic WPF tests for AutomationId/Name, keyboard reachability and 720
   epx reflow/scrolling. Do not create/promote visual candidates in this ticket.
9. Re-open every assertion against the checklist and run the focused Watch,
   client/session, shell and profile regressions.
10. Run `/code-review` Standards and Spec passes, fix all actionable findings,
    then run one non-incremental Release solution build and one full solution
    test pass. Record named environment skips and pre-existing failures exactly.

## Requirement mapping

| Checklist | Planned evidence |
| --- | --- |
| 1, 3, 4 | `WatchReadabilityAuditPresentationTests` and production integration |
| 2, 9 | `WatchReadabilityAuditQueryTests`, session/auto-refresh and integration |
| 5 | `WatchAreaFilterProfileTests` plus window integration |
| 6, 7 | ScriptedFakeHost AREA-application request timeline |
| 8 | Existing navigation-context tests plus production audit drill |
| 10 | `WatchV2ProductionShellTests` and audit/AREA production integration |
