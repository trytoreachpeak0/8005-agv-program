---
id: TC-055
type: test-case
title: "开启、关闭两方向均核验通过，记录正常"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-019"]
related_uc: ["UC-017"]
aliases: ["TC-055"]
---

# TC-055 开启、关闭两方向均核验通过，记录正常

## Preconditions 前置条件

维护人员依次打开、关闭目标仓位仓门。

## Test Steps 测试步骤

系统分别读取该仓位门状态 DI 信号，均与门的实际物理开合状态一致（打开时为"开启"、关闭时为"关闭"）。

## Expected Result 预期结果

系统记录本次测试结果为"正常"（维护人员、仓位号、时间戳）。

## Verifies 验证对象

[[fr-019-slot-door-state-detection-test|FR-019]] AC-1
