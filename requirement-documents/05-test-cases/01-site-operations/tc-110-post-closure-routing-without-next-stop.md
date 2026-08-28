---
id: TC-110
type: test-case
title: "整站结束后无下一站路由"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-041", "UC-046"]
aliases: ["TC-110"]
---

# TC-110 整站结束后无下一站路由

## Preconditions 前置条件

StopClosureCommit 已完成且 UpcomingStopPlan 为空。

## Test Steps 测试步骤

分别使用空载车辆和载有已提交 Sublot 的车辆执行后续路由。

## Expected Result 预期结果

空载车辆进入停车点分配/排队；载货车辆原地保持并产生调度计划异常告警，不自动前往停车点。

## Verifies 验证对象

FR-031 AC-11
