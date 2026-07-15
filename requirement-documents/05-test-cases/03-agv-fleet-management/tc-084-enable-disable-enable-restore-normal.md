---
id: TC-084
type: test-case
title: "启用，恢复正常状态"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-027"]
related_uc: ["UC-013"]
aliases: ["TC-084"]
---

# TC-084 启用，恢复正常状态

## Preconditions 前置条件

管理员对一台处于"已禁用"或"禁用待生效"的 AGV 点击"启用"。

## Test Steps 测试步骤

系统核验该 AGV 确实处于上述状态之一。

## Expected Result 预期结果

系统将该 AGV 状态恢复为其原本应有的正常状态，清除禁用相关标记，记录操作人、AGV、操作类型、时间戳。

## Verifies 验证对象

[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]] AC-3
