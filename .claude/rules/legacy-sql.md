---
paths:
  - "mes/sources/legacy-program-sql/**"
---

# Legacy SQL snapshot

`mes/sources/legacy-program-sql/<date>/` is a verbatim research snapshot of the
old program's SQL. It is not an approved query catalogue and not the customer's
current version: it contains write statements, procedural code, and business
assumptions that no longer hold. No tool, application, or deployment step may
load or execute it, and the snapshot itself is never edited — research findings
belong in `mes/experiments` and `mes/evidence`, and a new customer version gets
a new dated snapshot. Read the snapshot's own `README.md` and `catalog.csv`
before using anything from it; a `READ_ONLY_CANDIDATE_UNVERIFIED` label is a
research priority, not a safety approval.
