---
id: TC-012
type: test-case
title: "正确产品不可得进入待重放"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-012"]
---

# TC-012 正确产品不可得进入待重放

## Preconditions 前置条件

操作员已从纠错仓位取出错误产品，但正确产品暂时不可得；原仓位安全锁闭后为 EMPTY。

## Test Steps 测试步骤

系统执行纠错完成判定。

## Expected Result 预期结果

系统不把 EMPTY 记为纠错成功，进入 LoadCorrectionPending；保持任务、预留与 StationOperationGuard，禁止后续仓位装货。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-4
