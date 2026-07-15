---
id: TC-017
type: test-case
title: "任务已装载仓位，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-017"]
---

# TC-017 任务已装载仓位，拒绝

## Preconditions 前置条件

目标任务名下已有一个或多个仓位处于"已占用"状态。

## Test Steps 测试步骤

操作员点击"取消运送"。

## Expected Result 预期结果

系统拒绝本次取消请求，提示"该任务已装载产品，不能直接取消"（对应 UC-006 Exception Flow E2.2）。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-3
