---
id: TC-039
type: test-case
title: "仓位重新打开成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-014"]
related_uc: ["UC-044"]
aliases: ["TC-039"]
---

# TC-039 仓位重新打开成功

## Preconditions 前置条件

该 AGV 未在移动。

## Test Steps 测试步骤

系统向目标仓位下发开锁指令。

## Expected Result 预期结果

系统重新打开该仓位仓门，供操作员取出残留产品。

## Verifies 验证对象

[[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]] AC-2
