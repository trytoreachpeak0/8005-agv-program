# Ticket 20 test plan

Work in vertical red-green slices at the confirmed `ScriptedFakeHost V2 ->
production Watch window` seam. Each slice adds one behavior test, the minimum
production behavior, then a narrow passing run.

1. Project Host totals, stable order, AREA context, paging state, and all four
   lifecycle/presence outcomes without hiding unreadable Series.
2. Project full selected-Series evidence: generations, predecessor chain,
   lifecycle nodes, live fields, duplicate raw observations, current errors,
   error periods, immutable events, PollTrace, and ProjectionCommit.
3. Add latest-current-page refresh: acquire latest page one, direct-jump inside
   that snapshot, and atomically commit only the target page.
4. Replace the production placeholder with a responsive master-detail page and
   wire immediate initial load, filters, clear, previous/next/direct page, row
   selection, focused generation, evidence sections, and copy actions.
5. Add source navigation context and snapshot comparison. Search within current
   AREA first; show an explicit all-AREA confirmation before changing scope.
6. Prove loading/failure retention, expired-snapshot errors, stable reselection,
   and detail clearing through scripted Host sequences.
7. Add WPF semantic tests for named controls, automation names, keyboard focus,
   720 epx reflow/scrolling, and absolute-time copy payloads.
8. Re-open every assertion against the ticket checklist; run focused page,
   V2 client/session, presentation, shell, time, and clipboard regressions.
9. Run independent Standards, Spec, and correctness reviews, fix every
   actionable finding, then finish with a non-incremental solution build and one
   full solution test run plus only the necessary focused regression rechecks.
10. Do not run/promote golden candidates, packaged V1 journeys, DPI clones, or
    visual baselines locally; record the shared-train deferral in ticket 20.
