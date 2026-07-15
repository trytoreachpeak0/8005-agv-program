---
id: TC-078
type: test-case
title: "车辆已接入，拒绝重复创建"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-025"]
related_uc: ["UC-019"]
aliases: ["TC-078"]
---

# TC-078 车辆已接入，拒绝重复创建

## Preconditions 前置条件

目标 RCS/RIOT 车辆 ID 已存在于本地未归档或已归档的档案中。

## Test Steps 测试步骤

系统校验车辆 ID 唯一性。

## Expected Result 预期结果

系统拒绝重复创建，并引导管理员查看现有档案。

## Verifies 验证对象

[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] AC-3
