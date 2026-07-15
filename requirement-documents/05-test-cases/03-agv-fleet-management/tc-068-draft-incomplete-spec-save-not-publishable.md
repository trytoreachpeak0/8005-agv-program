---
id: TC-068
type: test-case
title: "规格缺失或不合法，允许暂存草稿但标记未达发布条件"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-022"]
related_uc: ["UC-038"]
aliases: ["TC-068"]
---

# TC-068 规格缺失或不合法，允许暂存草稿但标记未达发布条件

## Preconditions 前置条件

操作人员提交的草稿已通过唯一性、越界、重叠三类格式校验，但某仓位的尺寸或最大载重未填写，或数值不合法（如负数）。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统仍保存为 `Draft`，同时展示尚未满足的发布条件，不允许该草稿被直接发布。

## Verifies 验证对象

[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] AC-5
