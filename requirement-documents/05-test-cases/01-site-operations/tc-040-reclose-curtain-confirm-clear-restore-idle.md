---
id: TC-040
type: test-case
title: "重新关闭光幕确认清空，恢复空闲并记录"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-014"]
related_uc: ["UC-044", "UC-010"]
aliases: ["TC-040"]
---

# TC-040 重新关闭光幕确认清空，恢复空闲并记录

## Preconditions 前置条件

操作员重新关闭该仓位仓门后，光幕检测确认该仓位内确已清空。

## Test Steps 测试步骤

系统执行重新关闭后核验。

## Expected Result 预期结果

系统将该仓位状态恢复为 UC-010 预期的"空闲"；记录本次重新打开、取出残留及重新核验的过程（操作员、仓位号、时间戳）。

## Verifies 验证对象

[[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]] AC-3
