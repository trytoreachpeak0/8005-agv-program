---
id: TC-114
type: test-case
title: "装货硬件故障保持现场，不换仓且不自动清空"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-114"]
---

# TC-114 装货硬件故障保持现场，不换仓且不自动清空

## Preconditions 前置条件

一个 `ExpectedBasketCount = 3` 的 LoadBatch 已冻结目标仓位 1、2、3 并发起批量开锁；仓位 1、2 已形成明确逐仓事实，其中至少一仓已放入花篮；仓位 3 的锁 DI 失效，无法证明仓门是否锁闭；另有空闲仓位 4。

## Test Steps 测试步骤

车载端上报仓位 3 的关键硬件反馈无效，服务端处理本次装货异常。

## Expected Result 预期结果

系统保留目标仓位 1、2、3、全部预留、ProvisionalLoadState 和逐仓事实；不得把仓位 4 分配为替代仓位，不得发送任何新增或续行开锁指令，也不得自动打开仓位 1、2 要求清空。StationOperationGuard 保持，车辆不得离站，系统进入待人工处置状态。只有取得 R-09 或等效生产管理权限作出的 LoadCompensationDecision 且服务端授权后，才允许进入 LoadCompensationRecovery。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4、AC-4.1
