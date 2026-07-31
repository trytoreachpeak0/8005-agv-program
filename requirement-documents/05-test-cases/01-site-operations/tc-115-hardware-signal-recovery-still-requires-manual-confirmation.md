---
id: TC-115
type: test-case
title: "硬件信号恢复后仍需人工确认和服务端授权"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-115"]
---

# TC-115 硬件信号恢复后仍需人工确认和服务端授权

## Preconditions 前置条件

一个 LoadBatch 因原目标仓位的锁 DI 失效进入 VehicleRecoveryRequired；系统保留原目标仓位、原 SlotOperationAttemptId、预留和逐仓事实。维护后通信、锁 DI、光幕和开锁输出回读均恢复有效，实时状态可唯一解释。执行确认的登录人具有 R-11 或被显式授予的等效维护权限。

## Test Steps 测试步骤

1. 在尚未提交人工硬件恢复确认时观察系统行为。
2. 授权维护人员以个人身份提交 HardwareRecoveryConfirmation，但暂不下发服务端续行授权。
3. 服务端核验物理状态和人工确认后，明确授权原操作继续。

## Expected Result 预期结果

步骤 1 和步骤 2 均不得触发自动开锁或自动续行。确认记录包含确认人、时间、车辆、仓位和故障原因。只有步骤 3 后，车载端才可在原目标仓位、原 LoadBatch、原 SlotOperationAttemptId 上继续；不得换仓、不得创建新的装货尝试，也不得重新打开已经完成的仓位。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.2
