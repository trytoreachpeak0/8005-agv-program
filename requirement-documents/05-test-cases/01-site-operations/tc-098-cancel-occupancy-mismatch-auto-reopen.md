---
id: TC-098
type: test-case
title: "取消清空占用不符自动重开"
status: draft
created: 2026-07-30
updated: 2026-07-30
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-098"]
---

# TC-098 取消清空占用不符自动重开

## Preconditions 前置条件

某取消目标仓位要求 EMPTY；操作员关门后锁闭反馈有效，但光幕稳定为 OCCUPIED。

## Test Steps 测试步骤

车载端执行取消清空目标态闭环。

## Expected Result 预期结果

系统自动再次弹开该仓门并提示继续取出，不设强制放行次数上限；状态为 UNKNOWN 时暂停恢复，不自动循环。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-4

