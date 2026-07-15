---
id: TC-079
type: test-case
title: "配置不完整或不合法，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-025"]
related_uc: ["UC-019"]
aliases: ["TC-079"]
---

# TC-079 配置不完整或不合法，拒绝保存

## Preconditions 前置条件

必填配置缺失，或车型、电量阈值、调度权重等值不合法，或未选择任何模型版本。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存并逐项提示修正。

## Verifies 验证对象

[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] AC-4
