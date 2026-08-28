---
id: TC-101
type: test-case
title: "不同 SUBLOT 物理操作不得穿插"
status: draft
created: 2026-07-30
updated: 2026-07-30
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-101"]
---

# TC-101 不同 SUBLOT 物理操作不得穿插

## Preconditions 前置条件

SUBLOT-B 正在装货、纠错、补偿或取消；SUBLOT-A 已装好并可取消。

## Test Steps 测试步骤

操作员请求取消 A。

## Expected Result 预期结果

服务端以稳定忙碌原因拒绝授权，不打开 A 的仓位；B 到达稳定边界后允许重新发起 A 的取消。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-7

