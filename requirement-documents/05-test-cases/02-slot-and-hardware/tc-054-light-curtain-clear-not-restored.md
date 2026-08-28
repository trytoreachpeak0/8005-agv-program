---
id: TC-054
type: test-case
title: "移除遮挡后光幕仍显示有遮挡，标记异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-018"]
related_uc: ["UC-016"]
aliases: ["TC-054"]
---

# TC-054 移除遮挡后光幕仍显示有遮挡，标记异常

## Preconditions 前置条件

遮挡阶段核验通过（光幕已正确变为"有遮挡"）。

## Test Steps 测试步骤

维护人员移除测试物体/遮挡后，系统读取的光幕状态仍显示"有遮挡"。

## Expected Result 预期结果

系统判定该仓位光幕异常（无法恢复检测为无遮挡），标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"。

## Verifies 验证对象

[[fr-018-slot-light-curtain-function-test|FR-018]] AC-4
