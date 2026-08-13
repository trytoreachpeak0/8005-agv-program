# Tickets 13–14 TDD and implementation plan

## Vertical tracer bullets

1. Current attention union: active Series errors, latest unrecovered poll failure,
   TaskTypeProtection, and unassigned observations; exact total/facets/bounded stable order.
2. Current lifecycle: stable Series identity, evidence refresh without duplicate items,
   successful clear with permanent Error Search history retained, failure/incomplete no fake clear.
3. Atomic overview: one commit identity/time produces exact Series, Readability, Error,
   global attention summaries and structured first-page drill intents.
4. AREA isolation: changing areas changes only Series/Readability; global summaries and
   CatalogRevision stay fixed; local profile state is absent from the DTO.
5. Real dynamics: allowlisted state transitions only, half-open 24-hour window, latest
   five and stable tie order; empty state says `近期无重点动态` and exposes no health claim.
6. Deterministic concurrency: pause after fence A, commit B without reader blocking,
   release and prove response A is coherent; refresh proves coherent B.
7. Release gate: tracer/schema 14, focused real-SQL gate, solution build, full suite,
   independent Standards/Spec review.

## Requirement-to-test evidence

| Requirement | Planned public-seam evidence |
| --- | --- |
| Ticket 13 union, stable source identity/evidence | `Current_attention_unifies_all_sources_with_stable_identity_exact_facets_and_order` |
| Success-only recovery and permanent history | `Current_attention_clears_only_on_success_and_preserves_error_history` |
| Replay/conflict/non-success atomicity and bounded read | both Current Attention tests plus existing round-idempotency tests |
| One identifiable atomic commit snapshot | `Overview_returns_exact_same_commit_summaries_and_explicit_drill_intents` |
| AREA only scopes Series/Readability | `Overview_area_changes_only_series_and_readability` |
| Global active/recent errors and attention facets | exact-summary test and AREA isolation test |
| Only real latest-five 24h transitions; empty is not health | `Overview_returns_only_latest_five_real_transitions_and_neutral_empty_state` |
| Concurrent commit cannot tear cards | `Overview_is_wholly_old_then_wholly_new_when_commit_occurs_during_read` |
| Formal Host read and read-only behavior | all tests use HTTP; before/after projection receipts and frozen reads are compared |
