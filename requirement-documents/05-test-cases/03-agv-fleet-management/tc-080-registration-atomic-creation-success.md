---
id: TC-080
type: test-case
title: "校验通过，原子创建档案、绑定快照、生成仓位实例并记录审计"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-026"]
related_uc: ["UC-019"]
aliases: ["TC-080"]
---

# TC-080 校验通过，原子创建档案、绑定快照、生成仓位实例并记录审计

## Preconditions 前置条件

[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] 的全部校验均已通过，管理员已确认保存。

## Test Steps 测试步骤

系统执行接入事务。

## Expected Result 预期结果

系统在同一事务中创建本地 AGV 档案（含 RCS/RIOT 车辆 ID 映射、本地配置、绑定的模型型号/版本号/内容校验值快照）、按快照生成对应仓位实例记录、将 AGV 置为"已禁用"，并记录审计日志；管理员被提示完成检查后可通过 UC-013 启用车辆。

## Verifies 验证对象

[[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]] AC-1
