---
id: TC-056
type: test-case
title: "仓门已打开但信号仍显示关闭，标记异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-019"]
related_uc: ["UC-017"]
aliases: ["TC-056"]
---

# TC-056 仓门已打开但信号仍显示关闭，标记异常

## Preconditions 前置条件

维护人员已打开目标仓位仓门。

## Test Steps 测试步骤

系统读取的该仓位门状态 DI 信号未变化，仍显示"关闭"，与门实际已打开的物理状态不一致。

## Expected Result 预期结果

系统判定该仓位门状态传感器/反馈信号异常，标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"。

## Verifies 验证对象

[[fr-019-slot-door-state-detection-test|FR-019]] AC-2
