---
id: TC-035
type: test-case
title: "完成 UC-002 正常结束会话"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043", "UC-002"]
aliases: ["TC-035"]
---

# TC-035 完成 UC-002 正常结束会话

## Preconditions 前置条件

会话处于"仓门操作已锁定"阶段。

## Test Steps 测试步骤

操作员完成 [[uc-002-confirm-task-completion|UC-002]] 确认完成。

## Expected Result 预期结果

系统结束当前会话，记录结束时间及结束方式（"UC-002 确认完成"），界面恢复为"未验证"状态。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-2
