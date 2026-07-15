---
id: TC-033
type: test-case
title: "首次仓门操作触发锁定阶段"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-012"]
related_uc: ["UC-043"]
aliases: ["TC-033"]
---

# TC-033 首次仓门操作触发锁定阶段

## Preconditions 前置条件

当前会话处于"未开始仓门操作"阶段。

## Test Steps 测试步骤

会话内发生首次仓门打开动作。

## Expected Result 预期结果

系统将该会话状态更新为"仓门操作已锁定"。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-3
