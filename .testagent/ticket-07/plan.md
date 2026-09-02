# Ticket 07 TDD plan

Work one vertical slice at a time.

1. **Catalog epoch identity (red -> green)**
   - Add a real Host/SQL test proving a validator from database A cannot return 304 from database B when both revisions match.
   - Assert the Catalog body and ETag carry the new `HistoryEpoch`.
   - Update reference consumer HTTP tests so conditional reads send and validate the epoch-bound identity.

2. **Shared current snapshot identity and commit fence (red -> green)**
   - Extend production operational identities with `HistoryEpoch` and assert Current Attention and Overview expose it with their `ProjectionCommit`.
   - Acquire the commit-round read fence before selecting Attention/Overview identity.
   - Keep existing concurrent old-or-new public HTTP tests green.

3. **Current-only Attention and Overview reads (red -> green)**
   - Read active Series errors from `DemandSeriesCurrentConditions` and its maintained latest evidence pointer.
   - Read TaskTypeProtection from `TaskTypeProtectionStates` and its maintained sequence/commit pointers.
   - Keep unassigned evidence bounded to the selected current commit and PollRunFailure bounded to the latest PollTrace high-water.
   - Build Overview Series facets from `ReadCurrentDemandSeriesPageAsync`; build readability counts from `TransportDemands` + `CatalogItems`; build error counts from current conditions plus the bounded seven-day period window.

4. **Fail-closed query evidence (red -> green)**
   - Generalize the empty-vs-representative baseline comparison to the selected Ticket 07 surface.
   - Add fixture tests for raw-history access/growth, incomplete runtime IO/grant evidence, spills, and abnormal grants.
   - Run the three Ticket 07 surfaces against empty and representative history when the real SQL evidence environment is available.

5. **Validation and review**
   - Scoped tests after each slice.
   - Non-incremental solution build.
   - Tier 1 `dotnet test MesIngest.Tests`; confirm both Failed and Skipped.
   - `/code-review` Standards + Spec, fix findings, rerun affected checks, and commit only Ticket 07 changes.

