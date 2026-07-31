---
id: FR-013
type: functional-requirement
title: "Session Termination Rules 会话结束、换人与持久化规则"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-043", "UC-002", "UC-006", "UC-046"]
related_br: []
related_fr: ["FR-004", "FR-011", "FR-012", "FR-031"]
related_nfr: ["NFR-002"]
related_tc: ["TC-034", "TC-035", "TC-036", "TC-037", "TC-111", "TC-112"]
aliases: ["FR-013"]
---

# FR-013 Session Termination Rules 会话结束、换人与持久化规则

## Description 需求描述

活动或未收敛仓位操作中的 OperationSession 和车载当前工号不因空闲、掉线或重启自动清除。取消单个任务和完成单个 Sublot 也不结束会话；用户只有在不存在活动或未收敛 Sublot 时才能主动更换工号。人工或超时 StopClosureCommit 成功时立即结束到站操作会话并清除工号，不等待车辆实际开始移动。

暂停中的 Sublot 和执行日志不得由维护人员在车载端强制清除。必须重连对账，由服务端决定继续、终止或进入人工补偿。

## Acceptance Criteria 验收标准

- **AC-1（未收敛操作不自动结束）**
  - **Given** 存在活动、部分或待恢复的 Sublot
  - **When** 操作长时间无进展、掉线或车载重启
  - **Then** 工号、活动 Sublot 和执行日志保持，不以 StationDepartureWaitTimeout 结束
- **AC-2（Sublot 完成后可换人）**
  - **Given** 当前不存在活动、部分或未收敛的 Sublot
  - **Then** 用户可以主动更换工号，新工号必须重新校验
- **AC-3（StopClosureCommit 清除）**
  - **When** 人工或超时 StopClosureCommit 成功
  - **Then** 立即结束到站操作会话并清除车载工号，即使后续移动失败也不恢复
- **AC-4（禁止本地强制清除）**
  - **Given** 存在暂停或未结 Sublot
  - **Then** 维护人员可以查看和排障，但不能删除恢复记录

## Notes 备注

- UC-002 人工结束和 UC-046 自动超时均通过 StopClosureCommit 清除会话。
- 取消任务不结束到站会话；用户可能继续处理其它 Sublot。
