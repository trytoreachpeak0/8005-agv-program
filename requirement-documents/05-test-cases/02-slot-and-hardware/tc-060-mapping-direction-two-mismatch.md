---
id: TC-060
type: test-case
title: "方向二核对不通过，标记映射异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-020"]
related_uc: ["UC-018"]
aliases: ["TC-060"]
---

# TC-060 方向二核对不通过，标记映射异常

## Preconditions 前置条件

维护人员已现场手动触发某个物理仓位的传感器。

## Test Steps 测试步骤

维护人员核对发现软件侧显示的 DI 变化仓位编号与自己实际触发的物理仓位不一致。

## Expected Result 预期结果

系统将涉及的仓位标记为"映射异常"，暂停对其业务分配，记录本次核对结果。

## Verifies 验证对象

[[fr-020-bidirectional-io-point-mapping-verification|FR-020]] AC-3
