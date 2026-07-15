---
id: TC-066
type: test-case
title: "行/列/跨格非正整数或矩形越界，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-022"]
related_uc: ["UC-038"]
aliases: ["TC-066"]
---

# TC-066 行/列/跨格非正整数或矩形越界，拒绝保存

## Preconditions 前置条件

操作人员提交的草稿中，某仓位的起始行、起始列、跨行数或跨列数为零、负数，或超出所属面的行数/列数范围。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存，提示具体仓位及越界原因。

## Verifies 验证对象

[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] AC-3
