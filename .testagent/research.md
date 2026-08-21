# Ticket 22 test research

> Ticket 22 content below predates the DemandSeries Inspector E work. It is
> retained verbatim. Ticket 06 research is appended in a separate section at
> the end of this file.

## Confirmed production seams

The specification already confirms both relevant public seams:

- `ScriptedFakeHost -> MesIngestV2ApiClient -> WatchV2WorkspaceSession ->
  production WatchWorkspaceWindow -> UI Automation` is the Watch acceptance
  seam. Tests must not add a page-only Host/auth/cancellation/snapshot/paging
  bypass.
- Scripted `MesTaskUnionRound -> production Host/domain -> SQL Server ->
  versioned HTTP API` already covers the ErrorSearch and
  CurrentIngestAttention business contracts in tickets 11-13. Ticket 22
  consumes those contracts; it does not duplicate Host rules in the client.

## Existing authority and bounded target inventory

- Ticket 11 owns frozen `ErrorSearchAsOf`, UTC half-open windows, normalized
  filters, self-excluding facets, DemandSeries de-duplication, fixed order,
  exact totals and frozen cursor paging.
- Ticket 12 owns matched-period/detail semantics and the authorized bounded raw
  evidence endpoint: seven allowed fields, 20 items, 2,048 bytes per item and
  65,536 bytes total.
- Ticket 13 owns `CurrentIngestAttention` kinds, stable Series error identity,
  structured evidence/navigation and bounded stable paging.
- Ticket 18 owns single-Host/query/request/selection generations, late-response
  rejection, failure retention and same-snapshot detail relocation.
- Tickets 19-21 own the production Fluent shell, overview navigation, Demand
  Series, Readability Audit and local AREA profiles. Error Search and Current
  Attention are still production placeholders in `WatchWorkspaceWindow.xaml`.
- The V2 client/session/wire DTOs and ScriptedFakeHost routes already expose all
  Ticket 22 read capabilities. Missing scope is client query/presentation,
  production XAML/event wiring, navigation/drill-down and semantic UI tests.
- The requested `find-untested-sources` helper is not installed in this
  environment. One bounded manual pairing pass found no existing Ticket 22
  presenter/query/page test files; neighbouring Ticket 20/21 pairs define the
  conventions to follow.

## Existing test conventions

- SDK 10.0.302 with no `global.json` MTP runner setting: both test projects use
  VSTest through `Microsoft.NET.Test.Sdk`. Core tests use xUnit v2 and Watch UI
  tests use xUnit v3 through its VSTest adapter.
- Focused commands use `--filter "FullyQualifiedName~..."`.
- Pure presenters/query helpers live in `MesIngest.Watch` and are tested from
  `MesIngest.Tests`; production page behavior is exercised from
  `MesIngest.Watch.UiTests` through a real WPF window and ScriptedFakeHost.
- WPF tests use an STA dispatcher, deterministic gates rather than sleeps,
  `FindName`, stable `AutomationId`/Name assertions and no screen coordinates.
- Formal pixels, real-window UIA, high contrast and 96/120/144 DPI evidence
  belong to the one shared tickets 19-22 golden-machine train after all four
  non-pixel outputs are frozen.

## Acceptance checklist

1. Error Search uses the selected Variant A three-column hierarchy (category,
   de-duplicated Series results, matched evidence detail), equal top/bottom
   bounds at desktop width and an understandable responsive stack.
2. Category, code, ACTIVE/ENDED, 24h/7d/30d/all-history, SeriesId, DemandId,
   SUBLOT and 100/200 page size controls create normalized Host queries; the UI
   visibly reports frozen ErrorSearchAsOf, UTC `[from,to)` and conditions.
3. Host fixed order, exact Series total, facets and frozen server paging remain
   authoritative; detail shows only matching periods/evidence, out-of-window
   boundaries and distinct Demand generations.
4. Only a successful zero-result response renders “no history for these
   conditions”. Loading, cancellation, cursor/query failure and refresh failure
   are distinct; failure retains the previous snapshot, AsOf and committed
   conditions.
5. Default evidence displays field/value/rule, DemandId or WorkType, evidence
   time and PollTrace. Raw observations require an explicit action and display
   the returned allowlist/limits; denial or limit errors do not erase detail.
6. Current Attention renders only current `CurrentIngestAttention` items across
   SeriesError, PollRunFailure, TaskTypeProtection and
   UnassignedMesObservation, with exact totals/facets/stable paging and clear
   non-incident wording.
7. A Series attention item exposes its stable error identity and drills into
   Error Search with explicit ACTIVE/category/code/SeriesId conditions; global
   items retain structured PollTrace/WorkType evidence and do not invent
   acknowledgement or recovery actions.
8. Neither page sends the local `AreaFilterProfile`; historical errors, current
   attention, Host connection failure and Watch refresh failure remain visibly
   distinct.
9. Filters, ranges, paging, selection, detail, attention items, raw expansion
   and drill-down have stable UIA names/ids, keyboard focus and text/icon status
   semantics at supported desktop and minimum-width layouts.
10. Shared-train non-pixel suites run before one interactive golden deployment;
    Ticket 22 produces the final real-window preview, explicit user approval,
    named targeted-suite skips and cleanup evidence. Candidate stability,
    baseline promotion and DPI clones remain exclusively owned by Ticket 23.

## High-risk pseudo-mutations to verify

- Sending the currently applied AREA list to Error Search or Current Attention.
- Replacing a retained failed snapshot's conditions/AsOf with the attempted
  query or rendering failure as a successful empty list.
- Treating an ended Series period as current attention or drilling without an
  explicit ACTIVE state and stable error identity.
- Showing every detail period/evidence rather than only the Host-matched set.
- Eagerly requesting raw evidence, requesting a non-allowlisted field, or
  clearing the bounded explanation when raw access is denied.
- Local facet/page calculations replacing Host exact totals or frozen cursors.

---

# DemandSeries Inspector E — Ticket 06 test research

## Confirmed public seams

The feature spec and ADR 0018 pre-agree the seams required by TDD:

- `WatchDemandSeriesInspectorCoordinator` plus
  `IWatchDemandSeriesInspectorWindow` own single-instance creation, explicit
  show/restore/activation, non-activating updates, close/recreate, geometry
  hand-off, and shutdown cleanup.
- `WatchWorkspaceWindow` is the integration seam for current list selection,
  pending detail cancellation, Host replacement, main-window shutdown, and the
  one display preference controlling both top-level windows.
- `WatchV2PreferencesStore` is the persistence seam. Tests may inspect the
  versioned JSON document and launch real WPF windows from a loaded preference,
  but must not call private layout helpers or depend on visual-tree structure.
- Real `WatchDemandSeriesInspectorWindow` behavior is observable through WPF
  `WindowState`, `RestoreBounds`, `Owner`, `Topmost`, taskbar eligibility,
  standard system close, keyboard input, and normal bounds.

## Bounded target inventory and current behavior

- Production targets:
  `WatchDemandSeriesInspectorCoordinator.cs`,
  `WatchDemandSeriesInspectorWindow.xaml(.cs)`,
  `WatchWorkspaceWindow.xaml(.cs)`, and `WatchV2Preferences.cs`.
- Neighbouring tests:
  `WatchDemandSeriesInspectorCoordinatorTests.cs`,
  `WatchDemandSeriesInspectorShellTests.cs`,
  `RecordingDemandSeriesInspectorWindow.cs`, and
  `WatchV2PreferencesTests.cs`.
- Existing tests already pin single-instance explicit activation,
  non-activating selection updates, close/recreate, unowned/non-topmost/taskbar
  semantics, closed-no-fetch, pending-detail cancellation, and late-response
  rejection. Ticket 06 must extend these instead of duplicating them.
- Current workspace shutdown disposes the coordinator and Host replacement
  closes the Inspector. Current persistence records only main-window width and
  height under `rememberWindowSize`; it does not persist normal position,
  monitor identity, maximized state, or Inspector geometry, and opt-out JSON
  still carries supplied geometry values.
- Current Inspector defaults are 1200x800 with a 720x600 minimum. Its visible
  `Update` path does not explicitly restore a minimized window; `OpenOrShow` is
  the only path allowed to do so.
- The requested `find-untested-sources` helper is not installed or discoverable
  in this environment. A single bounded manual pairing pass above was used;
  discovery was not repeated.

## Test conventions and execution

- The repo is pinned to .NET 8 (`global.json` 8.0.423, effective SDK 8.0.424).
  `MesIngest.Tests` uses xUnit 2.4.2 through VSTest
  (`Microsoft.NET.Test.Sdk` 17.6.0), so focused commands use
  `dotnet test MesIngest.Tests --filter "FullyQualifiedName~..."`.
- WPF behavior tests use `StaTestRunner`, the `WpfDesktop` collection,
  deterministic dispatcher pumping, public window interaction, and no sleeps.
- File persistence tests use isolated temporary directories and always clean
  them. Geometry expectations use the current visible work area and tolerate
  one effective pixel for WPF/native rounding.
- This delegated TDD task is intentionally red-only: it edits tests and
  `.testagent/*`, runs the narrowest related tests, and preserves the first
  failing evidence for the production implementation agent.

## Acceptance checklist

1. Only explicit open/show restores and activates; selection/refresh updates
   content without restore, raise, activation, or focus theft.
2. Main and Inspector minimize independently; Inspector is unowned,
   non-topmost, taskbar/Alt+Tab eligible; system close closes it and Escape does
   not.
3. Closing ends investigation context and cancels pending detail; reopening
   loads the current list selection and resets Inspector-local tab/filter state.
4. Host replacement closes Inspector, rejects/cancels old-Host detail, and does
   not discard a valid saved layout.
5. Main-window shutdown actively closes Inspector, cancels work, and leaves no
   coordinator-owned window.
6. Legacy `rememberWindowSize` version-2 JSON loads; the UI exposes the upgraded
   "remember window layout" meaning through the same preference.
7. Opt-out persists no main/Inspector geometry; opt-in round-trips both normal
   bounds, Inspector monitor identity, and maximized state.
8. Invalid coordinates use the 1200x800 Inspector default subject to 720x600
   minimum and current work-area limits.
9. A missing saved monitor falls back to an available visible work area while
   preserving valid normal size; work-area shrink clamps the complete normal
   rectangle on-screen.
10. Tier 1 remains the implementation closure gate. Per AGENTS.md, this
    test-generation slice does not enter Tier 2/3 or touch golden baselines.

## High-risk pseudo-mutations

- Letting `Update` call `Show`, restore `WindowState`, or `Activate`.
- Activating a minimized Inspector without restoring it on explicit show.
- Closing the main window while the coordinator still holds a visible window.
- Letting an old Host detail complete after Host replacement.
- Persisting minimized bounds instead of `RestoreBounds`, or restoring maximized
  state before applying safe normal bounds.
- Storing coordinates while layout memory is disabled.
- Trusting a stale monitor name or off-screen rectangle without full visible
  work-area containment.
