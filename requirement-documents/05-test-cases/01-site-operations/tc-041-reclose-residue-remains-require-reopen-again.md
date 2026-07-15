---
id: TC-041
type: test-case
title: "重新关闭后仍有残留，要求再次打开"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-014"]
related_uc: ["UC-044"]
aliases: ["TC-041"]
---

# TC-041 重新关闭后仍有残留，要求再次打开

## Preconditions 前置条件

操作员重新关闭该仓位仓门后，光幕仍检测到产品残留。

## Test Steps 测试步骤

系统执行重新关闭后核验。

## Expected Result 预期结果

系统提示该仓位取出仍未完成，要求操作员再次重新打开该仓位确认，重复处理直至该仓位光幕确认已清空（对应 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] Exception Flow E6.1）。

## Verifies 验证对象

[[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]] AC-4
