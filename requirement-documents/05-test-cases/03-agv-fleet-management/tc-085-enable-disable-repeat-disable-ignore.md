---
id: TC-085
type: test-case
title: "重复点击禁用，忽略"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-027"]
related_uc: ["UC-013"]
aliases: ["TC-085"]
---

# TC-085 重复点击禁用，忽略

## Preconditions 前置条件

某台 AGV 已处于"已禁用"或"禁用待生效"状态。

## Test Steps 测试步骤

管理员再次点击"禁用"。

## Expected Result 预期结果

系统提示该 AGV 当前已处于禁用（或禁用待生效）状态，忽略本次重复操作，不重复记录。

## Verifies 验证对象

[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]] AC-4
