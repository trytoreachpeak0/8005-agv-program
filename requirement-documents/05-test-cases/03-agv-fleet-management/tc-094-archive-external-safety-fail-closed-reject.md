---
id: TC-094
type: test-case
title: "外部或安全状态不满足，fail-closed 拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-029"]
related_uc: ["UC-021"]
aliases: ["TC-094"]
---

# TC-094 外部或安全状态不满足，fail-closed 拒绝

## Preconditions 前置条件

目标 AGV 的 RCS/RIOT 队列不为空、任一仓门打开，或任一关键安全状态未知/异常。

## Test Steps 测试步骤

管理员发起归档。

## Expected Result 预期结果

系统采用 fail-closed，拒绝归档并显示具体原因。

## Verifies 验证对象

[[fr-029-agv-archive-eligibility-check-and-state-transition|FR-029]] AC-4
