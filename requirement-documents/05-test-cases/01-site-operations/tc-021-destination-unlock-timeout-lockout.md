---
id: TC-021
type: test-case
title: "开锁超时，异常锁定"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-008"]
related_uc: ["UC-010"]
aliases: ["TC-021"]
---

# TC-021 开锁超时，异常锁定

## Preconditions 前置条件

某仓位仓门未能在规定时间内正常打开。

## Test Steps 测试步骤

系统核验开锁结果。

## Expected Result 预期结果

系统提示该仓位开锁异常，将其标记为"异常锁定"，暂停对该仓位的后续操作；该 AGV 上其他待取料仓位不受影响，仍按计划打开（对应 UC-010 Exception Flow E2.1）。

## Verifies 验证对象

[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] AC-4
