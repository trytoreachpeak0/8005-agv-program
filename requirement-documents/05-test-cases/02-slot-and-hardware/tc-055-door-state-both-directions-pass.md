---
id: TC-055
type: test-case
title: "开锁弹门与关门闩合完整测试通过"
status: draft
created: 2026-07-14
updated: 2026-07-30
related_fr: ["FR-019"]
related_uc: ["UC-017"]
aliases: ["TC-055"]
---

# TC-055 开锁弹门与关门闩合完整测试通过

## Preconditions 前置条件

车辆处于配置维护态且整车无货；目标仓位初始锁 DI 为“锁闭”。

## Test Steps 测试步骤

系统发出开锁脉冲，维护人员目视确认弹簧自动弹门；系统确认锁 DI 变为“未锁”。DO 自动复位后锁 DI 仍为“未锁”。维护人员关门并使锁舌闩合。

## Expected Result 预期结果

系统确认锁 DI 变回“锁闭”，记录各阶段 DO/DI、目视结果、维护人员、仓位号和时间戳，判定测试通过。

## Verifies 验证对象

[[fr-019-slot-door-state-detection-test|FR-019]] AC-1
