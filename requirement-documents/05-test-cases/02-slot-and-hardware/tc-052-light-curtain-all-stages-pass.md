---
id: TC-052
type: test-case
title: "三阶段核验均通过，记录正常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-018"]
related_uc: ["UC-016"]
aliases: ["TC-052"]
---

# TC-052 三阶段核验均通过，记录正常

## Preconditions 前置条件

目标仓位仓门已开启，测试开始前光幕状态确为"无遮挡"。

## Test Steps 测试步骤

维护人员依次放入测试物体/遮挡光幕、再移除测试物体/遮挡，系统分别读取到光幕状态正确变为"有遮挡"、再恢复"无遮挡"。

## Expected Result 预期结果

系统记录本次测试结果为"正常"（维护人员、仓位号、时间戳）。

## Verifies 验证对象

[[fr-018-slot-light-curtain-function-test|FR-018]] AC-2
