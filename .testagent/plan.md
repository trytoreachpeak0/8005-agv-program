# Chinese-only Watch UI Tier 2 repair plan (2026-08-28)

## Phase 1 — classify against the selected prototypes

1. Read the selected prototype source and selection records for Overview,
   bilingual semantics, and the affected wide/responsive page geometries.
2. Map each failing landmark, row/column, control hierarchy, and command to the
   corresponding production element.
3. Mark every failure as stale localization expectation, production behavior
   defect, or prototype-parity defect before editing.

## Phase 2 — repair production behavior and layout

1. Keep known business codes out of normal Simplified Chinese presentation.
2. Preserve canonical codes in tags, requests, raw evidence, logs, JSON, and
   unknown-code fallback paths.
3. Restore any selected-prototype landmark/hierarchy lost by localization.
4. Fix selection disappearance and profile conflict/concurrency behavior only
   where the failing test still represents the selected interaction contract.

## Phase 3 — repair regression tests

1. Replace stale mixed Chinese/English display expectations with catalog-backed
   or exact pure-Chinese expectations.
2. Keep raw/canonical assertions at the API and explicit evidence boundaries.
3. Update hierarchy assertions only after prototype-to-production mapping proves
   the production structure is authoritative.

## Phase 4 — validation

1. Build locally and run the narrowest relevant non-visual tests.
2. Run Tier 1 once if production inputs changed after the earlier pass.
3. Re-run the authorized `watch-production-preview` suite on the Golden VM.
4. Inspect same-state screenshots side by side; do not promote baselines.

## Requirement mapping

| User requirement | Planned evidence |
| --- | --- |
| "不要这种中英文同时存在的ui" | Catalog/presentation assertions plus production screenshot audit in Simplified Chinese |
| "其他地方有没有这种类似的，一并改掉" | Full normal-UI source inventory, affected UI integration regressions, and Tier 2 production preview |
| Recommended boundary accepted | English-mode and unknown/raw-code fallback tests remain intact |

---

# Ticket 01 RED test plan (historical)

## Phase 1 — preference schema and migration

File: `mes/ingest/csharp/MesIngest.Tests/WatchBilingualPreferencesTests.cs`

1. `Missing_preferences_default_to_simplified_chinese_without_consulting_process_culture`
   - Vary current UI culture and load a missing explicit preference path.
   - Assert `SimplifiedChinese` in both cases.
2. `English_round_trips_with_refresh_main_and_inspector_layout_preferences`
   - Save top-level `WatchV2Preferences.DisplayLanguage = English` with non-default intervals, navigation preference, main layout, and Inspector layout; assert JSON persists the choice under `display.language`.
   - Assert the whole record round-trips and JSON remains local-display-only.
3. `Version_2_without_language_migrates_to_chinese_and_preserves_refresh_main_and_inspector_layout`
   - Load a valid version-2 document containing non-default refresh and both layouts.
   - Assert language defaults to Chinese and every legacy preference survives.
4. `Unknown_or_malformed_language_falls_back_to_chinese_without_discarding_other_valid_preferences`
   - Load current-schema documents with unknown string and malformed language token.
   - Assert startup succeeds, language is Chinese, and valid refresh/layout values survive.

## Phase 2 — real production window behavior

File: `mes/ingest/csharp/MesIngest.Tests/WatchBilingualFoundationProductionTests.cs`

1. `Fresh_production_window_starts_in_chinese_and_language_choices_are_self_named`
   - Create the real window from a missing temporary preference path.
   - Navigate to Settings and assert current Chinese shell text and exactly `简体中文`, `English` choices.
2. `Saving_english_reprojects_the_open_window_and_a_restarted_composition_restores_english`
   - Select English and invoke the real save command.
   - Assert immediately changed visible/UIA shell/settings text, then create a fresh composition over the same file and assert English restores.
3. `Failed_language_save_keeps_the_committed_runtime_language_and_visible_projection`
   - Use a preference target that deterministically rejects atomic replacement.
   - Attempt English save and assert runtime state plus visible shell remain Chinese.
4. `Unknown_saved_language_starts_the_real_window_without_losing_other_preferences`
   - Start the real production composition from an otherwise valid current document with an unknown language.
   - Assert the window opens in Chinese while its non-default refresh and navigation preferences survive.
5. `Composition_and_window_share_one_observable_language_state`
   - Assert the composition and created production window expose the same state instance, observers receive one committed change, and a subsequent catalog/window consumer sees the current value.
6. `Switching_language_preserves_active_page_canonical_filter_selection_focus_and_host_requests`
   - Initialize with a recording fake Host and controlled stable data, navigate to Demand Series, submit a canonical filter, select a row, and focus a stable control.
   - Save English through Settings, return/observe existing state, and assert request counts, `ActivePage`, canonical query/filter, selected identity, focus, and the same workspace ViewState object/value remain unchanged where the current seam exposes them.

## Phase 3 — strongly typed catalog contract

File: `mes/ingest/csharp/MesIngest.Tests/WatchTextCatalogContractTests.cs`

1. `Common_shell_and_settings_sections_expose_typed_bilingual_text_without_arbitrary_string_lookup`
   - Compile-time use of typed `Common`, `Shell`, and `Settings` properties from immutable language catalogs.
   - Reflection asserts no public `Get(string)`/indexer escape hatch.
2. `All_catalog_entries_are_nonempty_bilingual_and_have_matching_format_parameters`
   - Enumerate `WatchTextCatalog.AllEntries`; assert unique semantic IDs, both languages nonempty, no key-as-fallback, and identical placeholder sets.
3. `Unknown_code_description_is_localized_and_preserves_the_raw_code`
   - Assert Chinese/English neutral descriptions differ while an unfamiliar raw code is unchanged and not assigned known-code narrative.
4. `Structured_value_semantics_keep_all_six_missing_query_states_distinct_in_both_languages`
   - Assert SourceNotProvided, SystemUnknown, NotApplicable, NotLoaded, EmptyResult, and ReadFailed render as six distinct nonempty values in each language; a present raw value remains verbatim.
5. `Absolute_time_keeps_offset_while_relative_time_and_count_follow_display_language`
   - Use a fixed timestamp/clock and count.
   - Assert absolute `yyyy-MM-dd HH:mm:ss zzz` is invariant, relative prose differs, count culture/unit differs, and stable identifiers remain outside culture formatting.

## Requirement mapping

| Ticket 01 requirement | Planned evidence |
| --- | --- |
| Chinese default and self-named choices | Phase 1.1; Phase 2.1 |
| English immediate save/restart and no half-commit | Phase 1.2; Phase 2.2-2.3 |
| Legacy migration and damaged/unknown fallback preserving other preferences | Phase 1.3-1.4 |
| Shared composition language state | Phase 2.4 |
| Strongly typed catalog, unknown/raw, six semantics, time/count | Phase 3.1-3.5 |
| No Host request/page/filter/selection/focus/ViewState reset | Phase 2.5 |
| Parallel page ownership | Section-scoped catalog compile-time contract in Phase 3.1 and aggregate inventory in Phase 3.2 |
| No prototype production dependency | Project-reference/source-boundary assertion in Phase 3.1 or explicit source audit if a runtime test is not valuable |

## Validation

- Detect SDK/platform from `dotnet --version`, `global.json`, test csproj, `Directory.Build.props`, and `Directory.Packages.props`.
- Run a single VSTest filter covering only the three new Ticket 01 classes.
- Expected state for this generator handoff: RED because the production language/catalog contracts do not yet exist. Do not weaken, skip, or convert the tests to reflection-only placeholders merely to compile green.

# Watch overview structured activity explanations (2026-08-30)

## Planned tests

File: `mes/ingest/csharp/MesIngest.Tests/WatchOverviewPresentationTests.cs`

1. `Known_overview_event_types_project_human_conclusions_semantic_severity_and_navigation`
   - Table-drive every EventType emitted by the Overview SQL and pin its Chinese conclusion, semantic severity, visible severity text, and target page.
2. `Ended_error_periods_distinguish_recovery_demand_disappearance_and_series_archive`
   - Pin wording for `CONDITION_CLEARED`, `DEMAND_GONE`, and `SERIES_ARCHIVED`.
3. `Invalid_area_format_explains_observed_and_expected_values_from_the_frozen_snapshot`
   - Assert `INVALID_MES_FIELD_FORMAT`, `AREA`, observed `D7-04`, expected `D7-4`, and labeled metadata.
4. `Chinese_activity_metadata_localizes_known_work_type_and_escalates_unknown_codes`
   - Keep known WorkType raw codes out of normal visible Chinese while preserving an unfamiliar code in a Chinese escalation fallback.
5. `Poll_failure_uses_safe_detail_without_reclassifying_it_as_an_observed_value`
   - Assert poll diagnostics use `SafeDetail`, not `ObservedValue`.
6. `Structured_conflict_explanations_use_counts_and_localized_related_work_types`
   - Assert `ObservationCount` and `RelatedWorkTypes` produce bounded Chinese explanations without leaking known raw WorkType codes.

File: `mes/ingest/csharp/MesIngest.Tests/WatchOverviewSnapshotTests.cs`

7. `Invalid_area_activity_carries_a_same_snapshot_structured_explanation`
   - Through the real SQL-backed `/api/v2/watch-overview` seam, insert Area `D7-04`, locate `SERIES_ERROR_PERIOD_STARTED`, compare its projection commit to the enclosing snapshot, and assert the complete structured explanation.

File: `mes/ingest/csharp/MesIngest.Tests/WatchV2ProductionShellTests.cs`

8. `Recent_activity_rows_expose_distinct_shape_color_and_visible_severity_text`
   - Render Error, Warning, Success, and Informational rows; assert red/amber/green/blue color distinction, four semantic symbols, visible Chinese severity text, and severity-bearing accessible names.

File: `mes/ingest/csharp/MesIngest.Tests/WatchV2ApiClientTests.cs`

9. Strengthen `Overview_normalizes_area_scope_and_decodes_one_atomic_v2_snapshot`
   - Round-trip all eight optional explanation fields across the real Watch HTTP JSON decoder.

## Requirement mapping

| Requirement | Planned evidence |
| --- | --- |
| Structured same-snapshot explanations | Tests 3, 6, 7, and 9 |
| All emitted EventType human mappings | Test 1, fifteen theory rows |
| Concrete invalid AREA format | Tests 3 and 7 |
| End-reason wording | Test 2 |
| Semantic severities/navigation | Test 1 |
| Chinese WorkType and unknown fallback | Test 4 |
| Labeled metadata | Tests 3 and 4 |
| Color, shape, visible text accessibility | Test 8 |

## Validation

- Run one VSTest filter covering the three touched classes only.
- Preserve RED evidence if production implementation is incomplete; never weaken or skip a requirement to obtain green.
- Invoke `test-gap-analysis` after the first generated-test run and add only verified missing cases.
