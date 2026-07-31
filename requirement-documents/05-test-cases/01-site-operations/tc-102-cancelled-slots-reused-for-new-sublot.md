---
id: TC-102
type: test-case
title: "取消释放仓位供新 SUBLOT 复用"
status: draft
created: 2026-07-30
updated: 2026-07-30
related_fr: ["FR-007"]
related_uc: ["UC-001", "UC-006"]
aliases: ["TC-102"]
---

# TC-102 取消释放仓位供新 SUBLOT 复用

## Preconditions 前置条件

SUBLOT-A 已完成清空取消，服务端已发布包含取消终态和释放仓位的新版 CurrentStopWorklistSnapshot；SUBLOT-B 仍保留在其它仓位。

## Test Steps 测试步骤

操作员提交新的合法 SUBLOT-C。

## Expected Result 预期结果

系统允许 C 使用 A 释放的仓位，B 保持不变；A 的 DemandId 终态与调度侧 TransportDemandKey 永久抑制保持。MES 继续返回同键候选时 MesIngest 仍照常投影，调度不得创建或恢复业务任务；同一 SUBLOT 以后命中其它任务类型时不受本次抑制影响。

## Verifies 验证对象

[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]] AC-8
