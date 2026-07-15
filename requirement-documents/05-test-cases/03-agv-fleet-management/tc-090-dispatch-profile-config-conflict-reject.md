---
id: TC-090
type: test-case
title: "配置冲突，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-028"]
related_uc: ["UC-020"]
aliases: ["TC-090"]
---

# TC-090 配置冲突，拒绝保存

## Preconditions 前置条件

管理员提交的配置中 RCS/RIOT 车辆 ID 重复、外部车辆不存在，或服务区域等配置不合法。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存并显示具体冲突项。

## Verifies 验证对象

[[fr-028-agv-dispatch-profile-update-eligibility-and-persistence|FR-028]] AC-4
