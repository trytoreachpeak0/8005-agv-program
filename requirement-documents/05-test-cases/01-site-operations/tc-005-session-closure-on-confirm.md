---
id: TC-005
type: test-case
title: "会话结束联动"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-004"]
related_uc: ["UC-002", "UC-043"]
aliases: ["TC-005"]
---

# TC-005 会话结束联动

## Preconditions 前置条件

本次到站操作会话当前处于"仓门操作已锁定"阶段；FR-004 AC-1 的批量确认即将执行。

## Test Steps 测试步骤

系统完成批量确认。

## Expected Result 预期结果

该操作会话同时结束，界面恢复为"未验证"状态。

## Verifies 验证对象

[[fr-004-batch-task-completion-session-closure-and-non-reversibility|FR-004]] AC-2
