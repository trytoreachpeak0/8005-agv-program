# Chinese-only Watch UI Tier 2 repair research (2026-08-28)

## User requirement

> "这个地方消失还会写(GONE)的，不要这种中英文同时存在的ui，你帮我看看其他地方有没有这种类似的，一并改掉"

The user accepted the recommended boundary: known codes and static terminology in
normal Simplified Chinese UI render as Chinese only; English mode stays English;
unknown codes and explicitly technical/raw evidence keep their source value.

## Current validation boundary

- The focused catalog/presentation tests passed `70 / 70`.
- Tier 1 passed `939 / 939`, with `137` environment-dependent skips.
- The first authorized Tier 2 production preview ran on `gpt_win11` at
  `1920x1080`, `96 DPI`, light theme, `zh-CN`.
- Tier 2 result: `170` total, `53` failed, `6` skipped, `111` passed. The
  journey/screenshot phase did not run, so no visual approval artifact exists.
- Failure evidence is preserved under
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-bilingual-ui-chinese-only/run-20260828-193813-watch-production-preview`.

## Failure inventory

| Test group | Failures | Initial classification |
| --- | ---: | --- |
| `WatchTicket21AreaAndResponsiveIntegrationTests` | 24 | Mixed: stale `AREA`/command text assertions, selector presentation-shape changes, and real conflict/late-completion behavior checks |
| `WatchV2ProductionHostTests` | 5 | Stale `Host` text plus missing settings feedback landmark investigation |
| `WatchDemandSeriesProductionIntegrationTests` | 4 | Stale `Series`/`AREA` text, missing drill landmark, one timeout |
| `WatchErrorSearchProductionIntegrationTests` | 4 | Stale mixed terminology/count formatting |
| `WatchDemandAuditSelectedPrototypeIntegrationTests` | 3 | Stale technical label plus missing selected-layout landmarks |
| `WatchReadabilityAuditProductionIntegrationTests` | 3 | Stale `Host`/`Demand`/technical label assertions |
| `WatchSelectedPrototypeStructureTests` | 3 | Static text plus selected-prototype geometry mismatch |
| `WatchTicket22ResponsiveIntegrationTests` | 3 | Stale UIA/raw-code assertion plus header hierarchy mismatch |
| Current attention / overview / filter label / rejected layout | 4 | One real disappearing-selection behavior check and three stale/structural assertions |

## Constraints

- The selected real prototype sources, not screenshots alone, remain layout and
  interaction authority.
- Golden baselines must not be changed in this repair.
- Existing unrelated worktree edits are user-owned and must be preserved.
- Formal WPF visual validation runs only through the calibrated Golden VM.
- The code-testing tool catalog has no `find-untested-sources` or mutation tool;
  coverage/mutation completion will therefore use source-to-test inventory and
  targeted regression assertions rather than pretending those tools ran.

---

# Ticket 01 test research (historical)

## Bounded target inventory

- Ticket: `.scratch/mes-ingest-watch-bilingual-variant-a/issues/01-establish-persisted-production-language-switching.md`.
- Production seam: `WatchV2ApplicationComposition.Create(...)` creating a real `WatchWorkspaceWindow`, with a fake `IWatchV2ApiClient`, temporary connection/workspace preference paths, and controlled time where needed.
- Persistence seam: `WatchV2PreferencesStore.Load/Save`; required language state is `WatchV2Preferences.DisplayLanguage`, while JSON stores it under `display.language` so layout-only `WatchV2DisplayPreferences` reconstruction cannot reset the language.
- Supplemental catalog seam: immutable `WatchTextCatalog.For(WatchDisplayLanguage)` section APIs and `WatchTextCatalog.AllEntries` inventory. Ticket 01 owns only the `Common`, `Shell`, and `Settings` sections; later page tickets own their own sections.
- Runtime state seam: the composition-owned `WatchDisplayLanguageState` instance shared with its production window.
- Existing source/test references inspected: `WatchV2Preferences.cs`, `WatchV2ApplicationComposition.cs`, settings XAML/code-behind, `WatchV2PreferencesTests`, `WatchV2ProductionShellTests`, and neighboring demand-series window lifecycle tests.
- Explicitly out of scope: FluentPrototype dependencies or copied prototype localization, page-specific full translation for Tickets 02-09, Inspector synchronization owned by Ticket 05, notification lifecycle localization owned by Ticket 09, golden renderer execution, and production-code edits by this test-generator pass.

## Existing conventions

- xUnit 2.4.2 with VSTest (`Microsoft.NET.Test.Sdk` plus `xunit.runner.visualstudio`) targeting `net8.0-windows`.
- WPF tests use `[Collection("WpfDesktop")]` and `StaTestRunner.Run`.
- Tests exercise named production controls through `FindName`, raise routed click/selection events, and assert `AutomationProperties` plus visible control content.
- Filesystem tests create GUID-named directories below `Path.GetTempPath()` and remove only their exact directory in `finally`.
- Preference tests assert both typed round trips and exact JSON contract boundaries without reaching private serializer types.
- Shell tests build through the real composition and inject fake Host clients; request counters are asserted at the fake boundary.

## Pre-agreed seams

1. Real production composition -> real `WatchWorkspaceWindow`.
2. Fake Host client at `IWatchV2ApiClient`.
3. Temporary per-user preference path.
4. Controlled time where formatting or refresh could matter.
5. Supplemental public strongly typed catalog contract.

## Acceptance checklist

- [ ] "未保存语言偏好时以简体中文启动，语言选项始终以 `简体中文` 和 `English` 自称显示。"
- [ ] "保存 English 后当前生产窗口立即更新，重启后仍恢复 English；保存失败时运行时语言不产生模糊的半提交状态。"
- [ ] "旧偏好缺少语言字段时迁移为简体中文并保留刷新、窗口和 Inspector 布局；未知或损坏语言安全回退且应用仍可启动。"
- [ ] "应用组合根拥有唯一共享语言状态，新窗口继承当前值，现有窗口可观察同一状态；切换不读取 Windows 显示语言，也不修改 Host 或业务配置。"
- [ ] "集中、强类型目录同时覆盖固定文本、参数化文本、已知码、未知码回退、六种值/查询语义、绝对/相对时间及语言相关数量格式，调用方不能用任意字符串键或页面私有字典取文案。"
- [ ] "切换语言不增加 Host 请求，不改变当前页面、规范筛选代码、选择或焦点，也不通过重建业务 ViewState 完成翻译。"
- [ ] "建立清晰的页面实现所有权边界，使 Error Search 与接入告警等后续并行迁移不需要同时编辑同一页面专属实现单元。"
- [ ] "生产实现不引用 FluentPrototype，不携带 Tag 字典、视觉树遍历、假数据、评审条或原型语言按钮。"

## Constraints and likely RED causes

- The current preference schema is version 2 and has no top-level domain display-language property or persisted `display.language` field.
- The production settings page has no language selector and visible shell/settings text is hard-coded Chinese.
- The composition/window currently has no shared display-language state.
- No production `WatchTextCatalog`, structured display-value semantics, or language-aware time/count formatter exists.
- The intended first run is RED. Production implementation belongs to the parent implementation channel.

# Watch overview structured activity explanations (2026-08-30)

## Acceptance checklist

- [ ] "structured same-snapshot explanations"
- [ ] "all emitted EventType human mappings"
- [ ] "concrete INVALID_MES_FIELD_FORMAT AREA D7-04 expected D7-4"
- [ ] "end-reason wording"
- [ ] "semantic severities/navigation"
- [ ] "Chinese WorkType and unknown fallback"
- [ ] "labeled metadata"
- [ ] "color+shape+visible severity text accessibility"

## Production and test inventory

- The frozen snapshot contract is `MesIngest.Core/SeriesProjection/WatchOverviewContract.cs`; the activity explanation is an optional final record parameter so existing callers remain source-compatible.
- SQL activity materialization is in `MesIngest.Infrastructure/SqlServer/SqlServerMesIngestProjection.Overview.cs`; Host JSON projection is in `MesIngest.Host/NewMesIngestEndpoints.cs`; Watch presentation is in `MesIngest.Watch/WatchOverviewPresentation.cs`; recent-activity WPF rows are rendered in `MesIngest.Watch/WatchWorkspaceWindow.xaml.cs`.
- Existing target suites are `WatchOverviewPresentationTests`, `WatchOverviewSnapshotTests`, and `WatchV2ProductionShellTests` under `MesIngest.Tests`.
- The repository uses xUnit 2.4.2 on VSTest, targets `net8.0-windows`, and keeps WPF assertions on the `WpfDesktop` collection with `StaTestRunner.Run`.
- The code-testing source-discovery tool was searched for but is not available in this environment; source and test inventories were completed with `rg` and direct file inspection.

## Emitted overview EventType inventory

The Overview SQL emits fifteen operator-visible event types: `DEMAND_SERIES_STARTED`, `DEMAND_GONE`, `GONE_TIMEOUT_ARCHIVED`, `SERIES_ERROR_PERIOD_STARTED`, `SERIES_ERROR_PERIOD_ENDED`, `TRANSPORT_DEMAND_CREATED`, `TASK_TYPE_PROTECTION_ENTERED`, `TASK_TYPE_PROTECTION_RECOVERY_PROGRESS`, `TASK_TYPE_PROTECTION_CLEARED`, `TASK_TYPE_ABSENCE_AUTHORITY_RESTORED`, `UNASSIGNED_MES_OBSERVATION_APPEARED`, `UNASSIGNED_MES_OBSERVATION_CONTENT_CHANGED`, `UNASSIGNED_MES_OBSERVATION_CLEARED`, `POLL_RUN_FAILED`, and `POLL_RUN_RECOVERED`.

## Test seams

1. Pure presenter tests construct frozen activity snapshots and assert conclusion, explanation, labeled metadata, severity text, semantic severity, and navigation without a WPF dependency.
2. A SQL-backed API integration test creates the concrete invalid AREA observation and proves that the returned activity explanation is carried by the same projection commit as its enclosing snapshot.
3. A WPF shell test injects four severity variants through `IWatchV2ApiClient`, then inspects the rendered production rows for distinct symbols, visible severity labels, colors, and accessible names.
