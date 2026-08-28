---
id: TC-004
type: test-case
title: "整站结束原子提交"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-004"]
related_uc: ["UC-002", "UC-046"]
aliases: ["TC-004"]
---

# TC-004 整站结束原子提交

## Preconditions 前置条件

FR-003 核验通过，本站有多个尚未开始的待装任务。

## Test Steps 测试步骤

分别执行正常提交，并在其中一个取消记录写入时注入失败。

## Expected Result 预期结果

正常时本站、全部任务终态、取消抑制和审计一起提交；故障时全部回滚。

## Verifies 验证对象

FR-004 AC-1
