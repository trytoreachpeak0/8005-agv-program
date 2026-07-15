---
id: TC-086
type: test-case
title: "对非禁用状态点击启用，忽略"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-027"]
related_uc: ["UC-013"]
aliases: ["TC-086"]
---

# TC-086 对非禁用状态点击启用，忽略

## Preconditions 前置条件

某台 AGV 当前处于正常（非禁用）状态。

## Test Steps 测试步骤

管理员点击"启用"。

## Expected Result 预期结果

系统提示该 AGV 当前无需启用，忽略本次操作，不重复记录。

## Verifies 验证对象

[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]] AC-5
