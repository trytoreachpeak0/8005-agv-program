---
id: TC-106
type: test-case
title: "部分装货无进展只告警"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-001", "UC-046"]
aliases: ["TC-106"]
---

# TC-106 部分装货无进展只告警

## Preconditions 前置条件

一个三仓 LoadBatch 只完成一个目标仓位，当前所有仓门暂时锁闭。

## Test Steps 测试步骤

最后一个完成仓位后保持无物理进展 5 分钟。

## Expected Result 预期结果

系统产生“装货中断，需要继续装货或清空取消”告警；不自动提交 LoadBatch、不取消任务、不执行 StopClosureCommit 或发车。

## Verifies 验证对象

FR-031 AC-7
