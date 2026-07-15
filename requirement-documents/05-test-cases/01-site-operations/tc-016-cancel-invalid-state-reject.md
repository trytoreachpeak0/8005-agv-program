---
id: TC-016
type: test-case
title: "任务状态不满足条件，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-016"]
---

# TC-016 任务状态不满足条件，拒绝

## Preconditions 前置条件

目标任务当前状态已是"已完成"或"已取消"。

## Test Steps 测试步骤

操作员点击"取消运送"。

## Expected Result 预期结果

系统拒绝本次取消请求，提示"该任务当前状态不可取消"，并刷新待处理任务列表（对应 UC-006 Exception Flow E2.1）。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-2
