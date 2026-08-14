# Ticket 17 TDD plan and requirement evidence

## Red-green vertical slices

1. Freeze the exact contract identity, capability IDs, compatibility policy,
   OpenAPI location, and deployment/legacy gate. Red tests compare the whole
   discovery payload and reject a mismatched Host identity.
2. Publish an independent Production V2 OpenAPI document for the exact 17 GET
   routes. Add one metadata source for operations, query/header parameters,
   success/error schemas, status codes, limits, stable vocabularies, examples,
   and required/nullability.
3. Run one real Round -> Host -> SQL -> HTTP slice and cross-check discovery,
   empty/non-empty reads, catalog ETag/304, query/page/raw-size errors, remote
   authentication, and restricted raw evidence against OpenAPI.
4. Split ErrorSearch cursor binding mismatch from invalid/tampered credentials;
   retain distinct 410 missing-snapshot behavior and prove parity with
   ReadabilityAudit.
5. Commit canonical `pack/openapi/v2.json`; deep-compare live and static
   `info + paths + components + security`, and classify additive, breaking,
   and documentation-only candidate changes.
6. Update package, manifest, smoke, HTTP examples, install/upgrade guidance,
   and legacy V1 labels. Production gates require canonical V2 OpenAPI and
   reject every legacy route/document while Development may explicitly retain
   the isolated legacy surface.
7. Run focused tests after each slice, dependency tests regularly, the strict
   ticket gate, Release build, and full suite once. Independent Standards/Spec
   review is complete, findings are fixed and revalidated, and the ticket is
   ready for the final commit on the current branch.

## Requirement mapping

| Checklist | Planned public-seam evidence |
| --- | --- |
| 1 | `Contract_discovery_returns_exact_version_and_only_the_frozen_v2_capability_set`; `Contract_compatibility_requires_an_exact_version_and_schema_match` |
| 2, 6 | `Published_v2_openapi_contains_the_exact_read_surface_and_no_business_write_operations` |
| 3 | `Published_v2_openapi_freezes_required_nullable_enum_time_snapshot_and_error_semantics` |
| 4 | `Audit_and_error_credentials_distinguish_tampered_mismatched_and_expired`; `Catalog_etag_304_and_invalid_conditions_match_openapi` |
| 5 | `Runtime_round_sql_api_responses_conform_to_the_published_contract`; `V2_authentication_and_restricted_evidence_access_match_openapi` |
| 7 | `Development_legacy_surface_is_omitted_from_v2_discovery_openapi_and_reference_consumer` |
| 8 | `Production_release_rejects_legacy_surface_and_requires_canonical_v2_openapi` plus strict Ticket 17 gate |
| 9 | `Live_v2_openapi_matches_the_canonical_pack_snapshot`; `Compatibility_classifier_distinguishes_additive_breaking_and_documentation_drift` |
