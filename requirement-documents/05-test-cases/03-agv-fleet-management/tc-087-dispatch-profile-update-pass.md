---
id: TC-087
type: test-case
title: "核验与校验均通过，展示差异并保存"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-028"]
related_uc: ["UC-020"]
aliases: ["TC-087"]
---

# TC-087 核验与校验均通过，展示差异并保存

## Preconditions 前置条件

目标 AGV 已通过 UC-019 接入且未归档，处于"已禁用"，本地无未完成任务或站点作业，所有仓门均已确认关闭。

## Test Steps 测试步骤

管理员修改身份映射、车型、服务区域、电量阈值、调度权重或备注，系统校验 RCS/RIOT 车辆 ID、配置完整性、数值范围与内部一致性均通过。

## Expected Result 预期结果

系统展示修改前后差异，管理员确认后保存新配置，记录审计日志，并提示车辆仍处于禁用状态。

## Verifies 验证对象

[[fr-028-agv-dispatch-profile-update-eligibility-and-persistence|FR-028]] AC-1
