---
id: TC-027
type: test-case
title: "存在活跃会话时拒绝发起核验"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-011"]
related_uc: ["UC-043"]
aliases: ["TC-027"]
---

# TC-027 存在活跃会话时拒绝发起核验

## Preconditions 前置条件

当前站点/终端已存在其他仍处于活动状态（未开始或已锁定阶段均算）的会话。

## Test Steps 测试步骤

操作员尝试发起新的身份核验。

## Expected Result 预期结果

系统拒绝本次核验请求，提示须先结束当前会话。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-1
