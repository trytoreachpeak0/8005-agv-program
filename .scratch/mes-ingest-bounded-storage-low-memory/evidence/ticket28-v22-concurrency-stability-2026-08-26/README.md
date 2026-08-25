# Ticket 28 v2.2 concurrency stability evidence

## Outcome

The superseding 30-minute accelerated concurrency gate passed on the clean
`94cc7b07873528b358038a8d283146dba617264a` package. Ticket 28's stability result is green and
does not require a 24-hour soak. The superseding v2.2 closing cycle's sole real-SQL Tier 1 also
passed `921/921`, failed `0`, skipped `0`; Ticket 28 is done and its
stability/capacity/Tier-1 release prerequisites are green.

The prior 30-minute red evidence under contract/schema v2.1/28 remains unchanged in
`../ticket28-accelerated-stability-2026-08-25/`. A later 4-hour run on v2.2/29 also remains a
historical fail-closed result: it ran `14403.077s` and exposed two evidence-attribution defects
(ordinary request timers inherited the slowest sibling, and unrelated short
`ACTIVE_TRANSACTION` samples were treated as one persistent transaction). Those defects were
fixed before this superseding run; the 4-hour red result is not represented as a pass.

Ticket 27 was synchronized without reset or merge: upstream `8013b049`, `48c3d650`, and
`cdcf5620` are present on this branch as `0703207e`, `d02227a3`, and `cf0163bd`. Ticket 27 is
`done` under the accepted 15-day +30% hard-limit policy. Its old fail-closed decision is preserved
inside the capacity evidence, while 70% and nonlinearity are advisory warnings. The accepted
prediction is logical `10548.651 MB`, physical `10568 MB`, and LDF `343.190 MB`, below hard
limits `12288/16384/2048 MB`; nonlinearity `2.427779815` remains visible as a warning.

## Identity and environment

- Package manifest: 1,372 files; SHA-256
  `9e4052c73a76bc957b42a9c21a6eb63707f6fbfcdbf0630970e1676d16b2d66b`.
- Host / Watch / Reference Consumer SHA-256:
  `63ab59defc1db2c1d699f06274945e1728068f2ee814bfd8fbf0ff6376b07adc`,
  `ea27fe7fcf0f6403b095d946326d5c7d5224b32ade88df98d8ab163c79480f65`, and
  `f53aec909e5d1e709a2d5e5c4315f07b6b3cc9a95a6c41e5cbec06bedd4b2436`.
- Contract/schema/HistoryEpoch: `2026.08.new-mes-ingest.v2.2` / `29` /
  `C83B4821-C05B-4758-BA05-8D6564F99F51`.
- SQL Server default instance `16.0.1190.2`, major `16`, compatibility `160`, `SIMPLE`, max server
  memory `1536 MB`. The isolated MDF/LDF files used the healthy dedicated
  `F:\MesIngestTicket28` directory because the default C volume was below the product's 10%
  storage-health threshold. Published pressure thresholds were not changed.
- Published defaults remained 60-second start-to-start polling, 60/120/300-second backoff,
  Watch 30/60-second refresh, and 3600-second cleanup. The evidence-only profile used 1-second
  polling and 60-second cleanup, both 60x operation multipliers only.
- The clean Release deterministic contract passed `15/15`, failed `0`, skipped `0`; TRX SHA-256
  `98d96776b1f7c396ede639729ad604b02b4dcc3cc53a4ded11048c9a162ea309`, attestation SHA-256
  `1814fa08b5a85808c4ba1339d081e98f6b0a9c0ac352925f48431b72bc6a5157`.

## Workload and latency

- Duration `1801.701s`; 600 Series; 100 historical rounds; initial/max RawObservation rows
  `60,600 / 60,607`; eight concurrent clients; one midpoint Host restart.
- Operations: successful/total polls `1,777/1,777`; Watch API reads `13,475`; frozen detail reads
  `24,176`; catalog reads `1,925`; packaged Watch reads `10`; packaged Reference Consumer reads
  `2`; cleanup checks `30`; latency samples `39,576`; resource snapshots `32`.
- Overall P95/P99 were `171.7462/857.6105 ms`; maximum per-surface P95/P99 were
  `1151.5750/1716.1767 ms`, both below the hard `<2000/<5000 ms` SLO. First/last quartile P95
  improved from `218.0711` to `156.7262 ms`; all 18 required per-surface/process-generation stable
  stages were present and degradation count was zero.
- The slowest surface was ErrorSearch: overall P95/P99 `1151.5750/1716.1767 ms`; generation 2
  stable P95/P99 `1651.8629/1944.8069 ms`, with first/last-half P95
  `1166.6602/1759.3270 ms`. It remained below the absolute SLO and below the gate's degradation
  threshold; the result did not relax either limit.

## Seven historical red signals

1. RESOURCE_SEMAPHORE now uses workload-attributed deltas and consecutive active/pending grants,
   not every snapshot above a cumulative counter. New run: all instance/attributed deltas,
   active/pending samples, consecutive samples, and pending grants were zero.
2. LDF separates physical/used size, autogrowth, stable plateau, reuse wait, and actual oldest
   database transaction identity. New run: physical peak `136 MB`, used peak `63.910 MB`, one
   early autogrowth, zero stable/late growth, and stable used slope `-2.0829 MB/min`. The full
   timeline had two isolated `ACTIVE_TRANSACTION` samples (`0.213s` in generation 1 and `0.05s`
   in generation 2); the evaluated generation-2 stable tail contained one, so persistent count
   was one and the gate passed.
3. Host working set and handles are segmented by PID/process generation. Generation 2's stable
   tail used eight snapshots: WS slope `-0.0531 MB/min`, handle slope `0.9803/min`; peaks were
   `276.648 MB` and `770` handles. Cross-restart slopes are diagnostic only.
4. Catch-up analysis is session/process-generation scoped. Two poll generations, one intended
   restart, maximum concurrent polls one, and catch-up bursts zero.
5. Frozen DemandSeries now returns consistent 200 responses while intentional expiry separately
   proves `410 MES_INGEST_HISTORY_EXPIRED`. New run: HTTP errors/unexpected outcomes/frozen errors
   `0/0/0`; one expected 410 was excluded from error counts; frozen mismatch/windows without
   projection `0/0`, with 292 projection commits during frozen reads.
6. Spill attribution was localized by surface/query hash/operator and the poll-query sorts and
   grants were removed/bounded with existing schema indexes. New run: spills zero, XEvent drops
   zero, and spill diagnostics complete.
7. Ordinary API timers now stop when each task completes and latency is split by surface,
   process generation, stable phase, cleanup phase, and half-window. New run met both absolute
   SLOs and reported stable-stage degradation count zero.

## Resources, cleanup, and residuals

- Error 701 / spill / XEvent drop / max lock wait / unbounded lock wait / max pending grants:
  `0 / 0 / 0 / 0 ms / 0 / 0`.
- Host stable-tail WS/handle slopes `-0.0531 MB/min` and `0.9803 handles/min`; SQL WS slope
  `-0.1426 MB/min`; Host/SQL peaks `276.648/1367.445 MB`.
- Logical database / physical data / tempdb slopes: `-0.0713 / 0 / 0.1270 MB/min`.
  Database/tempdb version-store peaks: `30.000/35.688 MB`.
- Cleanup status `SUCCEEDED`, failure null, backlog zero; expired polls `101`, deleted initial raw
  rows `60,600`, final raw rows `3,558`. Earliest available advanced from
  `2026-08-10T05:56:41+08:00` to `2026-08-26T06:30:32+08:00`. StoragePressurePause samples were
  zero and final status was `HEALTHY`.
- Retry schedule, controlled 24-hour logical boundary, HistoryEpoch preservation, restart state,
  current logical-read growth, frozen pinning, and packaged clients all passed.
- The superseding run requested cleanup and left no owned scale database, XEvent session, Host
  process, or F-volume MDF/LDF file. One stopped XEvent definition from the earlier owned
  `scale-20260825T103839Z-9d5cacbc` attempt was identified and removed explicitly. Six unrelated
  zero-session Ticket01 databases and one Host process created on 2026-08-23 predated this run and
  were preserved. The independently captured post-Tier-1 receipt is `cleanup-audit.json` in this
  directory; the Ticket01 database count was six both before and after Tier 1.

## Evidence locations

- Machine-readable compact record: `stability-summary.json` in this directory.
- Superseding baseline raw report:
  `mes/ingest/csharp/.artifacts/ticket28-v22-94cc7b07/evidence/scale-20260825T222904Z-2c45bd09/scale-query-evidence.json`,
  SHA-256 `2ba9c4c9a326576385e54c47ebc16880529c1d5d76cf41f0a382359c355a515b`.
- Superseding stress raw report:
  `mes/ingest/csharp/.artifacts/ticket28-v22-94cc7b07/evidence/scale-20260825T222954Z-361aa512/scale-query-evidence.json`,
  SHA-256 `33d34ed1776c6eed9cafb88fad01cb7d3194f8e015362fe5a47302ef0776fb9a`.
- Historical 4-hour red raw report:
  `mes/ingest/csharp/.artifacts/ticket28-v22-78b96b32/evidence/scale-20260825T175709Z-b2cae193/scale-query-evidence.json`,
  SHA-256 `a096b99b8ff8e4f66f4d0354f1aafea4d666db7443bec0dcbc8d4080654507dc`.
- Closing Tier 1 TRX / attestation:
  `mes/ingest/csharp/.artifacts/ticket28-v22-94cc7b07/tier1/run-20260825T231541Z/`, SHA-256
  `49d47fb9d00d75d59f6ff5cc55423ad0b5db9812d24eaf35c251c96da5008edf` /
  `d78af32ca76f303f7497c79c690cf39922baa40d8e4dd3477365e41ee9b1f420`.
- Tier 2/3 and visual baseline validation were not run because there was no UI/XAML change.

## Tests and review

- Focused `ScaleAndQueryEvidenceGateTests`: `51 passed / 0 failed / 0 skipped`.
- Final pre-pressure dual-axis code review: Spec and Standards P0/P1/P2 `0` after all findings were
  fixed. Final pressure/evidence review also reported Spec and Standards P0/P1/P2 `0`.
- The superseding v2.2 closing cycle's sole real-SQL Tier 1 ran from `mes/ingest/csharp` through the exact
  `dotnet test MesIngest.Tests` wrapper on the default SQL Server instance, explicitly
  expecting/observing product major `16` and compatibility `160`: `921 passed / 0 failed /
  0 skipped / total 921`, exit `0`, duration `861.951s`, VSTest/xUnit v2, SDK `8.0.424`.
  Tier 1 source commit was `94cc7b07873528b358038a8d283146dba617264a`; no Tier 1 rerun occurred
  after the v2.2 product/test/build inputs stabilized.
