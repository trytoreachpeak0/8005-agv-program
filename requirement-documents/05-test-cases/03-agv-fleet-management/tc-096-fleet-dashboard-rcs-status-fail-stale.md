---
id: TC-096
type: test-case
title: "外部状态读取失败，保留旧数据并标记过期未知"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-030"]
related_uc: ["UC-022"]
aliases: ["TC-096"]
---

# TC-096 外部状态读取失败，保留旧数据并标记过期未知

## Preconditions 前置条件

管理员正在查看或刷新车队页面。

## Test Steps 测试步骤

RCS/RIOT 状态读取失败。

## Expected Result 预期结果

系统保留最近一次状态及其时间戳，明确标记为过期/未知，将该车辆判定为不可分配，记录接口异常并告警。

## Verifies 验证对象

[[fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning|FR-030]] AC-2
