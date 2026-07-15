---
id: TC-024
type: test-case
title: "关门后光幕检测残留，转 UC-044"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-009"]
related_uc: ["UC-010", "UC-044"]
aliases: ["TC-024"]
---

# TC-024 关门后光幕检测残留，转 UC-044

## Preconditions 前置条件

操作员已关闭目标仓位仓门，但光幕仍检测到产品残留。

## Test Steps 测试步骤

系统执行关门后核验。

## Expected Result 预期结果

系统不将该仓位回滚为"空闲"，转 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 处理；直至 UC-044 处理完毕、仓位恢复"空闲"后，才允许记录取出结果（对应 UC-010 Exception Flow E4.1）。

## Verifies 验证对象

[[fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation|FR-009]] AC-2
