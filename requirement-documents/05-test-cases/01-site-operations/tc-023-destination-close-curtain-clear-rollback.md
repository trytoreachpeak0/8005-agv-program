---
id: TC-023
type: test-case
title: "关门后光幕确认清空，回滚成功并记录"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-009"]
related_uc: ["UC-010"]
aliases: ["TC-023"]
---

# TC-023 关门后光幕确认清空，回滚成功并记录

## Preconditions 前置条件

操作员已关闭目标仓位仓门，光幕检测确认该仓位内确实已清空。

## Test Steps 测试步骤

系统执行关门后核验。

## Expected Result 预期结果

该仓位状态由"已占用"变为"空闲"，清除仓位—子批号映射关系并记录本次取出操作；若该任务全部目标仓位均已完成卸货，则任务自动完成，否则保持未结。

## Verifies 验证对象

[[fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation|FR-009]] AC-1
