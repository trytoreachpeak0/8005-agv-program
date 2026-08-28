---
id: TC-046
type: test-case
title: "启用核验通过，状态更新"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-016"]
related_uc: ["UC-014"]
aliases: ["TC-046"]
---

# TC-046 启用核验通过，状态更新

## Preconditions 前置条件

目标仓位当前状态为"已禁用（Disabled）"。

## Test Steps 测试步骤

操作人员点击"启用"。

## Expected Result 预期结果

系统将该仓位状态恢复为"空闲（Idle）"，清除禁用标记，重新可被 UC-001 分配使用。

## Verifies 验证对象

[[fr-016-slot-enable-disable-batch-eligibility-and-state-update|FR-016]] AC-3
