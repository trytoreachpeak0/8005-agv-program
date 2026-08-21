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
