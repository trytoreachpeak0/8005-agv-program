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

- Source commit at build: `6a5a3c28f601641396671099fc967c272701a6e8` (`sourceDirty=true` for this Ticket 27 implementation).
- Host SHA-256: `c70c8b35ac1c91f3c27502323d752a58e1e72961bc2ab956853935af3895d67d`.
- Final package manifest SHA-256: `2be5aca3aac5ae9fa105ae89834eff49077bb013fbf90916d9f6b3ec46809088` (1,372 files).
- Contract/schema: `2026.08.new-mes-ingest.v2.1` / `28`.
- Baseline run: `scale-20260824T211035Z-789c6a25`; HistoryEpoch `C372EB42-8A5F-424A-88A2-2C34B92808EA`.
- Sample run: `scale-20260824T211104Z-d5062cd5`; HistoryEpoch `4CA1B89E-F502-44CE-8174-9A305E24F342`.
- SQL data source / `SERVERPROPERTY(ServerName)`: `LAB-WIN-01`; Windows default-instance service: `MSSQLSERVER`; product `16.0.1190.2`, major `16`, Enterprise Evaluation, compatibility `160`, not LocalDB.
- Recovery/configuration: `SIMPLE`, max server memory `1536 MB`, final `log_reuse_wait_desc=NOTHING`.
- Fixed distribution: seed `8005`, 14 seconds/round, 600 observations/round, 600 Series, 70% active, 30% archived, 10% active errors; `RoundBatchSize=100`.
- Query evidence: DemandSeries surface, 1 warmup and 3 measurements, 357 actual plans, 84 statement metrics.

The full raw reports and actual ShowPlan XML are retained locally under
`mes/ingest/csharp/.artifacts/ticket27-fast-capacity-2026-08-25/`. The final baseline/sample JSON
SHA-256 values are `a9337e24ea67088dbdcb3d5ca9c9c507c79fa7c453766e8dca2bb311834ca053` and
`855f5a0f5c1805a7449c344dcbbb6ded8c0025a9cd629a78b83bbe766fff1ede`.

## Model and thresholds

Inputs and formula:

- Baseline logical used: `1.960935 MB`; sample logical used: `38.328120 MB`; observed growth: `36.367185 MB`.
- Observed growth: `0.087631771 MB/round` and `0.000146052952 MB/row` (about `153.15 bytes/row`).
- Target: `floor(30*86400/14) = 185,142` rounds and `111,085,200` rows.
- Logical formula: `(baselineLogicalMb + logicalMbPerRound * targetRounds) * 1.30`.
- Physical formula: `ceil(projectedLogicalUsedMb / 64 MB fixed autogrowth) * 64 MB`.
- LDF formula under SIMPLE: `max(sample LDF, load/query/cleanup physical LDF peak, used-log peak) * 1.30`.
- Linearity rule: at least four checkpoints and maximum/minimum positive segment rate no greater than `1.20`; observed `2.427779815`.

| Axis | 30-day +30% prediction | Final limit | 70% escalation point | Decision |
| --- | ---: | ---: | ---: | --- |
| Logical used | `21,094.167 MB` (`20.600 GiB`) | `12,288 MB` | `8,601.6 MB` | fail/escalate |
| Physical data files | `21,120 MB` (`20.625 GiB`) | `16,384 MB` | `11,468.8 MB` | fail/escalate |
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
- Active graph before and after was identical: 420 Series, 420 demands, 480 events, 60 current conditions, zero split Series.
- LDF grew from the 8 MB baseline to 200 MB during load/query and 263.992 MB after cleanup; incremental physical peak `255.992 MB`, peak used log `43.773 MB`, final reuse wait `NOTHING`.
- Database version-store peak: `136.25 MB`; tempdb version-store peak: `138.6875 MB`. Through query evidence, tempdb user-object delta was `0 MB` and internal-object delta was `+0.0625 MB` (shared-instance snapshots are retained in the raw report).
- Data and log files both used fixed `64 MB` autogrowth, not percent growth. Sample pre-cleanup files were 72 MB data / 200 MB log.
- The two owned evidence databases, server XEvent sessions, and evidence Host processes were removed. Residual evidence database/XEvent counts were `0 / 0`. The pre-existing Windows service `MesIngest` (`C:\MesIngest\service\MesIngest.Host.exe`) remained running and was not touched.
