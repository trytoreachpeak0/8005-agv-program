---
id: TC-092
type: test-case
title: "车辆未禁用，拒绝归档"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-029"]
related_uc: ["UC-021"]
aliases: ["TC-092"]
---

# TC-092 车辆未禁用，拒绝归档

## Preconditions 前置条件

目标 AGV 当前未处于"已禁用"状态。

## Test Steps 测试步骤

管理员发起归档。

## Expected Result 预期结果

系统拒绝归档，提示先通过 UC-013 禁用并等待禁用生效。

## Verifies 验证对象

[[fr-029-agv-archive-eligibility-check-and-state-transition|FR-029]] AC-2
