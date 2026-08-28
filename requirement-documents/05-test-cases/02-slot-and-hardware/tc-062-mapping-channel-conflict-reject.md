---
id: TC-062
type: test-case
title: "通道重复占用，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-021"]
related_uc: ["UC-039"]
aliases: ["TC-062"]
---

# TC-062 通道重复占用，拒绝保存

## Preconditions 前置条件

操作人员提交的配置中，某 IO 模块的某通道号已被本仓位其他点位类型或另一仓位占用。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存，提示冲突的具体 IO 模块、通道号及已占用该通道的仓位/点位类型。

## Verifies 验证对象

[[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]] AC-2
