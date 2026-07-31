---
id: TC-013
type: test-case
title: "待重放只允许继续或取消"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-013"]
---

# TC-013 待重放只允许继续或取消

## Preconditions 前置条件

当前操作处于 LoadCorrectionPending，原仓位为 EMPTY。

## Test Steps 测试步骤

操作员查看可用操作。

## Expected Result 预期结果

系统只允许重新打开原仓位完成重放，或转“清空并取消”；不得跳过该仓位或继续后续装货。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-5
