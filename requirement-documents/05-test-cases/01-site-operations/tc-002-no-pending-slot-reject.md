---
id: TC-002
type: test-case
title: "有剩余任务时要求二次确认"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-003"]
related_uc: ["UC-002"]
aliases: ["TC-002"]
---

# TC-002 有剩余任务时要求二次确认

## Preconditions 前置条件

车辆满足 StationDepartureWaiting，当前仍有两个尚未开始的待装 DemandId。

## Test Steps 测试步骤

操作员点击“本站装货完成”，随后分别取消和确认二次提示。

## Expected Result 预期结果

界面明确显示将取消 2 个任务；取消提示时不结束本站，确认后才进入 FR-004。

## Verifies 验证对象

FR-003 AC-2
