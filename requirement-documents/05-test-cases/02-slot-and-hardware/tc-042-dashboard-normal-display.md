---
id: TC-042
type: test-case
title: "正常展示仓位状态与关联信息"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-015"]
related_uc: ["UC-011"]
aliases: ["TC-042"]
---

# TC-042 正常展示仓位状态与关联信息

## Preconditions 前置条件

本地服务器与数据库运行正常。

## Test Steps 测试步骤

班组长/生产管理者打开仓位监控看板，或看板按周期/手动触发刷新。

## Expected Result 预期结果

系统读取并展示各仓位状态（空闲/已占用/异常锁定）、仓门开关状态；若某仓位为"已占用"，同时展示其关联的子批号及搬运任务信息（任务号、目标/交货站点、任务当前状态），与本地数据库当前记录一致。

## Verifies 验证对象

[[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]] AC-1
