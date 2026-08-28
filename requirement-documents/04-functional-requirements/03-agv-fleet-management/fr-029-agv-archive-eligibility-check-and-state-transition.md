---
id: FR-029
type: functional-requirement
title: "AGV Archive Eligibility Check and State Transition AGV 归档资格核验与状态迁移"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-021"]
related_br: ["BR-002"]
related_fr: []
related_nfr: []
related_tc: ["TC-091", "TC-092", "TC-093", "TC-094"]
aliases: ["FR-029"]
---

# FR-029 AGV Archive Eligibility Check and State Transition AGV 归档资格核验与状态迁移

## Description 需求描述

系统应当在管理员对某台 AGV 发起归档时，核验该 AGV 已处于"已禁用"且未归档、不存在进行中/等待装卸/异常待恢复或其他未结束的本地任务或作业、RCS/RIOT 任务队列为空、所有仓门关闭且关键安全状态正常可读取。全部满足时，系统展示归档影响（退出任务分配但保留全部历史，不影响 RCS/RIOT 车辆），管理员二次确认后，系统将该 AGV 标记为"已归档"，并记录操作人、时间和原因；不满足任一条件时，系统必须拒绝归档并提示具体原因，不产生部分归档的中间状态。归档不删除车辆、任务、仓位、日志或审计历史，也不删除 RCS/RIOT 中的车辆。

## Rationale 制定原因

归档会使该 AGV 永久退出 [[br-002-agv-allocation-eligibility|BR-002]] 候选集合且默认不允许再通过 UC-013 启用，属于影响范围较大、事实上不可逆的业务操作；因此在归档前必须确认车辆确实处于安全、无未结束业务的状态，并要求二次确认，避免误归档正在使用中的车辆。归档统一实现为软删除（不物理删除），是为了保留历史任务、仓位记录、配置版本与审计日志的可查询性（见 UC-021 Assumption）。

## Origin 需求来源

- [[uc-021-archive-agv|UC-021]] Normal Flow 第 2~7 步、Exception Flow E2.1、E3.1、E4.1、Postcondition

## Acceptance Criteria 验收标准

- **AC-1（条件均满足，二次确认后归档成功）**
  - **Given** 目标 AGV 已禁用且未归档，不存在未结束的本地任务/作业，RCS/RIOT 队列为空，所有仓门关闭且关键安全状态正常可读取
  - **When** 系统展示归档影响后，管理员二次确认
  - **Then** 系统将该 AGV 标记为"已归档"，记录操作人、时间和原因；历史任务、仓位记录、配置版本和审计日志仍可查询，RCS/RIOT 中的车辆保持不变

- **AC-2（车辆未禁用，拒绝归档）**
  - **Given** 目标 AGV 当前未处于"已禁用"状态
  - **When** 管理员发起归档
  - **Then** 系统拒绝归档，提示先通过 [[uc-013-enable-disable-agv|UC-013]] 禁用并等待禁用生效

- **AC-3（存在未结束业务，拒绝归档）**
  - **Given** 目标 AGV 存在进行中任务、等待装卸或异常待恢复的本地作业
  - **When** 管理员发起归档
  - **Then** 系统列出这些未结束的任务/作业，拒绝归档

- **AC-4（外部或安全状态不满足，fail-closed 拒绝）**
  - **Given** 目标 AGV 的 RCS/RIOT 队列不为空、任一仓门打开，或任一关键安全状态未知/异常
  - **When** 管理员发起归档
  - **Then** 系统采用 fail-closed，拒绝归档并显示具体原因

## Related 关联

- **Use Cases：** 支撑 [[uc-021-archive-agv|UC-021]]；归档前需先完成 [[uc-013-enable-disable-agv|UC-013]] 禁用
- **Business Rules：** 归档后该车辆退出 [[br-002-agv-allocation-eligibility|BR-002]] 候选集合第 1 条依赖的"未归档"条件
- **Functional Requirements：** 无强依赖
- **Non-Functional Requirements：** 无（见 Notes 说明理由）

## Verification 验证方式

- [[tc-091-archive-eligible-success|TC-091]]：条件均满足，二次确认后归档成功
- [[tc-092-archive-not-disabled-reject|TC-092]]：车辆未禁用，拒绝归档
- [[tc-093-archive-unfinished-business-reject|TC-093]]：存在未结束业务，拒绝归档
- [[tc-094-archive-external-safety-fail-closed-reject|TC-094]]：外部或安全状态不满足，fail-closed 拒绝

## Notes 备注

- 本 FR 未关联 `NFR-002`：[[uc-021-archive-agv|UC-021]] 的 Postcondition 段落本身没有显式要求"记录到审计日志"（对比 [[uc-013-enable-disable-agv|UC-013]] Postcondition 第 4 条、[[uc-020-maintain-agv-dispatch-profile|UC-020]] Postcondition 第 3 条均有类似的显式表述），Normal Flow 第 7 步虽提到"记录操作人、时间和原因"，但按既定的从严判断规则（以 Postcondition 是否显式要求为准，参照 [[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]]、[[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]] 被排除在 `NFR-002` 之外的先例）暂不纳入；若后续与用户确认归档也需要满足 `NFR-002` 的完整审计要求，应同步补充本 FR 的 `related_nfr` 并更新 `NFR-002`。
- 归档车辆默认不允许通过 UC-013 再次启用；归档恢复、RCS/RIOT 车辆 ID 被其他车辆复用时的处理规则仍为 TBD（见 UC-021 Notes），本 FR 不覆盖恢复场景。
