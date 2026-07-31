---
id: TC-063
type: test-case
title: "必填点位缺失，拒绝保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-021"]
related_uc: ["UC-039"]
aliases: ["TC-063"]
---

# TC-063 必填点位缺失，拒绝保存

## Preconditions 前置条件

操作人员提交的配置中，开锁 DO 点位或锁状态 DI 点位未填写。

## Test Steps 测试步骤

系统执行保存前校验。

## Expected Result 预期结果

系统拒绝保存，提示缺失的具体点位类型。

## Verifies 验证对象

[[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]] AC-3
