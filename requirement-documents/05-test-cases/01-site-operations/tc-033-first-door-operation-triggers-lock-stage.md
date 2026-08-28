---
id: TC-033
type: test-case
title: "活动 Sublot 内拒绝更换操作员"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-012"]
related_uc: ["UC-043"]
aliases: ["TC-033"]
---

# TC-033 活动 Sublot 内拒绝更换操作员

## Preconditions 前置条件

当前 Sublot 已在首次仓位操作前绑定操作员工号，且尚未形成 LoadBatch 自动提交闭环。

## Test Steps 测试步骤

用户尝试输入并切换为另一个工号。

## Expected Result 预期结果

系统拒绝更换，保留当前 Sublot 的原操作员绑定；不得以新工号继续该 Sublot。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-2
