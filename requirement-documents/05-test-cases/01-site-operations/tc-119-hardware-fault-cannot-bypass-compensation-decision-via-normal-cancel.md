---
id: TC-119
type: test-case
title: "硬件故障不能通过普通取消绕过整批清空决定"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-119"]
---

# TC-119 硬件故障不能通过普通取消绕过整批清空决定

## Preconditions 前置条件

一个 LoadBatch 因目标仓位锁 DI 失效处于 VehicleRecoveryRequired，尚无 R-09 或等效生产管理权限作出的 LoadCompensationDecision；当前登录人只有普通生产操作权限。

## Test Steps 测试步骤

当前登录人从 CurrentStopWorklist 对该 DemandId 发起普通“清空并取消”请求。

## Expected Result 预期结果

服务端拒绝普通取消并返回稳定原因码，不进入 LoadCancelPending，不下发任何开锁指令，也不改变原 LoadBatch 的业务目标。界面引导等待 R-09 或等效生产管理权限作出 LoadCompensationDecision，再进入专用补偿恢复。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-10
