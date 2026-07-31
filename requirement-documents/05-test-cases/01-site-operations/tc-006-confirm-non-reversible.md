---
id: TC-006
type: test-case
title: "发车失败不撤销整站结束"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_fr: ["FR-004"]
related_uc: ["UC-002", "UC-046"]
aliases: ["TC-006"]
---

# TC-006 发车失败不撤销整站结束

## Preconditions 前置条件

StopClosureCommit 已成功。

## Test Steps 测试步骤

使 RIoT 移动请求失败。

## Expected Result 预期结果

系统保留本站结束、任务取消和会话终结，显示等待发车重试并报警，不恢复本站操作。

## Verifies 验证对象

FR-004 AC-4
