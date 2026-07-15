---
id: TC-032
type: test-case
title: "会话内复用不重复验证身份"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-012"]
related_uc: ["UC-043", "UC-001", "UC-005", "UC-010", "UC-044"]
aliases: ["TC-032"]
---

# TC-032 会话内复用不重复验证身份

## Preconditions 前置条件

当前站点/终端存在有效操作会话。

## Test Steps 测试步骤

操作员在会话内执行一次或多次 [[uc-001-load-completed-lot-into-slot|UC-001]]/[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]/[[uc-010-unload-completed-lot-at-destination-station|UC-010]]/[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 等仓门操作。

## Expected Result 预期结果

系统复用当前会话，不要求重复验证身份，但该操作记录须关联当前会话的操作人身份。

## Verifies 验证对象

[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] AC-2
