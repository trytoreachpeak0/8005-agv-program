---
id: TC-036
type: test-case
title: "未锁定阶段主动提前结束会话"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043"]
aliases: ["TC-036"]
---

# TC-036 未锁定阶段主动提前结束会话

## Preconditions 前置条件

会话仍处于"未开始仓门操作"阶段。

## Test Steps 测试步骤

操作员点击"结束会话"（该操作不要求核验身份，终端前任何人均可执行）。

## Expected Result 预期结果

系统结束当前会话，记录结束时间及结束方式（"操作员主动提前结束"），界面恢复为"未验证"状态。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-3
