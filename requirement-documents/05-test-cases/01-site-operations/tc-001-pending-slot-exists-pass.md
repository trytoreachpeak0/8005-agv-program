---
id: TC-001
type: test-case
title: "存在待确认仓位，核验通过"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-003"]
related_uc: ["UC-002"]
aliases: ["TC-001"]
---

# TC-001 存在待确认仓位，核验通过

## Preconditions 前置条件

当前站点存在至少一个已装载或已取出、且仓门均已关闭的仓位。

## Test Steps 测试步骤

操作员点击"确认完成"按钮。

## Expected Result 预期结果

系统判定核验通过，进入批量确认（转 FR-004）。

## Verifies 验证对象

[[fr-003-confirm-completion-eligibility-check|FR-003]] AC-1
