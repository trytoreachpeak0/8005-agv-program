---
id: TC-056
type: test-case
title: "开锁后未弹门或锁 DI 未变化"
status: draft
created: 2026-07-14
updated: 2026-07-30
related_fr: ["FR-019"]
related_uc: ["UC-017"]
aliases: ["TC-056"]
---

# TC-056 开锁后未弹门或锁 DI 未变化

## Preconditions 前置条件

目标仓位初始锁 DI 为“锁闭”，系统已发出一次有效开锁脉冲。

## Test Steps 测试步骤

维护人员观察到仓门未正常弹开，或系统读取的锁 DI 仍为“锁闭”。

## Expected Result 预期结果

系统不得自动重复开锁；记录 DO 回读、锁 DI 和目视结果，将仓位标记为测试未通过和硬件不可操作，等待排查弹簧、锁舌、电磁铁、接线或反馈。

## Verifies 验证对象

[[fr-019-slot-door-state-detection-test|FR-019]] AC-2
