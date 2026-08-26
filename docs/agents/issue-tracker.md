# Issue tracker: Local Markdown

Issues and specs (you may know a spec as a PRD) for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Golden WPF validation checklist

Any ticket that changes `MesIngest.Watch` UI, XAML, Wpf.Ui controls, layout,
UI Automation, DPI behavior, or visual baselines must link
`docs/agents/golden-renderer.md` and include its Ticket checklist. The ticket
cannot claim visual acceptance from a local desktop, PowerShell Direct session,
RDP session, or an unapproved screenshot candidate.

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.

### Cross-repository findings

When a local Wayfinder map finds a problem owned by another project, create or
update the full problem record and its primary evidence in that project's
repository, then commit and push it there. The local `.scratch/` ticket may keep
only the minimum coordination pointer:

```markdown
Owning repository: <repository URL or verified path>
Owner issue/artifact: <link>
Published branch/commit: <branch and pushed commit>
Impact on this ticket: <one-line blocker or status>
```

Do not copy the external defect report, fix instructions, project-specific
evidence, implementation, or tests into this repository. If no owning or
integration repository has been designated, do not write the artifact locally;
ask the user to choose its destination.
