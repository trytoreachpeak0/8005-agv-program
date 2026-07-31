---
id: TC-103
type: test-case
title: "离站等待开始与视觉提醒"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-046"]
aliases: ["TC-103"]
---

# TC-103 离站等待开始与视觉提醒

## Preconditions 前置条件

车辆位于可继续装货站点并满足 StationDepartureWaiting；项目默认等待 5 分钟，当前站无覆盖值。

## Test Steps 测试步骤

1. 服务端建立本轮截止时间。
2. 推进服务端时间至剩余 60 秒和 10 秒。

## Expected Result 预期结果

车载端全程显示剩余时间和到期取消任务数；最后 60 秒显示黄色，最后 10 秒显示红色并逐秒闪烁；不播放声音、不显示续时入口。

## Verifies 验证对象

FR-031 AC-1、AC-3、AC-4
