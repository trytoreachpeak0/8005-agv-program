---
id: FR-005
type: functional-requirement
title: "Mis-Stored Retrieval Eligibility Check 存错取出资格核验"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-005"]
related_br: []
related_fr: ["FR-006"]
related_nfr: ["NFR-002"]
related_tc: ["TC-007", "TC-008"]
aliases: ["FR-005"]
---

# FR-005 Mis-Stored Retrieval Eligibility Check 存错取出资格核验

## Description 需求描述

系统应当在操作员选择某子批号发起"取出"请求后，核验该子批号关联的全部仓位是否均为"已占用"状态，且对应任务尚未通过 [[uc-002-confirm-task-completion|UC-002]] 确认完成。核验不通过时，系统必须拒绝本次取出请求，不进入批量开锁（批量开锁与回滚能力见 [[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]]）。

## Rationale 制定原因

防止对未占用仓位或已确认完成的任务发起纠错取出，避免破坏已经终态化的任务数据一致性；将 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] Normal Flow 2.1 步的系统核验点落实为可单独验收的能力。

## Origin 需求来源

- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] Normal Flow 第 2.1 步及 Exception Flow E2.1

## Acceptance Criteria 验收标准

- **AC-1（资格核验通过）**
  - **Given** 目标子批号关联的全部仓位当前状态均为"已占用"，且其关联任务尚未通过 UC-002 确认完成
  - **When** 操作员选择该子批号发起"取出"请求
  - **Then** 系统判定核验通过，进入批量开锁（见 FR-006）

- **AC-2（资格核验不通过，拒绝）**
  - **Given** 目标子批号关联的仓位中存在非"已占用"状态的仓位，或该子批号对应任务已通过 UC-002 确认完成
  - **When** 操作员发起"取出"请求
  - **Then** 系统拒绝本次取出请求，提示"当前不可取出"

## Related 关联

- **Use Cases：** 派生自 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]（取出前的系统核验点）；与 [[uc-002-confirm-task-completion|UC-002]] 的"已确认完成"状态互斥
- **Business Rules：** 无
- **Functional Requirements：** 核验通过后由 [[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] 承接批量开锁与回滚
- **Non-Functional Requirements：** 核验通过与拒绝结果均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]] 的关键操作可审计要求

## Verification 验证方式

- [[TC-007|TC-007]]：资格核验通过
- [[TC-008|TC-008]]：资格核验不通过，拒绝

## Notes 备注

- 本 FR 以"子批号"为最小操作单位：该子批号关联的全部仓位（可能一个或多个）作为一个整体参与核验，不支持只核验/取出其中部分仓位。
- 本操作不需要班组长审批（见 UC-005 Precondition 备注），核验通过后操作员可自行继续。
