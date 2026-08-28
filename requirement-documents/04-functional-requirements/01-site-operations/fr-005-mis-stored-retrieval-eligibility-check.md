---
id: FR-005
type: functional-requirement
title: "Load Correction Eligibility and Authorization 装货纠错资格核验与授权"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-005"]
related_br: []
related_fr: ["FR-006"]
related_nfr: ["NFR-002"]
related_tc: ["TC-007", "TC-008"]
aliases: ["FR-005"]
---

# FR-005 Load Correction Eligibility and Authorization 装货纠错资格核验与授权

## Description 需求描述

系统应在操作员对当前 SUBLOT 的已锁闭仓位发起“取出重放”时，核验 StopClosureCommit 尚未发生、所选仓位属于该 SUBLOT 的目标范围且实时为 OCCUPIED、当前操作员有效，并且同车没有另一 SUBLOT 的活动物理仓位操作。LoadBatch 可以尚未提交或已经自动提交。通过后，服务端必须在原 SlotOperationAttemptId 下授权单仓 LoadCorrection；不得把纠错扩大为整批取空，也不得改变任务、目标仓位或既有提交事实。

当前仓门尚未锁闭时的取出重放属于原仓位操作，不另发 LoadCorrectionCommand。StopClosureCommit 后拒绝普通纠错，即使车辆因发车失败仍在原地也不重新开放；车辆已离站时转异常卸出流程。

## Rationale 制定原因

花篮没有独立身份，放错只能由操作员指出具体物理仓位。以原仓位单仓纠错可以保持 LoadBatch 的目标集合和恢复边界，同时避免为了一个放错产品清空整个 SUBLOT。

## Acceptance Criteria 验收标准

- **AC-1（已锁闭原仓位纠错获授权）**
  - **Given** StopClosureCommit 尚未发生，所选仓位属于当前 SUBLOT、实时为 OCCUPIED，且没有另一 SUBLOT 的活动物理操作
  - **When** 已核验操作员发起“取出重放”
  - **Then** 服务端在原 SlotOperationAttemptId 下授权只包含该原仓位的 LoadCorrection，并暂停后续装货仓位

- **AC-2（不满足资格时拒绝并给出合法出口）**
  - **Given** StopClosureCommit 已发生、车辆已离站、所选仓位不属于当前 SUBLOT、状态不是 OCCUPIED，或另一 SUBLOT 正在执行物理操作
  - **When** 操作员请求 LoadCorrection
  - **Then** 服务端拒绝且不打开仓门；StopClosureCommit 已发生时不重新开放本站，已离站时引导异常卸出

## Related 关联

- **Use Cases：** [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]
- **Functional Requirements：** 授权后由 [[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] 执行原仓位纠错
- **Non-Functional Requirements：** 授权与拒绝均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-007|TC-007]]：原仓位纠错资格通过
- [[TC-008|TC-008]]：已提交、已离站或其它不合法状态拒绝

## Notes 备注

- 本 FR 不要求班组长审批或填写纠错原因。
- 当前仓门尚未锁闭时直接在原操作内更换，不属于本 FR 的服务端授权分支。
