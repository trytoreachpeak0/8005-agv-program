---
id: TC-061
type: test-case
title: "校验通过，保存为待核对状态"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-021"]
related_uc: ["UC-039"]
aliases: ["TC-061"]
---

# TC-061 校验通过，保存为待核对状态

## Preconditions 前置条件

操作人员已为目标仓位实例录入或修改点位信息（开锁 DO、门状态 DI、光幕 DI）。

## Test Steps 测试步骤

系统校验通道号未被重复占用，且必填点位均已填写，操作人员确认保存。

## Expected Result 预期结果

系统将该仓位映射配置状态置为"待核对"，记录变更内容、操作人、时间戳。

## Verifies 验证对象

[[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]] AC-1
