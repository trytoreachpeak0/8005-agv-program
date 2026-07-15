---
id: TC-006
type: test-case
title: "确认后不支持撤销"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-004"]
related_uc: ["UC-002"]
aliases: ["TC-006"]
---

# TC-006 确认后不支持撤销

## Preconditions 前置条件

一次确认完成操作已成功执行（FR-004 AC-1）。

## Test Steps 测试步骤

操作员事后发现误确认，请求撤销该次确认。

## Expected Result 预期结果

系统拒绝该撤销请求，不提供撤销能力（对应 UC-002 Exception Flow E3.1）。

## Verifies 验证对象

[[fr-004-batch-task-completion-session-closure-and-non-reversibility|FR-004]] AC-3
