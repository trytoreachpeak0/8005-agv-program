---
id: TC-014
type: test-case
title: "关门后光幕检测残留，需重新打开"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-014"]
---

# TC-014 关门后光幕检测残留，需重新打开

## Preconditions 前置条件

操作员已关闭某仓位仓门，但光幕仍检测到产品残留。

## Test Steps 测试步骤

系统执行关门后核验。

## Expected Result 预期结果

系统不将该仓位回滚为"空闲"，提示该仓位取出未完成并要求操作员重新打开该仓位，直至光幕确认无残留后才允许回滚（对应 UC-005 Exception Flow E5.1）。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-6
