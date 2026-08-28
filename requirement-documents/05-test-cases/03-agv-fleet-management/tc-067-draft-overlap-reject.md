---
id: TC-067
type: test-case
title: "同一面内仓位矩形重叠，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-022"]
related_uc: ["UC-038"]
aliases: ["TC-067"]
---

# TC-067 同一面内仓位矩形重叠，拒绝保存

## Preconditions 前置条件

操作人员提交的草稿中，同一面内两个仓位的占用矩形存在共享的基础格。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存，提示冲突的仓位编号及重叠位置。

## Verifies 验证对象

[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] AC-4
