---
id: TC-030
type: test-case
title: "8005 卸货不要求工号"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-011"]
related_uc: ["UC-043"]
aliases: ["TC-030"]
---

# TC-030 8005 卸货不要求工号

## Preconditions 前置条件

8005 项目车辆到达允许卸货的站点，服务端已生成本站点待卸货仓位集合。

## Test Steps 测试步骤

操作员进入卸货操作。

## Expected Result 预期结果

系统不要求扫描或输入工号，也不调用 MES 做卸货身份核验；审计记录项目的卸货身份核验策略处于关闭状态。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-4
