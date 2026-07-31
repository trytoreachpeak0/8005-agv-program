---
id: TC-009
type: test-case
title: "移动联锁拒绝纠错开锁"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005", "UC-004"]
aliases: ["TC-009"]
---

# TC-009 移动联锁拒绝纠错开锁

## Preconditions 前置条件

FR-005 已授权原仓位纠错；安全联锁判定 AGV 正在移动。

## Test Steps 测试步骤

车载端准备打开纠错仓位。

## Expected Result 预期结果

系统不输出开锁，保持原任务、SUBLOT、预留和 StationOperationGuard。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-1
