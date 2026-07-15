---
id: TC-031
type: test-case
title: "核验通过后建立会话（未开始仓门操作阶段）"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-012"]
related_uc: ["UC-043"]
aliases: ["TC-031"]
---

# TC-031 核验通过后建立会话（未开始仓门操作阶段）

## Preconditions 前置条件

[[fr-011-identity-and-role-verification-via-mes|FR-011]] 核验已通过。

## Test Steps 测试步骤

系统建立本次到站绑定的操作会话。

## Expected Result 预期结果

系统记录操作人身份、AGV、站点及会话开始时间，会话初始处于"未开始仓门操作"阶段；界面显示当前已验证的操作人身份，允许后续操作。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-1
