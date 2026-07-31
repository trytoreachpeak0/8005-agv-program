---
id: TC-122
type: test-case
title: "整批清空决定必须选择受控原因码"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-122"]
---

# TC-122 整批清空决定必须选择受控原因码

## Preconditions 前置条件

一个 LoadBatch 因关键硬件故障处于 VehicleRecoveryRequired；R-09 或等效生产管理权限已通过本次即时二次认证。

## Test Steps 测试步骤

1. 不选择原因码，仅填写自由文本备注后提交 LoadCompensationDecision。
2. 选择未知原因码后提交。
3. 分别选择 `HARDWARE_NOT_RECOVERABLE_ON_SITE`、`PRODUCTION_ABORTS_CURRENT_LOAD`，备注留空后提交。
4. 选择 `OTHER`、备注留空后提交。
5. 选择 `OTHER` 并填写非空备注后提交。

## Expected Result 预期结果

步骤 1、步骤 2 和步骤 4 均被拒绝，不生成 LoadCompensationDecision，不进入 LoadCompensationRequired。步骤 3 和步骤 5 允许提交并准确记录原因码与备注；接受决定本身仍不得自动开锁。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.7
