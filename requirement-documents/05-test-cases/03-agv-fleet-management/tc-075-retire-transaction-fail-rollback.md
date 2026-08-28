---
id: TC-075
type: test-case
title: "停用事务失败，回滚"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-024"]
related_uc: ["UC-038"]
aliases: ["TC-075"]
---

# TC-075 停用事务失败，回滚

## Preconditions 前置条件

二次认证已通过。

## Test Steps 测试步骤

状态转换或审计写入任一环节失败。

## Expected Result 预期结果

系统回滚整个操作，不产生部分状态变更，并提示稍后重试。

## Verifies 验证对象

[[fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation|FR-024]] AC-3
