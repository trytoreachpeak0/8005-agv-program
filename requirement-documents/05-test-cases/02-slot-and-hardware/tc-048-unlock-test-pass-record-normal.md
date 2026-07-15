---
id: TC-048
type: test-case
title: "开锁测试通过，记录正常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-017"]
related_uc: ["UC-015"]
aliases: ["TC-048"]
---

# TC-048 开锁测试通过，记录正常

## Preconditions 前置条件

维护人员已选择目标仓位并发起开锁测试。

## Test Steps 测试步骤

系统下发的开锁指令被 IO 模块正常接收，且维护人员现场确认该仓位仓门正常弹开/开启。

## Expected Result 预期结果

系统记录本次测试结果为"正常"（维护人员、仓位号、时间戳）。

## Verifies 验证对象

[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]] AC-1
