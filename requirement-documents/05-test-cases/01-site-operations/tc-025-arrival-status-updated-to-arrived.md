---
id: TC-025
type: test-case
title: "到站后状态更新为已到站"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-010"]
related_uc: ["UC-003"]
aliases: ["TC-025"]
---

# TC-025 到站后状态更新为已到站

## Preconditions 前置条件

系统接收到 [[uc-009-monitor-move-order-until-arrival|UC-009]] 传递的到站事件确认。

## Test Steps 测试步骤

系统处理该到站事件。

## Expected Result 预期结果

本地记录的该 AGV 状态由"移动中"更新为"已到站"。

## Verifies 验证对象

[[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]] AC-1
