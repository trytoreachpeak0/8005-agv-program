---
id: TC-074
type: test-case
title: "二次认证失败，不停用"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-024"]
related_uc: ["UC-038"]
aliases: ["TC-074"]
---

# TC-074 二次认证失败，不停用

## Preconditions 前置条件

操作人员已提交停用请求。

## Test Steps 测试步骤

再次刷卡或认证失败、超时、身份与当前操作人不一致，或权限不足。

## Expected Result 预期结果

系统不停用，保留原 `Published` 状态，记录失败审计。

## Verifies 验证对象

[[fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation|FR-024]] AC-2
