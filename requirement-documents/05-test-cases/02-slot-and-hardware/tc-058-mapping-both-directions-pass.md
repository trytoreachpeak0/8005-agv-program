---
id: TC-058
type: test-case
title: "双向核对均通过，记录映射通过"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-020"]
related_uc: ["UC-018"]
aliases: ["TC-058"]
---

# TC-058 双向核对均通过，记录映射通过

## Preconditions 前置条件

系统已按配置向目标仓位下发开锁 DO 指令，且维护人员已现场手动触发该物理仓位的传感器。

## Test Steps 测试步骤

维护人员核对确认：方向一中实际发生反应的物理仓位与配置中该 DO 点位对应的仓位编号一致；方向二中系统读取到的 DI 变化仓位编号与实际触发的物理仓位一致。

## Expected Result 预期结果

系统记录该仓位映射核对结果为"通过"。

## Verifies 验证对象

[[fr-020-bidirectional-io-point-mapping-verification|FR-020]] AC-1
