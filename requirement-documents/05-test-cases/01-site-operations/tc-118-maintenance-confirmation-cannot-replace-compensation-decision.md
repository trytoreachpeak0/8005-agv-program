---
id: TC-118
type: test-case
title: "维护确认不能代替整批清空决定"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-118"]
---

# TC-118 维护确认不能代替整批清空决定

## Preconditions 前置条件

一个 LoadBatch 因目标仓位关键硬件反馈故障处于 VehicleRecoveryRequired；准备三个个人账号：仅有 R-11 维护权限的账号、仅有普通生产操作权限的账号，以及同时具有 R-11 与 R-09 两项独立权限的兼任账号。

## Test Steps 测试步骤

1. 仅有 R-11 维护权限的账号提交 HardwareRecoveryConfirmation 后，尝试作出 LoadCompensationDecision。
2. 仅有普通生产操作权限的账号申请并尝试作出 LoadCompensationDecision。
3. 兼任账号先以 R-11 权限提交 HardwareRecoveryConfirmation，再为整批清空决定完成即时二次认证，并以 R-09 权限作出 LoadCompensationDecision。

## Expected Result 预期结果

步骤 1 和步骤 2 的 LoadCompensationDecision 均被拒绝，系统保持原业务目标且不得进入 LoadCompensationRequired；其中有效的 HardwareRecoveryConfirmation 只证明设备状态。步骤 3 的两项动作分别通过各自权限核验，且 LoadCompensationDecision 关联本次有效二次认证，形成两个独立事实；系统不得把其中任一动作自动推导为另一动作。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.5
