---
id: TC-048
type: test-case
title: "开锁测试通过，记录正常"
status: draft
created: 2026-07-14
updated: 2026-07-30
related_fr: ["FR-017"]
related_uc: ["UC-015"]
aliases: ["TC-048"]
---

# TC-048 开锁测试通过，记录正常

## Preconditions 前置条件

车辆已在线获准进入配置维护态，整车无货且机构初始安全；维护人员已选择目标仓位。

## Test Steps 测试步骤

车载端发送一次开锁脉冲，维护人员确认仓门正常弹开；系统确认锁 DI 变为未锁、DO 自动复位。维护人员随后关门并使锁舌闩合。

## Expected Result 预期结果

系统确认锁 DI 恢复锁闭，记录各阶段 DO/DI、目视结果、维护人员、仓位号和时间戳。

## Verifies 验证对象

[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]] AC-1
