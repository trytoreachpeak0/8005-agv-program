---
id: TC-007
type: test-case
title: "资格核验通过"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-005"]
related_uc: ["UC-005"]
aliases: ["TC-007"]
---

# TC-007 资格核验通过

## Preconditions 前置条件

目标子批号关联的全部仓位当前状态均为"已占用"，且其关联任务尚未通过 UC-002 确认完成。

## Test Steps 测试步骤

操作员选择该子批号，发起"取出"请求。

## Expected Result 预期结果

系统判定核验通过，进入批量开锁（转 FR-006）。

## Verifies 验证对象

[[fr-005-mis-stored-retrieval-eligibility-check|FR-005]] AC-1
