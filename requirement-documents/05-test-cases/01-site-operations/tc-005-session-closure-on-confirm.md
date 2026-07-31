---
id: TC-005
type: test-case
title: "整站提交立即结束操作会话"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-004", "FR-013"]
related_uc: ["UC-002", "UC-043", "UC-046"]
aliases: ["TC-005"]
---

# TC-005 整站提交立即结束操作会话

## Preconditions 前置条件

OperationSession 和 OnboardOperatorContext 有效。

## Test Steps 测试步骤

完成 StopClosureCommit，但暂不让 RIoT 移动成功。

## Expected Result 预期结果

操作会话已经结束、车载工号已经清除，本站扫码与纠错入口保持关闭。

## Verifies 验证对象

FR-004 AC-2
