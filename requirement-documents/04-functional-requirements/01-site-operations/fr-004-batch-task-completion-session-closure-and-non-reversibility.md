---
id: FR-004
type: functional-requirement
title: "Atomic Stop Closure and Departure Handoff 整站原子结束与发车交接"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-002", "UC-046"]
related_br: []
related_fr: ["FR-003", "FR-013", "FR-031"]
related_nfr: ["NFR-002"]
related_tc: ["TC-004", "TC-005", "TC-006", "TC-105", "TC-111", "TC-112"]
aliases: ["FR-004"]
---

# FR-004 Atomic Stop Closure and Departure Handoff 整站原子结束与发车交接

## Description 需求描述

FR-003 核验通过后，系统应将当前停靠终结、全部尚未开始待装 DemandId 的取消终态、取消抑制和审计作为一个不可分割的 StopClosureCommit。人工结束使用 `CANCELLED_BY_STOP_COMPLETE`，超时使用 `CANCELLED_BY_STATION_TIMEOUT`。提交时结束 OperationSession 并清除 OnboardOperatorContext；随后必须让车载采用最新作业与计划投影、通过 PreDepartureSafetyCheck，最后才可请求移动。

## Acceptance Criteria 验收标准

- **AC-1（原子提交）**
  - **Given** FR-003 核验通过
  - **When** 系统执行 StopClosureCommit
  - **Then** 本站终结、全部剩余任务终态、取消抑制和审计全部成功或全部回滚，不存在部分取消

- **AC-2（提交即结束会话）**
  - **Given** StopClosureCommit 成功
  - **When** RIoT 移动尚未开始或下发失败
  - **Then** OperationSession 已结束、OnboardOperatorContext 已清除，本站操作入口不重新开放

- **AC-3（发车交接顺序）**
  - **Given** StopClosureCommit 成功
  - **When** 系统准备发车
  - **Then** 车载先采用最新 CurrentStopWorklistSnapshot 和 UpcomingStopPlanSnapshot，再通过 PreDepartureSafetyCheck，最后才接收移动请求

- **AC-4（移动失败不撤销）**
  - **Given** StopClosureCommit 成功
  - **When** RIoT 移动请求失败
  - **Then** 本站结束和取消终态保持，系统进入等待发车重试并报警

## Related 关联

- **Use Cases：** [[uc-002-confirm-task-completion|UC-002]]、[[uc-046-handle-station-departure-wait-timeout|UC-046]]
- **Functional Requirements：** 前置 FR-003；会话规则 FR-013；自动触发 FR-031
- **Non-Functional Requirements：** 原子提交和业务审计满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

TC-004～TC-006、TC-105、TC-111、TC-112。

## Notes 备注

本 FR 原“批量确认任务完成”语义已被 LoadBatch 自动提交替代；保留 FR 编号以维持追溯链接。
