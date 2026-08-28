# 15 — 行级解析失败归类为 Incomplete

**What to build:** CSV/Oracle 快照中行级解析失败（如 `ParseDates` 抛错、空 `TASK_TYPE`）应得到 `SnapshotOutcomeKind.Incomplete` + `POLL_INCOMPLETE`（数据质量），不得经 runner catch-all 变成 `POLL_FAILURE`（链路失败）。缺列 Incomplete 已修好，本票补齐行级路径。

**Blocked by:** None — can start immediately（07 / 03 相关行为已落地；本票为 review Standards / Ticket 07 跟进）

**Status:** ready-for-human

- [x] `CsvFileMesSnapshotSource`：不可解析的 `DATES`、空/空白 `TASK_TYPE`（及同类行级硬失败）返回 `Incomplete`，不向外抛导致整轮 `POLL_FAILURE`
- [x] `OracleMesSnapshotSource`：同等行级硬失败与 CSV 分类一致（`Incomplete`，非链路 `Failure`）
- [x] `IngestRoundRunner`：Incomplete → `POLL_INCOMPLETE`、不变更 presence；真正的源/IO/超时仍为 `POLL_FAILURE`
- [x] 源与 runner 测试覆盖：坏日期行、空 TASK_TYPE → Incomplete / `POLL_INCOMPLETE`；缺列 Incomplete 回归仍绿

## Comments

- 2026-07-27: From `/code-review ffe1f49` Standards / README Ticket 07. Missing-column Incomplete already fixed in prior batch (`f920d01`). Remaining: `CsvFileMesSnapshotSource.ParseDates` throws `InvalidDataException`; empty TASK_TYPE not treated as Incomplete; runner catch-all maps exceptions to `POLL_FAILURE`. Spec story 45: incomplete/failed polls must not wrongly mutate presence; classification should separate data-quality from link failure.
- 2026-07-27: Implemented. CSV/Oracle row-level hard fails (bad DATES, blank TASK_TYPE/SUBLOT, short rows) return `Incomplete`; runner maps to `POLL_INCOMPLETE` without presence mutation. Full suite green (116 tests).
