---
id: TC-099
type: test-case
title: "正式提交后取消保留历史"
status: draft
created: 2026-07-30
updated: 2026-07-30
related_fr: ["FR-007"]
related_uc: ["UC-002", "UC-006"]
aliases: ["TC-099"]
---

# TC-099 正式提交后取消保留历史

## Preconditions 前置条件

LoadBatch 已自动提交，但 StopClosureCommit 尚未发生。

## Test Steps 测试步骤

操作员完成该 DemandId 的清空并取消。

## Expected Result 预期结果

最终有效状态变为 CANCELLED_BY_OPERATOR；原确认人、原提交事实、取消操作和逐仓清空证据全部保留，不删除或覆盖历史。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-5
