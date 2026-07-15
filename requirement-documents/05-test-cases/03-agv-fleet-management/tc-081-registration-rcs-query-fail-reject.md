---
id: TC-081
type: test-case
title: "RCS/RIOT 车辆列表查询失败，不允许凭空创建"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-026"]
related_uc: ["UC-019"]
aliases: ["TC-081"]
---

# TC-081 RCS/RIOT 车辆列表查询失败，不允许凭空创建

## Preconditions 前置条件

管理员正在接入流程中。

## Test Steps 测试步骤

系统无法取得完整的 RCS/RIOT 车辆列表。

## Expected Result 预期结果

系统不允许凭空手工创建 RCS 车辆 ID，提示接口异常并记录日志。

## Verifies 验证对象

[[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]] AC-2
