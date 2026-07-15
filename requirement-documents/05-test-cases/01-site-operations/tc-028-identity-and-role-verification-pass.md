---
id: TC-028
type: test-case
title: "身份与岗位权限核验通过"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-011"]
related_uc: ["UC-043"]
aliases: ["TC-028"]
---

# TC-028 身份与岗位权限核验通过

## Preconditions 前置条件

当前站点/终端不存在活动会话，操作员扫描工牌一维码或手动输入工号。

## Test Steps 测试步骤

系统提交 MES 核验人员身份及岗位权限，MES 返回有效的人员身份，且该人员岗位权限满足当前站点/场景所需的操作权限。

## Expected Result 预期结果

系统判定核验通过，进入会话建立（见 [[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]]）。

## Verifies 验证对象

[[fr-011-identity-and-role-verification-via-mes|FR-011]] AC-2
