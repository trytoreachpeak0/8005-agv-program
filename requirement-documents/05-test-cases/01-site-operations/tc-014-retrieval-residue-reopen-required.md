---
id: TC-014
type: test-case
title: "纠错目标态不符自动弹锁"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-014"]
---

# TC-014 纠错目标态不符自动弹锁

## Preconditions 前置条件

纠错重放要求 OCCUPIED；操作员关闭原仓门后，锁闭反馈有效但光幕稳定为 EMPTY。

## Test Steps 测试步骤

系统执行仓位目标态闭环。

## Expected Result 预期结果

系统自动再次输出开锁脉冲弹开原仓门并提示放入正确产品，不设强制放行次数上限；若光幕为 UNKNOWN，则暂停恢复而不自动循环。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-6
