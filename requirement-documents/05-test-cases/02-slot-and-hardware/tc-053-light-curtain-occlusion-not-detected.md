---
id: TC-053
type: test-case
title: "遮挡后光幕仍显示无遮挡，标记异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-018"]
related_uc: ["UC-016"]
aliases: ["TC-053"]
---

# TC-053 遮挡后光幕仍显示无遮挡，标记异常

## Preconditions 前置条件

测试开始前光幕状态核验通过（"无遮挡"）。

## Test Steps 测试步骤

维护人员放入测试物体/遮挡光幕后，系统读取的光幕状态仍显示"无遮挡"。

## Expected Result 预期结果

系统判定该仓位光幕异常（检测不到遮挡），标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"。

## Verifies 验证对象

[[fr-018-slot-light-curtain-function-test|FR-018]] AC-3
