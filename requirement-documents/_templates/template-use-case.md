<%*
const ucNum = await tp.system.prompt("用例编号数字部分（3位，如 006）", "");
const ucId = "UC-" + ucNum.padStart(3, "0");
const ucNameEn = await tp.system.prompt("Use Case Name 用例名称（英文）", "");
const ucNameCn = await tp.system.prompt("用例名称（中文）", "");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% ucId %>
type: use-case
title: "<% ucNameEn %> <% ucNameCn %>"
status: draft
priority: TBD
created_by: TBD
updated_by: TBD
created: <% today %>
updated: <% today %>
primary_actor: TBD
secondary_actor: TBD
frequency: TBD
related_uc: []
related_br: []
aliases: ["<% ucId %>"]
---

# <% ucId %> <% ucNameEn %> <% ucNameCn %>

## Description 描述

TBD 待补充

## Trigger 触发条件

TBD 待补充

## Precondition 前置条件

TBD 待补充

## Postcondition 后置条件

TBD 待补充

## Assumption 假设

TBD 待补充

## Normal Flow 正常流程

TBD 待补充

## Alternative Flow 备选流程

TBD 待补充

## Exception Flow 异常流程

TBD 待补充

## Notes 备注

TBD 待补充

## Related Use Cases 关联用例

TBD 待补充

## Other Information 其他信息


