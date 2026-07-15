---
id: TC-083
type: test-case
title: "禁用且队列不为空，先禁用待生效再自动转为已禁用"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-027"]
related_uc: ["UC-013"]
aliases: ["TC-083"]
---

# TC-083 禁用且队列不为空，先禁用待生效再自动转为已禁用

## Preconditions 前置条件

管理员对一台当前非禁用状态的 AGV 点击"禁用"，且该 AGV 当前 RIOT 任务队列不为空。

## Test Steps 测试步骤

系统核验队列非空，将该 AGV 状态置为"禁用待生效"；当前任务不受影响，继续执行至完成或取消，队列重新变空。

## Expected Result 预期结果

系统自动将该 AGV 状态转为"已禁用"，无需人工二次确认。

## Verifies 验证对象

[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]] AC-2
