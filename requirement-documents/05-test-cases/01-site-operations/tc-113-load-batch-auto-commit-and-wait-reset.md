---
id: TC-113
type: test-case
title: "LoadBatch 物理闭环后自动提交并重新计时"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002", "FR-031"]
related_uc: ["UC-001", "UC-046"]
aliases: ["TC-113"]
---

# TC-113 LoadBatch 物理闭环后自动提交并重新计时

## Preconditions 前置条件

一个三仓 LoadBatch 已完成前两个目标仓位，第三仓正在装货；服务端没有收到任何人工批次确认。

## Test Steps 测试步骤

使第三仓达到 `OCCUPIED + 锁闭 + 开锁输出已复位` 且安全状态有效。

## Expected Result 预期结果

服务端自动整体提交 LoadBatch，不等待额外的人工批次确认；车辆重新进入 StationDepartureWaiting 并建立完整的新等待期限。StopClosureCommit 前，已核验操作员仍可按 FR-005 对原仓位请求 LoadCorrection。

## Verifies 验证对象

FR-002 AC-5、FR-031 AC-2
