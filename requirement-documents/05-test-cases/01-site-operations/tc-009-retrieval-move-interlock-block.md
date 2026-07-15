---
id: TC-009
type: test-case
title: "移动联锁拒绝开锁"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005", "UC-004"]
aliases: ["TC-009"]
---

# TC-009 移动联锁拒绝开锁

## Preconditions 前置条件

已通过 FR-005 核验；按 UC-004 Flow A 判定 AGV 当前处于移动状态。

## Test Steps 测试步骤

系统准备下发批量开锁指令。

## Expected Result 预期结果

系统拒绝本次开门/开锁，不下发开锁指令（对应 UC-004 Exception Flow EA1.1）。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-1
