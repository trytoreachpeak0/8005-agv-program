---
id: TC-022
type: test-case
title: "打开后实物不符，异常锁定"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-008"]
related_uc: ["UC-010"]
aliases: ["TC-022"]
---

# TC-022 打开后实物不符，异常锁定

## Preconditions 前置条件

某仓位打开后，操作员核验发现该仓位内实际无产品，或存放的产品与系统记录的子批号不符。

## Test Steps 测试步骤

操作员上报该仓位状态异常。

## Expected Result 预期结果

系统将该仓位标记为"异常锁定"，暂停对该仓位的后续操作；该 AGV 上其他待取料仓位不受影响（对应 UC-010 Exception Flow E2.2）。

## Verifies 验证对象

[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] AC-5
