# Map 25 SUBLOT_BOX_COUNT contract readiness

Result: `PUBLISHED_IMPLEMENTATION_READY_WITH_DEPLOYMENT_AND_FIELD_GATES_OPEN`

This evidence records a published, read-only MesIngest implementation prerequisite for
Wayfinder Map 25. It is not a formal W2G-IS-00 through W2G-IS-07 G3 PASS, was not
deployed to the live Host, did not call a RIoT mutation, and did not move a vehicle.
The revision carrying this file is the implementation revision.

## Frozen contract

- Contract: `2026.08.new-mes-ingest.v2.3`, schema `29`.
- Capability: `SUBLOT_BOX_COUNT|1.0|GET /api/v2/sublot-box-count`.
- Oracle artifact: `SUBLOT_BOX_COUNT/sha256:4d2784513bfb85506c190cf138d833ad38dc27102dc33df8161c3f41fbaf26ff`.
- Input: exactly one non-blank `sublot`, at most 256 characters, passed as one
  provider bind parameter without SQL concatenation.
- Output: exact `queryId`, original `sublot`, positive integer `maxBoxCount`, and
  `observedAt` UTC identity. Missing, malformed, non-positive, fractional,
  overflowing, unavailable, or timed-out results fail closed.
- The release package carries exactly the two approved, hash-pinned, read-only SQL
  artifacts: `MES_TASK_UNION` and `SUBLOT_BOX_COUNT`. Publish, smoke, factory
  acceptance, scale/query, and manifest validation use the same allowlist.

## Verification

- Targeted Release tests for the endpoint, bind boundary, contract/OpenAPI,
  package, factory tools, and evidence gates: `150 passed, 0 failed, 1 skipped`.
  The skip is the existing live SQL response conformance test that needs its
  external SQL Server environment.
- Release build: `0 warnings, 0 errors`.
- Changed C# files pass targeted `dotnet format --verify-no-changes`; all changed
  PowerShell scripts pass the PowerShell parser; `git diff --check` passes.
- Final Tier 1 `dotnet test MesIngest.Tests`: `806 passed, 2 failed, 133 skipped`.
  Both failures are unchanged-scope WPF visual/layout tests on the current desktop:
  `WatchAreaProfileAppliedSnapshotTests.The_line_number_gutter_still_carries_ink_after_the_editor_scrolls`
  and
  `WatchV2ProductionShellTests.Production_composition_creates_the_six_page_fluent_v2_shell_without_forbidden_refresh_controls`
  (`expected 900`, `actual 885.33333333333337`). No Watch production code, XAML,
  baseline, or Golden renderer artifact was changed. The 133 skips require the
  external SQL Server test environment.

## Open gates

- The user explicitly authorized publishing the implementation branch together with
  its 60 existing unpublished factory-validation ancestors. The implementation is
  published as
  `codex/map25-sublot-box-count@cbf5717406db39b3182beac4233fa1fdb45b7406`
  and was fetched back from the remote at the same commit. It has not been deployed.
- The live Host remains v2.2 and has not been restarted or replaced.
- Map 25 still has seven unresolved AREA/EQP assignments. Battery threshold,
  approved runtime package-capacity configuration, Onboard credential, and a real
  stopped/parking signal provider remain open.
- RIoT mutation and vehicle movement still require separate authorization.
