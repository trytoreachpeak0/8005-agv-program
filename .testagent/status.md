# Chinese-only Watch UI Tier 2 repair status (2026-08-29)

- [x] User authorized Tier 2 and confirmed the expanded 53-failure repair.
- [x] Preserved the failed Golden evidence; no baseline was touched.
- [x] Recorded the 53 failures by test group.
- [x] Completed selected-prototype mapping for structural failures.
- [x] Repaired production behavior/layout defects.
- [x] Updated stale localization/UIA assertions, including localized Inspector automation names.
- [x] Tier 1 final gate: `939 passed / 0 failed / 137 skipped` in 6 minutes 50 seconds. The named skips require the real SQL Server environment variables documented by the repository.
- [x] Tier 2 final production preview passed: `ticket-bilingual-ui-chinese-only-final/run-20260829-011332-watch-production-preview`.
- [x] Inspected the final overview, readability, and Inspector screenshots; normal Chinese UI no longer contains `GONE`, `VISIBLE`, `PASS`, `FAIL`, or `SERIES_LIFECYCLE`.
- [x] User visually approved the final calibrated screenshots on 2026-08-29 and confirmed the change is publishable. No baseline was touched.

---

# Ticket 01 test-generator status (historical)

## Implementation green update

- The parent implementation completed the production language foundation and
  corrected two test-fixture setup defects exposed by the first green run.
- Focused Ticket 01 plus existing preferences/shell regression run:
  `48 passed / 0 failed / 0 skipped`.
- Tier 1 handoff gate:
  `852 passed / 0 failed / 136 skipped` in 8 minutes 16 seconds. The runner
  named every skip; the skipped integration groups require the real SQL Server
  environment that is not configured for this run.
- `MesIngest.Watch.UiTests` restored and compiled successfully with
  `0 warnings / 0 errors`; no Golden/tier 2 suite was executed.

## Initial RED result

- Research and plan are recorded in `.testagent/research.md` and `.testagent/plan.md`.
- Added 15 focused Ticket 01 tests across three new xUnit classes.
- No production code, prototype source, baseline, or unrelated dirty file was edited.
- SDK/platform detection: .NET SDK `8.0.424` selected by root `global.json` (`8.0.423`, latest patch); xUnit 2.4.2 on VSTest via `Microsoft.NET.Test.Sdk` 17.6.0.
- Narrow command:
  `dotnet test MesIngest.Tests --filter "FullyQualifiedName~WatchBilingualPreferencesTests|FullyQualifiedName~WatchBilingualFoundationProductionTests|FullyQualifiedName~WatchTextCatalogContractTests" -v minimal`
- Expected RED result: exit code 1 at compile time. First missing production contract is `CS0246: WatchDisplayLanguage could not be found` in `WatchBilingualFoundationProductionTests.cs:236`.

## Generated test inventory

### `WatchBilingualPreferencesTests`

1. `Missing_preferences_default_to_simplified_chinese_without_consulting_process_culture`
2. `English_round_trips_with_refresh_main_and_inspector_layout_preferences`
3. `Version_2_without_language_migrates_to_chinese_and_preserves_refresh_main_and_inspector_layout`
4. `Unknown_or_malformed_language_falls_back_to_chinese_without_discarding_other_valid_preferences`

### `WatchBilingualFoundationProductionTests`

1. `Fresh_production_window_starts_in_chinese_and_language_choices_are_self_named`
2. `Saving_english_reprojects_the_open_window_and_a_restarted_composition_restores_english`
3. `Failed_language_save_keeps_the_committed_runtime_language_and_visible_projection`
4. `Unknown_saved_language_starts_the_real_window_without_losing_other_preferences`
5. `Composition_and_window_share_one_observable_language_state`
6. `Switching_language_preserves_active_page_canonical_filter_selection_focus_and_host_requests`

### `WatchTextCatalogContractTests`

1. `Common_shell_and_settings_sections_expose_typed_bilingual_text_without_arbitrary_string_lookup`
2. `All_catalog_entries_are_nonempty_bilingual_and_have_matching_format_parameters`
3. `Unknown_code_description_is_localized_and_preserves_the_raw_code`
4. `Structured_value_semantics_keep_all_six_missing_query_states_distinct_in_both_languages`
5. `Absolute_time_keeps_offset_while_relative_time_and_count_follow_display_language`

## Static pseudo-mutation review

The production language feature does not yet compile, so empirical mutation injection and a green baseline are impossible at this RED handoff. Findings below are static/unverified and were used only to strengthen the tests, not reported as proven production gaps.

| Hypothetical defect | Test sensitivity |
| --- | --- |
| Default from `CurrentUICulture` instead of fixed Chinese | Killed by the two non-Chinese culture rows in the missing-preferences theory. |
| Persist language outside local `display` or omit it | Killed by the exact `display.language = en-US` JSON assertion and Host/credential exclusions. |
| Migrate v2 by falling back the whole document | Killed by exact non-default refresh, navigation, main-window, and Inspector layout assertions. |
| Treat an invalid v3 language as whole-document corruption | Killed by three malformed-language rows retaining every other valid preference. |
| Commit runtime English before persistence succeeds | Killed by the directory-target save-failure test observing state and visible shell text. |
| Recreate independent language state for the window | Killed by reference identity plus one-change notification assertions. |
| Translate by refreshing/rebuilding session state | Killed by fake request count, workspace-state reference identity, canonical filter, selected identity, focus, and active-page assertions. |
| Return Chinese Shell/Settings text for English | Killed by typed section literals and real-window UIA/content assertions. |
| Omit a section from `AllEntries` while its own entries exist | Originally survived the initial plan; fixed by asserting all 11 section boundaries implement `IWatchTextCatalogSection` and `AllEntries` equals the union of their inventories. |
| Collapse multiple missing/query semantics to one dash | Killed by six distinct/nonempty/no-dash assertions in both languages. |
| Localize or strip absolute offset, or leave relative/count units fixed | Killed by exact absolute output plus language-different relative and count assertions. |

## Remaining boundaries owned by later tickets

- Page-specific catalog entry completeness and visible migration beyond Common/Shell/Settings.
- Existing Inspector synchronization (Ticket 05), feedback lifecycle (Ticket 09), and copy/UIA closeout (Ticket 10).
- Golden desktop preview and DPI validation are not authorized in this test-generator pass.
- A source audit for copied prototype-only patterns remains a review/build gate; the runtime assembly-reference assertion only prevents a direct FluentPrototype dependency.
