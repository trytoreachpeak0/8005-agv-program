---
id: TC-015
type: test-case
title: "未装货任务直接取消"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-015"]
---

# TC-015 未装货任务直接取消

## Preconditions 前置条件

目标 DemandId 尚未产生物理装载，车辆未离站且没有其它活动物理仓位操作。

## Test Steps 测试步骤

操作员从 CurrentStopWorklist 选择该任务并确认“清空并取消”。

## Expected Result 预期结果

服务端授权空范围；车载端报告 ALL_EMPTY；服务端完成取消、记录操作并发布新版 CurrentStopWorklistSnapshot。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-1
