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

MES 返回“人员不存在”、岗位权限不足，或因网络/接口异常无法返回结果。

## Expected Result 预期结果

系统不更新当前工号、不允许以该工号开始新的 Sublot，并记录失败审计；界面提示身份或权限核验失败。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-2
