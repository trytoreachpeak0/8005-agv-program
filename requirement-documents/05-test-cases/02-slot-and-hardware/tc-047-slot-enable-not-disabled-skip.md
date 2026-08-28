---
id: TC-047
type: test-case
title: "启用核验不通过，跳过"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-016"]
related_uc: ["UC-014"]
aliases: ["TC-047"]
---

# TC-047 启用核验不通过，跳过

## Preconditions 前置条件

目标仓位当前并非"已禁用"状态。

## Test Steps 测试步骤

操作人员点击"启用"。

## Expected Result 预期结果

系统跳过该仓位的启用操作，提示"无需启用：当前并非禁用状态"；本次请求中其余满足条件的仓位不受影响，仍按计划继续启用。

## Verifies 验证对象

[[fr-016-slot-enable-disable-batch-eligibility-and-state-update|FR-016]] AC-4
