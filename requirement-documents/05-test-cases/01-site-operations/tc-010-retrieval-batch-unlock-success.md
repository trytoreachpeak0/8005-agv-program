---
id: TC-010
type: test-case
title: "批量开锁成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-010"]
---

# TC-010 批量开锁成功

## Preconditions 前置条件

AGV 未在移动；已通过 FR-005 核验。

## Test Steps 测试步骤

系统一次性向该子批号关联的全部仓位下发开锁指令，各仓门在规定时间内正常打开。

## Expected Result 预期结果

系统允许操作员从全部仓位中取出产品。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-2
