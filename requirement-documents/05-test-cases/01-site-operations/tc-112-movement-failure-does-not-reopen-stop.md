---
id: TC-112
type: test-case
title: "发车失败不重新开放本站"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031", "FR-004", "FR-013"]
related_uc: ["UC-002", "UC-046"]
aliases: ["TC-112"]
---

# TC-112 发车失败不重新开放本站

## Preconditions 前置条件

StopClosureCommit 已完成，RIoT 移动下发被配置为失败。

## Test Steps 测试步骤

执行发车并观察失败后的任务、会话和界面状态。

## Expected Result 预期结果

已取消任务和已结束会话不恢复，本站操作入口保持关闭；界面显示“本站已结束，等待发车重试”并产生告警。

## Verifies 验证对象

FR-031 AC-12
