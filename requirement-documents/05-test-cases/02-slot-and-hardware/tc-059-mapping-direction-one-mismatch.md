---
id: TC-059
type: test-case
title: "方向一核对不通过，标记映射异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-020"]
related_uc: ["UC-018"]
aliases: ["TC-059"]
---

# TC-059 方向一核对不通过，标记映射异常

## Preconditions 前置条件

系统已按配置中指向该仓位的 DO 点位下发开锁指令。

## Test Steps 测试步骤

维护人员核对发现实际发生反应（弹开）的物理仓位与配置中该 DO 点位对应的仓位编号不一致。

## Expected Result 预期结果

系统将涉及的仓位标记为"映射异常"，暂停对其业务分配，记录本次核对结果。

## Verifies 验证对象

[[fr-020-bidirectional-io-point-mapping-verification|FR-020]] AC-2
