---
id: TC-073
type: test-case
title: "认证通过，原子停用且历史引用不受影响"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_fr: ["FR-024"]
related_uc: ["UC-038"]
aliases: ["TC-073"]
---

# TC-073 认证通过，原子停用且历史引用不受影响

## Preconditions 前置条件

操作人员已为某个 `Published` 版本填写非空停用原因，并已查看当前引用该版本的 AGV 数量及清单。

## Test Steps 测试步骤

操作人员再次刷卡或认证成功。

## Expected Result 预期结果

系统原子地将该版本置为 `Retired`，记录审计；该版本不再允许被 UC-019 选用于新接入，已引用该版本的历史 AGV 及其仓位实例保持不变、继续有效。

## Verifies 验证对象

[[fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation|FR-024]] AC-1
