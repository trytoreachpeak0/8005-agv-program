---
id: FR-006
type: functional-requirement
title: "Same-Slot Load Correction and Pending Recovery 原仓位装货纠错与待重放恢复"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-005", "UC-004", "UC-006"]
related_br: []
related_fr: ["FR-005", "FR-031"]
related_nfr: ["NFR-002"]
related_tc: ["TC-009", "TC-010", "TC-011", "TC-012", "TC-013", "TC-014"]
aliases: ["FR-006"]
---

# FR-006 Same-Slot Load Correction and Pending Recovery 原仓位装货纠错与待重放恢复

## Description 需求描述

FR-005 授权后，车载端只打开所选原仓位，要求操作员完成 `OCCUPIED → EMPTY → OCCUPIED`，并在有效锁闭反馈后以稳定光幕状态和开锁输出复位证明纠错成功。正确产品必须放回原仓位；原任务、SUBLOT、DemandId、SlotOperationAttemptId、目标仓位集合、预留与仓位映射均不改变。

错误产品已取出但正确产品暂时不可得时，系统进入 LoadCorrectionPending，允许安全锁闭空仓，但不得视为成功或继续后续装货。该状态只允许原仓位继续重放，或转 FR-007 清空并取消。

## Acceptance Criteria 验收标准

- **AC-1（移动或安全联锁阻断）**
  - **Given** FR-005 已授权，但 AGV 正在移动或安全联锁不允许开锁
  - **When** 车载端准备打开纠错仓位
  - **Then** 不输出开锁并保持当前任务与预留

- **AC-2（只打开原仓位）**
  - **Given** 安全联锁通过
  - **When** 执行 LoadCorrection
  - **Then** 退出 StationDepartureWaiting、停止离站倒计时，只打开操作员选择的原仓位，不打开同一 SUBLOT 的其它仓位，后续装货暂停

- **AC-3（原仓位重放成功）**
  - **Given** 操作员从原仓位取出错误产品并把正确产品放回
  - **When** 仓门锁闭反馈有效，光幕稳定为 OCCUPIED 且开锁输出已复位
  - **Then** 可靠记录 LoadCorrectionResult；仓位—SUBLOT 映射和既有 LoadBatch 提交事实不变，恢复剩余装货或重新进入 StationDepartureWaiting 并从完整时长计时

- **AC-4（正确产品暂时不可得）**
  - **Given** 错误产品已取出，原仓位锁闭后为 EMPTY
  - **When** 操作员暂时无法放入正确产品
  - **Then** 进入 LoadCorrectionPending；保持任务、SUBLOT、预留与 StationOperationGuard，禁止后续仓位装货

- **AC-5（待重放的合法出口）**
  - **Given** 当前为 LoadCorrectionPending
  - **When** 操作员继续处理
  - **Then** 只允许重新打开原仓位完成重放，或转 FR-007 清空并取消；不得跳过该仓位

- **AC-6（目标态闭环）**
  - **Given** 纠错仓位锁闭后仍为 EMPTY
  - **When** 车载端取得明确有效的占用状态
  - **Then** 自动再次弹锁并要求放入，且不设强制放行次数上限；若状态为 UNKNOWN 或机构状态无效，则暂停进入恢复而非自动循环

## Related 关联

- **Use Cases：** [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]
- **Functional Requirements：** 前置授权依赖 [[fr-005-mis-stored-retrieval-eligibility-check|FR-005]]；放弃装货转 [[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]]
- **Non-Functional Requirements：** 纠错、待重放与恢复记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-009|TC-009]]：移动联锁拒绝纠错开锁
- [[TC-010|TC-010]]：只打开原仓位
- [[TC-011|TC-011]]：原仓位重放成功
- [[TC-012|TC-012]]：正确产品不可得进入待重放
- [[TC-013|TC-013]]：待重放只允许继续或取消
- [[TC-014|TC-014]]：目标态不符自动弹锁，UNKNOWN 暂停

## Notes 备注

- 支持反复纠错，不限制业务次数；每次都使用新的 MessageId，但保持原 SlotOperationAttemptId。
- LoadCorrection 不是整批清空，也不清除仓位—SUBLOT 映射。
