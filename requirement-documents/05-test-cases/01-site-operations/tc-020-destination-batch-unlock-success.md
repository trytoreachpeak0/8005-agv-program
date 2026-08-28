---
id: TC-020
type: test-case
title: "批量开锁成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-008"]
related_uc: ["UC-010"]
aliases: ["TC-020"]
---

# TC-020 批量开锁成功

## Preconditions 前置条件

AGV 未在移动；服务端已生成覆盖一个或多个 Sublot 的本站点待卸货仓位集合，且目标仓位分布在一个或多个 IO 模块。

## Test Steps 测试步骤

车载端按 IO 模块对目标仓位分组：同一模块内使用 Modbus 功能码 `0x0F` 一次写入多个连续线圈；多个模块并行下发批量开锁命令。

## Expected Result 预期结果

所有下发成功的目标仓位由弹簧结构自动弹门，锁 DI 变为未锁；界面按仓位展示结果，允许操作员尽快取走全部目标产品，而不是逐门等待和确认。

## Verifies 验证对象

[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] AC-3、AC-6
