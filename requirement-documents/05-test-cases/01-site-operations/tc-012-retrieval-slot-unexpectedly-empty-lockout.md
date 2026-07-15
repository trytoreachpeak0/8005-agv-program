---
id: TC-012
type: test-case
title: "打开后实际为空，异常锁定"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-006"]
related_uc: ["UC-005"]
aliases: ["TC-012"]
---

# TC-012 打开后实际为空，异常锁定

## Preconditions 前置条件

某仓位已打开，操作员核验发现该仓位内实际没有产品，与系统记录不一致。

## Test Steps 测试步骤

操作员上报该仓位状态异常。

## Expected Result 预期结果

系统将该仓位标记为"异常锁定"，暂停分配该仓位；该子批号关联的其他仓位不受影响，可正常继续取出流程（对应 UC-005 Exception Flow E3.2）。

## Verifies 验证对象

[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] AC-4
