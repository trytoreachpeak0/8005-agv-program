---
id: TC-057
type: test-case
title: "关门后锁 DI 未锁闭"
status: draft
created: 2026-07-14
updated: 2026-07-30
related_fr: ["FR-019"]
related_uc: ["UC-017"]
aliases: ["TC-057"]
---

# TC-057 关门后锁 DI 未锁闭

## Preconditions 前置条件

目标仓位已开锁且 DO 已自动复位，维护人员执行关门。

## Test Steps 测试步骤

系统读取的锁 DI 仍为“未锁”。

## Expected Result 预期结果

系统不得把仓门视为安全锁闭，提示维护人员重新关门；持续失败时记录测试失败，将仓位判为硬件不可操作并排查机构、接线或反馈。

## Verifies 验证对象

[[fr-019-slot-door-state-detection-test|FR-019]] AC-3
