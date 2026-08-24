# Ticket 11 Verify.Xaml scenario review

- Product/business reviewer: user
- Product decision: `这版符合` (2026-08-10), after reviewing the final four-page golden-machine preview
- Technical review: stable v17 candidate contact sheets, raw core-state PNGs, XML parsing, dimensions, and SHA-256 manifest
- Global tolerance or masks: none
- Historical baselines overwritten: no

Each proposal below has its own `before.png`, `after.png`, `diff.png`, `before.xml`,
`after.xml`, and hashes in `proposal-manifest.json`.

- [x] `alerts-active-selected-1440x900` — active list, scope semantics, selected warning, and exact previous/current targets retained.
- [x] `alerts-empty-1440x900` — empty result surface and filter hierarchy remain visible.
- [x] `alerts-failure-retains-results-1440x900` — failure banner is visible while the prior result/detail context remains.
- [x] `alerts-loaded-2560x1440` — 2K off-screen layout preserves the D/E hierarchy and uses the additional workspace.
- [x] `alerts-loading-1440x900` — loading state retains shell, filters, paging, and relationship area.
- [x] `alerts-resolved-1440x900` — resolved segment and selected relationship semantics remain distinct from active alerts.
- [x] `demands-empty-1440x900` — empty list state preserves filter and detail-region affordances.
- [x] `demands-failure-retains-results-1440x900` — failure banner does not erase the last successful task context.
- [x] `demands-gone-selected-1440x900` — independent GONE state, task conclusion, and related-alert cards remain visible.
- [x] `demands-loaded-2560x1440` — 2K off-screen layout preserves hierarchy and extra horizontal workspace.
- [x] `demands-loading-1440x900` — loading state retains the prior shell and deterministic placeholders.
- [x] `demands-visible-selected-1440x900` — five core columns, selected task, and exact/business-key alert cards match the accepted design.
- [x] `overview-degraded-active-alert-1440x900` — degraded heading and active-alert summary are explicit without changing navigation.
- [x] `overview-healthy-1440x900` — healthy host, poll, alert, and visible-demand summaries match the accepted shell.
- [x] `overview-loaded-2560x1440` — 2K overview keeps the four-card information hierarchy.
- [x] `overview-offline-stale-1440x900` — offline/stale banner and retained last-known summaries are unambiguous.
- [x] `settings-default-1440x900` — credential, timeout, auto-refresh, apply, and reset controls remain reachable.
- [x] `settings-loaded-2560x1440` — 2K settings layout remains left-weighted and readable without hierarchy drift.
- [x] `settings-validation-error-1440x900` — validation copy is visible next to the affected settings workflow.

Decision: all 19 proposals approved individually for promotion into the new, previously
empty `Baselines/SelectedUi` directory.
