---
id: TC-121
type: test-case
title: "班组长审批不替换 Sublot 生产操作员"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-012"]
related_uc: ["UC-043", "UC-001"]
aliases: ["TC-121"]
---

# TC-121 班组长审批不替换 Sublot 生产操作员

## Preconditions 前置条件

活动 Sublot 已绑定生产操作员 A，OperationSession 和 OnboardOperatorContext 有效；LoadBatch 因关键硬件故障处于 VehicleRecoveryRequired。R-09 B 具有整批清空决定权限。

## Test Steps 测试步骤

R-09 B 在生产操作员 A 的当前作业界面刷自己的卡，通过二次认证并作出 LoadCompensationDecision。

## Expected Result 预期结果

系统记录 A 为该 Sublot 的生产操作员、B 为 LoadCompensationDecision 决策人；A 的 Sublot 绑定和 OnboardOperatorContext 保持不变，OperationSession 不退出、不重建且不转移给 B。后续补偿仍须由操作员发起并取得服务端授权。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-5
