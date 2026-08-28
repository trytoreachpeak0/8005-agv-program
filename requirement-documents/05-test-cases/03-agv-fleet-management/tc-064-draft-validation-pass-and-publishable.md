---
id: TC-064
type: test-case
title: "格式校验与规格均通过，保存为可发布的 Draft"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-022"]
related_uc: ["UC-038"]
aliases: ["TC-064"]
---

# TC-064 格式校验与规格均通过，保存为可发布的 Draft

## Preconditions 前置条件

操作人员已为某型号的 `Draft` 版本配置面列表及仓位定义（编号、所属面、起始行/列、跨行数/跨列数、规格）。

## Test Steps 测试步骤

系统校验面标识与仓位编号均唯一、行列与跨格均为正整数且矩形不越界、同一面内仓位矩形互不重叠，且每个仓位的规格字段均已填写完整。

## Expected Result 预期结果

系统保存为 `Draft`，且该版本满足后续发布所需的字段完整性条件。

## Verifies 验证对象

[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] AC-1
