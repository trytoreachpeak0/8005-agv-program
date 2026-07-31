---
id: TC-123
type: test-case
title: "装货补偿整批清空后统一取消搬运需求"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-123"]
---

# TC-123 装货补偿整批清空后统一取消搬运需求

## Preconditions 前置条件

准备三个分别使用 `HARDWARE_NOT_RECOVERABLE_ON_SITE`、`PRODUCTION_ABORTS_CURRENT_LOAD` 和 `OTHER` 的 LoadCompensationDecision；每个 LoadBatch 均已取得服务端授权。另准备一个尚有目标仓位未能证明 EMPTY 或安全锁闭的补偿操作。

## Test Steps 测试步骤

1. 三个不同原因码的操作分别完成全部目标仓位的 LoadCompensationRecovery，服务端接收并核验可靠的 LoadCompensationResult。
2. 查询各自的原 SlotOperationAttemptId、整批仓位预留、DemandId、取消抑制和后续派车状态。
3. 对尚未安全清空完整目标范围的操作上报不完整或状态不确定的结果。
4. 模拟 MES 在人工扫码过站前持续返回已完成补偿的相同 TransportDemandKey，并另行模拟同一 SUBLOT 命中其它任务类型。

## Expected Result 预期结果

三种原因下，原 SlotOperationAttemptId 都终结为 `COMPENSATED`，相关仓位预留均被释放，原 DemandId 均终结为 `CANCELLED_BY_LOAD_COMPENSATION`，对应 TransportDemandKey 被调度永久抑制，不得误记为 `CANCELLED_BY_OPERATOR`；MES 持续返回同键候选时 MesIngest 仍照常投影，调度不得创建或恢复业务任务、派车或创建补偿后重试尝试。原因码分别保留用于审计，但不改变业务后果。尚未证明整批安全清空的操作不得取消 DemandId、释放预留或允许车辆离站。同一 SUBLOT 命中其它任务类型时属于不同业务键，可正常处理。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.8
