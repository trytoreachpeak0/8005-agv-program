---
id: TC-107
type: test-case
title: "待卸任务阻断离站等待"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-031"]
related_uc: ["UC-010", "UC-046"]
aliases: ["TC-107"]
---

# TC-107 待卸任务阻断离站等待

## Preconditions 前置条件

分别准备纯卸货站，以及仍有待卸任务的装卸混合站。

## Test Steps 测试步骤

使仓位机构暂时 DepartureSafe，并观察离站等待。

## Expected Result 预期结果

待卸任务未完成时不启动离站等待；纯卸货站卸完直接结束，混合站完成卸货且服务端裁定仍可继续装货后才启动。

## Verifies 验证对象

FR-031 AC-8
