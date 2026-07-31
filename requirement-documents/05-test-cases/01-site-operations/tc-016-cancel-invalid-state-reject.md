---
id: TC-016
type: test-case
title: "已离站或不合法状态拒绝取消"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-016"]
---

# TC-016 已离站或不合法状态拒绝取消

## Preconditions 前置条件

车辆已离站，或目标 DemandId 已取消/处于不允许取消的终态。

## Test Steps 测试步骤

操作员点击"取消运送"。

## Expected Result 预期结果

服务端返回 REJECTED 与稳定原因码，不下发任何开锁；已离站装货问题引导异常卸出。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-9
