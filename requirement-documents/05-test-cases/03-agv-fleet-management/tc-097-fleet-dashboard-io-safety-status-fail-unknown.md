---
id: TC-097
type: test-case
title: "IO 或安全状态读取失败，标记未知并判定不可分配"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-030"]
related_uc: ["UC-022"]
aliases: ["TC-097"]
---

# TC-097 IO 或安全状态读取失败，标记未知并判定不可分配

## Preconditions 前置条件

管理员正在查看或刷新车队页面。

## Test Steps 测试步骤

某台车辆的仓门、光幕或安全状态读取失败。

## Expected Result 预期结果

系统将对应状态标记为未知，判定该车辆不可分配，并显示具体缺失项。

## Verifies 验证对象

[[fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning|FR-030]] AC-3
