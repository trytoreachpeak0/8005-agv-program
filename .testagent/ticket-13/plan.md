# Ticket 13 test plan

1. Add a pure policy test for the tick-before / exact-boundary / tick-after rules and exact 30-day duration.
2. Add one real-SQL integration test that commits duplicate and invalid raw evidence, advances the production retention seam across the boundary, and verifies whole-multiset 200 -> 410 behavior, the 404 distinction, earliest boundary, and unchanged current Series state.
3. Add one real-SQL lifecycle test that drives a minimal Series through VISIBLE -> GONE -> ARCHIVED, verifies first `EligibilityAt` and due time, then reappears with an active condition/event to cancel eligibility and becomes GONE again to establish a new timestamp.
4. Add a schema contract assertion for the explicit raw-expiration marker and Series eligibility timestamp/index.
5. Run only the new class while iterating. Re-open every assertion against the ticket checklist, then run Tier 1 once.
