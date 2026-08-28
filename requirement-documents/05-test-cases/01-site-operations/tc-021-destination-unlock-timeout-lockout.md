---
id: TC-021
type: test-case
title: "多模块批量开锁部分失败"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-008"]
related_uc: ["UC-010"]
aliases: ["TC-021"]
---

# TC-021 多模块批量开锁部分失败

## Preconditions 前置条件

目标仓位分布在多个 IO 模块，其中一个模块通信失败；另一个模块批量写入成功，但其中某个仓位的锁 DI 未变为未锁。

## Test Steps 测试步骤

车载端记录各模块命令结果，并逐仓位读取锁 DI 核验实际开锁结果。

## Expected Result 预期结果

系统按仓位记录部分成功结果：已确认打开的仓位可继续卸货；通信失败模块中的仓位标记为结果未知并等待通信恢复后核验；锁 DI 未变化的仓位报告“开锁或弹门失败”，暂停该仓位后续操作。不得把整批误判为全成功或全失败。

## Verifies 验证对象

[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] AC-4、AC-6
