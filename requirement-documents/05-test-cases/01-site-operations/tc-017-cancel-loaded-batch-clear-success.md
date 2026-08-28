---
id: TC-017
type: test-case
title: "已装货任务批量清空后取消"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-007"]
related_uc: ["UC-006"]
aliases: ["TC-017"]
---

# TC-017 已装货任务批量清空后取消

## Preconditions 前置条件

所选 DemandId 已部分或全部装货，车辆未离站；完整目标范围同时包含 OCCUPIED 与 EMPTY 仓位。

## Test Steps 测试步骤

操作员确认“清空并取消”，完成所有目标仓位的取出与关门。

## Expected Result 预期结果

车载端只批量打开所选 DemandId 的 OCCUPIED 仓位，跳过 EMPTY；完整目标范围全部证明 EMPTY 且机构安全后报告 ALL_EMPTY，服务端完成取消。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-2、AC-3
