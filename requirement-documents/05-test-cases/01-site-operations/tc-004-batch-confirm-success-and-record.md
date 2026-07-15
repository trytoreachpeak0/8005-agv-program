---
id: TC-004
type: test-case
title: "批量确认成功并记录"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-004"]
related_uc: ["UC-002"]
aliases: ["TC-004"]
---

# TC-004 批量确认成功并记录

## Preconditions 前置条件

FR-003 核验已通过（当前站点存在待确认仓位，且仓门/光幕状态一致）。

## Test Steps 测试步骤

系统执行批量确认。

## Expected Result 预期结果

该站点所有待确认仓位对应的进行中任务状态一次性变为"已完成"；系统记录本次确认操作（操作员、任务、仓位、时间戳）。

## Verifies 验证对象

[[fr-004-batch-task-completion-session-closure-and-non-reversibility|FR-004]] AC-1
