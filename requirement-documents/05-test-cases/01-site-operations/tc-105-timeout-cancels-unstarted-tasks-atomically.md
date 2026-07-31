---
id: TC-105
type: test-case
title: "超时原子取消本站未开始任务"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031", "FR-004"]
related_uc: ["UC-046"]
aliases: ["TC-105"]
---

# TC-105 超时原子取消本站未开始任务

## Preconditions 前置条件

车辆已提交一个 LoadBatch，本站仍有两个尚未开始的待装 DemandId，且持续满足 StationDepartureWaiting。

## Test Steps 测试步骤

让等待期限届满。

## Expected Result 预期结果

本站结束与两个任务的 `CANCELLED_BY_STATION_TIMEOUT`、取消抑制和系统审计原子持久化；已提交 LoadBatch 保持不变。任一写入失败时整笔回滚，车辆不离站。

## Verifies 验证对象

FR-031 AC-5
