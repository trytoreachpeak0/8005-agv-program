---
id: TC-036
type: test-case
title: "StopClosureCommit 清除工号和到站会话"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043"]
aliases: ["TC-036"]
---

# TC-036 StopClosureCommit 清除工号和到站会话

## Preconditions 前置条件

车辆满足 StationDepartureWaiting，OperationSession 与 OnboardOperatorContext 有效。

## Test Steps 测试步骤

分别执行人工与超时 StopClosureCommit，并让其中一次后续移动失败。

## Expected Result 预期结果

StopClosureCommit 成功时立即结束会话并清除工号；后续移动失败不恢复本站会话或工号。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-3
