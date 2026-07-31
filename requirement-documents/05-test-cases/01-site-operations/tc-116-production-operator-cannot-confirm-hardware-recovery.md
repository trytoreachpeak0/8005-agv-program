---
id: TC-116
type: test-case
title: "普通生产操作员不能确认硬件恢复"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-116"]
---

# TC-116 普通生产操作员不能确认硬件恢复

## Preconditions 前置条件

一个 LoadBatch 因目标仓位的锁 DI 失效进入 VehicleRecoveryRequired；当前登录人只有普通生产操作权限，没有 R-11 或等效维护权限。

## Test Steps 测试步骤

当前登录人尝试提交 HardwareRecoveryConfirmation。

## Expected Result 预期结果

系统拒绝提交，不生成有效的 HardwareRecoveryConfirmation，并保持 VehicleRecoveryRequired；不得发送开锁或续行指令。拒绝行为记录当前人员、时间、车辆、仓位和失败原因。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.3
