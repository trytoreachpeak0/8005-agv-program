---
id: FR-016
type: functional-requirement
title: "Slot Enable/Disable Batch Eligibility and State Update 仓位启用/禁用批量核验与状态更新"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-30
related_uc: ["UC-014"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-044", "TC-045", "TC-046", "TC-047"]
aliases: ["FR-016"]
---

# FR-016 Slot Enable/Disable Batch Eligibility and State Update 仓位启用/禁用批量核验与状态更新

## Description 需求描述

系统对批量启用/禁用请求逐仓核验并独立处理。禁用无活动、预留或内容的仓位时立即生效；存在活动 Sublot、预留或业务内容时进入待禁用（Disable Pending），阻止新分配但不撤销既有业务，待业务确认结束后自动禁用。启用只改变服务端仓位管理可用性，不能覆盖车载仓位可操作性。

管理状态变化须可靠同步到车载端；同步和对账完成前不得用于新 Sublot。HMI 在固定物理位置显示管理状态和硬件可操作性。

## Acceptance Criteria 验收标准

- **AC-1（立即禁用）**
  - **Given** 仓位无活动、预留和业务内容
  - **When** 操作人员禁用
  - **Then** 立即置为已禁用并阻止新分配
- **AC-2（待禁用）**
  - **Given** 仓位已被活动 Sublot 使用、预留或载有产品
  - **When** 操作人员禁用
  - **Then** 置为待禁用，既有业务继续、新业务禁止；业务确认结束后自动转已禁用
- **AC-3（启用不覆盖硬件故障）**
  - **Given** 服务端管理禁用且车载仓位不可操作
  - **When** 操作人员启用
  - **Then** 清除管理禁用，但最终仍因车载硬件不可操作而不可使用
- **AC-4（批量独立结果）**
  - **Then** 每个仓位分别返回立即生效、待生效、已启用或失败原因，并记录审计

## Notes 备注

- 人工禁用是业务管理策略；硬件故障由车载端立即形成 SlotOperability，不走待禁用。
- 仓位身份和 HMI 位置不随管理状态变化。
