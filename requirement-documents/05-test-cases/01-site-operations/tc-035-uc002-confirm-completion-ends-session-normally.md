---
id: TC-035
type: test-case
title: "完成 Sublot 后保留工号并允许换人"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043", "UC-002"]
aliases: ["TC-035"]
---

# TC-035 完成 Sublot 后保留工号并允许换人

## Preconditions 前置条件

当前 Sublot 已完成全部目标仓位并形成 LoadBatch 自动提交闭环。

## Test Steps 测试步骤

操作员先查看当前工号，然后主动输入另一个工号。

## Expected Result 预期结果

Sublot 完成时原工号仍被保留；系统允许发起换人，但新工号必须通过服务端/MES 校验后才能作为后续 Sublot 的默认操作员。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-2
