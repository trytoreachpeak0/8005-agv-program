---
id: TC-008
type: test-case
title: "资格核验不通过，拒绝"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-005"]
related_uc: ["UC-005"]
aliases: ["TC-008"]
---

# TC-008 资格核验不通过，拒绝

## Preconditions 前置条件

目标子批号关联的仓位中存在非"已占用"状态的仓位，或该子批号对应任务已通过 UC-002 确认完成。

## Test Steps 测试步骤

操作员选择该子批号，发起"取出"请求。

## Expected Result 预期结果

系统拒绝本次取出请求，提示"当前不可取出"（对应 UC-005 Exception Flow E2.1）。

## Verifies 验证对象

[[fr-005-mis-stored-retrieval-eligibility-check|FR-005]] AC-2
