# Ticket 18 test status

## Current

- Ticket, replacement V2 contract, relevant ADRs, repository agent rules, and
  implement/TDD/test/review skills were read before implementation.
- The confirmed seam is `ScriptedFakeHost -> production HTTP client ->
  WatchV2WorkspaceSession`; no page-only adapter was added.
- Ticket 18 implementation is complete. Independent Standards and Spec reviews
  both pass after follow-up fixes for caller-canceled connection ownership,
  selection concurrency, and production auto-refresh dispatch.
- No XAML, UI Automation, DPI, or visual-baseline file changed, so the golden
  WPF renderer is intentionally outside this non-visual ticket's feedback loop.

## Red-green evidence

- V2 client tests first failed because the production client/session did not
  exist. They now cover exact contract version/schema/capabilities, normalized
  query URIs, Bearer/correlation transport, all list/detail/raw reads, wire-to-
  Core mapping, response contract identity, structured errors, redaction, and
  an invalid empty custom error window: 14/14 pass.
- Scripted Host tests first exposed the in-memory legacy bypass. The fake now
  hosts Kestrel on an ephemeral loopback port and scripts real method/path/query,
  Bearer, JSON, status, delay/cancellation, paging snapshot/cursor, and all ten
  V2 contract/business operations.
- Workspace tests first failed on missing Host/query/request admission and
  retained-state semantics. They now cover Host replacement and failed apply,
  strict connection gating, normalized query/request/Host generations,
  caller cancellation even when a handler ignores its token, retained success
  with success/failure timestamps and staleness, cursor 410 without first-page
  fallback, response contract mismatch, and distinct failure kinds.
- Selection tests cover SeriesId and DemandId relocation/removal, changing A to
  B while refresh is fetching A's detail, and two same-ID detail requests. The
  selection generation and detail cancellation gate prevent every older detail
  from committing.
- Auto-refresh first failed because only a passive schedule existed. The
  production coordinator now dispatches all five normalized view queries into
  the workspace via a controllable one-shot `ITimer`; it is always interval-
  based, single-flight, drops busy ticks, applies interval changes, and cancels
  on disposal. Its deterministic no-sleep suite passes 16/16.

## Focused validation

- `WatchV2ApiClientTests`: 14 passed, 0 failed, 0 skipped.
- `WatchV2AutoRefreshTests`: 16 passed, 0 failed, 0 skipped.
- `WatchV2WorkspaceSessionTests` + `ScriptedFakeHostV2SurfaceTests`: 23 passed,
  0 failed, 0 skipped.
- Production Watch project builds with 0 warnings and 0 errors.

## Pseudo-mutation audit

The following mutations were injected one at a time, observed to fail their new
or strengthened test, and then reverted:

- remove Host generation from snapshot admission;
- remove request generation from same-query admission;
- accept discovered schema/capability drift;
- preserve selection/detail while applying a failed replacement Host.

No mutation marker remains.

## Final solution run

- The required full solution command was started exactly once:
  `dotnet test MesIngest.sln --no-restore --verbosity minimal`.
- Ticket 18's Watch UI project completed with 105 passed, 27 expected visual /
  interactive-environment skips, and 0 failed. The general test project reported
  663 passed, 99 SQL/environment skips, and 3 failures.
- All three failed test areas are byte-for-byte unchanged from `HEAD`. A focused
  rerun made the UI Automation title-bar test pass. The two stable pre-existing
  failures are: `INSTALL.md` at `HEAD` contains the string
  `openapi/v1.json` although its test forbids any occurrence, and the latency
  retention test stamps its old file from real `DateTime.UtcNow` while applying
  a fixed 2026-07-31 retention clock, which no longer makes that file older than
  the cutoff on 2026-08-14. They were not expanded into ticket 18.
