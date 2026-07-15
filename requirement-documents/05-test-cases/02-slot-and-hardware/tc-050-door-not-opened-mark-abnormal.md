---
id: TC-050
type: test-case
title: "仓门未能正常弹开，标记异常锁定"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-017"]
related_uc: ["UC-015"]
aliases: ["TC-050"]
---

# TC-050 仓门未能正常弹开，标记异常锁定

## Preconditions 前置条件

开锁指令已被 IO 模块正常接收。

## Test Steps 测试步骤

维护人员现场核验发现该仓位仓门未能正常弹开/开启。

## Expected Result 预期结果

系统将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"。

## Verifies 验证对象

[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]] AC-3
