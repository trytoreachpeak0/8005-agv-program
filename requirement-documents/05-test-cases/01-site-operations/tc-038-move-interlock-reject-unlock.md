---
id: TC-038
type: test-case
title: "移动联锁拒绝开锁"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-014"]
related_uc: ["UC-044", "UC-004"]
aliases: ["TC-038"]
---

# TC-038 移动联锁拒绝开锁

## Preconditions 前置条件

目标仓位处于"仓门已关闭，但光幕检测到残留产品"的异常状态，且按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 判定该 AGV 当前处于移动状态。

## Test Steps 测试步骤

系统准备下发重新开锁指令。

## Expected Result 预期结果

系统拒绝本次开门/开锁，不得下发开锁指令。

## Verifies 验证对象

[[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]] AC-1
