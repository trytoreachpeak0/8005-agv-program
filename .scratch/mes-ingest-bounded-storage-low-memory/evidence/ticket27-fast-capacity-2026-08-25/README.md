# Ticket 27 fast capacity projection evidence

## Outcome

The fast gate failed closed and requires the explicit full-scale escalation. It did not
materialize the 111,085,200-row 30-day profile. The representative run used 415 historical
rounds plus one 600-row current round: exactly 249,600 `DemandRawObservations`.

Failure codes:

- `CAPACITY_GROWTH_NONLINEAR`
- `CAPACITY_LOGICAL_70_PERCENT_ESCALATION`
- `CAPACITY_PHYSICAL_70_PERCENT_ESCALATION`

The release remains blocked. The recorded next validation is the existing
`Invoke-ScaleAndQueryEvidence.ps1 -ProfileDays 30 -ConfirmFullScaleEscalation
MESINGEST_FULL_SCALE_ESCALATION` path. Content addressing remains a later decision only if that
full-scale validation also fails.

## Identity and replay

- Clean source commit at build: `89c54eed2f0f64284a6fbd5f587a0d9e0f6eefb9` (`sourceDirty=false`).
- Host SHA-256: `b224fde5b5cced91c00d5b9f7647a65072007e0a320fc3e4ffff0f5052fc0485`.
- Final package manifest SHA-256: `ae501c3ad63010b7ff6379535f3bd6158cf3b048070c35eaa786c289fd3a36e3` (1,372 files).
- Contract/schema: `2026.08.new-mes-ingest.v2.1` / `28`.
- Baseline run: `scale-20260824T212917Z-e6d66c5f`; HistoryEpoch `A9655F58-65B8-45A0-9723-BCE017D91E88`.
- Sample run: `scale-20260824T212942Z-78243ac8`; HistoryEpoch `BD300811-18B9-4094-9A2D-B5D3A66647E3`.
- SQL data source / `SERVERPROPERTY(ServerName)`: `LAB-WIN-01`; Windows default-instance service: `MSSQLSERVER`; product `16.0.1190.2`, major `16`, Enterprise Evaluation, compatibility `160`, not LocalDB.
- Recovery/configuration: `SIMPLE`, max server memory `1536 MB`, final `log_reuse_wait_desc=NOTHING`.
- Fixed distribution: seed `8005`, 14 seconds/round, 600 observations/round, 600 Series, 70% active, 30% archived, 10% active errors; `RoundBatchSize=100`.
- Query evidence: DemandSeries surface, 1 warmup and 3 measurements, 357 actual plans, 84 statement metrics.

The full raw reports and actual ShowPlan XML are retained locally under
`mes/ingest/csharp/.artifacts/ticket27-clean-evidence-2026-08-25/`. The final baseline/sample JSON
SHA-256 values are `efff269e3cf721fcdb8b8d6d691ca5d5fa60c0421f381d61d2c9d847441aa92e` and
`77f2749765ede8e008f83cf4ce4b8cd7098a655b4843523bd57c034922058af4`.

## Model and thresholds

Inputs and formula:

- Baseline logical used: `1.960935 MB`; sample logical used: `38.328120 MB`; observed growth: `36.367185 MB`.
- Observed growth: `0.087631771 MB/round` and `0.000146052952 MB/row` (about `153.15 bytes/row`).
- Target: `floor(30*86400/14) = 185,142` rounds and `111,085,200` rows.
- Logical formula: `((baselineLogicalMb + logicalMbPerRound * targetRounds) * 1.30) + projectedTombstoneMb`.
- Tombstone formula: `(0.03125 MB / 25 measured tombstones) * 180 fixed archived Series * 1.30 = 0.2925 MB`.
- Version-store/tempdb transient formulas: measured peaks times `1.30`, yielding `177.85625 MB` and `182.89375 MB`; they have no separate ticket threshold.
- Physical formula: `72 MB start + ceil((projectedLogicalUsedMb - 72 MB) / 64 MB fixed autogrowth) * 64 MB`.
- LDF formula under SIMPLE: `max(sample LDF, load/query/cleanup physical LDF peak, used-log peak) * 1.30`.
- Linearity rule: at least four checkpoints and maximum/minimum positive segment rate no greater than `1.20`; observed `2.427779815`.

| Axis | 30-day +30% prediction | Final limit | 70% escalation point | Decision |
| --- | ---: | ---: | ---: | --- |
| Logical used | `21,094.459 MB` (`20.600 GiB`) | `12,288 MB` | `8,601.6 MB` | fail/escalate |
| Physical data files | `21,128 MB` (`20.633 GiB`) | `16,384 MB` | `11,468.8 MB` | fail/escalate |
| LDF | `343.190 MB` | `2,048 MB` | `1,433.6 MB` | pass this axis |

The three PAGE-compressed raw-observation allocations measured/projected as follows:

| Index | Kind | Sample used | Observed growth | 30-day +30% |
| --- | --- | ---: | ---: | ---: |
| `PK_MesIngest_DemandRawObservations` | clustered | `11.898437 MB` | `11.851562 MB` | `6,873.527 MB` |
| `IX_MesIngest_DemandRawObservations_Series` | nonclustered | `10.031250 MB` | `10.000000 MB` | `5,799.670 MB` |
| `IX_MesIngest_DemandRawObservations_Demand` | nonclustered | `14.117187 MB` | `14.078125 MB` | `8,164.841 MB` |

Checkpoints were `(rounds, rows, logical MB, physical data MB, LDF MB)`:
`(0,0,2.40,72,8)`, `(100,60000,9.97,72,72)`, `(200,120000,17.74,72,136)`,
`(300,180000,27.45,72,200)`, `(400,240000,37.70,72,200)`, and
`(415,249000,38.33,72,200)`.

## Cleanup and transient storage

- Production Host cleanup ran with only its check interval accelerated to 1 second. Published defaults remained: hourly (`3600s`), `210,000` raw rows/batch, `25` whole Series/batch, `15s` budget.
- Deleted `249,600 / 249,600` RawObservation rows and `25 / 25` retention-eligible whole Series; wrote 25 tombstones. Remaining raw rows and eligible Series: `0 / 0`.
- Tombstone clustered and nonclustered allocations each used `0.015625 MB` (`0.070312 MB` reserved) for 25 rows.
- Active graph before and after had the identical 1,500-fact SHA-256 `661d764938228dba93fe2ef936fa873bfbc7200bf78a6a889915b6db8297f376`: 420 Series, 420 generation-bearing demands, 480 events, 60 current conditions, 60 error periods, 60 error-evidence rows, zero split Series.
- LDF grew from the 8 MB baseline to 200 MB during load/query and 263.992 MB after cleanup; incremental physical peak `255.992 MB`, peak used log `64.293 MB`, final reuse wait `NOTHING`.
- Database version-store peak: `136.8125 MB` (projected +30% `177.85625 MB`); tempdb version-store peak: `140.6875 MB` (modeled tempdb +30% impact `182.89375 MB`). Through query evidence, tempdb user-object and internal-object deltas were both `0 MB` (shared-instance snapshots are retained in the raw report).
- Data and log files both used fixed `64 MB` autogrowth, not percent growth. Sample pre-cleanup files were 72 MB data / 200 MB log.
- The two owned evidence databases, server XEvent sessions, and evidence Host processes were removed. Residual evidence database/XEvent counts were `0 / 0`. The pre-existing Windows service `MesIngest` (`C:\MesIngest\service\MesIngest.Host.exe`) remained running and was not touched.

## Tests, review, and handoff

- Development ran only `ScaleAndQueryEvidenceGateTests`: final focused result `21 passed / 0 failed / 0 skipped`.
- The sole Tier 1 run used `dotnet test MesIngest.Tests` through `Invoke-RuntimeFeedbackTier1.ps1` from `mes/ingest/csharp`, with the explicit `LAB-WIN-01/master` real-SQL connection, expected/actual major `16`, and expected/actual compatibility `160`.
- Tier 1 result: `882 passed / 0 failed / 0 skipped / total 882`, exit code `0`, duration `11m05s`; VSTest/xUnit v2, SDK `8.0.424`.
- Tier 1 TRX SHA-256: `e2922066b447538f4f65999bb317aed5177c9c7362e538c604958cc4527a1d9e`; attestation SHA-256: `94cd712b7079a57f23689a85f1624d619cba33d92fd2956b266415bae732ab99`.
- The Tier 1 run created and removed all of its isolated databases. Five zero-session `MesIngest_Ticket01_*` databases already existed before its `2026-08-25T05:33:10+08:00` start (latest creation `03:04:40`) and were preserved as unrelated state; no new residual database remained.
- Final two-axis review after fixes: Standards `0` findings; Spec `0` findings; Ticket 28 scope diff `0`.
- No Watch UI/XAML change was made, so Tier 2/3 were not applicable and were not run.
- Human action: keep release blocked and authorize/schedule the recorded full 30-day validation before revisiting content addressing.
