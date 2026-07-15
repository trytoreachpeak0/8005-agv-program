---
id: TC-013
type: test-case
title: "关门后光幕确认清空，回滚成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-013"]
---

# TC-013 关门后光幕确认清空，回滚成功

## Preconditions 前置条件

全部仓位仓门已关闭，光幕检测确认各仓位内确实已无产品残留。

## Test Steps 测试步骤

系统执行关门后核验与回滚。

## Expected Result 预期结果

该子批号关联的全部仓位状态由"已占用"回滚为"空闲"，清除仓位—子批号映射关系；记录本次取出操作（操作员、原子批号、仓位号、时间戳）；相关搬运任务状态保持"进行中"。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-5
