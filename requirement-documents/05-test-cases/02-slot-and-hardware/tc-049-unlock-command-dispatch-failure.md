---
id: TC-049
type: test-case
title: "开锁指令下发失败，记录异常"
status: draft
created: 2026-07-14
updated: 2026-07-30
related_fr: ["FR-017"]
related_uc: ["UC-015"]
aliases: ["TC-049"]
---

# TC-049 开锁指令下发失败，记录异常

## Preconditions 前置条件

车辆处于配置维护态，车载端已持久化开锁测试准备状态。

## Test Steps 测试步骤

车载端核验发现开锁指令未被 IO 模块正常接收（如通信超时、IO 模块无响应）。

## Expected Result 预期结果

系统提示开锁指令下发异常，不重复开锁，保留诊断记录并判定测试异常。

## Verifies 验证对象

[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]] AC-2
