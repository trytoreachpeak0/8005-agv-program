---
id: FR-028
type: functional-requirement
title: "AGV Dispatch Profile Update Eligibility and Persistence AGV 调度配置更新资格核验与持久化"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-020"]
related_br: ["BR-002", "BR-008"]
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-087", "TC-088", "TC-089", "TC-090"]
aliases: ["FR-028"]
---

# FR-028 AGV Dispatch Profile Update Eligibility and Persistence AGV 调度配置更新资格核验与持久化

## Description 需求描述

系统应当在管理员修改某台已接入 AGV 的本地业务配置（身份映射、车型、服务区域、最低接单电量、调度权重、维护备注）并确认保存前，核验该车辆未归档、已处于"已禁用"（非"禁用待生效"）、本地无未完成任务或站点作业，且所有仓门均已确认关闭；并校验 RCS/RIOT 车辆 ID、配置完整性、数值范围与内部一致性。核验或校验不通过时，系统必须拒绝进入可保存状态或拒绝保存，并提示具体原因；仓位编号、位置、规格等由绑定的模型版本快照决定的内容始终只读展示，不提供修改入口。核验与校验均通过后，系统展示修改前后差异，管理员确认后保存新配置，AGV 保持"已禁用"，并记录审计日志。

## Rationale 制定原因

配置变更（尤其服务区域、电量阈值、调度权重）会立即影响后续 [[uc-023-allocate-transport-tasks-to-agv|UC-023]] 的候选过滤与排序，若允许在车辆仍有未完成作业或仓门未关闭时修改，可能导致正在执行的业务与新配置产生不一致的中间状态；要求"已禁用+无未完成作业+仓门关闭"三重前提，是为了确保配置变更时车辆处于一个安全、稳定的快照点。仓位结构改为只读，是执行 [[br-008-agv-slot-model-versioning|BR-008]] 第 3 条"接入后不允许更换型号/版本、不允许修改已生成仓位"的直接后果。

## Origin 需求来源

- [[uc-020-maintain-agv-dispatch-profile|UC-020]] Normal Flow 第 2~7 步、Exception Flow E2.1、E2.2、E5.1、Postcondition

## Acceptance Criteria 验收标准

- **AC-1（核验与校验均通过，展示差异并保存）**
  - **Given** 目标 AGV 已通过 UC-019 接入且未归档，处于"已禁用"，本地无未完成任务或站点作业，所有仓门均已确认关闭
  - **When** 管理员修改身份映射、车型、服务区域、电量阈值、调度权重或备注，系统校验 RCS/RIOT 车辆 ID、配置完整性、数值范围与内部一致性均通过
  - **Then** 系统展示修改前后差异，管理员确认后保存新配置，记录审计日志，并提示车辆仍处于禁用状态

- **AC-2（车辆未完全停用，拒绝进入可保存状态）**
  - **Given** 目标车辆未禁用、处于"禁用待生效"，或存在本地未完成作业
  - **When** 管理员尝试进入配置保存流程
  - **Then** 系统拒绝进入可保存状态，提示先完成作业并通过 [[uc-013-enable-disable-agv|UC-013]] 禁用

- **AC-3（仓门或安全状态不满足，fail-closed 拒绝）**
  - **Given** 目标车辆任一仓门打开，或仓门、光幕、安全状态未知/异常
  - **When** 管理员尝试保存配置
  - **Then** 系统采用 fail-closed，拒绝保存影响调度的配置并提示处理现场状态

- **AC-4（配置冲突，拒绝保存）**
  - **Given** 管理员提交的配置中 RCS/RIOT 车辆 ID 重复、外部车辆不存在，或服务区域等配置不合法
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存并显示具体冲突项

## Related 关联

- **Use Cases：** 支撑 [[uc-020-maintain-agv-dispatch-profile|UC-020]]；只读展示的仓位结构来源于 [[uc-038-maintain-agv-slot-model|UC-038]] 经 [[uc-019-register-agv-from-rcs|UC-019]] 绑定的快照
- **Business Rules：** 落实 [[br-008-agv-slot-model-versioning|BR-008]] 第 3 条（仓位结构只读、不可更换型号）；维护结果影响 [[br-002-agv-allocation-eligibility|BR-002]] 依赖的服务区域/电量/权重等配置
- **Functional Requirements：** 无强依赖
- **Non-Functional Requirements：** 配置变更须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-020-maintain-agv-dispatch-profile|UC-020]] Postcondition 3 明确要求记录审计日志）

## Verification 验证方式

- [[tc-087-dispatch-profile-update-pass|TC-087]]：核验与校验均通过，展示差异并保存
- [[tc-088-dispatch-profile-not-fully-stopped-reject|TC-088]]：车辆未完全停用，拒绝进入可保存状态
- [[tc-089-dispatch-profile-door-safety-fail-closed-reject|TC-089]]：仓门或安全状态不满足，fail-closed 拒绝
- [[tc-090-dispatch-profile-config-conflict-reject|TC-090]]：配置冲突，拒绝保存

## Notes 备注

- 本 FR 不覆盖仅修改维护备注是否可免除"已禁用"条件——UC-020 Alternative Flow A4.1 明确该点仍为 TBD，当前统一按 Normal Flow 处理，不单独拆分 AC。
- 配置版本回滚机制仍为 TBD（见 UC-020 Notes），本 FR 只覆盖当前变更的校验与持久化，不覆盖历史版本回滚能力。
- "最低接单电量"与 [[uc-037-maintain-agv-charging-strategy-configuration|UC-037]] 的充电触发/完成阈值是两个独立配置项，本 FR 不做二者的联动或一致性校验（见 UC-020 Notes）。
