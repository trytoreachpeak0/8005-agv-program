---
id: TC-007
type: test-case
title: "原仓位纠错资格通过"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-005"]
related_uc: ["UC-005"]
aliases: ["TC-007"]
---

# TC-007 原仓位纠错资格通过

## Preconditions 前置条件

LoadBatch 已自动提交，但 StopClosureCommit 尚未发生；所选仓位属于当前 SUBLOT、已锁闭且实时为 OCCUPIED，没有另一 SUBLOT 的活动物理操作。

## Test Steps 测试步骤

已核验操作员选择放错的原仓位，发起“取出重放”。

## Expected Result 预期结果

服务端在原 SlotOperationAttemptId 下授权只包含所选原仓位的 LoadCorrection，停止离站倒计时且不撤销原 LoadBatch 提交。

## Verifies 验证对象

[[fr-005-mis-stored-retrieval-eligibility-check|FR-005]] AC-1
