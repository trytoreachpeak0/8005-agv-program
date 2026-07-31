---
id: FR-004
type: functional-requirement
title: "取出纠错场景支持"
status: review
created: 2026-07-09
updated: 2026-07-10
related_uc: ["UC-005"]
related_dr: ["DR-003", "DR-010", "DR-013", "DR-014"]
related_fr: ["FR-002", "FR-003", "FR-006", "FR-012"]
aliases: ["FR-004"]
---

# FR-004 取出纠错场景支持

## Description 需求描述

支持从光幕 DI 为“有遮挡”的仓位取出存错产品。开锁只能由主系统写 Modbus DO 发起；正常开锁后弹簧自动弹门，控制 API 再模拟取出和关门。

取出生效时清除实际光幕遮挡，光幕 DI 正常情况下立即变为"无遮挡"，仓位占用随即被推导为"空闲"，不要求等到关门。模拟器不独立存储占用状态。若光幕 DI 已注入延迟或不跟随故障，则派生占用只跟随当时可读的光幕 DI。

## Origin 需求来源

根目录 [UC-005 取出仓位中存错的产品](../../../requirement-documents/03-use-cases/uc-005-retrieve-mis-stored-product-from-slot.md)。

## Acceptance Criteria 验收标准

- 可由主系统对任意光幕 DI 为“有遮挡”的仓位写开锁 DO；门自动弹开且锁 DI 确认未锁后，通过控制 API 执行“取出→关门”。
- 取出生效时光幕 DI 立即变为"无遮挡"，派生占用立即为"空闲"，关门不是占用变化的前置条件。
- 控制 API 不提供开锁动作；门关闭时取出等非法迁移被拒绝，且状态保持不变。
- 支持 UC-005 异常分支：开锁失败、开门后发现仓位实际为空、关门后光幕仍检测到残留。

## Related Use Case 关联用例

[UC-005 取出仓位中存错的产品](../../../requirement-documents/03-use-cases/uc-005-retrieve-mis-stored-product-from-slot.md)。

## Verification 验证方式

- **TC-FR-004-001（预留）**：Given 光幕 DI 为有遮挡的仓位已通过 Modbus 开锁并自动弹门；When API 依次执行取出、关门；Then 光幕 DI 变为无遮挡，关门后锁 DI 变为锁闭。
- **TC-FR-004-002（预留）**：Given 仓位仍关闭；When API 请求取出；Then 请求被拒绝并返回原因，DO、DI、门状态与实际遮挡均不变。
- **TC-FR-004-003（预留）**：Given 仓位已开门但光幕 DI 为无遮挡；When API 请求取出；Then 返回"仓位实际为空"的明确结果，不制造独立占用状态，现有状态保持不变。
- **TC-FR-004-004（预留）**：Given 取出时已注入光幕 DI 不跟随；When API 执行取出并关门；Then 光幕 DI 仍显示有遮挡，派生占用仍为已占用，供主系统识别残留异常。
