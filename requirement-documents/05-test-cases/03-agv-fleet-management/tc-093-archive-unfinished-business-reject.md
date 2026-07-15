---
id: TC-093
type: test-case
title: "存在未结束业务，拒绝归档"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-029"]
related_uc: ["UC-021"]
aliases: ["TC-093"]
---

# TC-093 存在未结束业务，拒绝归档

## Preconditions 前置条件

目标 AGV 存在进行中任务、等待装卸或异常待恢复的本地作业。

## Test Steps 测试步骤

管理员发起归档。

## Expected Result 预期结果

系统列出这些未结束的任务/作业，拒绝归档。

## Verifies 验证对象

[[fr-029-agv-archive-eligibility-check-and-state-transition|FR-029]] AC-3
