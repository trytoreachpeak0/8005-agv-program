---
id: TC-032
type: test-case
title: "跨 Sublot 复用工号且不重复验证"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-012"]
related_uc: ["UC-043", "UC-001", "UC-005", "UC-010", "UC-044"]
aliases: ["TC-032"]
---

# TC-032 跨 Sublot 复用工号且不重复验证

## Preconditions 前置条件

当前到站会话已保存一个通过校验的工号，且不存在活动、部分或未收敛的 Sublot。

## Test Steps 测试步骤

操作员输入并完成多个不同 Sublot，期间未主动更换工号。

## Expected Result 预期结果

系统不要求重复输入或校验工号；每个 Sublot 在首次仓位操作前绑定该工号，操作记录可追溯到同一操作员。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-2
