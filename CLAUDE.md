@AGENTS.md

# Claude Code

The instructions for this repository are in `AGENTS.md`, imported above so that
every coding agent reads the same text. Write new rules there, not here. This
file holds only what is specific to Claude Code, and keeps `@AGENTS.md` as its
first line. This repository has no CI, so nothing checks that line; keep it.

Matt Pocock's skills ship as the `mattpocock-skills` plugin and are
explicit-only. Use one only when the user names it directly (for example,
`/mattpocock-skills:diagnosing-bugs`, `/mattpocock-skills:implement`, or "use
the prototype skill"). Ordinary requests should be handled directly.

- Matt Pocock's engineering skills are installed as the `mattpocock-skills` plugin (user-level, from the `claude-plugins-official` marketplace). Invoke them namespaced: `/mattpocock-skills:<name>`.
- The ponytail skills live in `.claude/skills/` and are model-invocable — unlike the Matt skills, they can fire without being named.
- `code-review` collides with Claude Code's bundled `/code-review`. Use `/mattpocock-skills:code-review` for Matt's Standards+Spec review; bare `/code-review` (and `/code-review ultra`) stays the bundled one.
- Subagents are pre-authorised when a skill dispatches them as its own process — `/mattpocock-skills:code-review` fans Standards and Spec out in parallel. Exploration and search stay inline with Grep/Glob/Read, however broad the task sounds.
