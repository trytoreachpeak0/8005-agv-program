<%*
const brNum = await tp.system.prompt("业务规则编号数字部分（3位，如 001）", "");
const brId = "BR-" + brNum.padStart(3, "0");
const brTitle = await tp.system.prompt("业务规则标题", "");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% brId %>
type: business-rule
title: "<% brTitle %>"
status: draft
created: <% today %>
updated: <% today %>
related_uc: []
aliases: ["<% brId %>"]
---

# <% brId %> <% brTitle %>

## Rule Statement 规则内容

TBD 待补充

## Rationale 制定原因

TBD 待补充

## Source 来源

TBD 待补充（如：客户访谈、法规、行业标准等）

## Related Use Cases 关联用例

TBD 待补充
