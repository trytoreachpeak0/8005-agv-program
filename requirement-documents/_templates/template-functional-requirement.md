<%*
const frNum = await tp.system.prompt("功能需求编号数字部分（3位，如 001）", "");
const frId = "FR-" + frNum.padStart(3, "0");
const frTitle = await tp.system.prompt("功能需求标题", "");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% frId %>
type: functional-requirement
title: "<% frTitle %>"
status: draft
priority: TBD
created: <% today %>
updated: <% today %>
related_uc: []
related_br: []
related_tc: []
aliases: ["<% frId %>"]
---

# <% frId %> <% frTitle %>

## Description 需求描述

TBD 待补充

## Origin 需求来源

TBD 待补充（如：[[BR-001|BR-001]]、[[UC-001|UC-001]]）

## Acceptance Criteria 验收标准

TBD 待补充

## Related Use Case 关联用例

TBD 待补充

## Verification 验证方式

TBD 待补充（关联对应 Test Case，如 [[TC-001|TC-001]]）
