---
id: FR-010
type: functional-requirement
title: "Arrival Status Update and Operation Panel Navigation 到站状态更新与操作面板界面跳转"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-003"]
related_br: []
related_fr: []
related_nfr: []
related_tc: ["TC-025", "TC-026"]
aliases: ["FR-010"]
---

# FR-010 Arrival Status Update and Operation Panel Navigation 到站状态更新与操作面板界面跳转

## Description 需求描述

系统应当在收到 [[uc-009-monitor-move-order-until-arrival|UC-009]] 传递的到站事件确认后，将本地记录的该 AGV 状态由"移动中"更新为"已到站"，并触发操作面板界面自动跳转到该站点对应的装卸操作界面，作为 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-006-cancel-transport-task-upon-arrival|UC-006]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等后续站点操作的入口。

## Rationale 制定原因

到站状态更新与界面跳转是后续所有站点操作的唯一入口：若状态未及时更新或界面未跳转，操作员将无法感知到站、无法发起任何后续装卸/取消/核验动作。将 [[uc-003-agv-arrives-at-designated-station|UC-003]] Normal Flow 中的两个系统动作落实为可单独验收的能力切片。

## Origin 需求来源

- [[uc-003-agv-arrives-at-designated-station|UC-003]] Normal Flow 第 2、3 步及 Postcondition 第 2、3 条

## Acceptance Criteria 验收标准

- **AC-1（到站后状态更新为已到站）**
  - **Given** 系统接收到 [[uc-009-monitor-move-order-until-arrival|UC-009]] 传递的到站事件确认
  - **When** 系统处理该到站事件
  - **Then** 本地记录的该 AGV 状态由"移动中"更新为"已到站"

- **AC-2（界面自动跳转装卸操作界面）**
  - **Given** 该 AGV 状态已更新为"已到站"
  - **When** 系统完成状态更新
  - **Then** 操作面板界面自动跳转到该站点对应的装卸操作界面，不需要操作员手动操作

## Related 关联

- **Use Cases：** 支撑 [[uc-003-agv-arrives-at-designated-station|UC-003]]；本 FR 的界面跳转结果是 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-006-cancel-transport-task-upon-arrival|UC-006]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等 UC 的 Trigger 来源
- **Business Rules：** 无——UC-003 本身不实现 [[br-001-dispatch-task-range|BR-001]]（"派车任务范围"），仅在 Notes 中提及该规则是从本 UC 拆分出去的，因此本 FR 不登记
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 无（见下方 Notes 说明）

## Verification 验证方式

- [[TC-025|TC-025]]：到站后状态更新为已到站
- [[TC-026|TC-026]]：界面自动跳转装卸操作界面

## Notes 备注

- 本 FR 不登记 `related_nfr`：[[uc-003-agv-arrives-at-designated-station|UC-003]] 的 Postcondition 未显式要求记录审计（与 UC-001/UC-002/UC-005/UC-006/UC-010/UC-043/UC-044 明确写"记录到本地数据库用于追溯"不同），保持"不是每条 FR 都需要 NFR"的既定原则，不强行附加。
- 本 FR 不与本批其他 FR（FR-011~FR-014）配对：UC-003 与 UC-043/UC-044 在语义上彼此独立，仅存在"到站 → 操作会话建立"的时间先后关系，不属于同一能力切片的拆分。
