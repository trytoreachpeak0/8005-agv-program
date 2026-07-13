<%*
const drNum = await tp.system.prompt("决策记录编号数字部分（3位，如 001）", "");
const drId = "DR-" + drNum.padStart(3, "0");
const drTitle = await tp.system.prompt("决策标题", "");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% drId %>
type: decision-record
title: "<% drTitle %>"
status: decided
created: <% today %>
updated: <% today %>
related_fr: []
related_uc: []
aliases: ["<% drId %>"]
---

# <% drId %> <% drTitle %>

## Decision 决策

TBD 待补充

## Rationale 理由

TBD 待补充

## Alternatives Considered 备选方案

TBD 待补充（如有）

## Related 关联

TBD 待补充
