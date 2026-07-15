---
id: TC-077
type: test-case
title: "所选模型版本不可用，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-025"]
related_uc: ["UC-019"]
aliases: ["TC-077"]
---

# TC-077 所选模型版本不可用，拒绝保存

## Preconditions 前置条件

管理员选择的模型版本当前处于 `Draft` 或 `Retired` 状态。

## Test Steps 测试步骤

系统校验该版本是否为 `Published`。

## Expected Result 预期结果

系统拒绝保存，提示"该型号版本不可用于接入"，引导管理员改选其他 `Published` 版本或联系型号维护人员发布新版本。

## Verifies 验证对象

[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] AC-2
