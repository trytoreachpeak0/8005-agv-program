---
id: TC-011
type: test-case
title: "原仓位重放成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-011"]
---

# TC-011 原仓位重放成功

## Preconditions 前置条件

所选原仓位已打开；操作员已取出错误产品并把正确产品放回原仓位。

## Test Steps 测试步骤

操作员关门，系统取得有效锁闭反馈、稳定 OCCUPIED 与开锁输出复位。

## Expected Result 预期结果

系统可靠记录 LoadCorrectionResult；仓位—SUBLOT 映射、原 SlotOperationAttemptId 与既有 LoadBatch 提交事实不变，并恢复剩余装货或重新进入 StationDepartureWaiting。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-3
