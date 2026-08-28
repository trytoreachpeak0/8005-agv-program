---
id: TC-082
type: test-case
title: "禁用且队列为空，立即禁用"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-027"]
related_uc: ["UC-013"]
aliases: ["TC-082"]
---

# TC-082 禁用且队列为空，立即禁用

## Preconditions 前置条件

管理员对一台当前非禁用状态的 AGV 点击"禁用"。

## Test Steps 测试步骤

系统核验该 AGV 当前 RIOT 任务队列为空。

## Expected Result 预期结果

系统立即将该 AGV 状态置为"已禁用"，记录操作人、AGV、操作类型、时间戳。

## Verifies 验证对象

[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]] AC-1
