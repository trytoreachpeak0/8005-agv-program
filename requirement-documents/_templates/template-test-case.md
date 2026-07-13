<%*
const tcNum = await tp.system.prompt("测试用例编号数字部分（3位，如 001）", "");
const tcId = "TC-" + tcNum.padStart(3, "0");
const tcTitle = await tp.system.prompt("测试用例标题", "");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% tcId %>
type: test-case
title: "<% tcTitle %>"
status: draft
created: <% today %>
updated: <% today %>
related_fr: []
related_uc: []
aliases: ["<% tcId %>"]
---

# <% tcId %> <% tcTitle %>

## Preconditions 前置条件

TBD 待补充

## Test Steps 测试步骤

TBD 待补充

## Expected Result 预期结果

TBD 待补充

## Verifies 验证对象

TBD 待补充（如：[[FR-001|FR-001]]）
