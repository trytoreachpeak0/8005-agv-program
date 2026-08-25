# Ticket 27 — 15-day retention and capacity evidence

This bundle records the 2026-08-25 follow-up decision that all executable MesIngest history
retention is 15 days. It supplements, and does not replace or edit,
`../ticket27-fast-capacity-2026-08-25/`, which remains the historical 30-day red result.

## Build and environment

- Clean product commit: `87d401b3b39a8dea32bc330f9d0d38f5d0bd28d2`; `sourceDirty=false`.
- Published Host SHA-256: `eb67d27e1b4b5abb0f29134aea1cacbf03f099acf3ab9256bcbfdf5c4f4f502d`.
- Contract/schema: `2026.08.new-mes-ingest.v2.2` / `29`; `ERROR_SEARCH` capability `2.1`.
- SQL identity: local default instance service `LAB-WIN-01/MSSQLSERVER`, data source and
  `SERVERPROPERTY(ServerName)` `LAB-WIN-01`, SQL Server `16.0.1190.2` major 16,
  compatibility 160, engine edition 3; explicitly not LocalDB.
- Database policy: SIMPLE recovery, max server memory 1536 MB, fixed 64 MB data/LDF
  autogrowth, percent growth disabled.
- Package: 1,372-file Release/win-x64 bundle;
  `RELEASE-MANIFEST.json` SHA-256
  `5c293f10a1d26b889fc46f89ed82e57695f438195052b7bf17393bcdc92acd2d`.

## Sample and model

- Fixed Ticket 02 distribution: seed 8005, 14 seconds/round, 600 observations/round,
  600 Series, 70% active / 30% archived / 10% active-error.
- Baseline: 600 current RawObservation. Representative sample: 415 historical rounds /
  249,000 historical rows plus 600 current rows = exactly 249,600 RawObservation.
- Target: `floor(15*86400/14) = 92,571` historical rounds and
  `92,571*600 = 55,542,600` historical RawObservation rows. Full target was not materialized.
- Baseline/sample logical used: 1.960935 / 38.328120 MB. Observed growth:
  36.367185 MB = 0.087631771 MB/round = 0.000146052952 MB/row.
- Formula:
  `((baselineLogicalMb + logicalMbPerRound * targetRounds) * 1.30) + projectedTombstoneMb`.
  Tombstones use
  `(observedTombstoneMb / observedTombstoneCount) * projectedTombstoneCount * 1.30`.
  The 30% factor is the safety margin, not a retention duration.
- Prediction: logical used 10,548.650601 MB; physical data file 10,568 MB using
  `72 + ceil((logical-72)/64)*64`; LDF 343.189844 MB using
  `max(sample LDF, peak physical log, peak used log) * 1.30` under SIMPLE recovery.
- Final limits: 12,288 / 16,384 / 2,048 MB. 70% escalation thresholds:
  8,601.6 / 11,468.8 / 1,433.6 MB for logical / physical / LDF.
- Segment-rate max/min ratio: 2.427779815, above the 1.20 linearity bound.
- Gate: failed closed with `CAPACITY_GROWTH_NONLINEAR` and
  `CAPACITY_LOGICAL_70_PERCENT_ESCALATION`. Physical and LDF predictions are below their
  70% thresholds, and all three predictions are below final limits. Release remains blocked;
  the existing escalation path is a separately approved full `ProfileDays 15` run. Content
  addressing is reconsidered only if that full-scale validation also fails.

## Storage, cleanup, and transient resources

- DemandRawObservations PAGE allocations at 249,600 rows:
  clustered PK 11.898437 MB, Series nonclustered index 10.031250 MB, Demand nonclustered
  index 14.117187 MB. All three required indexes reported `PAGE` compression.
- Tombstones: 25 observed rows; clustered and nonclustered allocations each 0.015625 MB.
  Projection for 180 archived Series plus 30% margin: 0.292500 MB.
- Database version-store peak: 136.8125 MB; reported with margin as 177.85625 MB.
  tempdb version-store peak: 140.25 MB; reported impact with margin as 182.325 MB.
  tempdb user-object delta through queries was 0 MB; internal-object delta was -0.1875 MB.
- Log stages: after bootstrap `NOTHING` / 7.992188 MB physical / 1.15625 MB used;
  after load `NOTHING` / 199.992188 / 43.507813 MB; after queries `NOTHING` /
  199.992188 / 43.785156 MB; after cleanup `ACTIVE_TRANSACTION` / 263.992188 /
  18.003906 MB. Physical LDF increment was 255.992188 MB. The final nonblank reuse wait is
  recorded rather than normalized away.
- Cleanup used only an accelerated 1-second check interval. Published defaults remained
  3600 seconds / 210,000 raw rows / 25 whole Series / 15 seconds.
- Cleanup deleted 249,600/249,600 RawObservation and 25/25 eligible Series, wrote 25
  tombstones, and left 0 RawObservation / 0 eligible Series. The active graph stayed exactly
  420 Series, 420 generation-bearing demands, 480 events, 60 conditions, 60 error periods,
  60 evidence rows, 1,500 facts, split count 0, with identical SHA-256
  `661d764938228dba93fe2ef936fa873bfbc7200bf78a6a889915b6db8297f376`.
- Both named scale databases were ownership-checked and removed; residual Ticket 27 15-day
  scale databases: 0.

## Watch preview and raw evidence

- Golden-machine `watch-production-preview` passed on `GPT-WIN11`, interactive Session 1,
  1920x1080, 96 DPI / 100%, light theme, zh-CN, China Standard Time, SoftwareOnly.
- `watch-vm-tests`: 146 passed / 0 failed / 5 named fixture-only skips;
  `watch-ui-journeys`: 1 passed / 0 failed / 0 skipped. The five skips require candidate or
  golden-fixture environment variables and are not part of this production preview path.
- Named Tier 2 skips:
  `WatchWindowCandidateEquivalenceTests.Candidate_directories_are_visually_equivalent`,
  `WatchWindowVisualEquivalenceGoldenFixtureTests.The_recorded_antialiasing_flip_is_accepted`,
  `WatchWindowVisualEquivalenceGoldenFixtureTests.A_one_pixel_glyph_shift_is_rejected`,
  `WatchWindowVisualEquivalenceGoldenFixtureTests.A_different_page_is_rejected`, and
  `WatchWindowVisualEquivalenceGoldenFixtureTests.A_one_pixel_control_geometry_change_is_rejected`.
- Scheduled task result 0; task absent after cleanup; residual processes 0; post-cleanup
  environment result 0. No candidate or baseline was promoted. The production journey expanded
  `ErrorSearchWindowFilter`, asserted the visible `最近 15 天` option, and captured
  `06a-error-search-15-day-window.png` (SHA-256
  `1c1182d2e780fc33406480b55aac858c5a1a513f499926399fcc31c1b349c7ad`). Explicit human review
  of that exact preview remains required before visual approval.
- Raw baseline bundle:
  `mes/ingest/csharp/.artifacts/ticket27-15day-evidence-2026-08-25/scale-20260825T071241Z-52633e35/`
  (JSON SHA-256 `33ba83b4f2778005a732808e3682b6749d714b39728c1a24e40afb22891d0f8f`).
- Raw sample bundle:
  `mes/ingest/csharp/.artifacts/ticket27-15day-evidence-2026-08-25/scale-20260825T071312Z-9547f8cb/`
  (JSON SHA-256 `6d391e93e5aaf7a295a08f1108fd14578c8469b2f5406de61b50c89535cd2def`).
- Golden evidence:
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-27/run-20260825-153220-watch-production-preview/`;
  exact preview:
  `watch-ui/20260825-153248-852/production-workspace-19-22/06a-error-search-15-day-window.png`.

## Tests and review

- Focused TDD evidence included the intentional red Raw/Series 15-day boundary tests, focused
  real-SQL retention tests (3/3), ErrorSearch/Watch tests (31/31), capacity fixture matrix
  (21/21 after recalibrating the 15-day threshold mutation), exact contract/package tests
  (36/36), and per-capability release/cutover freeze tests (2/2); all reported zero skips.
- The first full Tier 1 attempt is preserved as red evidence: 879 passed / 3 failed / 0 skipped /
  total 882, 11m47s. The three failures were stale 30-day earliest-boundary expectations in
  ErrorSearchDetail and PollTrace tests plus an OpenAPI capability enum still expecting only
  `2.0`. TRX SHA-256:
  `430a1f1d287ca643caeba92c46995e177ef4fef5d7841305be30540bfc0f3b10`; raw directory:
  `mes/ingest/csharp/.artifacts/ticket27-15day-tier1-final/run-20260825T074342Z/`.
- After exact test-contract fixes and a final review, the closing Tier 1 wrapper ran exact
  `dotnet test MesIngest.Tests` from `mes/ingest/csharp` against `LAB-WIN-01/master`: 882 passed /
  0 failed / 0 skipped / total 882, exit 0, 12m35s. Product major 16 and compatibility 160 were
  both measured. TRX SHA-256:
  `e5171b9f21e393e906acd03ebc2298429952fba78bc595f0d0dedf315c91610b`; attestation SHA-256:
  `e762cf8294edcb855b711c9d1707ca6fd313ad5050a8f1da2d92fbcf7f3ae976`; raw directory:
  `mes/ingest/csharp/.artifacts/ticket27-15day-tier1-final-green/run-20260825T080027Z/`.
- Code review reached fixed point after three review/fix cycles: final Standards `No findings`;
  final Spec `No findings`. Ticket 28 diff: 0. The old tracked 30-day evidence diff: 0.
- Tier 3 was not run: no candidate/baseline promotion was authorized or needed, and human visual
  approval remains pending.
- Ticket 27 scale databases created by this follow-up: 0 residual. Five `MesIngest_Ticket01_*`
  databases with zero user sessions predated this follow-up (creation times from 2026-08-24 to
  2026-08-25 03:04) and were not deleted outside task ownership.
