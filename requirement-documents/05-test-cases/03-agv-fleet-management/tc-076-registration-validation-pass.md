---
id: TC-076
type: test-case
title: "模型版本、车辆 ID 与配置均校验通过，允许继续接入"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-025"]
related_uc: ["UC-019"]
aliases: ["TC-076"]
---

# TC-076 模型版本、车辆 ID 与配置均校验通过，允许继续接入

## Preconditions 前置条件

管理员已选择一台未接入的 RCS/RIOT 车辆，填写本地名称、车型、服务区域、最低接单电量、调度权重、维护备注，并独立选择某个多仓位 AGV 模型的一个版本。

## Test Steps 测试步骤

系统校验该模型版本处于 `Published` 状态、该车辆 ID 未被任何本地档案占用、必填配置均已填写且合法。

## Expected Result 预期结果

系统允许管理员确认保存，进入原子创建环节。

## Verifies 验证对象

[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] AC-1
