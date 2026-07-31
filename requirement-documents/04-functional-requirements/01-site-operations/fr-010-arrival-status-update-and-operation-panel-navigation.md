---
id: FR-010
type: functional-requirement
title: "Arrival Overview and Work Projection Refresh 到站车辆概览与作业投影刷新"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-30
related_uc: ["UC-003"]
related_br: ["BR-001"]
related_fr: []
related_nfr: []
related_tc: ["TC-025", "TC-026"]
aliases: ["FR-010"]
---

# FR-010 Arrival Overview and Work Projection Refresh 到站车辆概览与作业投影刷新

## Description 需求描述

系统应当在收到 [[uc-009-monitor-move-order-until-arrival|UC-009]] 传递的可信到站事件后，把该站切换为当前停靠，刷新车载车辆概览（OnboardVehicleOverview）、当前停靠作业清单（CurrentStopWorklist）和后续停靠计划（UpcomingStopPlan），并自动跳转到本站作业界面。车载端不拥有任务或调度事实，但必须以只读方式知道本站全部待装、待卸作业以及接下来的业务停靠。

## Rationale 制定原因

只显示“已到站”不足以支持现场操作：操作员还需要知道本站要做什么、下一步去哪里，以及车辆是否通信就绪、正在作业或因安全联锁禁止移动。将这些信息作为相互独立的投影展示，可以在不把任务与调度权威下放到车载端的前提下提供完整现场认知。

## Origin 需求来源

- [[uc-003-agv-arrives-at-designated-station|UC-003]] Normal Flow 与 Postcondition
- [[br-001-dispatch-task-range|BR-001]] 后续停靠计划可见性

## Acceptance Criteria 验收标准

- **AC-1（到站后状态更新为已到站）**
  - **Given** 系统接收到 [[uc-009-monitor-move-order-until-arrival|UC-009]] 传递的到站事件确认
  - **When** 系统处理该到站事件
  - **Then** 本地记录的该 AGV 状态由"移动中"更新为"已到站"

- **AC-2（界面自动跳转装卸操作界面）**
  - **Given** 该 AGV 状态已更新为"已到站"
  - **When** 系统完成状态更新
  - **Then** 操作面板界面自动跳转到该站点对应的装卸操作界面，不需要操作员手动操作

- **AC-3（刷新当前停靠作业清单）**
  - **Given** 该站已被可信到站事件切换为当前停靠
  - **When** 服务端生成 CurrentStopWorklistSnapshot
  - **Then** 清单同时覆盖本次停靠已排定的待装任务和车上目标为本站的待卸任务；复合停靠时两类同时显示
  - **And** 每项至少显示 SUBLOT、作业类型、应处理/已完成/剩余数量、起终点、任务状态、可用操作和关联仓位摘要

- **AC-4（刷新后续停靠计划）**
  - **Given** 服务端已经为该车排定尚未到达的业务停靠
  - **When** 车载端应用 UpcomingStopPlanSnapshot
  - **Then** 按顺序显示站点、停靠目的、任务数量与摘要、计划状态，并仅在数据可信时显示 ETA
  - **And** 不显示 RIOT 路径节点，也不允许车载端编辑、换序或自行推导路线

- **AC-5（四维车辆概览互不覆盖）**
  - **Given** 车载作业界面正在显示该车状态
  - **When** 任一状态维度发生变化
  - **Then** 分别显示运行、通信与业务就绪、当前作业、安全与联锁四个维度
  - **And** 安全与联锁以车载实时 IO 为准；不安全时置顶显示“禁止移动”及具体原因

- **AC-6（离线快照只读且标记过期）**
  - **Given** 车载端与服务端失联
  - **When** 界面仍保留最后的作业清单或后续停靠计划
  - **Then** 明确标记“离线数据，可能已过期”
  - **And** 禁止基于旧快照开始、取消或扩展新的业务

- **AC-7（作业完成、发车、到站分别切换）**
  - **Given** 操作员已确认本站作业完成
  - **When** RIOT 尚未确认开始移动
  - **Then** 当前站保持“作业已完成，等待发车”
  - **When** RIOT 确认开始移动
  - **Then** 显示“正在前往”下一站，但不把下一站标记为当前站
  - **When** 下一站收到可信到站确认
  - **Then** 才将其切换为当前站并启用新的作业清单

## Related 关联

- **Use Cases：** 支撑 [[uc-003-agv-arrives-at-designated-station|UC-003]]；本 FR 的界面跳转结果是 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-006-cancel-transport-task-upon-arrival|UC-006]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等 UC 的 Trigger 来源
- **Business Rules：** [[br-001-dispatch-task-range|BR-001]] 定义服务端形成并调整后续业务停靠计划的边界
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 无（见下方 Notes 说明）

## Verification 验证方式

- [[TC-025|TC-025]]：到站后状态更新为已到站
- [[TC-026|TC-026]]：界面自动跳转装卸操作界面
- AC-3～AC-7 尚需新增对应测试用例，现有 TC-025/TC-026 不覆盖作业清单、后续停靠、四维概览与离线过期行为

## Notes 备注

- 本 FR 不登记 `related_nfr`：[[uc-003-agv-arrives-at-designated-station|UC-003]] 的 Postcondition 未显式要求记录审计（与 UC-001/UC-002/UC-005/UC-006/UC-010/UC-043/UC-044 明确写"记录到本地数据库用于追溯"不同），保持"不是每条 FR 都需要 NFR"的既定原则，不强行附加。
- 本 FR 不与本批其他 FR（FR-011~FR-014）配对：UC-003 与 UC-043/UC-044 在语义上彼此独立，仅存在"到站 → 操作会话建立"的时间先后关系，不属于同一能力切片的拆分。
