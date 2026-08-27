# Ticket 01 test research

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
