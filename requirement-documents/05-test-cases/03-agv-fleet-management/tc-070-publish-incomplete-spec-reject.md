---
id: TC-070
type: test-case
title: "仓位规格仍缺失或不合法，拒绝发布"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-023"]
related_uc: ["UC-038"]
aliases: ["TC-070"]
---

# TC-070 仓位规格仍缺失或不合法，拒绝发布

## Preconditions 前置条件

目标 `Draft` 中存在仓位的尺寸或最大载重未填写，或数值不合法。

## Test Steps 测试步骤

操作人员发起发布。

## Expected Result 预期结果

系统拒绝发布，提示具体缺失或不合法的字段，`Draft` 状态保持不变。

## Verifies 验证对象

[[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]] AC-2
