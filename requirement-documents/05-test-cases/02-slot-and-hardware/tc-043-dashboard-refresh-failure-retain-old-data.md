---
id: TC-043
type: test-case
title: "刷新时数据读取异常，保留旧数据并标注"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-015"]
related_uc: ["UC-011"]
aliases: ["TC-043"]
---

# TC-043 刷新时数据读取异常，保留旧数据并标注

## Preconditions 前置条件

看板已展示上一次成功读取到的数据。

## Test Steps 测试步骤

系统按周期或手动触发刷新时，读取本地数据库/服务发生异常。

## Expected Result 预期结果

系统提示"数据刷新失败，请稍后重试"，保留上一次成功读取到的数据，并标注该数据的最后刷新时间，不得与最新真实状态混淆；系统持续尝试重新读取。

## Verifies 验证对象

[[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]] AC-2
