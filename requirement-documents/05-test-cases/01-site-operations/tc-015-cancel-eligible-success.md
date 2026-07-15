---
id: TC-015
type: test-case
title: "核验通过，取消并记录"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-015"]
---

# TC-015 核验通过，取消并记录

## Preconditions 前置条件

目标任务当前状态为"新建"或"进行中"，且该任务名下没有任何仓位处于"已占用"状态。

## Test Steps 测试步骤

操作员选中该任务并点击"取消运送"。

## Expected Result 预期结果

系统将该任务状态更新为"已取消"，从该站点待处理/可装载任务列表中移除，并记录本次取消操作（操作员、任务、子批号、时间戳）。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-1
