# Ticket 04 test research

## Bounded target inventory

- Ticket: `.scratch/demand-series-inspector-e/issues/04-deliver-real-event-investigation.md`
- Design authority inspected: `codex/prototype-demand-series-inspector` at `5ef7e367`, especially `prototypes/DemandSeriesInspectorPrototype/InspectorWindow.xaml` and `.xaml.cs`; the ticket/spec supplies the final exact filter labels.
- Production presentation seam: `MesIngest.Watch/WatchDemandSeriesInspectorPresentation.cs`
  - `Project(DemandSeriesDetailSnapshot, string?)`
  - `EventsForDemand(string?)`
- Production interaction seam: `MesIngest.Watch/WatchDemandSeriesInspectorWindow.xaml` and `.xaml.cs`
  - public update/event surface through `IWatchDemandSeriesInspectorWindow`
  - WPF controls located by stable AutomationId/name and exercised through routed control interaction
- Existing tests to extend:
  - `MesIngest.Tests/WatchDemandSeriesInspectorPresentationTests.cs`
  - `MesIngest.Tests/WatchDemandSeriesInspectorCoordinatorTests.cs`
- Out of scope: production code, prototype code, UI golden baselines, Host/API integration, snapshot-refresh races owned by Ticket 05.
- `find-untested-sources` is not installed or exposed in this environment. Discovery was therefore bounded manually to the two named public seams and their existing paired test files.

## Existing conventions and platform

- .NET SDK: `global.json` pins 8.0.423 with latest patch; detected SDK is 8.0.424.
- Test platform: VSTest (`Microsoft.NET.Test.Sdk` 17.6.0); no `TestingPlatformDotnetTestSupport` signal.
- Framework: xUnit 2.4.2, `[Fact]`, `Assert.*`.
- WPF tests run inside `StaTestRunner.Run` and locate named controls with `FindName`.
- `MesIngest.Tests.csproj` already references `MesIngest.Watch.csproj`; no project change is required.
- Narrow command: `dotnet test MesIngest.Tests --filter "FullyQualifiedName~WatchDemandSeriesInspectorPresentationTests|FullyQualifiedName~WatchDemandSeriesInspectorCoordinatorTests"` from `mes/ingest/csharp`.
- Tier 1 belongs to the implementation owner after green: `dotnet test MesIngest.Tests` from `mes/ingest/csharp`. This test-generator pass intentionally records red-before-green and does not run Tier 2/3.

## Acceptance checklist

| Requirement | Planned evidence |
| --- | --- |
| “事件”作为与“世代分析”平级的一级 Tab，全宽显示冻结快照中的真实 `DemandSeriesEvent` 字段和 payload evidence。 | Public WPF test asserts peer tabs plus event-grid bindings for every production event field. Full-width visual parity remains golden-preview evidence. |
| 事件始终按 `SeriesSequence` 的提交顺序稳定呈现，不因过滤、渲染或刷新重新排序。 | Presentation projection/filter test plus WPF related/all roundtrip identity-and-order assertions. |
| 过滤器提供“全部 Series 事件”和“当前 Demand 相关事件”，并明确当前过滤上下文。 | Public WPF test asserts the two exact labels and context label/DemandId/count in both modes. |
| “相关事件”从选中世代原子切换到事件 Tab 并按该 DemandId 过滤；返回全部事件无需 Host 请求。 | Public WPF related-action and all/related roundtrip test; outward request counter remains zero. |
| 过滤只操作同一不可变事件集合，不修改、重新获取、复制或合成领域事实。 | Presentation and WPF tests assert reference identity of projected event rows before/after filters and unchanged original collection/order. |
| 切换选中世代后，相关事件过滤上下文与新 DemandId 一致；切换 Series 时清除旧 Series 的过滤状态。 | Two public WPF state-transition tests: focused-generation update while related mode is active; cross-Series update resets tab/filter/grid/context. |
| 不显示原型便利事件；生产事件字段、subject、PollTrace、projection commit、payload version 和 payload 均可追溯。 | Presentation test asserts no convenience event and exact EventId/SeriesId/subject/trace/commit/version/payload values; WPF test asserts all corresponding bindings. |
| 公开 presentation/交互测试覆盖全部事件、相关事件、过滤往返、稳定顺序、无额外请求和 Series 切换清理。 | The generated presentation and WPF interaction tests directly cover every listed behavior. |
| 自动化名称和键盘操作覆盖事件 Tab、相关事件动作、过滤器和事件证据网格。 | WPF contract test asserts stable AutomationId/name plus focus/tab-stop semantics for each named control. Native WPF button/radio/tab/grid keyboard behavior is retained. |
| 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。 | Implementation owner evidence after production reaches green; this generator runs only the narrow red command. |
| Read `docs/agents/golden-renderer.md`. | Read during research together with `docs/agents/fluent-ui.md`. |
| Ran the required golden-machine suites through an interactive task. | Non-test implementation/validation evidence; prohibited in this test-only subtask without user authorization. |
| User approved the final real-window preview (visual changes only). | User/implementation-owner evidence, not automatable here. |
| Recorded the unique evidence directory and all named skips. | Golden/Tier 1 validation evidence, not produced by this test-only subtask. |
| Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI. | Golden validation evidence, not produced by this test-only subtask. |

## Current gaps found

- The event projection/filter logic already orders by `SeriesSequence`, retains real payloads, and filters locally, but the existing test does not assert every production field or reference identity.
- The production filters currently display `全部事件` and a dynamic `仅 {DemandId}`, not the exact required labels.
- The event grid currently omits visible bindings for `EventId`, `SeriesId`, and `PayloadVersion`.
- Existing WPF coverage opens related events but does not test all-to-related-to-all roundtrip, generation-focus consistency, Series reset, or the absence of outward requests from every event control.
