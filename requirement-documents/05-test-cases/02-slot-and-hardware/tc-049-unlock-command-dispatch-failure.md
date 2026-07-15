---
id: TC-049
type: test-case
title: "开锁指令下发失败，记录异常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-017"]
related_uc: ["UC-015"]
aliases: ["TC-049"]
---

# TC-049 开锁指令下发失败，记录异常

## Preconditions 前置条件

维护人员已发起开锁测试。

## Test Steps 测试步骤

系统核验发现该开锁指令未能被 IO 模块正常接收（如通信超时、IO 模块无响应）。

## Expected Result 预期结果

系统提示该仓位开锁指令下发异常，记录本次测试结果为"异常"。

## Verifies 验证对象

[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]] AC-2
