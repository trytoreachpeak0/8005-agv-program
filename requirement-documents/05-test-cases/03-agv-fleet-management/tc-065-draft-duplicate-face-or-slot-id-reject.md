---
id: TC-065
type: test-case
title: "面标识或仓位编号重复，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-022"]
related_uc: ["UC-038"]
aliases: ["TC-065"]
---

# TC-065 面标识或仓位编号重复，拒绝保存

## Preconditions 前置条件

操作人员提交的草稿中，存在重复的面标识或仓位编号。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存，提示冲突的具体标识。

## Verifies 验证对象

[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] AC-2
