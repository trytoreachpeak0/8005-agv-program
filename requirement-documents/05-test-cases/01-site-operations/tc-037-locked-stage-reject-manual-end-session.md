---
id: TC-037
type: test-case
title: "未结 Sublot 禁止本地强制清除"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-013"]
related_uc: ["UC-043"]
aliases: ["TC-037"]
---

# TC-037 未结 Sublot 禁止本地强制清除

## Preconditions 前置条件

存在暂停中、部分完成或尚未收敛的 Sublot，车载端保存有恢复日志。

## Test Steps 测试步骤

维护人员尝试在车载端删除操作上下文或强制结束会话。

## Expected Result 预期结果

系统允许查看诊断信息但拒绝删除恢复记录或清除工号，提示必须恢复连接并由服务端完成对账和处置。

## Verifies 验证对象

[[fr-013-session-termination-rules|FR-013]] AC-4
