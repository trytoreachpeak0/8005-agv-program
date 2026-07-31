---
id: TC-027
type: test-case
title: "活动 Sublot 内拒绝更换工号"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-011"]
related_uc: ["UC-043"]
aliases: ["TC-027"]
---

# TC-027 活动 Sublot 内拒绝更换工号

## Preconditions 前置条件

当前 Sublot 已绑定一个通过校验的工号，且仍处于活动、部分或未收敛状态。

## Test Steps 测试步骤

操作员扫描或手动输入另一个工号。

## Expected Result 预期结果

系统拒绝更换并保留原工号，提示同一 Sublot 内不能更换操作员；不得因新工号本身有效而覆盖原绑定。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-3
