---
id: TC-108
type: test-case
title: "断联使截止时间失效"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-046"]
aliases: ["TC-108"]
---

# TC-108 断联使截止时间失效

## Preconditions 前置条件

离站等待正在倒计时。

## Test Steps 测试步骤

1. 使 VehicleConnectionSession 失效并跨过原截止时间。
2. 恢复连接，完成 RecoveryHandshake 和最新投影对账。

## Expected Result 预期结果

断联期间不取消、不发车；恢复后建立完整的新等待期限，不沿用原截止时间。

## Verifies 验证对象

FR-031 AC-9
