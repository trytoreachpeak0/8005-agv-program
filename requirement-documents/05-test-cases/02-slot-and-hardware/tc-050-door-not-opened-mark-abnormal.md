---
id: TC-050
type: test-case
title: "仓门未弹开，标记硬件不可操作"
status: draft
created: 2026-07-14
updated: 2026-07-30
related_fr: ["FR-017"]
related_uc: ["UC-015"]
aliases: ["TC-050"]
---

# TC-050 仓门未弹开，标记硬件不可操作

## Preconditions 前置条件

开锁指令已被 IO 模块正常接收。

## Test Steps 测试步骤

维护人员现场核验发现该仓位仓门未能正常弹开/开启。

## Expected Result 预期结果

系统不自动重复开锁，将该仓位标记为测试未通过和硬件不可操作，暂停新的业务分配并记录 DO 回读、锁 DI 和目视结果；人工启用不能覆盖该结果。

## Verifies 验证对象

[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]] AC-3
