---
id: TC-109
type: test-case
title: "装货开始与超时竞态"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-046"]
aliases: ["TC-109"]
---

# TC-109 装货开始与超时竞态

## Preconditions 前置条件

倒计时即将届满，准备同一 DemandId 的合法装货开始请求。

## Test Steps 测试步骤

分别控制装货开始先持久化和超时结束先持久化。

## Expected Result 预期结果

装货先成功时超时失效；超时先成功时新装货请求被拒绝，任务保持取消且不复活；不存在两者同时成功。

## Verifies 验证对象

FR-031 AC-6
