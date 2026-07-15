---
id: TC-089
type: test-case
title: "仓门或安全状态不满足，fail-closed 拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-028"]
related_uc: ["UC-020"]
aliases: ["TC-089"]
---

# TC-089 仓门或安全状态不满足，fail-closed 拒绝

## Preconditions 前置条件

目标车辆任一仓门打开，或仓门、光幕、安全状态未知/异常。

## Test Steps 测试步骤

管理员尝试保存配置。

## Expected Result 预期结果

系统采用 fail-closed，拒绝保存影响调度的配置并提示处理现场状态。

## Verifies 验证对象

[[fr-028-agv-dispatch-profile-update-eligibility-and-persistence|FR-028]] AC-3
