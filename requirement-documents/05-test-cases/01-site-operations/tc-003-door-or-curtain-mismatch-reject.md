---
id: TC-003
type: test-case
title: "未收敛或状态不明时拒绝本站结束"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-003"]
related_uc: ["UC-002", "UC-046"]
aliases: ["TC-003"]
---

# TC-003 未收敛或状态不明时拒绝本站结束

## Preconditions 前置条件

分别准备部分 LoadBatch、待卸任务、LoadCorrectionPending、断联和 DepartureSafe 无效状态。

## Test Steps 测试步骤

尝试人工结束本站或推进到自动超时。

## Expected Result 预期结果

每种状态均拒绝 StopClosureCommit，不取消任务、不发车，并给出明确阻断原因。

## Verifies 验证对象

FR-003 AC-3
