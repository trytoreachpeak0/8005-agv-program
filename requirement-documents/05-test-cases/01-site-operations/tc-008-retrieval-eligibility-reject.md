---
id: TC-008
type: test-case
title: "不合法纠错状态拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-005"]
related_uc: ["UC-005"]
aliases: ["TC-008"]
---

# TC-008 不合法纠错状态拒绝

## Preconditions 前置条件

分别准备 StopClosureCommit 已发生、车辆已离站、所选仓位不属于当前 SUBLOT/不是 OCCUPIED，或另一 SUBLOT 正在执行物理操作。

## Test Steps 测试步骤

操作员请求对所选仓位执行 LoadCorrection。

## Expected Result 预期结果

系统拒绝且不打开仓门；StopClosureCommit 已发生时不重新开放本站，已离站时引导异常卸出。

## Verifies 验证对象

[[fr-005-mis-stored-retrieval-eligibility-check|FR-005]] AC-2
