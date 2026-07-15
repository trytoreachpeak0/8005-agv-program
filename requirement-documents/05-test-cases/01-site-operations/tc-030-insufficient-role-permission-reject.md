---
id: TC-030
type: test-case
title: "岗位权限不足，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-011"]
related_uc: ["UC-043"]
aliases: ["TC-030"]
---

# TC-030 岗位权限不足，拒绝

## Preconditions 前置条件

MES 返回有效的人员身份。

## Test Steps 测试步骤

该人员岗位权限不满足当前站点/场景所需的操作权限。

## Expected Result 预期结果

系统不建立会话，提示"当前人员权限不足，无法在本站点操作"。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-4
