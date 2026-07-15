---
id: FR-004
type: functional-requirement
title: "Batch Task Completion, Session Closure and Non-Reversibility 批量确认完成、会话结束与不可撤销"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-002"]
related_br: []
related_fr: ["FR-003"]
related_nfr: ["NFR-002"]
related_tc: ["TC-004", "TC-005", "TC-006"]
aliases: ["FR-004"]
---

# FR-004 Batch Task Completion, Session Closure and Non-Reversibility 批量确认完成、会话结束与不可撤销

## Description 需求描述

系统应当在 [[fr-003-confirm-completion-eligibility-check|FR-003]] 核验通过后，将当前站点所有已装载或已取出（仓门已关闭）仓位对应的进行中任务状态一次性批量更新为"已完成"，并记录本次确认操作（操作员、任务、仓位、时间戳）。若本次到站操作会话（见 [[uc-043-verify-identity-and-manage-operation-session|UC-043]]）处于"仓门操作已锁定"阶段，确认完成须同时结束该会话，使界面恢复为"未验证"状态。已完成的确认操作不支持撤销：即使操作员事后发现误确认，系统也必须拒绝任何撤销请求。

## Rationale 制定原因

批量确认是本次到站收尾的唯一正常出口，必须保证任务状态、会话状态和审计记录三者原子一致；不支持撤销是因为确认完成即意味着 AGV 准备移动到下一站点，撤销与"AGV 是否已经/即将移动"存在冲突（见 UC-002 Notes）。

## Origin 需求来源

- [[uc-002-confirm-task-completion|UC-002]] Normal Flow 第 3、3.1、4 步、Postcondition 第 1~3 条及 Exception Flow E3.1

## Acceptance Criteria 验收标准

- **AC-1（批量确认成功并记录）**
  - **Given** FR-003 核验已通过
  - **When** 系统执行批量确认
  - **Then** 该站点所有待确认仓位对应的进行中任务状态一次性变为"已完成"；系统记录本次确认操作（操作员、任务、仓位、时间戳）

- **AC-2（会话结束联动）**
  - **Given** 本次到站操作会话当前处于"仓门操作已锁定"阶段
  - **When** 系统完成批量确认（AC-1）
  - **Then** 该操作会话同时结束，界面恢复为"未验证"状态

- **AC-3（确认后不支持撤销）**
  - **Given** 一次确认完成操作已成功执行（AC-1）
  - **When** 操作员事后发现误确认并请求撤销
  - **Then** 系统拒绝该撤销请求，不提供撤销能力；误确认的补救转人工后续处理（不在本 FR 范围内）

## Related 关联

- **Use Cases：** 支撑 [[uc-002-confirm-task-completion|UC-002]]；会话结束联动依赖 [[uc-043-verify-identity-and-manage-operation-session|UC-043]] 定义的会话阶段模型
- **Business Rules：** 无
- **Functional Requirements：** 前置核验依赖 [[fr-003-confirm-completion-eligibility-check|FR-003]]
- **Non-Functional Requirements：** 批量确认与记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]] 的关键操作可审计要求

## Verification 验证方式

- [[TC-004|TC-004]]：批量确认成功并记录
- [[TC-005|TC-005]]：会话结束联动
- [[TC-006|TC-006]]：确认后不支持撤销

## Notes 备注

- 任务完成结果不需要同步上报给 MES（与 UC-002 Postcondition 备注一致）。
- 本 FR 不处理"确认前发现存错"的场景，那属于 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 范围。
