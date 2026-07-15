---
id: TC-020
type: test-case
title: "批量开锁成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-008"]
related_uc: ["UC-010"]
aliases: ["TC-020"]
---

# TC-020 批量开锁成功

## Preconditions 前置条件

AGV 未在移动；已生成待取料清单。

## Test Steps 测试步骤

系统向待取料清单中的仓位下发开锁指令，仓门在规定时间内正常打开。

## Expected Result 预期结果

系统允许操作员从该仓位取出产品。

## Verifies 验证对象

[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] AC-3
