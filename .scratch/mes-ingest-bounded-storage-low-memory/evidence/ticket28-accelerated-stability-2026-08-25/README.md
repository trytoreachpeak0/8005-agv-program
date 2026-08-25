# Ticket 28 accelerated concurrency stability evidence

## Outcome

The 30-minute gate completed and failed closed. The recorded next validation is a 4-hour or
24-hour real soak after resolving the seven named risk signals. Ticket 28 is `ready-for-human`,
not complete, and release readiness is false.

Ticket 27 remains an independent blocker and was preserved byte-for-byte by SHA-256
`d8ceab54c915f8aef3a63a29d74f41abfbe50e350c0f9f3ea97b6e2666ded612`: projected logical
`21094.459486 MB`, physical `21128 MB`, LDF `343.189844 MB`, and nonlinearity
`2.4277798145421`.

## Identity and environment

- Clean source/package commit: `f84fee2e4140ab16f8bdec77c7a8d762c557fa84`; 1,372-file manifest
  SHA-256 `abdf37ae95466272042eb5dc29744522b076e6915a53b6ff8f2810d5a9012fc4`.
- Host / Watch / Reference Consumer SHA-256:
  `6eef95709fa121577b852bc6715d3a9552f61e68128b11c38da33845334c0734`,
  `289ae373ed3daf69501b7e72bce1f8146833a53659b29ea2729155c9634a22d3`, and
  `addd5a9e4b85e09cc6f435be46d7a84cb9fd981c1af763c708c90c3fab6e7180`.
- Contract/schema/HistoryEpoch: `2026.08.new-mes-ingest.v2.1` / `28` /
  `2F88502D-8F71-4C79-9EE7-FB150E917D85`.
- SQL Server default instance `16.0.1190.2`, major `16`, compatibility `160`, `SIMPLE`, max server
  memory `1536 MB`. The isolated evidence files were placed on the healthy F volume; published
  application storage thresholds were unchanged.
- Published defaults remained 60-second start-to-start polling, 60/120/300-second failure
  backoff, Watch 30/60-second refresh, and 3600-second cleanup. The evidence profile used 1-second
  polling and 60-second cleanup, both 60x operation multipliers only.

The Release deterministic contract run passed `13/13`, failed `0`, skipped `0`. TRX SHA-256 is
`95fa12c21b0e7ae7f0ccb08d442d2267678fc4b6888537984ae076a57ac1d22f`; attestation SHA-256 is
`59d159bb66afd4a3fbaf07f47ac1d2e3ca94ed4fb9002c63a941323834feb617`.

## Workload and SLOs

- Duration `1801.366896s`; 600 Series; 100 historical rounds; initial/max RawObservation rows
  `60,600 / 60,717`; eight concurrent clients; one midpoint Host restart.
- Operations: successful/total polls `1,701/1,701`; Watch reads `12,369`; frozen reads `24,580`;
  catalog reads `1,767`; packaged Watch reads `10`; packaged Reference Consumer reads `2`;
  cleanup checks `30`; resource snapshots `32`.
- API samples `38,784`; P95/P99 `876.3353/1196.1121 ms` (both under 2s/5s); first/last quartile
  P95 `278.3607/1063.18 ms`, so latency degradation failed.
- Poll concurrency was 1, but one catch-up burst was observed. HTTP errors totaled 69; a precursor
  diagnostic run identified the same failing surface as a frozen DemandSeries HTTP 500, while the
  final compact evidence records the fail-closed total rather than response bodies.
- Current logical-read growth passed. Frozen mismatches/windows without projection were `0/0`,
  with 372 projection commits during frozen windows.

## Resource, waits, and cleanup

- Error 701 / XEvent dropped events / max lock wait / unbounded lock waits / max pending grants:
  `0 / 0 / 0 ms / 0 / 0`.
- The conservative RESOURCE_SEMAPHORE gate counted 18 snapshots whose cumulative wait counter
  remained above the first sample. The counter actually increased in 2 intervals by 11 waiting
  tasks total; active pending grants peaked at zero. It remains a red wait signal, but is not
  described as 18 intervals of continuously active grants. Spills were `2,881`.
- Host/SQL working-set slopes `1.2723/-0.1259 MB/min`; peaks `419.863/1452.031 MB`.
- Host handle peak `895`, slope `5.4486 handles/min` (red).
- Logical DB / physical data / LDF / tempdb slopes: `-0.07965 / 0 / 2.13931 / 0.15460 MB/min`;
  LDF is red. Database/tempdb version-store peaks were `21.5/26.1875 MB`.
- Cleanup succeeded with no failure or backlog: expired polls `101`, deleted raw rows `60,600`,
  final raw rows `3,400`. Earliest available advanced from `2026-07-01T07:36:41+08:00` to
  `2026-08-25T07:36:46.8905912+08:00`. StoragePressurePause samples were zero and final status was
  `HEALTHY`.
- Retry schedule, controlled 24-hour logical boundary, HistoryEpoch across restart, and restart
  state all passed.

Gate failures: `STABILITY_CATCH_UP_BURST`, `STABILITY_HANDLE_TREND`, `STABILITY_HTTP_ERROR`,
`STABILITY_LATENCY_DEGRADATION`, `STABILITY_LDF_TREND`, `STABILITY_RESOURCE_SEMAPHORE`, and
`STABILITY_SPILL`.

## Evidence locations and residuals

- Compact machine-readable record: `stability-summary.json` in this directory.
- Local baseline raw report:
  `mes/ingest/csharp/.artifacts/ticket28-stability-f84fee2e/scale-20260824T233536Z-4973dfff/scale-query-evidence.json`,
  SHA-256 `6264c5d4c7750ab9c5e762f6b403ea35f35497fa9c26b31c1c2d2b84c7fe04a6`.
- Local stress raw report:
  `mes/ingest/csharp/.artifacts/ticket28-stability-f84fee2e/scale-20260824T233620Z-99e32a86/scale-query-evidence.json`,
  SHA-256 `57cabece72a1a7467cd2600b9dd6a237a2d1ecbd39dc855b2ed9e19d4bb117bc`.
- The owned SQL database, XEvent session, Host processes, database files, and empty dedicated
  F-volume directory were removed. No Tier 2/3 or visual baseline
  was run because there was no Watch UI/XAML change.
- Human action: investigate the seven red signals and schedule the required 4h/24h real soak.
  Tier 1 results will be appended only after post-stress review.
