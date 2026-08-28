---
id: TC-044
type: test-case
title: "禁用核验通过，状态更新"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-016"]
related_uc: ["UC-014"]
aliases: ["TC-044"]
---

# TC-044 禁用核验通过，状态更新

## Preconditions 前置条件

目标仓位当前状态为"空闲（Idle）"。

## Test Steps 测试步骤

操作人员点击"禁用"。

## Expected Result 预期结果

系统将该仓位状态置为"已禁用（Disabled）"，不再出现在 UC-001 分配空闲仓位时的可选范围内。

## Verifies 验证对象

[[fr-016-slot-enable-disable-batch-eligibility-and-state-update|FR-016]] AC-1
