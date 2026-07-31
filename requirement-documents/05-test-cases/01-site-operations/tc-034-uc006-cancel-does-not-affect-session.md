---
id: TC-034
type: test-case
title: "未收敛操作无进展、掉线和重启不清除上下文"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043", "UC-006"]
aliases: ["TC-034"]
---

# TC-034 未收敛操作无进展、掉线和重启不清除上下文

## Preconditions 前置条件

车载端已持久化当前工号、部分或待恢复 Sublot 和执行日志，车辆不满足 StationDepartureWaiting。

## Test Steps 测试步骤

依次模拟物理操作长时间无进展、车载端与服务端掉线以及车载程序重启。

## Expected Result 预期结果

系统只产生中断告警，不以离站等待超时结束会话；重启后恢复当前工号、活动 Sublot 和执行日志，不重复验证工号。掉线期间不开始新的仓位操作。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-1
