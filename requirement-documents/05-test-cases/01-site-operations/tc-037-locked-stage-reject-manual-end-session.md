---
id: TC-037
type: test-case
title: "锁定阶段拒绝手动结束会话"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043"]
aliases: ["TC-037"]
---

# TC-037 锁定阶段拒绝手动结束会话

## Preconditions 前置条件

会话已处于"仓门操作已锁定"阶段。

## Test Steps 测试步骤

操作员尝试点击"结束会话"。

## Expected Result 预期结果

系统拒绝该请求，提示"本次到站操作已开始，必须先完成 UC-002 确认完成才能结束会话"。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-4
