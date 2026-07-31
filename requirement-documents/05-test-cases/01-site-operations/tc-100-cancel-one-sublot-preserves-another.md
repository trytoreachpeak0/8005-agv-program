---
id: TC-100
type: test-case
title: "取消一个 SUBLOT 保留另一个"
status: draft
created: 2026-07-30
updated: 2026-07-30
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-100"]
---

# TC-100 取消一个 SUBLOT 保留另一个

## Preconditions 前置条件

SUBLOT-A 已装入仓位 1、2，SUBLOT-B 已装入仓位 3、4；两批均处于稳定状态，车辆未离站。

## Test Steps 测试步骤

操作员选择 A 的 DemandId，执行“清空并取消”。

## Expected Result 预期结果

系统只批量打开并清空仓位 1、2；B 的仓位 3、4、任务、确认记录与业务占用保持不变。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-6

