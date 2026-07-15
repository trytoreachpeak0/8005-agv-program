---
id: FR-003
type: functional-requirement
title: "Confirm Completion Eligibility Check 确认完成前置核验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-002"]
related_br: []
related_fr: ["FR-004"]
related_nfr: ["NFR-002"]
related_tc: ["TC-001", "TC-002", "TC-003"]
aliases: ["FR-003"]
---

# FR-003 Confirm Completion Eligibility Check 确认完成前置核验

## Description 需求描述

系统应当在操作员点击"确认完成"后，核验当前站点是否存在至少一个已装载或已取出（仓门均已关闭）、状态发生变化待确认的仓位；并核验这些待确认仓位的仓门/光幕状态是否与系统记录一致。任一核验不通过时，系统必须拒绝本次确认，不进入批量状态更新（批量更新与落库能力见 [[fr-004-batch-task-completion-session-closure-and-non-reversibility|FR-004]]）。

## Rationale 制定原因

避免操作员误点确认（尚未做任何装卸操作）或在仓位实物状态与系统记录不一致时被错误确认为完成，从而污染任务追溯数据；将 [[uc-002-confirm-task-completion|UC-002]] Normal Flow 第 2、2.1、2.2 步的系统核验点落实为可单独验收的能力。

## Origin 需求来源

- [[uc-002-confirm-task-completion|UC-002]] Normal Flow 第 2、2.1、2.2 步及 Exception Flow E2.1、E2.2

## Acceptance Criteria 验收标准

- **AC-1（存在待确认仓位，核验通过）**
  - **Given** 当前站点存在至少一个已装载或已取出、且仓门均已关闭的仓位
  - **When** 操作员点击"确认完成"
  - **Then** 系统判定核验通过，进入批量确认（见 FR-004）

- **AC-2（无待确认仓位，拒绝）**
  - **Given** 当前站点没有任何已装载或已取出（仓门已关闭）的仓位
  - **When** 操作员点击"确认完成"
  - **Then** 系统拒绝执行本次确认，提示"当前无可确认的装载/取出内容"

- **AC-3（仓门未关好或光幕异常，拒绝）**
  - **Given** 待确认仓位中存在仓门未关好，或光幕检测结果与系统记录状态不一致的情况
  - **When** 系统核验待确认仓位的仓门/光幕状态
  - **Then** 系统拒绝本次确认，提示操作员先处理该仓位

## Related 关联

- **Use Cases：** 派生自 [[uc-002-confirm-task-completion|UC-002]]（确认完成前的系统核验点）
- **Business Rules：** 无
- **Functional Requirements：** 核验通过后由 [[fr-004-batch-task-completion-session-closure-and-non-reversibility|FR-004]] 承接批量确认与落库
- **Non-Functional Requirements：** 核验通过与拒绝结果均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]] 的关键操作可审计要求

## Verification 验证方式

- [[TC-001|TC-001]]：存在待确认仓位，核验通过
- [[TC-002|TC-002]]：无待确认仓位，拒绝
- [[TC-003|TC-003]]：仓门未关好或光幕异常，拒绝

## Notes 备注

- 本 FR 不核验"该站点是否存在搬运任务"，理由与 UC-002 Precondition 备注一致：AGV 到站即意味着必然存在对应任务，任务在装载/确认过程中不会被取消或变更（由其他机制保证）。
- 本 FR 不区分"已装载"还是"已取出"，两类待确认仓位共用同一套核验逻辑，与 UC-002 泛化后的范围一致。
