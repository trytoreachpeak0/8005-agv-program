# Ticket 19 test research

## Confirmed production seam

The specification confirms the integration boundary as `ScriptedFakeHost ->
production MesIngest.Watch -> UI Automation / golden machine`. Ticket 19 must
therefore exercise the real V2 HTTP client, strict contract discovery,
`WatchV2WorkspaceSession`, auto-refresh coordinator, presenter/window, and WPF
semantic controls. A page-only fake or legacy `WatchHostSession` is not an
acceptable substitute.

## Frozen upstream authority

- Ticket 14 supplies one atomic `WatchOverviewSnapshot`: Host snapshot identity,
  normalized queried `MesAreas`, four summaries, at most five real 24-hour
  transitions, explicit no-activity state, and structured first-page navigation
  intents.
- Ticket 18 supplies the production V2 client/session. Applying a Host publishes
  an empty new Host generation before I/O; refresh failure retains the entire
  last successful snapshot; late/cancelled work cannot cross Host/query/request
  generations.
- Ticket 18 auto-refresh is interval-only and always on for the five Host data
  views. Allowed intervals are 10/30/60/300 seconds, only the visible data view
  is scheduled, and activation never performs the initial read.

## Existing production gap

- `App` still starts the legacy composition and a large V1 `MainWindow` using
  old poll-health/demand/alert endpoints.
- The legacy shell exposes four ListBox pages, manual refresh/cancel commands,
  and an auto-refresh enabled switch. Those controls contradict ticket 19.
- No production type represents local AREA profile context, and the V2 session /
  coordinator has no UI notification when a background refresh commits.
- Existing visual journeys and baselines encode the legacy shell. They must not
  be promoted independently while tickets 20-22 are still in the shared train.

## Test conventions and constraints

- .NET 8 WPF, nullable enabled. `MesIngest.Tests` uses xUnit v2/VSTest;
  `MesIngest.Watch.UiTests` uses xUnit v3 standalone and supplies the real
  loopback `ScriptedFakeHost`.
- WPF semantic tests run on STA and pump the Dispatcher; deterministic async
  tests use `TaskCompletionSource`, never sleeps.
- Public behavior assertions target automation names, navigation identity,
  visible state text, session generations, snapshots, and persisted JSON.
  Private control trees and prototype constants are not copied as authority.
- Any changed production UI must satisfy `docs/agents/fluent-ui.md` and
  `docs/agents/golden-renderer.md`: one `FluentWindow`, one integrated
  `TitleBar`, one `NavigationView`, dynamic Wpf.Ui theme resources, keyboard /
  UIA semantics, 1440x900 baseline and 720 effective minimum.
- Ticket 19 currently performs non-pixel validation only. Golden-machine
  deployment, baseline decisions, DPI clones, and user approval are deferred
  until tickets 19-22 freeze and share one preview deployment.

## Acceptance risks to mutate explicitly

1. Production accidentally keeps launching the legacy composition.
2. Interval-only edits accidentally call `ApplyAsync` and clear the Host.
3. A failed replacement Host leaks the old Host snapshot.
4. A failed AREA query relabels the retained Host snapshot with the new local
   profile rather than showing the committed `Snapshot.MesAreas` separately.
5. Auto-refresh commits without notifying/marshalling the WPF projection.
6. Overview cards are recomputed from different reads or turn no activity into
   a health claim.
7. Drill-down drops Host-provided filters, cursor-null, or page-one semantics.
8. Settings persist a credential or expose enabled/manual-refresh controls.
