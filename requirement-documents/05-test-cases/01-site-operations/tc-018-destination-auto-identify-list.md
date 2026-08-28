---
id: TC-018
type: test-case
title: "自动识别待取料清单"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-008"]
related_uc: ["UC-010"]
aliases: ["TC-018"]
---

# TC-018 自动识别待取料清单

## Preconditions 前置条件

AGV 已到达某站点，且该 AGV 上存在一个或多个"已占用"且关联任务目标站点等于当前站点的仓位。

## Test Steps 测试步骤

系统在到站后执行仓位识别。

## Expected Result 预期结果

系统自动列出这些仓位/任务作为本次到站待取料清单，不要求操作员扫码。

## Verifies 验证对象

[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] AC-1
