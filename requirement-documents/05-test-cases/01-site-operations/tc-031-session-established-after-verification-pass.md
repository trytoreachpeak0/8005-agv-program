---
id: TC-031
type: test-case
title: "核验通过后建立并持久化操作员上下文"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-012"]
related_uc: ["UC-043"]
aliases: ["TC-031"]
---

# TC-031 核验通过后建立并持久化操作员上下文

## Preconditions 前置条件

[[fr-011-identity-and-role-verification-via-mes|FR-011]] 核验已通过。

## Test Steps 测试步骤

服务端通过 MES 完成工号和岗位权限校验，车载端收到核验结果。

## Expected Result 预期结果

系统记录操作人身份、AGV、站点及会话开始时间；车载端持久化当前工号和核验引用，界面显示当前已验证的操作员，后续 Sublot 默认复用该工号。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-1
