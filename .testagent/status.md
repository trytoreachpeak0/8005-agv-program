# Ticket 07 test-generation status

## Current state

- Research and requirement-to-test mapping complete.
- Six real SQL Server / production Host / formal API tracer tests are implemented and green.
- Ticket 07 production implementation is complete: per-WorkType policy, schema, atomic projection,
  GONE/archive authority filtering, focused v2 reads, and PollTrace decision evidence.
- Fixed review point: `112590abce17a245f69de1c5d596ac5191d167c1`.

## Requirement evidence

| Verbatim requirement | Evidence |
| --- | --- |
| 每个 WorkType 独立维护健康非零基线；某类型从健康非零结果骤降为零时进入 TaskTypeProtection/PausedZeroDrop，该轮及保护期间的成功空轮不能把该类型 Demand 标为 GONE 或推进归档。 | `Zero_drop_enters_protection_and_only_unprotected_work_type_marks_gone`; `Protected_gone_series_does_not_archive_while_other_work_type_can_archive` |
| 一个 WorkType 受保护时，其它 WorkType 仍按各自观测和缺席权威正常创建、更新或标记 GONE；保护状态、计数和恢复进度不得跨类型串扰。 | `Zero_drop_enters_protection_and_only_unprotected_work_type_marks_gone`; `Distinct_recognizable_keys_define_healthy_count_without_raw_duplicate_inflation` |
| 受保护类型连续两轮获得健康非零结果后才解除保护；第二轮只完成解除，下一轮完整结果才恢复该类型的缺席权威，不能在解除同轮自相矛盾地确认 GONE。 | `Two_nonzero_rounds_clear_protection_but_following_round_restores_authority_before_absence_can_mark_gone` |
| FAILURE、INCOMPLETE、幂等重放和内容冲突不建立健康基线、不推进连续恢复计数，也不解除保护；RestartBarrier 与类型保护同时存在时，只有两者都允许的轮次才具有缺席权威。 | `Failure_incomplete_replay_and_conflict_do_not_change_protection_recovery_or_events`; `Protection_progress_survives_restart_and_both_gates_must_allow_absence_authority` |
| 保护进入、每步恢复进度、解除和权威恢复都产生稳定事件，并作为当前 CurrentIngestAttention 与轮次证据由正式 API 查询；结束后不保留为当前项，但历史事实仍可追溯。 | `Zero_drop_enters_protection_and_only_unprotected_work_type_marks_gone`; `Two_nonzero_rounds_clear_protection_but_following_round_restores_authority_before_absence_can_mark_gone` |
| 保护状态和恢复进度在 Host 重启后保持，不能因进程重启提前获得缺席权威或丢失保护证据。 | `Protection_progress_survives_restart_and_both_gates_must_allow_absence_authority` |
| 真实 SQL Server → 正式 API 验收同时驱动至少两个 WorkType，证明目标类型进入保护、保护空轮不 GONE、其它类型继续对账、两轮非零恢复以及随后权威空轮才 GONE。 | `Invoke-Ticket07SqlServerGate.ps1`: 6 passed, 0 skipped on SQL Server 2022 / compatibility 160. |

## Verification

- Release solution build: 0 warnings, 0 errors.
- Ticket 07 SQL Server/API gate: 6 passed, 0 skipped.
- Ticket 01/02/05/06 SQL regression slice: 19 passed, 0 skipped.
- Full `MesIngest.Tests`: 542 passed, 19 legacy SQL tests skipped, 2 unrelated existing
  environment-sensitive WPF/telemetry failures; no Ticket 07 or changed-path failures.
- Two-axis review: Spec had no findings; Standards had two P3 smells, both resolved
  (removed unused event-order helper; reused a shared SQL-test environment scope).
