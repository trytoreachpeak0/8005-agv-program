---
id: TC-045
type: test-case
title: "禁用核验不通过，跳过"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-016"]
related_uc: ["UC-014"]
aliases: ["TC-045"]
---

# TC-045 禁用核验不通过，跳过

## Preconditions 前置条件

目标仓位当前状态为"已占用（Occupied）"或"异常锁定"。

## Test Steps 测试步骤

操作人员点击"禁用"。

## Expected Result 预期结果

系统跳过该仓位的禁用操作，提示"禁用失败：当前非空闲状态"；本次请求中其余满足条件的仓位不受影响，仍按计划继续禁用。

## Verifies 验证对象

[[fr-016-slot-enable-disable-batch-eligibility-and-state-update|FR-016]] AC-2
