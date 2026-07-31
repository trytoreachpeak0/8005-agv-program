---
id: FR-003
type: functional-requirement
title: "Stop Closure Eligibility Check 本站结束资格核验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-002", "UC-046"]
related_br: []
related_fr: ["FR-004", "FR-031"]
related_nfr: ["NFR-002"]
related_tc: ["TC-001", "TC-002", "TC-003"]
aliases: ["FR-003"]
---

# FR-003 Stop Closure Eligibility Check 本站结束资格核验

## Description 需求描述

系统应在人工或超时结束本站前，以服务端权威状态核验车辆确实处于 StationDepartureWaiting：当前站允许继续装货、没有必须完成的卸货、活动或未收敛仓位操作，车载业务就绪，当前作业与计划投影为最新，且 DepartureSafe 有效。人工结束还必须重新核验操作员身份；有剩余待装任务时必须向操作员明确数量并取得二次确认。

## Acceptance Criteria 验收标准

- **AC-1（无剩余任务可直接结束）**
  - **Given** 车辆满足 StationDepartureWaiting、人工身份有效且无剩余待装任务
  - **When** 操作员请求结束本站
  - **Then** 资格核验通过，无需剩余任务二次确认

- **AC-2（有剩余任务要求二次确认）**
  - **Given** 车辆满足 StationDepartureWaiting 且仍有 N 个尚未开始的待装 DemandId
  - **When** 操作员请求结束本站
  - **Then** 系统显示 N 和取消影响，只有二次确认后才允许进入 FR-004

- **AC-3（未收敛或状态不明时拒绝）**
  - **Given** 存在待卸任务、部分 LoadBatch、LoadCorrectionPending、活动仓位操作、断联、过期投影或 DepartureSafe 无效
  - **When** 人工或超时尝试结束本站
  - **Then** 系统拒绝 StopClosureCommit，返回或记录明确阻断原因

## Related 关联

- **Use Cases：** [[uc-002-confirm-task-completion|UC-002]]、[[uc-046-handle-station-departure-wait-timeout|UC-046]]
- **Functional Requirements：** 核验通过后由 FR-004 执行原子提交；自动计时条件由 FR-031 规定
- **Non-Functional Requirements：** 核验与拒绝原因满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

TC-001～TC-003。

## Notes 备注

本 FR 原“任务确认完成”语义已被 ADR-cross-0054 的 LoadBatch 自动提交和 ADR-cross-0055 的 StopClosureCommit 替代；保留 FR 编号以维持追溯链接。
