---
id: TC-010
type: test-case
title: "纠错只打开原仓位"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-010"]
---

# TC-010 纠错只打开原仓位

## Preconditions 前置条件

AGV 未移动；FR-005 已授权一个已锁闭原仓位，当前 SUBLOT 还有其它已装或待装仓位。

## Test Steps 测试步骤

车载端执行 LoadCorrection 开锁。

## Expected Result 预期结果

系统只打开所选原仓位，暂停后续装货，不打开同一 SUBLOT 的其它仓位。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-2
