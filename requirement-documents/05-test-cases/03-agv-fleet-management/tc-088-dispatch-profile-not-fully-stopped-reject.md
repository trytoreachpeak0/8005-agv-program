---
id: TC-088
type: test-case
title: "车辆未完全停用，拒绝进入可保存状态"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-028"]
related_uc: ["UC-020"]
aliases: ["TC-088"]
---

# TC-088 车辆未完全停用，拒绝进入可保存状态

## Preconditions 前置条件

目标车辆未禁用、处于"禁用待生效"，或存在本地未完成作业。

## Test Steps 测试步骤

管理员尝试进入配置保存流程。

## Expected Result 预期结果

系统拒绝进入可保存状态，提示先完成作业并通过 UC-013 禁用。

## Verifies 验证对象

[[fr-028-agv-dispatch-profile-update-eligibility-and-persistence|FR-028]] AC-2
