---
id: TC-001
type: test-case
title: "无剩余任务时本站结束资格通过"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-003"]
related_uc: ["UC-002"]
aliases: ["TC-001"]
---

# TC-001 无剩余任务时本站结束资格通过

## Preconditions 前置条件

车辆满足 StationDepartureWaiting，操作员身份有效，当前无剩余待装任务。

## Test Steps 测试步骤

操作员点击“本站装货完成”。

## Expected Result 预期结果

系统核验通过，无需显示剩余任务二次确认，进入 FR-004。

## Verifies 验证对象

FR-003 AC-1
