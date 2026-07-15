---
id: TC-091
type: test-case
title: "条件均满足，二次确认后归档成功"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-029"]
related_uc: ["UC-021"]
aliases: ["TC-091"]
---

# TC-091 条件均满足，二次确认后归档成功

## Preconditions 前置条件

目标 AGV 已禁用且未归档，不存在未结束的本地任务/作业，RCS/RIOT 队列为空，所有仓门关闭且关键安全状态正常可读取。

## Test Steps 测试步骤

系统展示归档影响后，管理员二次确认。

## Expected Result 预期结果

系统将该 AGV 标记为"已归档"，记录操作人、时间和原因；历史任务、仓位记录、配置版本和审计日志仍可查询，RCS/RIOT 中的车辆保持不变。

## Verifies 验证对象

[[fr-029-agv-archive-eligibility-check-and-state-transition|FR-029]] AC-1
