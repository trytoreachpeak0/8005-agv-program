---
id: TC-117
type: test-case
title: "班组长决定硬件故障后的整批清空"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-117"]
---

# TC-117 班组长决定硬件故障后的整批清空

## Preconditions 前置条件

一个 LoadBatch 因目标仓位关键硬件反馈故障处于 VehicleRecoveryRequired；系统保留原 SlotOperationAttemptId、完整目标仓位、预留和逐仓事实。当前登录人具有 R-09 或被显式授予的等效生产管理权限。

## Test Steps 测试步骤

当前登录人在提交前再次刷卡或认证，选择 `HARDWARE_NOT_RECOVERABLE_ON_SITE` 或 `PRODUCTION_ABORTS_CURRENT_LOAD` 并可选填写备注，再以个人身份作出 LoadCompensationDecision，决定不再继续原装货并整批清空。

## Expected Result 预期结果

服务端核验本次有效二次认证、R-09 或等效生产管理权限和有效原因码后接受该业务决定，记录原因码及可选备注，并可将原 SlotOperationAttemptId 置为 LoadCompensationRequired；不得因决定本身自动开锁、清空或结束原任务。只有操作员随后发起补偿且服务端完成状态核验并明确授权后，才允许进入 LoadCompensationRecovery。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.4
