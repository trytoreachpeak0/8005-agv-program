---
id: TC-069
type: test-case
title: "规格完整、认证通过，原子生成不可变新版本"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-023"]
related_uc: ["UC-038"]
aliases: ["TC-069"]
---

# TC-069 规格完整、认证通过，原子生成不可变新版本

## Preconditions 前置条件

目标 `Draft` 已通过格式校验且仓位规格填写完整，操作人员已填写发布原因并查看与上一 `Published` 版本的差异。

## Test Steps 测试步骤

操作人员再次刷卡或认证成功。

## Expected Result 预期结果

系统以原子事务生成新的不可变 `Published` 版本（含 `modelId`、单调递增 `version`、全局唯一 `modelVersionId`、面与仓位定义、发布时间、发布人、内容校验值），记录审计。

## Verifies 验证对象

[[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]] AC-1
