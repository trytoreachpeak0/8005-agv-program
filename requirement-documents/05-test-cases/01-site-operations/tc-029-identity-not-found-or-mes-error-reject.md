---
id: TC-029
type: test-case
title: "人员身份不存在或 MES 返回异常，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-011"]
related_uc: ["UC-043"]
aliases: ["TC-029"]
---

# TC-029 人员身份不存在或 MES 返回异常，拒绝

## Preconditions 前置条件

系统已提交扫码/工号至 MES 核验。

## Test Steps 测试步骤

MES 返回"人员不存在"，或因网络/接口异常无法返回结果。

## Expected Result 预期结果

系统不建立会话，提示"身份核验失败，请重新扫码或联系管理员"，不泄露具体失败原因是否为账号不存在。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-3
