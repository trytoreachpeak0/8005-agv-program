---
id: TC-003
type: test-case
title: "仓门未关好或光幕异常，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-003"]
related_uc: ["UC-002"]
aliases: ["TC-003"]
---

# TC-003 仓门未关好或光幕异常，拒绝

## Preconditions 前置条件

待确认仓位中存在仓门未关好，或光幕检测结果与系统记录状态不一致的情况。

## Test Steps 测试步骤

操作员点击"确认完成"按钮，系统核验待确认仓位的仓门/光幕状态。

## Expected Result 预期结果

系统拒绝本次确认，提示操作员先处理该仓位（对应 UC-002 Exception Flow E2.2）。

## Verifies 验证对象

[[fr-003-confirm-completion-eligibility-check|FR-003]] AC-3
