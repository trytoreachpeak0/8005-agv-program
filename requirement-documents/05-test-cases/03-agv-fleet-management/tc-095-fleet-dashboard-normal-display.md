---
id: TC-095
type: test-case
title: "正常展示车辆列表并按 BR-002 计算可分配结论"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-030"]
related_uc: ["UC-022"]
aliases: ["TC-095"]
---

# TC-095 正常展示车辆列表并按 BR-002 计算可分配结论

## Preconditions 前置条件

管理员打开 AGV 车队页面，本地档案、配置、本地作业状态，以及 RCS/RIOT 与仓门/光幕/安全状态均可正常读取。

## Test Steps 测试步骤

系统按 BR-002 计算每台车的可分配结论。

## Expected Result 预期结果

系统展示车辆列表（本地名称、RCS ID、车型、启停/归档状态、位置、电量、任务、仓门、可分配结论），管理员可打开详情查看完整配置、当前作业、状态时间戳和不可分配原因。

## Verifies 验证对象

[[fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning|FR-030]] AC-1
