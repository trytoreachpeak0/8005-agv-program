---
id: TC-011
type: test-case
title: "开锁超时，异常锁定"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-011"]
---

# TC-011 开锁超时，异常锁定

## Preconditions 前置条件

批量开锁指令已下发，其中某仓位仓门未能在规定时间内正常打开。

## Test Steps 测试步骤

系统核验开锁结果。

## Expected Result 预期结果

系统将该仓位标记为"异常锁定"，暂停对该仓位的后续操作；该子批号关联的其他仓位不受影响，仍按计划打开（对应 UC-005 Exception Flow E3.1）。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-3
