# Initial requirement-evidence snapshot

This is an evidence capture, not an authority or approval classification. It does not modify source requirement materials.

## Capture identity

- Started (local): 2026-08-03T10:50:41.5202253+08:00
- Started (UTC): 2026-08-03T02:50:41.5202253Z
- Completed (local): 2026-08-03T10:50:48.2268823+08:00
- Completed (UTC): 2026-08-03T02:50:48.2268823Z
- Repository root: C:\Users\szy\Desktop\xinji\8005多仓位AGV
- Branch: szy_document_dev
- HEAD: 1469d6309d00b0abb792f6cd686aed68286e638e
- Upstream: origin/szy_document_dev
- Candidate files: 1809
- Content hash: SHA-256 of the actual working-directory bytes
- Discovery errors: None.

## Candidate policy

The manifest takes a deliberately broad document-shaped candidate set from the actual working directory, including tracked, untracked, and ignored files. It includes Markdown/text, structured data, PDF/Office, image, HTML/XML, and diagram formats. Inclusion does not imply that a file is a requirement or authoritative.

Dependency, build-output, test-output, IDE, and cache directory names are excluded by the capture script. This map and its evidence directory (`.scratch/current-requirements-baseline/`) are also excluded from the candidate set because they are newly-created governance records, not recovered source requirements; they remain visible in the raw worktree status. If later inventory discovers requirement evidence outside this candidate policy, it must be recorded in a new snapshot rather than silently added to this one.

## Git status counts

- tracked-clean: 1704
- untracked: 105

## Files

- `candidate-documents.tsv`: candidate path, Git state, SHA-256, byte size, and last-write UTC.
- `worktree-status.txt`: raw `git status --porcelain=v1 --branch --untracked-files=all` output captured during this run.
- `discovery-errors.txt`: stderr from file discovery; empty means no discovery errors.
- `capture.ps1`: the exact repeatable capture method. Re-running it overwrites this evidence directory and therefore creates a new observation, not the original observation.

## Verification boundary

The manifest fixes the observed bytes and Git state at capture time. Later file changes must not overwrite the meaning of this capture; compare current hashes to the manifest or create a separately timestamped snapshot.
