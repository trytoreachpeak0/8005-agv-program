---
id: TC-071
type: test-case
title: "二次认证失败，不发布"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-023"]
related_uc: ["UC-038"]
aliases: ["TC-071"]
---

# TC-071 二次认证失败，不发布

## Preconditions 前置条件

操作人员已提交发布请求。

## Test Steps 测试步骤

再次刷卡或认证失败、超时、身份与当前操作人不一致，或权限不足。

## Expected Result 预期结果

系统不生成新版本，保留原 `Draft` 状态，记录失败审计。

## Verifies 验证对象

[[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]] AC-3
