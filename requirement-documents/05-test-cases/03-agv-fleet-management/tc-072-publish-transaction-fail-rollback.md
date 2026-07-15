---
id: TC-072
type: test-case
title: "发布事务失败，整体回滚"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-023"]
related_uc: ["UC-038"]
aliases: ["TC-072"]
---

# TC-072 发布事务失败，整体回滚

## Preconditions 前置条件

二次认证已通过。

## Test Steps 测试步骤

版本持久化、状态转换、内容校验值计算或审计写入任一环节失败。

## Expected Result 预期结果

系统回滚整个操作，不产生新版本或部分状态变更，并提示稍后重试。

## Verifies 验证对象

[[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]] AC-4
