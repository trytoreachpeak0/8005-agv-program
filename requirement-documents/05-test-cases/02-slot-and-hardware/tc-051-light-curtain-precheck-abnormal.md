---
id: TC-051
type: test-case
title: "测试开始前光幕状态异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-018"]
related_uc: ["UC-016"]
aliases: ["TC-051"]
---

# TC-051 测试开始前光幕状态异常

## Preconditions 前置条件

目标仓位仓门已开启，仓位内实际为空。

## Test Steps 测试步骤

系统读取该仓位光幕状态显示为"有遮挡"，且清空仓位后仍显示"有遮挡"。

## Expected Result 预期结果

系统判定该仓位光幕异常，标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"。

## Verifies 验证对象

[[fr-018-slot-light-curtain-function-test|FR-018]] AC-1
