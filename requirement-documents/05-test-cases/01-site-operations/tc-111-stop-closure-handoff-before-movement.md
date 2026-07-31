---
id: TC-111
type: test-case
title: "整站结束后同步与安全核验先于移动"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031", "FR-004", "FR-013"]
related_uc: ["UC-002", "UC-046"]
aliases: ["TC-111"]
---

# TC-111 整站结束后同步与安全核验先于移动

## Preconditions 前置条件

StopClosureCommit 即将成功，车辆存在下一 PlannedStop。

## Test Steps 测试步骤

观察会话清理、投影确认、安全核验与 RIoT 移动请求的顺序。

## Expected Result 预期结果

先结束 OperationSession 并清除 OnboardOperatorContext，再由车载采用最新 CurrentStopWorklistSnapshot 和 UpcomingStopPlanSnapshot，随后通过 PreDepartureSafetyCheck，最后才发送移动请求。

## Verifies 验证对象

FR-031 AC-10
