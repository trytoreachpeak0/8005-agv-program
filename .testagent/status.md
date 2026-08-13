# Ticket 10 test-generation status

## Current state

- Ticket 10 implementation complete against fixed review point `04c7792`.
- Production seam: scripted `MesTaskUnionRound` -> `RoundIngestor` -> real SQL Server -> `/api/v2/readability-audit` list/detail.
- Contract/schema identity advanced to `new-mes-ingest.tracer.10` / `10`.

## Executable evidence

- `Invoke-Ticket10SqlServerGate.ps1 -ExpectedProductMajor 16 -ExpectedCompatibilityLevel 160`: 7 passed, 0 failed, 0 skipped on real SQL Server.
- Ticket 08/09 real-SQL regressions after review refactor: 10/10 and 15/15 passed, both with 0 skipped.
- `dotnet build MesIngest.sln --configuration Release --no-incremental`: succeeded with 0 errors (only NU1900 vulnerability-feed availability warnings).
- Full core suite: 592 passed, 19 skipped, 2 unrelated existing/environment failures (`LatencyTelemetryTests` stale-file retention and `MainWindowUiAutomationTests` caption double-click maximize); focused rerun reproduced both outside ticket10 surfaces.
- Empirical test-gap probes killed 3/3 mutations: blocker priority, maximum page size, and cross-purpose token signing.
- Two-axis review against `04c7792`: Spec passed with no P0/P1/P2 deviations; Standards found no hard violations. Core/SQL blocker-catalog duplication was removed before final validation. Shared list/detail SQL extraction was left as a judgement-call follow-up because changing the validated query shape would add delivery risk; endpoint parsers remain domain-specific so browse and audit retain distinct error contracts.

## Requirement evidence

- Stable seven-code catalog and lead priority: `Blocker_catalog_is_complete_and_lead_priority_never_discards_other_reasons`.
- Filter normalization, page limits, and domain matching: `Audit_query_normalizes_identifiers_sets_and_enforces_page_contract`.
- Snapshot/cursor binding and tamper/cross-purpose rejection: `Audit_tokens_bind_snapshot_filters_area_order_contract_and_reject_tampering_or_reuse`.
- All-generations lifecycle/readability: `Audit_lists_every_demand_generation_with_readability_separate_from_lifecycle`.
- Filter/AREA/facets/order/detail/catalog equivalence: `Audit_filters_facets_area_order_and_detail_share_one_exact_snapshot`.
- Frozen list/detail with unchanged CatalogRevision: `Audit_snapshot_stays_frozen_when_blockers_change_without_catalog_revision`.
- Stable keyset continuation plus explicit credential failures: `Audit_order_and_bounded_pages_are_stable_and_credentials_fail_explicitly`.
