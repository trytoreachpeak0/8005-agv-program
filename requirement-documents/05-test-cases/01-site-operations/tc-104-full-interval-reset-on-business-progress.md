---
id: TC-104
type: test-case
title: "有效业务进展后重新计满"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-046"]
aliases: ["TC-104"]
---

# TC-104 有效业务进展后重新计满

## Preconditions 前置条件

离站等待只剩 1 分钟。

## Test Steps 测试步骤

分别验证 LoadBatch 自动提交、LoadCorrection 安全闭环，以及新增待装 DemandId 的新版作业清单被车载确认。

## Expected Result 预期结果

每种事件均建立完整的新 5 分钟期限，不沿用旧的 1 分钟；普通状态刷新和排序变化不重置。

## Verifies 验证对象

FR-031 AC-2
