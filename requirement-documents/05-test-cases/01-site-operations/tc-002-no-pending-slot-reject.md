---
id: TC-002
type: test-case
title: "无待确认仓位，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-003"]
related_uc: ["UC-002"]
aliases: ["TC-002"]
---

# TC-002 无待确认仓位，拒绝

## Preconditions 前置条件

当前站点没有任何已装载或已取出（仓门已关闭）的仓位。

## Test Steps 测试步骤

操作员点击"确认完成"按钮。

## Expected Result 预期结果

系统拒绝执行本次确认，提示"当前无可确认的装载/取出内容"（对应 UC-002 Exception Flow E2.1）。

## Verifies 验证对象

[[fr-003-confirm-completion-eligibility-check|FR-003]] AC-2
